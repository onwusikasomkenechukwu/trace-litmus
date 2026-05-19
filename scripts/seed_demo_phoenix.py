"""Seed a local Phoenix instance with demo data for TraceLitmus Phase 1.

This script writes data directly to Phoenix through REST endpoints. TraceLitmus
must still read/audit that data through `@arizeai/phoenix-mcp`.
"""

from __future__ import annotations

from datetime import UTC, datetime
from json import dumps, loads
from os import environ
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def load_env_file(path: Path | None = None) -> None:
    env_path = path or Path.cwd() / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def phoenix_request(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    base_url = environ.get("PHOENIX_BASE_URL", "http://127.0.0.1:6006").rstrip("/")
    api_key = environ.get("PHOENIX_API_KEY", "")
    data = dumps(body).encode("utf-8") if body is not None else None
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["api_key"] = api_key
    request = Request(f"{base_url}{path}", data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Phoenix API {method} {path} failed: {exc.code} {error_body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach Phoenix at {base_url}: {exc}") from exc
    return loads(response_body) if response_body else {}


def seed_dataset(dataset_name: str) -> str:
    examples = [
        {
            "input": {"question": "What evidence supports claim A?"},
            "output": {"answer": "Source S1 supports claim A."},
            "metadata": {"split": "demo", "topic": "claim-a"},
        },
        {
            "input": {"question": "Which source contradicts claim B?"},
            "output": {"answer": "Source S2 contradicts claim B."},
            "metadata": {"split": "demo", "topic": "claim-b"},
        },
        {
            "input": {"question": "Summarize support for claim C."},
            "output": {"answer": "Source S3 supports claim C with measured evidence."},
            "metadata": {"split": "demo", "topic": "claim-c"},
        },
    ]
    response = phoenix_request(
        "POST",
        "/v1/datasets/upload?sync=true",
        {
            "action": "append",
            "name": dataset_name,
            "inputs": [item["input"] for item in examples],
            "outputs": [item["output"] for item in examples],
            "metadata": [item["metadata"] for item in examples],
        },
    )
    dataset_id = response.get("data", {}).get("dataset_id")
    if not dataset_id:
        raise RuntimeError(f"Phoenix did not return a dataset_id: {response}")
    return str(dataset_id)


def create_experiment(dataset_id: str, *, name: str, metadata: dict[str, Any]) -> str:
    response = phoenix_request(
        "POST",
        f"/v1/datasets/{dataset_id}/experiments",
        {
            "name": name,
            "description": "TraceLitmus Phase 1 seeded experiment metadata.",
            "metadata": metadata,
            "repetitions": 1,
        },
    )
    experiment_id = response.get("data", {}).get("id")
    if not experiment_id:
        raise RuntimeError(f"Phoenix did not return an experiment id: {response}")
    return str(experiment_id)


def main() -> None:
    load_env_file()
    project_name = environ.get("PHOENIX_PROJECT_NAME", "tracelitmus-demo")
    dataset_name = environ.get("PHOENIX_DATASET_NAME", f"{project_name}-dataset")
    stamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")

    dataset_id = seed_dataset(dataset_name)
    baseline_id = create_experiment(
        dataset_id,
        name=f"{project_name}-baseline-{stamp}",
        metadata={
            "tracelitmus_role": "baseline",
            "baseline_experiment_id": "self",
            "project_name": project_name,
            "sample_size": 3,
        },
    )
    candidate_id = create_experiment(
        dataset_id,
        name=f"{project_name}-candidate-missing-baseline-{stamp}",
        metadata={
            "tracelitmus_role": "candidate",
            "project_name": project_name,
            "sample_size": 3,
            "intentionally_missing": "baseline_experiment_id",
        },
    )

    print(f"Seeded dataset: {dataset_name} ({dataset_id})")
    print(f"Seeded baseline experiment: {baseline_id}")
    print(f"Seeded candidate experiment missing baseline metadata: {candidate_id}")


if __name__ == "__main__":
    main()
