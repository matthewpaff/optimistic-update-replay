# Optimistic Update Replay

Replay a single pending optimistic edit with rollback, refresh versions, and conflict handling.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external server, Redis, Celery, or network access is required.

## Run

```console
python -m optimistic_replay --help
python -m optimistic_replay examples/sample.json
python -m optimistic_replay --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Requires integer value, nonnegative version, and up to 500 events. begin requires id/value and permits one pending mutation. resolve requires matching id and success; a success commits only if the saved base version still matches, otherwise it becomes conflict; failure rolls back. refresh requires value/version and accepts only newer versions; a pending edit remains displayed until resolution. Every outcome reports visible value, confirmed version, and pending ID. This deterministic state exercise is not React, a browser, a server, or a multi-client concurrency guarantee.

## Learning focus

The modeled 2020 optimistic UI update and stale-cache invalidation learning themes. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `optimistic_replay/core.py`: validated parsing, storage, or state transitions.
- `optimistic_replay/cli.py`: JSON command interface.
- `optimistic_replay/generate_fixtures.py`: original deterministic validation cases.
- `optimistic_replay/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 525 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
