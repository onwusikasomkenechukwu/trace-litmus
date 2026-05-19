# Arize AX Setup

This note is for configuring the Arize AX CLI profile used to inspect hosted Arize resources while TraceLitmus waits for a confirmed Phoenix-compatible hosted endpoint. [Certain]

Do not put API keys, space IDs, or exported shell commands in this file. [Certain]

## Install AX CLI

AX CLI requires Python 3.11 or newer. [Certain]

```powershell
python --version
python -m pip install arize-ax-cli
ax --version
```

The Arize AX docs also mention tool-based installs such as `uv tool install arize-ax-cli` or `pipx install arize-ax-cli` for agent setup workflows. [Likely]

## Create a profile correctly

Use a simple local profile name. [Certain]

Good profile names:

- `tracelitmus` [Certain]
- `default` [Certain]

Bad profile names:

- `export ARIZE_SPACE_ID=...` [Certain]
- an API key [Certain]
- a space ID [Certain]
- any copied shell command [Certain]

The profile name is just a local label for the AX CLI profile. [Certain]

```powershell
ax profiles create tracelitmus
```

When prompted, enter:

- API key: paste the Arize API key into the API key prompt only. [Certain]
- Region: enter the Arize routing region in the region prompt, for example a documented Arize region such as `us-east-1b`, if that is the region for the account. [Likely]
- Output format: choose `json`. [Certain]

Warning: do not paste `export ARIZE_SPACE_ID=...` into the profile name field. [Certain]

Non-interactive shape, using placeholders only:

```powershell
ax profiles create tracelitmus `
  --api-key "<ARIZE_API_KEY>" `
  --region "<ARIZE_REGION>" `
  --output-format json
```

Prefer the interactive prompt or environment-variable references when possible so secrets are not left in terminal history. [Likely]

## Verify the profile

```powershell
ax profiles show tracelitmus
ax profiles use tracelitmus
ax projects list
```

`ax profiles show` should show the profile settings without requiring secrets to be pasted into repo files. [Certain]

If you need to inspect spaces for setup, use the AX command appropriate for the account and request JSON output. [Likely]

```powershell
ax spaces list -o json
```

Do not copy space IDs or API keys into committed files. [Certain]

## Avoid committing secrets

Do not commit:

- `.env` [Certain]
- AX profile TOML files [Certain]
- files containing `ARIZE_API_KEY`, `PHOENIX_API_KEY`, `GOOGLE_API_KEY`, or `ARIZE_SPACE_ID` values [Certain]
- copied terminal transcripts that include key material [Certain]

On Windows, AX profiles are stored under `%USERPROFILE%\.arize\profiles\<profile>.toml`. [Certain]

Keep AX profile files outside this repository. [Certain]

Before public submission, search for accidental secrets:

```powershell
rg -n "ARIZE_API_KEY|ARIZE_SPACE_ID|PHOENIX_API_KEY|GOOGLE_API_KEY|AIza|ak_" .
```

If a secret appears in git history or chat, rotate it. [Certain]

## Mapping Arize / Phoenix hosted values into TraceLitmus

TraceLitmus does not use the AX profile directly for MCP mode. [Certain]

TraceLitmus needs these runtime values:

- `PHOENIX_BASE_URL`: hosted Phoenix-compatible base URL reachable from the app or Cloud Run. [Certain]
- `PHOENIX_API_KEY`: set only if the hosted endpoint requires it. [Likely]
- `PHOENIX_PROJECT_NAME`: project to audit, expected demo value `tracelitmus-demo`. [Certain]

Hosted Phoenix endpoint not confirmed yet; manual verification required.

Local process-scoped example with placeholders:

```powershell
$env:PHOENIX_BASE_URL="https://HOSTED_PHOENIX_ENDPOINT"
$env:PHOENIX_API_KEY="PHOENIX_API_KEY_IF_REQUIRED"
$env:PHOENIX_PROJECT_NAME="tracelitmus-demo"

python -m tracelitmus.cli audit --project tracelitmus-demo --source mcp --output reports/demo_mcp.md

Remove-Item Env:\PHOENIX_BASE_URL
Remove-Item Env:\PHOENIX_API_KEY
Remove-Item Env:\PHOENIX_PROJECT_NAME
```

Do not use `PHOENIX_BASE_URL=http://127.0.0.1:6006` in Cloud Run. [Certain]

## Sources

- Arize AX CLI overview: https://arize.com/docs/api-clients/cli/overview [Certain]
- Arize AX profile commands: https://arize.com/docs/api-clients/cli/profiles [Certain]
- Arize AX agent setup note: https://arize.com/docs/ax/set-up-with-ai-assistants [Likely]
