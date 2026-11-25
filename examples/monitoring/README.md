# Fictional monitoring and recoverable evidence

A standalone Python example distinguishes fresh healthy/unhealthy observations from stale, future-dated or absent data. It creates a compact diagnostic summary while retaining the original bytes.

Run from the portfolio root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s examples/monitoring -v
PYTHONDONTWRITEBYTECODE=1 python3 examples/monitoring/monitor.py
```

Measured November 24, 2026 ET: 9/9 tests passed. A fictional 5,424-byte log produced a 105-byte summary; original bytes were unchanged. Stale and absent readings classified UNKNOWN.

The summary is lossy; the original remains necessary for detailed analysis. The digest checks consistency, not authenticity against a malicious writer. No host health queries, real logs, persisted monitoring or external services are involved. Byte counts are not measured tokens or cost.
