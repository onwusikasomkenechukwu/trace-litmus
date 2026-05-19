# Phase 9 Public Repo File Set

## Commit These Files And Directories

Recommended public commit set: [Certain]

- `README.md` [Certain]
- `LICENSE` [Certain]
- `pyproject.toml` [Certain]
- `streamlit_app.py` [Certain]
- `Dockerfile` [Certain]
- `.dockerignore` [Certain]
- `.gitignore` [Certain]
- `.env.example` [Certain]
- `src/` [Certain]
- `scripts/` [Certain]
- `docs/` [Certain]
- `templates/` [Certain]
- `tests/fixtures/` if the fixtures remain synthetic and safe. [Certain]

## Do Not Commit These Files And Directories

Do not commit: [Certain]

- `.env` [Certain]
- `*.env` files with local values. [Certain]
- service account JSON files. [Certain]
- credential JSON files. [Certain]
- `.streamlit/secrets.toml` [Certain]
- local cache folders. [Certain]
- `.venv/` [Certain]
- `__pycache__/` [Certain]
- `*.pyc` [Certain]
- `node_modules/` [Certain]
- generated reports that may include secrets or local-only status. [Certain]
- Docker, Streamlit, Phoenix, or Cloud Run logs if they include local paths or credentials. [Certain]

## Generated Reports

Current generated Markdown reports under `reports/` should not be committed. [Certain]

`.gitignore` already excludes `reports/*.md` and `reports/*.html`. [Certain]

If sanitized sample reports are needed later, place them under `docs/examples/` and verify they contain no secrets, no local-only credentials, and no claims that hosted Phoenix MCP works. [Certain]

## Fixture Safety

`tests/fixtures/` is acceptable to commit if it contains synthetic demo data only. [Certain]

Fixtures should not include copied Phoenix Cloud responses containing private account IDs, real user data, API keys, or service metadata. [Certain]

## Current Workspace Notes

`.env` exists locally and is intentionally excluded. [Certain]

This folder is not initialized as git yet. [Certain]

Generated report files exist locally under `reports/`, but they are ignored by `.gitignore`. [Certain]

