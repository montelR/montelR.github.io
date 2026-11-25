# Fictional review handoff regression

A standalone Python standard-library example of separating positive evidence from permission to continue. All data is fictional. No browser, network, credentials, database or external service is required.

Run from the repository root:

```sh
HANDOFF_VARIANT=baseline PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s examples/session_handoff -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s examples/session_handoff -v
```

The first command intentionally exits 1 with two failing assertions: a different actor and an empty actor are incorrectly allowed. The second exits 0 with all eight tests passing. Both use unchanged expectations. The model only evaluates a Boolean policy.

| Scenario | Expected | Baseline | Corrected |
| --- | --- | --- | --- |
| Designated reviewer, accepted current revision | Allow | Allow | Allow |
| Different actor, same accepted revision | Deny | Allow | Deny |
| Missing actor | Deny | Allow | Deny |
| No acceptance | Deny | Deny | Deny |
| Stale revision | Deny | Deny | Deny |
| Wrong document | Deny | Deny | Deny |
| Closed review | Deny | Deny | Deny |
| Newer unreviewed revision | Deny | Deny | Deny |

Measured November 24, 2026 ET: initial rule failed exactly two tests; corrected rule passed all eight; explicit baseline rerun reproduced both failures. This educational model is not the original Sentinel Work implementation, authentication system or production security solution. Real systems must establish trusted identity, atomic authorization, session lifetime and replay protection independently.
