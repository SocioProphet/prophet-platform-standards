"""
OTEL Instrumentation: Propagation Engine
Implements ADR-060 (OTEL Observability and Telemetry Standards)

This module provides OpenTelemetry instrumentation for the propagation engine.
The propagation engine identifies dependent repositories and triggers deployment
pipelines when upstream changes are detected.

It emits:
  - Traces: repo changed → dependents identified → deploy started
  - Metrics: propagation success rate, end-to-end latency, repos affected
  - Tags: repo, dependents_count, latency_ms

Usage:
    from otel.engine_instrumentation import instrument_engine, PropagationTracer
    instrument_engine()
    
    tracer = PropagationTracer()
    with tracer.trace_propagation(repo="SocioProphet/sociosphere") as ctx:
        ctx.set_dependents(["dep-a", "dep-b"])
        ctx.set_deploy_started()

ADR References: ADR-060
"""

import os
import time
import logging
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import List, Optional

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.trace import StatusCode, NonRecordingSpan
from opentelemetry.propagate import inject, extract
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
OTEL_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
SERVICE_NAME_ENV = os.environ.get("OTEL_SERVICE_NAME", "propagation-engine")
SERVICE_VERSION_ENV = os.environ.get("SERVICE_VERSION", "1.0.0")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

# Module-level singletons
_tracer: Optional[trace.Tracer] = None
_meter: Optional[metrics.Meter] = None

# Metric instruments
_propagation_runs_counter = None
_propagation_success_counter = None
_propagation_failure_counter = None
_propagation_duration_histogram = None
_repos_affected_counter = None
_propagation_success_rate_gauge = None


def instrument_engine() -> None:
    """
    Initialize OTEL for the propagation engine.
    Call once at application startup.
    """
    global _tracer, _meter
    global _propagation_runs_counter, _propagation_success_counter
    global _propagation_failure_counter, _propagation_duration_histogram
    global _repos_affected_counter, _propagation_success_rate_gauge

    resource = Resource.create({
        SERVICE_NAME: SERVICE_NAME_ENV,
        SERVICE_VERSION: SERVICE_VERSION_ENV,
        "deployment.environment": ENVIRONMENT,
        "platform": "prophet-platform",
        "adr.reference": "ADR-060",
    })

    # Tracer Provider
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=OTEL_ENDPOINT, insecure=True),
            max_export_batch_size=512,
        )
    )
    trace.set_tracer_provider(tracer_provider)
    _tracer = trace.get_tracer(SERVICE_NAME_ENV)

    # Meter Provider
    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[
            PeriodicExportingMetricReader(
                exporter=OTLPMetricExporter(endpoint=OTEL_ENDPOINT, insecure=True),
                export_interval_millis=15_000,
            )
        ],
    )
    metrics.set_meter_provider(meter_provider)
    _meter = metrics.get_meter(SERVICE_NAME_ENV)

    # Create instruments per ADR-060 metric definitions
    _propagation_runs_counter = _meter.create_counter(
        name="prophet_propagation_runs_total",
        description="Total propagation engine runs",
        unit="1",
    )
    _propagation_success_counter = _meter.create_counter(
        name="prophet_propagation_success_total",
        description="Total successful propagations",
        unit="1",
    )
    _propagation_failure_counter = _meter.create_counter(
        name="prophet_propagation_failures_total",
        description="Total failed propagations",
        unit="1",
    )
    _propagation_duration_histogram = _meter.create_histogram(
        name="prophet_propagation_end_to_end_duration_seconds",
        description="End-to-end propagation duration from webhook to deploy complete",
        unit="s",
        explicit_bucket_boundaries_advisory=[
            1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0, 600.0
        ],
    )
    _repos_affected_counter = _meter.create_counter(
        name="prophet_propagation_repos_affected_total",
        description="Total number of dependent repos affected by propagation",
        unit="1",
    )
    _propagation_success_rate_gauge = _meter.create_gauge(
        name="prophet_propagation_success_rate",
        description="Rolling propagation success rate (target: >=0.90)",
        unit="1",
    )

    logger.info(
        "Propagation engine OTEL instrumentation initialized",
        extra={"service": SERVICE_NAME_ENV, "endpoint": OTEL_ENDPOINT}
    )


@dataclass
class PropagationContext:
    """
    Context object passed through a propagation trace.
    Holds the active span and collects propagation metadata.
    """
    repo: str
    span: trace.Span
    start_time: float = field(default_factory=time.time)
    dependents: List[str] = field(default_factory=list)
    deploy_started: bool = False
    deploy_completed: bool = False
    pipeline_run_name: Optional[str] = None
    trace_context: dict = field(default_factory=dict)

    def set_dependents(self, repos: List[str]) -> None:
        """Record identified dependent repositories."""
        self.dependents = repos
        self.span.set_attribute("propagation.dependents_count", len(repos))
        self.span.set_attribute("propagation.dependents", ",".join(repos[:10]))  # cap at 10
        logger.info(
            "Dependents identified",
            extra={"repo": self.repo, "dependents_count": len(repos), "dependents": repos}
        )

    def set_deploy_started(self, pipeline_run_name: Optional[str] = None) -> None:
        """Record that deployment has been triggered."""
        self.deploy_started = True
        self.pipeline_run_name = pipeline_run_name
        self.span.add_event(
            "deploy.started",
            attributes={
                "pipeline_run": pipeline_run_name or "unknown",
                "dependents_count": len(self.dependents),
            }
        )

    def set_deploy_completed(self) -> None:
        """Record that deployment has completed successfully."""
        self.deploy_completed = True
        duration = time.time() - self.start_time
        self.span.set_attribute("propagation.e2e_duration_seconds", duration)
        self.span.add_event("deploy.completed")

    def get_trace_headers(self) -> dict:
        """Get W3C traceparent headers for propagating context to downstream services."""
        headers = {}
        inject(headers)
        return headers


class PropagationTracer:
    """
    High-level tracer for the propagation engine.
    Wraps the full propagation lifecycle in a structured trace.
    """

    def __init__(self):
        self._tracer = _tracer or trace.get_tracer(SERVICE_NAME_ENV)

    @contextmanager
    def trace_propagation(
        self,
        repo: str,
        upstream_trace_headers: Optional[dict] = None,
    ):
        """
        Context manager that wraps a full propagation run in a trace.

        Creates a root span "propagation.run" with child spans for:
          - propagation.identify_dependents
          - propagation.trigger_pipeline
          - propagation.await_completion

        Args:
            repo: Upstream repository that triggered propagation
            upstream_trace_headers: W3C traceparent headers from webhook event
                                   (links this trace to the webhook trace)

        Yields:
            PropagationContext: context object to record metadata

        Example:
            with tracer.trace_propagation("SocioProphet/sociosphere") as ctx:
                deps = find_dependents(ctx.repo)
                ctx.set_dependents(deps)
                run_name = trigger_pipeline(ctx.repo)
                ctx.set_deploy_started(run_name)
                await_pipeline(run_name)
                ctx.set_deploy_completed()
        """
        # Extract upstream context (links webhook span to this propagation span)
        parent_context = None
        if upstream_trace_headers:
            parent_context = extract(upstream_trace_headers)

        with self._tracer.start_as_current_span(
            name="propagation.run",
            kind=trace.SpanKind.INTERNAL,
            context=parent_context,
        ) as span:
            span.set_attribute("propagation.repo", repo)
            span.set_attribute("adr.reference", "ADR-060")
            span.set_attribute("platform", "prophet-platform")

            ctx = PropagationContext(repo=repo, span=span)

            # Record trace context for downstream headers
            inject(ctx.trace_context)

            # Record run counter
            if _propagation_runs_counter:
                _propagation_runs_counter.add(1, attributes={"repo": repo})

            try:
                yield ctx

                # Success path
                duration = time.time() - ctx.start_time
                span.set_status(StatusCode.OK)

                if _propagation_success_counter:
                    _propagation_success_counter.add(1, attributes={"repo": repo})

                if _propagation_duration_histogram:
                    _propagation_duration_histogram.record(duration, attributes={"repo": repo})

                if _repos_affected_counter and ctx.dependents:
                    _repos_affected_counter.add(
                        len(ctx.dependents),
                        attributes={"upstream_repo": repo}
                    )

                logger.info(
                    "Propagation completed",
                    extra={
                        "repo": repo,
                        "dependents_count": len(ctx.dependents),
                        "duration_s": duration,
                        "trace_id": span.get_span_context().trace_id,
                    }
                )

            except Exception as exc:
                span.set_status(StatusCode.ERROR, str(exc))
                span.record_exception(exc)

                if _propagation_failure_counter:
                    _propagation_failure_counter.add(1, attributes={"repo": repo})

                logger.error(
                    "Propagation failed",
                    extra={
                        "repo": repo,
                        "error": str(exc),
                        "trace_id": span.get_span_context().trace_id,
                    }
                )
                raise

    def trace_identify_dependents(self, repo: str):
        """Context manager for the 'identify dependents' sub-step."""
        tracer = self._tracer
        return tracer.start_as_current_span(
            name="propagation.identify_dependents",
            kind=trace.SpanKind.INTERNAL,
            attributes={"propagation.upstream_repo": repo},
        )

    def trace_trigger_pipeline(self, repo: str, pipeline_name: str):
        """Context manager for the 'trigger pipeline' sub-step."""
        tracer = self._tracer
        return tracer.start_as_current_span(
            name="propagation.trigger_pipeline",
            kind=trace.SpanKind.INTERNAL,
            attributes={
                "propagation.repo": repo,
                "propagation.pipeline_name": pipeline_name,
            },
        )


# ─────────────────────────────────────────────────────────────
# Example: Instrumented propagation engine
# ─────────────────────────────────────────────────────────────
def example_propagation_engine():
    """
    Example of a fully instrumented propagation engine.
    Copy this pattern into your propagation engine service.
    """
    instrument_engine()
    tracer = PropagationTracer()

    def find_dependents(repo: str) -> List[str]:
        """Discover repos that depend on the given repo."""
        # ... actual dependency graph lookup ...
        return ["SocioProphet/dep-a", "SocioProphet/dep-b"]

    def trigger_tekton_pipeline(repo: str) -> str:
        """Trigger a Tekton PipelineRun for the given repo."""
        # ... actual Tekton API call ...
        return f"build-test-deploy-{int(time.time())}"

    def process_webhook_event(event: dict) -> None:
        repo = event["repository"]["full_name"]
        # Extract trace context from webhook event headers
        trace_headers = event.get("_trace_headers", {})

        with tracer.trace_propagation(repo, upstream_trace_headers=trace_headers) as ctx:
            # Step 1: Identify dependents
            with tracer.trace_identify_dependents(repo):
                dependents = find_dependents(repo)
                ctx.set_dependents(dependents)

            # Step 2: Trigger pipeline for each dependent
            for dep_repo in dependents:
                with tracer.trace_trigger_pipeline(dep_repo, "build-test-deploy"):
                    run_name = trigger_tekton_pipeline(dep_repo)
                    ctx.set_deploy_started(run_name)

            ctx.set_deploy_completed()

    # Simulate receiving a webhook event
    example_event = {
        "repository": {"full_name": "SocioProphet/sociosphere"},
        "_trace_headers": {},
    }
    process_webhook_event(example_event)
