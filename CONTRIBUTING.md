# Contributing to ai-code-generator-studio

Thanks for wanting to help build the studio. This is a Windows-first Python
desktop tool that turns natural-language prompts into compilable code across
Python, C++, C#, and Java targets. Contributions are welcome from anyone who
can read a pipeline and ship a worker.

## Ground rules

- One concern per pull request. A new ingest handler is a PR. A new output
  driver is a PR. Refactors that touch the pipeline graph need a short design
  note in the PR body.
- Every worker (`src/pipeline/workers/*.py`) must be pure in its `process()`
  method: input job in, output job out, no global mutation. Side effects go
  through the `services/` layer.
- Tests live next to nothing — they live in `tests/`. If you add a worker,
  add a test that feeds it a fixture job and asserts on the emitted artifact.
- Type hints are mandatory on public functions. `mypy --strict` runs in CI.

## Dev setup

```
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

Run the suite:

```
pytest -q
```

Run the studio locally against a fixture prompt:

```
python -m src.bootstrap --prompt "write a fastapi healthcheck" --target python
```

## Commit style

Conventional commits. `feat(worker): add rust output driver` is good.
`fixed stuff` is not.

## Code of conduct

Be decent. Roast code, not people.