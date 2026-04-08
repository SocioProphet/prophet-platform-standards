# OTEL Instrumentation Guide

How to instrument a new service with OpenTelemetry for the Prophet Platform.

All instrumentation follows ADR-060. Reference implementations are in `otel/`.

---

## Quick Start

### 1. Install Dependencies

**Python:**
```bash
pip install \
  opentelemetry-sdk \
  opentelemetry-exporter-otlp-proto-grpc \
  opentelemetry-instrumentation-flask \
  opentelemetry-instrumentation-requests \
  opentelemetry-instrumentation-sqlalchemy \
  opentelemetry-propagator-b3
```

**Node.js:**
```bash
npm install \
  @opentelemetry/sdk-node \
  @opentelemetry/exporter-otlp-grpc \
  @opentelemetry/instrumentation-http \
  @opentelemetry/instrumentation-express \
  @opentelemetry/propagator-b3
```

### 2. Configure Environment Variables

Add these to your pod spec (or `.env` for local development):

```yaml
env:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "http://localhost:4317"   # OTEL Collector sidecar
  - name: OTEL_SERVICE_NAME
    value: "my-service-name"
  - name: OTEL_SERVICE_VERSION
    valueFrom:
      fieldRef:
        fieldPath: metadata.annotations['app.kubernetes.io/version']
  - name: ENVIRONMENT
    valueFrom:
      fieldRef:
        fieldPath: metadata.labels['environment']
  - name: OTEL_TRACES_SAMPLER
    value: "parentbased_traceidratio"
  - name: OTEL_TRACES_SAMPLER_ARG
    value: "0.1"   # 10% sampling (100% for errors via tail sampling)
```

---

## Flask Application

Use `otel/webhook-instrumentation.py` as the reference. Key steps:

```python
from otel.webhook_instrumentation import instrument_app, get_tracer, get_meter

app = Flask(__name__)

# Initialize OTEL (call once at startup)
instrument_app(app)

# Get tracer for manual spans
tracer = get_tracer()

@app.route("/webhook", methods=["POST"])
def webhook():
    with tracer.start_as_current_span("webhook.process") as span:
        span.set_attribute("webhook.repo", request.json.get("repository", {}).get("full_name"))
        span.set_attribute("webhook.event", request.headers.get("X-GitHub-Event"))
        # ... process webhook ...
        return jsonify({"status": "ok"}), 200
```

### What Gets Instrumented Automatically

With `FlaskInstrumentor`, these are automatic:
- HTTP request/response spans (method, status, URL, duration)
- Exception recording on 5xx responses
- Request context propagation (W3C traceparent)

---

## APScheduler Jobs

Use `otel/scheduler-instrumentation.py` as the reference:

```python
from otel.scheduler_instrumentation import instrument_scheduler, trace_job, record_api_call

# Initialize OTEL (call once at startup)
instrument_scheduler()

scheduler = BlockingScheduler()

@trace_job(job_name="my-scheduled-job", repo="SocioProphet/my-repo", api_calls_estimate=3)
def my_job():
    # Record GitHub API calls for quota tracking
    record_api_call("/repos/{owner}/{repo}/commits", "SocioProphet/my-repo", count=1)
    # ... job logic ...

scheduler.add_job(my_job, "interval", minutes=5)
scheduler.start()
```

---

## Propagation Engine

Use `otel/engine-instrumentation.py` as the reference:

```python
from otel.engine_instrumentation import instrument_engine, PropagationTracer

instrument_engine()
tracer = PropagationTracer()

def process_event(event: dict):
    repo = event["repository"]["full_name"]
    trace_headers = event.get("_trace_headers", {})
    
    with tracer.trace_propagation(repo, upstream_trace_headers=trace_headers) as ctx:
        with tracer.trace_identify_dependents(repo):
            deps = find_dependents(repo)
            ctx.set_dependents(deps)
        
        for dep in deps:
            with tracer.trace_trigger_pipeline(dep, "build-test-deploy"):
                run_name = trigger_pipeline(dep)
                ctx.set_deploy_started(run_name)
        
        ctx.set_deploy_completed()
```

---

## Metrics to Emit

All services **SHOULD** emit the following standard metrics per ADR-060:

### Request Metrics (Flask/HTTP services)
```python
meter = get_meter()

request_duration = meter.create_histogram(
    "prophet_api_request_duration_seconds",
    unit="s",
    description="API request duration",
    explicit_bucket_boundaries_advisory=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)
request_counter = meter.create_counter(
    "prophet_api_requests_total",
    unit="1",
    description="Total API requests"
)
```

### Error Metrics
```python
error_counter = meter.create_counter(
    "prophet_errors_total",
    unit="1",
    description="Total errors by type"
)
```

### Business Metrics (service-specific)
Define service-specific metrics following the naming convention:
```
prophet_<service>_<metric>_<unit>
```

Examples:
- `prophet_webhook_deliveries_total`
- `prophet_propagation_runs_total`
- `prophet_scheduler_job_duration_seconds`

---

## Trace Context Propagation

When calling downstream services, propagate the trace context:

```python
from opentelemetry.propagate import inject, extract
from opentelemetry import trace

# Inject into outgoing HTTP headers
headers = {}
inject(headers)
response = requests.post(url, headers=headers, json=payload)

# Extract from incoming webhook event payload
incoming_headers = event.get("_trace_headers", {})
context = extract(incoming_headers)
with tracer.start_as_current_span("my.span", context=context):
    ...
```

When triggering a Tekton PipelineRun, include the trace context in annotations:

```python
trace_headers = {}
inject(trace_headers)

pipeline_run = {
    "apiVersion": "tekton.dev/v1",
    "kind": "PipelineRun",
    "metadata": {
        "generateName": "build-test-deploy-",
        "annotations": {
            "otel.trace.context": json.dumps(trace_headers)
        }
    },
    ...
}
```

---

## Testing Locally with jaeger-all-in-one

Use Jaeger all-in-one for local trace validation:

```bash
# Start Jaeger all-in-one
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \    # Jaeger UI
  -p 4317:4317 \      # OTLP gRPC
  -p 4318:4318 \      # OTLP HTTP
  jaegertracing/all-in-one:1.55

# Set OTEL endpoint to local Jaeger
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_SERVICE_NAME=my-service

# Run your service
python my_service.py

# View traces at http://localhost:16686
```

### Verifying Metrics Locally

```bash
# Start Prometheus
docker run -d --name prometheus \
  -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# prometheus.yml
# scrape_configs:
#   - job_name: my-service
#     static_configs:
#       - targets: ['host.docker.internal:8889']
```

---

## Logging Best Practices

All logs **MUST** be structured JSON and include `trace_id` and `span_id`:

```python
import logging
import json
from opentelemetry import trace

class OTELLogFormatter(logging.Formatter):
    def format(self, record):
        span = trace.get_current_span()
        ctx = span.get_span_context()
        
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "service": "my-service",
            "message": record.getMessage(),
            "trace_id": format(ctx.trace_id, '032x') if ctx.is_valid else None,
            "span_id": format(ctx.span_id, '016x') if ctx.is_valid else None,
        }
        if hasattr(record, '__dict__'):
            log_data.update({k: v for k, v in record.__dict__.items()
                            if k not in ('msg', 'args', 'levelname', 'levelno', 
                                         'pathname', 'filename', 'module', 'exc_info',
                                         'exc_text', 'stack_info', 'lineno', 'funcName',
                                         'created', 'msecs', 'relativeCreated', 'thread',
                                         'threadName', 'processName', 'process', 'name')})
        return json.dumps(log_data)

# Apply formatter
handler = logging.StreamHandler()
handler.setFormatter(OTELLogFormatter())
logging.root.addHandler(handler)
```

---

## Troubleshooting

### Spans not appearing in Jaeger
1. Check OTEL_EXPORTER_OTLP_ENDPOINT is set correctly
2. Verify the OTEL Collector sidecar is running: `kubectl logs <pod> -c otel-collector`
3. Check for gRPC connection errors in the collector logs

### Metrics not appearing in Prometheus
1. Verify Prometheus is scraping port 8889 of the OTEL Collector
2. Check metric names match the `prophet_` prefix convention
3. Wait for the first export interval (15 seconds)

### High cardinality causing performance issues
1. Avoid using high-cardinality values (user IDs, UUIDs) as metric labels
2. Use trace attributes instead of metric labels for high-cardinality data
