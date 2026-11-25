"""Local fictional Git fixture; no network or private source access."""
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

FILES = ("design.txt", "checks.txt", "notes.txt")


def git(directory: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(directory), *args], text=True,
        stderr=subprocess.PIPE,
    ).rstrip("\n")


def create_fixture(directory: Path) -> str:
    git(directory, "init", "-q", "--object-format=sha1")
    for name, value in zip(FILES, ("Design: review first", "Checks: preserve evidence", "Notes: fictional only")):
        (directory / name).write_text(value + "\n")
    git(directory, "add", *FILES)
    git(directory, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-qm", "Fictional source snapshot")
    return git(directory, "rev-parse", "HEAD")


def retrieve(source: Path, expected: str, requests: tuple[str, ...], *, batch: bool):
    """Compare separate snapshots to one shared snapshot; exact fixture paths only."""
    if not 1 <= len(requests) <= 4 or any(p not in FILES for p in requests):
        raise ValueError("bounded fixture paths required")
    if len(expected) != 40 or any(c not in "0123456789abcdef" for c in expected):
        raise ValueError("exact revision required")
    source = source.resolve()
    output, clones = [], 0
    groups = (requests,) if batch else tuple((p,) for p in requests)
    with TemporaryDirectory() as tmp:
        for group in groups:
            dest = Path(tmp) / f"snapshot-{clones}"
            git(Path(tmp), "clone", "-q", "--local", "--no-hardlinks", "--no-checkout",
                "--", str(source), str(dest))
            clones += 1
            if git(dest, "rev-parse", "HEAD") != expected:
                raise ValueError("snapshot revision mismatch")
            for path in group:
                output.append(subprocess.check_output(
                    ["git", "-C", str(dest), "show", f"{expected}:{path}"],
                    stderr=subprocess.PIPE))
    return tuple(output), clones


def benchmark():
    with TemporaryDirectory() as tmp:
        source = Path(tmp)
        revision = create_fixture(source)
        for label, paths in (("two reads", FILES[:2]), ("three reads", FILES)):
            a, count_a = retrieve(source, revision, paths, batch=False)
            b, count_b = retrieve(source, revision, paths, batch=True)
            assert a == b
            print(f"{label}: exact match; clones {count_a} -> {count_b}")


if __name__ == "__main__":
    benchmark()
