# Docker Smoke Test

## Build

```powershell
docker build -t tracelitmus .
```

## Run

```powershell
docker run --rm -p 8080:8080 --env-file .env tracelitmus
```

If no `.env` file exists, create one from `.env.example` first. [Certain]

## Open

Open `http://127.0.0.1:8080`. [Certain]

## Expected Checks

- Streamlit loads. [Certain]
- Offline mode runs. [Certain]
- Gemini fallback displays if no key is present and Gemini explanation is enabled. [Certain]
- MCP mode works if `PHOENIX_BASE_URL` points to a Phoenix endpoint reachable from inside the container. [Certain]
- MCP mode fails visibly with an actionable error if `PHOENIX_BASE_URL` is unreachable. [Certain]

## Notes

Inside Docker, `127.0.0.1` means the container itself. [Certain]

To reach Phoenix on the host machine from Docker Desktop, try `PHOENIX_BASE_URL=http://host.docker.internal:6006`. [Likely]

## Local Environment Blocker Observed During Phase 4 And Phase 5

Docker was not available in the current shell during Phase 4 or Phase 5 validation. [Certain]

Exact error:

```text
docker : The term 'docker' is not recognized as the name of a cmdlet, function, script file, or operable program.
```
