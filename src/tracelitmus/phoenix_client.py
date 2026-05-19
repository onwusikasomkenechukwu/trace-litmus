"""Phoenix MCP client with offline fixture support and real stdio MCP mode."""

from __future__ import annotations

from json import JSONDecodeError, dumps, loads
from os import environ
from pathlib import Path
from shutil import which
from subprocess import PIPE, Popen
from threading import Thread
from typing import Any

from .models import PhoenixDataset, PhoenixExperiment, PhoenixProject


class PhoenixMCPError(RuntimeError):
    """Raised when the Phoenix MCP server or protocol call fails."""


def load_env_file(path: Path | None = None) -> None:
    """Load simple KEY=VALUE pairs from `.env` without overriding process env."""

    env_path = path or Path.cwd() / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


class _StdioMCPTransport:
    def __init__(self, command: list[str]) -> None:
        self.command = command
        self._next_id = 1
        self._stderr_lines: list[str] = []
        self.process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self._stderr_thread = Thread(target=self._drain_stderr, daemon=True)
        self._stderr_thread.start()
        self._initialize()

    def _drain_stderr(self) -> None:
        if self.process.stderr is None:
            return
        for raw_line in self.process.stderr:
            self._stderr_lines.append(raw_line.decode("utf-8", errors="replace").rstrip())

    @property
    def stderr_tail(self) -> str:
        return "\n".join(self._stderr_lines[-20:])

    def close(self) -> None:
        if self.process.poll() is None:
            self.process.terminate()

    def _send(self, message: dict[str, Any]) -> None:
        if self.process.stdin is None:
            raise PhoenixMCPError("Phoenix MCP process stdin is unavailable.")
        body = dumps(message).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        self.process.stdin.write(header + body)
        self.process.stdin.flush()

    def _read_response(self) -> dict[str, Any]:
        if self.process.stdout is None:
            raise PhoenixMCPError("Phoenix MCP process stdout is unavailable.")

        header_bytes = bytearray()
        while b"\r\n\r\n" not in header_bytes:
            chunk = self.process.stdout.read(1)
            if not chunk:
                raise PhoenixMCPError(
                    "Phoenix MCP process exited before sending a response."
                    f"\nStderr:\n{self.stderr_tail}"
                )
            header_bytes.extend(chunk)

        headers = header_bytes.decode("ascii", errors="replace").split("\r\n")
        content_length = None
        for header in headers:
            if header.lower().startswith("content-length:"):
                content_length = int(header.split(":", 1)[1].strip())
                break
        if content_length is None:
            raise PhoenixMCPError(f"MCP response missing Content-Length header: {headers}")

        body = self.process.stdout.read(content_length)
        try:
            return loads(body.decode("utf-8"))
        except JSONDecodeError as exc:
            raise PhoenixMCPError(f"MCP response was not valid JSON: {body!r}") from exc

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        request_id = self._next_id
        self._next_id += 1
        self._send(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params or {},
            }
        )
        response = self._read_response()
        if "error" in response:
            error = response["error"]
            raise PhoenixMCPError(
                f"MCP {method} failed: {error.get('message', error)}"
                f"\nStderr:\n{self.stderr_tail}"
            )
        return response.get("result", {})

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def _initialize(self) -> None:
        self.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "tracelitmus", "version": "0.1.0"},
            },
        )
        self.notify("notifications/initialized")

    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        result = self.request("tools/call", {"name": name, "arguments": arguments})
        if result.get("isError"):
            raise PhoenixMCPError(f"MCP tool {name} returned an error: {result}")
        content = result.get("content", [])
        if not content:
            return None
        first = content[0]
        if first.get("type") != "text":
            return first
        text = first.get("text", "")
        try:
            return loads(text)
        except JSONDecodeError:
            return text


class PhoenixMCPClient:
    CONFIRMED_TOOLS = (
        "list-prompts",
        "get-latest-prompt",
        "get-prompt-by-identifier",
        "get-prompt-version",
        "list-prompt-versions",
        "get-prompt-version-by-tag",
        "list-prompt-version-tags",
        "add-prompt-version-tag",
        "upsert-prompt",
        "list-projects",
        "get-spans",
        "get-span-annotations",
        "list-datasets",
        "get-dataset-examples",
        "get-dataset-experiments",
        "add-dataset-examples",
        "list-experiments-for-dataset",
        "get-experiment-by-id",
    )

    def __init__(
        self,
        *,
        offline: bool = False,
        source: str = "offline",
        fixture_path: Path | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
        mcp_command: str | None = None,
        mcp_package: str | None = None,
    ) -> None:
        load_env_file()
        self.offline = offline or source == "offline"
        self.source = "offline" if self.offline else source
        self.fixture_path = fixture_path or self._default_fixture_path()
        self.base_url = base_url or environ.get("PHOENIX_BASE_URL", "http://127.0.0.1:6006")
        self.api_key = api_key if api_key is not None else (
            environ.get("PHOENIX_API_KEY") or environ.get("PHOENIX_TOKEN", "")
        )
        self.mcp_command = mcp_command or environ.get("PHOENIX_MCP_COMMAND", "npx")
        self.mcp_package = mcp_package or environ.get("PHOENIX_MCP_PACKAGE", "@arizeai/phoenix-mcp@latest")
        self._fixture: dict[str, Any] | None = None
        self._transport: _StdioMCPTransport | None = None

    @staticmethod
    def _default_fixture_path() -> Path:
        return Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "sample_phoenix_response.json"

    def close(self) -> None:
        if self._transport is not None:
            self._transport.close()
            self._transport = None

    def __enter__(self) -> "PhoenixMCPClient":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def _command(self) -> list[str]:
        if not self.mcp_command:
            raise PhoenixMCPError("PHOENIX_MCP_COMMAND is required for source=mcp.")
        if not self.mcp_package:
            raise PhoenixMCPError("PHOENIX_MCP_PACKAGE is required for source=mcp.")
        executable = which(self.mcp_command) or self.mcp_command
        command = [executable, "-y", self.mcp_package, "--baseUrl", self.base_url]
        if self.api_key:
            command.extend(["--apiKey", self.api_key])
        return command

    def _mcp(self) -> _StdioMCPTransport:
        if self.offline:
            raise PhoenixMCPError("MCP calls are disabled in offline mode.")
        if self.source != "mcp":
            raise PhoenixMCPError(f"Unsupported Phoenix client source: {self.source}")
        if self._transport is None:
            try:
                self._transport = _StdioMCPTransport(self._command())
            except OSError as exc:
                raise PhoenixMCPError(
                    "Failed to start Phoenix MCP server. "
                    f"Command: {' '.join(self._command())}. Error: {exc}"
                ) from exc
        return self._transport

    def _call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        return self._call_tool_with_mcp_library(name, arguments)

    def _call_tool_with_mcp_library(self, name: str, arguments: dict[str, Any]) -> Any:
        try:
            import anyio
            from mcp import ClientSession
            from mcp.client.stdio import StdioServerParameters, stdio_client
        except ModuleNotFoundError as exc:
            raise PhoenixMCPError(
                "The Python `mcp` package is required for source=mcp. "
                "Install project dependencies before running the MCP audit."
            ) from exc

        async def run_tool() -> Any:
            command = self._command()
            parameters = StdioServerParameters(command=command[0], args=command[1:])
            try:
                async with stdio_client(parameters) as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        await session.initialize()
                        result = await session.call_tool(name, arguments)
            except Exception as exc:
                raise PhoenixMCPError(
                    f"MCP tool {name} failed through @arizeai/phoenix-mcp: {exc}"
                ) from exc
            if getattr(result, "isError", False):
                raise PhoenixMCPError(f"MCP tool {name} returned an error: {result}")
            content = getattr(result, "content", [])
            if not content:
                return None
            first = content[0]
            text = getattr(first, "text", None)
            if text is None and isinstance(first, dict):
                text = first.get("text")
            if text is None:
                return first
            try:
                return loads(text)
            except JSONDecodeError:
                return text

        try:
            return anyio.run(run_tool)
        except PhoenixMCPError:
            raise
        except Exception as exc:
            raise PhoenixMCPError(f"MCP tool {name} failed with {type(exc).__name__}: {exc}") from exc

    def load_offline_fixture(self) -> dict[str, Any]:
        if not self.offline:
            raise PhoenixMCPError("Offline fixture loading is disabled for source=mcp.")
        if self._fixture is None:
            self._fixture = loads(self.fixture_path.read_text(encoding="utf-8"))
        return self._fixture

    def _fixture_or_raise(self, key: str) -> Any:
        return self.load_offline_fixture().get(key, [])

    def list_prompts(self, limit: int = 100) -> Any:
        if self.offline:
            return self._fixture_or_raise("prompts")[:limit]
        return self._call_tool("list-prompts", {"limit": limit})

    def get_latest_prompt(self, prompt_identifier: str) -> Any:
        if self.offline:
            return self._fixture_or_raise("prompt_versions")[0]
        return self._call_tool("get-latest-prompt", {"prompt_identifier": prompt_identifier})

    def get_prompt_by_identifier(self, prompt_identifier: str) -> Any:
        if self.offline:
            return self.get_latest_prompt(prompt_identifier)
        return self._call_tool("get-prompt-by-identifier", {"prompt_identifier": prompt_identifier})

    def get_prompt_version(self, prompt_version_id: str) -> Any:
        if self.offline:
            return next(
                item for item in self._fixture_or_raise("prompt_versions") if item["id"] == prompt_version_id
            )
        return self._call_tool("get-prompt-version", {"prompt_version_id": prompt_version_id})

    def list_prompt_versions(self, prompt_identifier: str, limit: int = 100) -> Any:
        if self.offline:
            return self._fixture_or_raise("prompt_versions")[:limit]
        return self._call_tool(
            "list-prompt-versions",
            {"prompt_identifier": prompt_identifier, "limit": limit},
        )

    def get_prompt_version_by_tag(self, prompt_identifier: str, tag_name: str) -> Any:
        if self.offline:
            return next(
                item for item in self._fixture_or_raise("prompt_versions") if item.get("version_tag") == tag_name
            )
        return self._call_tool(
            "get-prompt-version-by-tag",
            {"prompt_identifier": prompt_identifier, "tag_name": tag_name},
        )

    def list_prompt_version_tags(self, prompt_version_id: str, limit: int = 100) -> Any:
        if self.offline:
            return [item.get("version_tag") for item in self._fixture_or_raise("prompt_versions")[:limit]]
        return self._call_tool(
            "list-prompt-version-tags",
            {"prompt_version_id": prompt_version_id, "limit": limit},
        )

    def add_prompt_version_tag(self, prompt_version_id: str, name: str, description: str | None = None) -> Any:
        if self.offline:
            raise NotImplementedError("Write operations are not implemented in offline mode.")
        return self._call_tool(
            "add-prompt-version-tag",
            {"prompt_version_id": prompt_version_id, "name": name, "description": description},
        )

    def upsert_prompt(self, **kwargs: Any) -> Any:
        if self.offline:
            raise NotImplementedError("Write operations are not implemented in offline mode.")
        return self._call_tool("upsert-prompt", kwargs)

    def list_projects(self, limit: int = 100, cursor: str | None = None, include_experiment_projects: bool = False) -> Any:
        if self.offline:
            return self._fixture_or_raise("projects")[:limit]
        arguments: dict[str, Any] = {
            "limit": limit,
            "include_experiment_projects": include_experiment_projects,
        }
        if cursor:
            arguments["cursor"] = cursor
        return self._call_tool("list-projects", arguments)

    def get_spans(self, project_name: str, **kwargs: Any) -> Any:
        if self.offline:
            return {"spans": self._fixture_or_raise("spans"), "nextCursor": None}
        return self._call_tool("get-spans", {"projectName": project_name, **kwargs})

    def get_span_annotations(self, project_name: str, span_ids: list[str], **kwargs: Any) -> Any:
        if self.offline:
            return {"annotations": self._fixture_or_raise("span_annotations"), "nextCursor": None}
        return self._call_tool(
            "get-span-annotations",
            {"projectName": project_name, "spanIds": span_ids, **kwargs},
        )

    def list_datasets(self, limit: int = 100) -> Any:
        if self.offline:
            return self._fixture_or_raise("datasets")[:limit]
        return self._call_tool("list-datasets", {"limit": limit})

    def get_dataset_examples(self, dataset_id: str | None = None, dataset_name: str | None = None) -> Any:
        if self.offline:
            if dataset_id is None:
                dataset_id = next(
                    item["id"] for item in self._fixture_or_raise("datasets") if item["name"] == dataset_name
                )
            examples = [
                item for item in self._fixture_or_raise("dataset_examples") if item["dataset_id"] == dataset_id
            ]
            return {"dataset_id": dataset_id, "examples": examples}
        arguments = self._dataset_selector(dataset_id=dataset_id, dataset_name=dataset_name)
        return self._call_tool("get-dataset-examples", arguments)

    def get_dataset_experiments(self, dataset_id: str | None = None, dataset_name: str | None = None) -> Any:
        if self.offline:
            if dataset_id is None:
                dataset_id = next(
                    item["id"] for item in self._fixture_or_raise("datasets") if item["name"] == dataset_name
                )
            return [item for item in self._fixture_or_raise("experiments") if item["dataset_id"] == dataset_id]
        arguments = self._dataset_selector(dataset_id=dataset_id, dataset_name=dataset_name)
        return self._call_tool("get-dataset-experiments", arguments)

    def add_dataset_examples(self, dataset_name: str, examples: list[dict[str, Any]]) -> Any:
        if self.offline:
            raise NotImplementedError("Write operations are not implemented in offline mode.")
        return self._call_tool("add-dataset-examples", {"dataset_name": dataset_name, "examples": examples})

    def list_experiments_for_dataset(
        self,
        dataset_id: str | None = None,
        dataset_name: str | None = None,
        limit: int = 100,
    ) -> Any:
        if self.offline:
            return self.get_dataset_experiments(dataset_id=dataset_id, dataset_name=dataset_name)
        arguments = {**self._dataset_selector(dataset_id=dataset_id, dataset_name=dataset_name), "limit": limit}
        return self._call_tool("list-experiments-for-dataset", arguments)

    def get_experiment_by_id(self, experiment_id: str) -> Any:
        if self.offline:
            return next(item for item in self._fixture_or_raise("experiments") if item["id"] == experiment_id)
        return self._call_tool("get-experiment-by-id", {"experiment_id": experiment_id})

    @staticmethod
    def _dataset_selector(dataset_id: str | None = None, dataset_name: str | None = None) -> dict[str, str]:
        if dataset_id:
            return {"dataset_id": dataset_id}
        if dataset_name:
            return {"dataset_name": dataset_name}
        raise PhoenixMCPError("dataset_id or dataset_name is required.")

    @staticmethod
    def normalize_project(raw: dict[str, Any]) -> PhoenixProject:
        return PhoenixProject(
            id=str(raw.get("id", "")),
            name=str(raw.get("name", "")),
            description=raw.get("description"),
        )

    @staticmethod
    def normalize_dataset(raw: dict[str, Any]) -> PhoenixDataset:
        version = (
            raw.get("version")
            or raw.get("version_id")
            or raw.get("latest_version_id")
            or raw.get("updated_at")
            or "unknown"
        )
        return PhoenixDataset(id=str(raw.get("id", "")), name=str(raw.get("name", "")), version=str(version))

    @staticmethod
    def normalize_experiment(raw: dict[str, Any], *, sample_size: int = 0) -> PhoenixExperiment:
        metadata = raw.get("metadata") or {}
        metrics = raw.get("metrics") or {}
        inferred_sample_size = raw.get("sample_size") or raw.get("num_examples") or raw.get("repetitions") or sample_size
        return PhoenixExperiment(
            id=str(raw.get("id", "")),
            dataset_id=str(raw.get("dataset_id", "")),
            prompt_version_id=raw.get("prompt_version_id"),
            metrics=metrics,
            metadata=metadata,
            sample_size=int(inferred_sample_size or 0),
        )
