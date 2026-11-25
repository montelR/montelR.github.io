"""Invented document-review outcomes, not exported Sentinel Work cases."""
from gate import Pair

# Five variations of the same underlying redundant-review mechanism.
HOLD_CASES = tuple(
    Pair(f"repeat-{i}", "stale-preview", True, "review", "ready",
         "review", "ready", 1, 0)
    for i in range(1, 6)
) + (
    Pair("new-content", "necessary-review", False, "review", "review",
         "review", "review", 1, 1),
    Pair("invalid-state", "invalid-state", False, "blocked", "blocked",
         "blocked", "blocked", 0, 0),
)

# A genuinely separate invented benefit: duplicate review scheduling.
SECOND_MECHANISM = Pair("duplicate-schedule", "duplicate-schedule", True,
                        "review", "ready", "review", "ready", 1, 0)
