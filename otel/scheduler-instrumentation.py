"""
OTEL Instrumentation: Scheduler (APScheduler)
Implements ADR-060 (OTEL Observability and Telemetry Standards)

This module provides OpenTelemetry instrumentation for an APScheduler-based
scheduler service. It emits:
  - Traces: one span per job execution with duration, status, and job tags
  - Metrics: job run count, duration histograms, failure rates, cost tracking
  - Tags: job name, repo, cost estimate

Usage:
    from otel.scheduler_instrumentation import instrument_scheduler, trace_job
    instrument_scheduler()

    scheduler = BlockingScheduler()
    scheduler.add_job(my_job, 'interval', minutes=5)

ADR References: ADR-060
"""

import os
import time
import logging
import functools
from typing import Optional, Callable, Any

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.trace import StatusCode

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────
OTEL_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
SERVICE_NAME_ENV = os.environ.get("OTEL_SERVICE_NAME", "scheduler")
SERVICE_VERSION_ENV = os.environ.get("SERVICE_VERSION", "1.0.0")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

# Global instruments (initialized once)
_tracer: Optional[trace.Tracer] = None
_meter: Optional[metrics.Meter] = None
_job_run_counter = None
_job_duration_histogram = None
_job_failure_counter = None
_github_api_calls_counter = None
_cost_gauge = None


def instrument_scheduler() -> None:
    """
    Initialize OTEL TracerProvider and MeterProvider for the scheduler.
    Call this once at application startup before creating the APScheduler instance.
    """
    global _tracer, _meter
    global _job_run_counter, _job_duration_histogram, _job_failure_counter
    global _github_api_calls_counter, _cost_gauge

    resource = Resource.create({
        SERVICE_NAME: SERVICE_NAME_ENV,
        SERVICE_VERSION: SERVICE_VERSION_ENV,
        "deployment.environment": ENVIRONMENT,
        "platform": "prophet-platform",
        "adr.reference": "ADR-060",
    })

    # ── Tracer Provider ──────────────────────────────────────
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=OTEL_ENDPOINT, insecure=True),
            max_export_batch_size=512,
        )
    )
    trace.set_tracer_provider(tracer_provider)
    _tracer = trace.get_tracer(SERVICE_NAME_ENV)

    # ── Meter Provider ───────────────────────────────────────
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

    # ── Create metric instruments ────────────────────────────
    _job_run_counter = _meter.create_counter(
        name="prophet_scheduler_job_runs_total",
        description="Total number of scheduler job runs",
        unit="1",
    )
    _job_duration_histogram = _meter.create_histogram(
        name="prophet_scheduler_job_duration_seconds",
        description="Scheduler job duration in seconds",
        unit="s",
        explicit_bucket_boundaries_advisory=[
            0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0, 120.0, 300.0
        ],
    )
    _job_failure_counter = _meter.create_counter(
        name="prophet_scheduler_job_failures_total",
        description="Total number of scheduler job failures",
        unit="1",
    )
    _github_api_calls_counter = _meter.create_counter(
        name="prophet_github_api_calls_total",
        description="Total GitHub API calls made by scheduler",
        unit="1",
    )
    _cost_gauge = _meter.create_gauge(
        name="prophet_github_api_cost_per_sprint",
        description="Estimated GitHub API cost per repo per sprint",
        unit="api_calls",
    )

    logger.info(
        "Scheduler OTEL instrumentation initialized",
        extra={"service": SERVICE_NAME_ENV, "endpoint": OTEL_ENDPOINT}
    )


def trace_job(
    job_name: str,
    repo: Optional[str] = None,
    api_calls_estimate: int = 0,
) -> Callable:
    """
    Decorator to trace an APScheduler job function.

    Emits:
      - Span: scheduler.job.<job_name>
      - Span attributes: job_name, repo, duration_ms, status
      - Metrics: job_runs_total, job_duration_seconds, cost_per_sprint

    Args:
        job_name: Human-readable job name (e.g. "propagation-check")
        repo: GitHub repository full name (e.g. "SocioProphet/sociosphere")
        api_calls_estimate: Estimated GitHub API calls this job makes

    Example:
        @trace_job(job_name="propagation-check", repo="SocioProphet/sociosphere", api_calls_estimate=5)
        def check_propagation():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            tracer = _tracer or trace.get_tracer(SERVICE_NAME_ENV)
            start_time = time.time()

            job_attrs = {
                "scheduler.job_name": job_name,
                "scheduler.repo": repo or "all",
                "adr.reference": "ADR-060",
                "platform": "prophet-platform",
            }

            with tracer.start_as_current_span(
                name=f"scheduler.job.{job_name}",
                kind=trace.SpanKind.INTERNAL,
            ) as span:
                for k, v in job_attrs.items():
                    span.set_attribute(k, v)

                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time

                    span.set_status(StatusCode.OK)
                    span.set_attribute("scheduler.duration_ms", int(duration * 1000))
                    span.set_attribute("scheduler.status", "success")

                    # Record metrics
                    _record_job_metrics(
                        job_name=job_name,
                        repo=repo,
                        duration=duration,
                        success=True,
                        api_calls=api_calls_estimate,
                    )
                    return result

                except Exception as exc:
                    duration = time.time() - start_time
                    span.set_status(StatusCode.ERROR, str(exc))
                    span.record_exception(exc)
                    span.set_attribute("scheduler.status", "failed")
                    span.set_attribute("scheduler.error", str(exc))

                    _record_job_metrics(
                        job_name=job_name,
                        repo=repo,
                        duration=duration,
                        success=False,
                        api_calls=0,
                    )
                    raise

        return wrapper
    return decorator


def _record_job_metrics(
    job_name: str,
    repo: Optional[str],
    duration: float,
    success: bool,
    api_calls: int,
) -> None:
    """Record standard job metrics after each run."""
    attrs = {
        "job_name": job_name,
        "repo": repo or "all",
        "status": "success" if success else "failure",
    }

    if _job_run_counter:
        _job_run_counter.add(1, attributes=attrs)

    if _job_duration_histogram:
        _job_duration_histogram.record(duration, attributes={"job_name": job_name, "repo": repo or "all"})

    if not success and _job_failure_counter:
        _job_failure_counter.add(1, attributes={"job_name": job_name, "repo": repo or "all"})

    if api_calls > 0 and _github_api_calls_counter:
        _github_api_calls_counter.add(
            api_calls,
            attributes={"repo": repo or "all", "job": job_name}
        )


def record_api_call(endpoint: str, repo: str, count: int = 1) -> None:
    """
    Record a GitHub API call for quota and cost tracking.

    Call this inside any function that makes GitHub API requests.

    Args:
        endpoint: GitHub API endpoint (e.g. "/repos/{owner}/{repo}/contents")
        repo: GitHub repository full name
        count: Number of API calls made (default: 1)
    """
    if _github_api_calls_counter:
        _github_api_calls_counter.add(
            count,
            attributes={"endpoint": endpoint, "repo": repo}
        )


# ─────────────────────────────────────────────────────────────
# Example: Instrumented APScheduler job
# ─────────────────────────────────────────────────────────────
def example_scheduler():
    """
    Example of a fully instrumented APScheduler setup.
    Copy this pattern into your scheduler service.
    """
    from apscheduler.schedulers.blocking import BlockingScheduler

    instrument_scheduler()
    scheduler = BlockingScheduler()

    @trace_job(
        job_name="propagation-check",
        repo="SocioProphet/sociosphere",
        api_calls_estimate=10,
    )
    def check_propagation():
        """Check for upstream changes and trigger propagation pipeline."""
        tracer = _tracer or trace.get_tracer(SERVICE_NAME_ENV)

        with tracer.start_as_current_span("propagation.check_upstream") as span:
            span.set_attribute("repo", "SocioProphet/sociosphere")
            # ... check GitHub for upstream changes ...
            record_api_call("/repos/SocioProphet/sociosphere/commits", "SocioProphet/sociosphere")

        with tracer.start_as_current_span("propagation.identify_dependents") as span:
            # ... identify dependent repos ...
            span.set_attribute("dependents_found", 3)

        with tracer.start_as_current_span("propagation.trigger_pipeline") as span:
            # ... trigger Tekton PipelineRun ...
            span.set_attribute("pipeline_run_name", "build-test-deploy-abc123")

    @trace_job(
        job_name="api-quota-check",
        api_calls_estimate=1,
    )
    def check_api_quota():
        """Check GitHub API rate limit and update quota metric."""
        tracer = _tracer or trace.get_tracer(SERVICE_NAME_ENV)

        with tracer.start_as_current_span("api_quota.check") as span:
            record_api_call("/rate_limit", "all")
            # ... fetch rate limit from GitHub API ...
            # ... update _cost_gauge ...

    scheduler.add_job(check_propagation, "interval", minutes=5, id="propagation-check")
    scheduler.add_job(check_api_quota, "interval", minutes=15, id="api-quota-check")
    scheduler.start()
