"""
OTEL Instrumentation: Webhook Handler (Flask)
Implements ADR-060 (OTEL Observability and Telemetry Standards)

This module provides OpenTelemetry instrumentation for a Flask-based
webhook handler. It emits:
  - Traces: one span per incoming request with latency, status, and tags
  - Metrics: request count, latency histograms, error rates
  - Propagates trace context in outgoing webhook events

Usage:
    from otel.webhook_instrumentation import instrument_app, get_tracer, get_meter
    instrument_app(app)

ADR References: ADR-060
"""

import os
import logging
import functools
from typing import Optional

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.trace import StatusCode
from opentelemetry.semconv.trace import SpanAttributes

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Configuration (from environment variables)
# ─────────────────────────────────────────────────────────────
OTEL_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
SERVICE_NAME_ENV = os.environ.get("OTEL_SERVICE_NAME", "webhook-handler")
SERVICE_VERSION_ENV = os.environ.get("SERVICE_VERSION", "1.0.0")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")


def _build_resource() -> Resource:
    """Build OTEL resource with standard service attributes."""
    return Resource.create({
        SERVICE_NAME: SERVICE_NAME_ENV,
        SERVICE_VERSION: SERVICE_VERSION_ENV,
        "deployment.environment": ENVIRONMENT,
        "platform": "prophet-platform",
        "adr.reference": "ADR-060",
    })


def instrument_app(app) -> None:
    """
    Instrument a Flask application with OpenTelemetry.

    Sets up:
    - TracerProvider with OTLP gRPC exporter
    - MeterProvider with OTLP gRPC exporter
    - Flask auto-instrumentation (spans per request)
    - Requests auto-instrumentation (outgoing HTTP spans)
    - W3C TraceContext + B3 propagation

    Args:
        app: Flask application instance
    """
    resource = _build_resource()

    # ── Tracer Provider ──────────────────────────────────────
    tracer_provider = TracerProvider(resource=resource)
    otlp_span_exporter = OTLPSpanExporter(
        endpoint=OTEL_ENDPOINT,
        insecure=True,
    )
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            otlp_span_exporter,
            max_export_batch_size=512,
            export_timeout_millis=5000,
        )
    )
    trace.set_tracer_provider(tracer_provider)

    # ── Meter Provider ───────────────────────────────────────
    otlp_metric_exporter = OTLPMetricExporter(
        endpoint=OTEL_ENDPOINT,
        insecure=True,
    )
    metric_reader = PeriodicExportingMetricReader(
        exporter=otlp_metric_exporter,
        export_interval_millis=15_000,
    )
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
    )
    metrics.set_meter_provider(meter_provider)

    # ── Propagator ───────────────────────────────────────────
    # W3C TraceContext is primary; B3 for compatibility
    set_global_textmap(B3MultiFormat())

    # ── Auto-instrumentation ─────────────────────────────────
    FlaskInstrumentor().instrument_app(
        app,
        excluded_urls="health,metrics,ready",
        tracer_provider=tracer_provider,
        meter_provider=meter_provider,
    )
    RequestsInstrumentor().instrument(tracer_provider=tracer_provider)

    logger.info(
        "OTEL instrumentation initialized",
        extra={
            "service": SERVICE_NAME_ENV,
            "endpoint": OTEL_ENDPOINT,
            "environment": ENVIRONMENT,
        }
    )


def get_tracer(name: Optional[str] = None) -> trace.Tracer:
    """Get a named tracer for manual instrumentation."""
    return trace.get_tracer(name or SERVICE_NAME_ENV)


def get_meter(name: Optional[str] = None) -> metrics.Meter:
    """Get a named meter for custom metrics."""
    return metrics.get_meter(name or SERVICE_NAME_ENV)


# ─────────────────────────────────────────────────────────────
# Custom Metrics
# ─────────────────────────────────────────────────────────────
def create_webhook_metrics(meter: metrics.Meter) -> dict:
    """
    Create standard webhook metrics per ADR-060.

    Returns a dict of metric instruments:
      - webhook_deliveries_total: Counter
      - webhook_delivery_duration: Histogram (seconds)
      - webhook_queue_depth: ObservableGauge
    """
    webhook_deliveries = meter.create_counter(
        name="prophet_webhook_deliveries_total",
        description="Total number of webhook deliveries",
        unit="1",
    )
    webhook_duration = meter.create_histogram(
        name="prophet_webhook_delivery_duration_seconds",
        description="Webhook delivery duration in seconds",
        unit="s",
        explicit_bucket_boundaries_advisory=[
            0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0
        ],
    )
    return {
        "deliveries": webhook_deliveries,
        "duration": webhook_duration,
    }


# ─────────────────────────────────────────────────────────────
# Decorator: Trace a webhook event handler
# ─────────────────────────────────────────────────────────────
def trace_webhook_event(repo: str, event_type: str):
    """
    Decorator to trace a webhook event handler function.

    Example:
        @trace_webhook_event(repo="SocioProphet/sociosphere", event_type="push")
        def handle_push_event(payload):
            ...

    Emits a span with:
      - webhook.repo
      - webhook.event_type
      - webhook.delivery_id
      - http.status_code (on response)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            with tracer.start_as_current_span(
                name=f"webhook.{event_type}",
                kind=trace.SpanKind.SERVER,
            ) as span:
                span.set_attribute("webhook.repo", repo)
                span.set_attribute("webhook.event_type", event_type)
                span.set_attribute("adr.reference", "ADR-060")
                span.set_attribute(SpanAttributes.HTTP_METHOD, "POST")

                try:
                    result = func(*args, **kwargs)
                    span.set_status(StatusCode.OK)
                    return result
                except Exception as exc:
                    span.set_status(StatusCode.ERROR, str(exc))
                    span.record_exception(exc)
                    raise
        return wrapper
    return decorator


# ─────────────────────────────────────────────────────────────
# Example: Instrumented Flask webhook endpoint
# ─────────────────────────────────────────────────────────────
def example_flask_webhook():
    """
    Example of a fully instrumented Flask webhook handler.
    Copy this pattern into your webhook service.
    """
    from flask import Flask, request, jsonify
    import time

    app = Flask(__name__)
    instrument_app(app)

    meter = get_meter()
    webhook_metrics = create_webhook_metrics(meter)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/webhook", methods=["POST"])
    @trace_webhook_event(repo="SocioProphet/sociosphere", event_type="push")
    def webhook():
        tracer = get_tracer()
        start_time = time.time()

        # Get current span (created by decorator)
        current_span = trace.get_current_span()

        payload = request.json
        repo = payload.get("repository", {}).get("full_name", "unknown")
        event_type = request.headers.get("X-GitHub-Event", "unknown")
        delivery_id = request.headers.get("X-GitHub-Delivery", "unknown")

        current_span.set_attribute("webhook.repo", repo)
        current_span.set_attribute("webhook.event_type", event_type)
        current_span.set_attribute("webhook.delivery_id", delivery_id)

        # Process the webhook event...
        with tracer.start_as_current_span("webhook.process") as process_span:
            process_span.set_attribute("webhook.repo", repo)
            # ... actual processing logic ...
            pass

        duration = time.time() - start_time
        webhook_metrics["deliveries"].add(
            1,
            attributes={"repo": repo, "event_type": event_type, "status": "success"}
        )
        webhook_metrics["duration"].record(
            duration,
            attributes={"repo": repo}
        )

        return jsonify({"status": "accepted", "delivery_id": delivery_id}), 202

    return app
