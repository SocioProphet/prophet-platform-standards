# Audit Log Guide

Reference guide for querying, exporting, and understanding the Prophet Platform audit log.

The audit log is defined in ADR-050 and stores immutable records of every build, deploy, policy decision, and secret access event on the platform.

---

## Schema Reference

See `schemas/audit-log-schema.avro` for the canonical Avro schema. Key fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID string | Primary key (immutable) |
| `timestamp` | long (epoch ms) | Event time (UTC, immutable) |
| `actor.user_id` | string/null | GitHub user login |
| `actor.service_account` | string/null | Kubernetes ServiceAccount name |
| `action` | string | Action performed (e.g. `task.build`, `deploy.prod`) |
| `resource.repo` | string | GitHub repository full name |
| `resource.ref` | string | Git branch, tag, or commit SHA |
| `status` | enum | `success`, `failure`, `in_progress` |
| `adr_reference` | string | ADR governing this event |
| `trace_id` | string | OTEL trace ID for correlation |
| `image_digest` | string | SHA256 of built/deployed image |
| `signature` | string | cosign signature OCI reference |

---

## Querying the Audit Log

### By Repository

```sql
-- All events for a specific repo in the last 30 days
SELECT id, timestamp, actor_user_id, actor_service_account, action, status, adr_reference
FROM audit_events
WHERE resource_repo = 'SocioProphet/sociosphere'
  AND timestamp > EXTRACT(EPOCH FROM NOW() - INTERVAL '30 days') * 1000
ORDER BY timestamp DESC;
```

### By Actor (User)

```sql
-- All actions by a specific user
SELECT id, timestamp, action, resource_repo, resource_ref, status
FROM audit_events
WHERE actor_user_id = 'mdheller'
ORDER BY timestamp DESC
LIMIT 100;
```

### By Action Type

```sql
-- All production deployments
SELECT id, timestamp, actor_user_id, actor_service_account, resource_repo, status, image_digest
FROM audit_events
WHERE action = 'deploy.prod'
ORDER BY timestamp DESC;

-- All build failures in the last 7 days
SELECT id, timestamp, actor_service_account, resource_repo, resource_ref, details
FROM audit_events
WHERE action = 'task.build'
  AND status = 'failure'
  AND timestamp > EXTRACT(EPOCH FROM NOW() - INTERVAL '7 days') * 1000
ORDER BY timestamp DESC;
```

### By Commit SHA

```sql
-- Full audit trail for a specific commit
SELECT id, timestamp, action, actor_user_id, actor_service_account, status, details
FROM audit_events
WHERE resource_ref = 'abc123def456'
   OR details LIKE '%abc123def456%'
ORDER BY timestamp ASC;
```

### By Time Range

```sql
-- Events on a specific date (for incident investigation)
SELECT id, timestamp, action, actor_user_id, resource_repo, status
FROM audit_events
WHERE timestamp BETWEEN
  EXTRACT(EPOCH FROM '2026-04-06 00:00:00'::timestamp) * 1000
  AND EXTRACT(EPOCH FROM '2026-04-06 23:59:59'::timestamp) * 1000
ORDER BY timestamp ASC;
```

### By Policy / ADR Reference

```sql
-- All events referencing ADR-050 (security/compliance events)
SELECT id, timestamp, action, resource_repo, status, details
FROM audit_events
WHERE adr_reference = 'ADR-050'
ORDER BY timestamp DESC
LIMIT 500;
```

### Correlate with OTEL Traces

```sql
-- Find the audit event for a specific OTEL trace
SELECT id, timestamp, action, actor_user_id, resource_repo, status, pipeline_run_name
FROM audit_events
WHERE trace_id = '4bf92f3577b34da6a3ce929d0e0e4736';
```

---

## Exporting Audit Reports

### CSV Export (for compliance review)

```sql
-- Export last 90 days of production deployments to CSV
COPY (
  SELECT
    to_timestamp(timestamp / 1000) AT TIME ZONE 'UTC' AS event_time,
    COALESCE(actor_user_id, actor_service_account) AS actor,
    action,
    resource_repo,
    resource_ref,
    status,
    image_digest,
    adr_reference
  FROM audit_events
  WHERE action IN ('deploy.staging', 'deploy.prod')
    AND timestamp > EXTRACT(EPOCH FROM NOW() - INTERVAL '90 days') * 1000
  ORDER BY timestamp ASC
) TO '/tmp/deploy-audit-report.csv' CSV HEADER;
```

### JSON Export (for SIEM integration)

```bash
# Export to JSON via psql
psql -d audit_db -c "
COPY (
  SELECT row_to_json(ae) FROM (
    SELECT * FROM audit_events
    WHERE timestamp > EXTRACT(EPOCH FROM NOW() - INTERVAL '30 days') * 1000
    ORDER BY timestamp ASC
  ) ae
) TO STDOUT;
" > audit-events-30d.jsonl
```

---

## Compliance Templates

### SOC 2 Type II: Change Management

Query for evidence of controlled deployment process:

```sql
-- Evidence: all changes were deployed via pipeline (not manual kubectl)
SELECT
  COUNT(*) AS total_deploys,
  SUM(CASE WHEN actor_service_account = 'tekton-build-sa' THEN 1 ELSE 0 END) AS pipeline_deploys,
  SUM(CASE WHEN actor_user_id IS NOT NULL THEN 1 ELSE 0 END) AS manual_deploys
FROM audit_events
WHERE action IN ('deploy.staging', 'deploy.prod')
  AND timestamp > EXTRACT(EPOCH FROM NOW() - INTERVAL '90 days') * 1000;

-- Evidence: all images are signed before deployment
SELECT
  COUNT(*) AS total_builds,
  SUM(CASE WHEN signature IS NOT NULL THEN 1 ELSE 0 END) AS signed_builds,
  ROUND(100.0 * SUM(CASE WHEN signature IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS signing_pct
FROM audit_events
WHERE action = 'task.build'
  AND timestamp > EXTRACT(EPOCH FROM NOW() - INTERVAL '90 days') * 1000;
```

### SOC 2 Type II: Access Control

```sql
-- Evidence: no unauthorized access attempts
SELECT timestamp, actor_user_id, action, resource_repo, details
FROM audit_events
WHERE action = 'rbac.violation'
  AND timestamp > EXTRACT(EPOCH FROM NOW() - INTERVAL '90 days') * 1000
ORDER BY timestamp DESC;
```

### SLSA Level 3 Evidence

```sql
-- Evidence: all images have SBOM and provenance attestation
SELECT
  resource_repo,
  resource_ref,
  image_digest,
  sbom_url,
  attestation_url,
  signature
FROM audit_events
WHERE action = 'task.build'
  AND status = 'success'
  AND timestamp > EXTRACT(EPOCH FROM NOW() - INTERVAL '90 days') * 1000
ORDER BY timestamp DESC;
```

---

## Retention Policy

Per ADR-050:

| Data | Retention | Policy |
|------|-----------|--------|
| Audit log records | **1 year minimum** | Append-only; records cannot be deleted or modified |
| Archived records (>1 year) | Indefinite (cost permitting) | Cold storage (e.g., S3 Glacier) |
| OTEL traces | 7 days | Jaeger data store |
| Application logs | 30 days | Loki data store |
| Metrics | 15 days | Prometheus TSDB |

### Archiving Old Records

```sql
-- Archive records older than 1 year to cold storage
-- (Run this as a scheduled job, not deletion)
INSERT INTO audit_events_archive
SELECT * FROM audit_events
WHERE timestamp < EXTRACT(EPOCH FROM NOW() - INTERVAL '1 year') * 1000;

-- After archiving, update archival_status (do NOT delete)
UPDATE audit_events
SET archived = true
WHERE timestamp < EXTRACT(EPOCH FROM NOW() - INTERVAL '1 year') * 1000;
```

---

## Audit Log Integrity

The audit log **MUST** be append-only. To verify integrity:

```sql
-- Check for any modified records (none should exist)
-- If your DB supports audit triggers, verify no UPDATE/DELETE operations
SELECT schemaname, tablename, operation, usename, timestamp
FROM pg_stat_activity
WHERE query LIKE '%UPDATE audit_events%'
   OR query LIKE '%DELETE FROM audit_events%';
```

For additional tamper-evidence, each batch of audit records should be:
1. Hashed (SHA256)
2. Hash stored in a separate immutable ledger
3. Compared periodically to detect unauthorized modifications
