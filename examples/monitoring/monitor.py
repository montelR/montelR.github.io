"""Fictional read-only monitoring and evidence model, no host queries."""
from dataclasses import dataclass
from hashlib import sha256
import json


@dataclass(frozen=True)
class Reading:
    observed_at: int
    healthy: bool


def classify(reading: Reading | None, now: int, max_age: int = 60) -> str:
    if max_age < 0:
        raise ValueError("invalid maximum age")
    if reading is None or reading.observed_at > now or now - reading.observed_at > max_age:
        return "UNKNOWN"
    return "HEALTHY" if reading.healthy else "UNHEALTHY"


def summarize(raw: bytes) -> tuple[bytes, bytes]:
    """Preserve original bytes and provide bounded counts plus a digest."""
    lines = raw.splitlines()
    summary = json.dumps({
        "lines": len(lines),
        "errors": sum(line.startswith(b"ERROR ") for line in lines),
        "sha256": sha256(raw).hexdigest(),
    }, sort_keys=True).encode()
    return raw, summary


def verify(raw: bytes, summary: bytes) -> bool:
    return summarize(raw)[1] == summary


def demo():
    raw = b"INFO fictional observation\n" * 200 + b"ERROR fictional failure\n"
    saved, summary = summarize(raw)
    assert saved == raw and verify(saved, summary)
    print(f"Fictional evidence: {len(raw)} raw bytes; {len(summary)} summary bytes")
    print("Fresh:", classify(Reading(100, True), 110))
    print("Stale:", classify(Reading(100, True), 200))
    print("Missing:", classify(None, 200))


if __name__ == "__main__":
    demo()
