# Phase 9 Git Initialization Commands

## Status

This folder is not initialized as git yet. [Certain]

Do not commit automatically. [Certain]

Run these commands manually after reviewing the secret hygiene doc. [Certain]

## Safe Initialization

```powershell
cd C:\Users\onwus\Downloads\gemini-agents-2026
git init
git status
git add README.md LICENSE pyproject.toml streamlit_app.py Dockerfile .dockerignore .gitignore .env.example src scripts docs templates tests
git status
```

## What To Check Before Commit

Confirm `git status` does not show: [Certain]

- `.env` [Certain]
- generated `reports/*.md` files. [Certain]
- service account JSON files. [Certain]
- credential JSON files. [Certain]
- `.streamlit/secrets.toml` [Certain]
- `.venv/` [Certain]
- `__pycache__/` [Certain]
- `node_modules/` [Certain]

## Optional Pre-Commit Scan

Run this before the first commit: [Certain]

```powershell
rg -n "AIza|GOOGLE_API_KEY=\\s*\\S|PHOENIX_API_KEY=\\s*\\S|PHOENIX_TOKEN=\\s*\\S|ARIZE_API_KEY=\\s*\\S|ARIZE_SPACE_ID=\\s*\\S|sk-ant|BEGIN PRIVATE KEY|client_secret|service_account|credentials" --glob '!.env' .
```

Only placeholders, docs warnings, and source-code environment variable names should appear. [Certain]

Do not commit if an actual key value appears. [Certain]

