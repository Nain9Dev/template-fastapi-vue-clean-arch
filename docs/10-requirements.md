# Requirements

Stable functional requirements written in EARS notation.

| ID | Requirement | Status |
|---|---|---|
| REQ-001 | When the service starts, the system shall initialize database schema idempotently without blocking worker startup. | Implemented |
| REQ-002 | When an item is created, the title shall contain at least 3 non-whitespace characters or return HTTP 400 ProblemDetails. | Implemented |
| REQ-003 | When the `/api/v1/health` endpoint is probed, the system shall return status 200 with operational metrics. | Implemented |
| REQ-004 | When running in local development, the system shall support zero-config sqlite+aiosqlite fallback without mandatory Docker. | Implemented |
