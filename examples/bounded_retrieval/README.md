# Fictional bounded Git retrieval

A disposable local Git repository with three invented files compares one fresh clone per read with a single shared clone. Both paths check the expected revision and return original blob bytes in order. Only three fixture paths and groups of one to four requests are accepted. Temporary repositories are removed automatically.

Requires Python 3 and Git. Run from the portfolio root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s examples/bounded_retrieval -v
PYTHONDONTWRITEBYTECODE=1 python3 examples/bounded_retrieval/retrieval.py
```

Measured November 24, 2026 ET: 7/7 tests passed. Two reads required 2 versus 1 clone; three reads required 3 versus 1. Retrieved bytes matched the originals. Invalid revisions, paths and request sizes were rejected.

These are local Git operation counts, not network latency, token usage, revocation tests or private gateway code. No live repository or credentials are used.
