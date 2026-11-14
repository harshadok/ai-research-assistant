# Verification — 14 November 2026

## Automated checks

- Python backend suite: **4 passed** in the local development environment.
- `python -m pip check`: no broken requirements for the installed project environment.
- Deterministic tests isolate provider failures using doubles; the real-provider checks below are separate evidence.
- GitHub Actions runs the backend suite on Python 3.11 without requiring model weights or credentials.

## Real-provider checks

- Live Wikipedia search and article fetching succeeded for “Retrieval-augmented generation”.
- Real local-model synthesis returned four claims whose supporting quotes were present in the fetched source.
- Unknown source IDs and fabricated quotes were rejected by deterministic tests.
- Quote presence does not establish factual truth or entailment; the API and exports disclose this scope.

## Scope

This is a runnable single-user local portfolio implementation. Smoke checks on synthetic/public data are not a production-readiness claim, a general quality benchmark, or proof that an AI output is always correct. See README for supported formats, runtime dependencies and operational boundaries.
