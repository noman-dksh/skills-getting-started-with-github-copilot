Tests for the FastAPI backend

Run tests from the repository root:

```bash
python3 -m pip install -r requirements.txt
pytest -q
```

Notes:
- Tests use the Arrange-Act-Assert (AAA) pattern.
- Tests use `httpx.AsyncClient` and `pytest-asyncio`.
- The in-memory `activities` dict is restored after each test by an autouse fixture.
