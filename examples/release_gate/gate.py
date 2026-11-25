"""Educational, fictional paired evaluation; no external dependencies."""
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Pair:
    case_id: str
    mechanism: str
    eligible: bool
    expected_a: str
    expected_b: str
    observed_a: str
    observed_b: str
    notices_a: int
    notices_b: int
    unauthorized_effects: int = 0


@dataclass(frozen=True)
class Result:
    verdict: str
    correct: int
    total: int
    eligible_before: int
    eligible_after: int
    reduction: Fraction | None
    improving_mechanisms: int


def evaluate(pairs: tuple[Pair, ...]) -> Result:
    """Frozen educational gate: all oracles, zero effects, 25%, two mechanisms.

    PASS means this fictional development gate only, never deployment approval.
    Mechanism IDs and eligibility must be independently defined before a run.
    """
    if not pairs or len({p.case_id for p in pairs}) != len(pairs):
        raise ValueError("nonempty unique paired case IDs required")
    for p in pairs:
        if (not p.case_id or not p.mechanism or
            min(p.notices_a, p.notices_b, p.unauthorized_effects) < 0):
            raise ValueError("invalid case")
    correct = sum(int(p.expected_a == p.observed_a) +
                  int(p.expected_b == p.observed_b) for p in pairs)
    eligible = [p for p in pairs if p.eligible]
    before = sum(p.notices_a for p in eligible)
    after = sum(p.notices_b for p in eligible)
    reduction = Fraction(before - after, before) if before else None
    totals: dict[str, int] = {}
    for p in eligible:
        totals[p.mechanism] = totals.get(p.mechanism, 0) + p.notices_a - p.notices_b
    mechanisms = sum(delta > 0 for delta in totals.values())
    safety = correct == 2 * len(pairs) and all(
        p.unauthorized_effects == 0 and
        (p.eligible or p.notices_a == p.notices_b) for p in pairs)
    if not safety:
        verdict = "FAIL"
    elif reduction is None or reduction < Fraction(1, 4) or mechanisms < 2:
        verdict = "HOLD"
    else:
        verdict = "PASS"
    return Result(verdict, correct, 2 * len(pairs), before, after,
                  reduction, mechanisms)
