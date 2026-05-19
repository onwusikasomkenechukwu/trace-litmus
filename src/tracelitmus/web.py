"""Thin Streamlit UI for local TraceLitmus demos."""

from __future__ import annotations

from datetime import datetime
from os import environ
from pathlib import Path
from traceback import format_exc
from urllib.parse import urlsplit, urlunsplit

import streamlit as st

from .phoenix_client import load_env_file
from .cli import run_audit, run_mcp_audit


def _report_dir() -> Path:
    return Path(environ.get("TRACE_LITMUS_REPORT_DIR", "reports"))


def _default_output(source: str) -> Path:
    if source == "Phoenix MCP":
        return _report_dir() / "demo_mcp.md"
    return _report_dir() / "demo.md"


def _default_source() -> str:
    value = environ.get("TRACE_LITMUS_DEFAULT_SOURCE", "offline").strip().lower()
    if value in {"mcp", "phoenix", "phoenix mcp"}:
        return "Phoenix MCP"
    return "Offline fixture"


def _default_project(source: str) -> str:
    configured = environ.get("TRACE_LITMUS_DEFAULT_PROJECT")
    if configured:
        return configured
    return "tracelitmus-demo" if source == "Phoenix MCP" else "demo"


def _gemini_enabled_default() -> bool:
    return environ.get("TRACE_LITMUS_ENABLE_GEMINI", "").lower() in {"1", "true", "yes"}


def _phoenix_base_url() -> str:
    return environ.get("PHOENIX_BASE_URL", "http://127.0.0.1:6006")


def _redact_url(value: str) -> str:
    parsed = urlsplit(value)
    if parsed.username or parsed.password:
        netloc = parsed.hostname or ""
        if parsed.port:
            netloc = f"{netloc}:{parsed.port}"
        return urlunsplit((parsed.scheme, netloc, parsed.path, "[redacted-query]" if parsed.query else "", ""))
    if parsed.query:
        return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "[redacted-query]", ""))
    return value


def _is_hosted_runtime() -> bool:
    return bool(environ.get("K_SERVICE") or environ.get("CLOUD_RUN_JOB"))


def _is_localhost_url(value: str) -> bool:
    host = (urlsplit(value).hostname or "").lower()
    return host in {"127.0.0.1", "localhost", "::1"}


def _run_selected_audit(
    source: str,
    project: str,
    output_path: Path,
    *,
    gemini_explanation: bool,
) -> str:
    if source == "Phoenix MCP":
        path = run_mcp_audit(
            project=project,
            output=str(output_path),
            gemini_explanation=gemini_explanation,
        )
    else:
        path = run_audit(
            project=project,
            offline=True,
            output=str(output_path),
            gemini_explanation=gemini_explanation,
        )
    return path.read_text(encoding="utf-8")


def main() -> None:
    load_env_file()
    st.set_page_config(page_title="TraceLitmus", layout="wide")
    st.title("TraceLitmus")
    st.caption("A reproducibility litmus test for Phoenix LLM evaluation experiments.")

    with st.sidebar:
        st.header("Audit")
        source_options = ["Offline fixture", "Phoenix MCP"]
        default_source = _default_source()
        source = st.radio(
            "Source",
            source_options,
            index=source_options.index(default_source),
            help="Phoenix MCP runs the live @arizeai/phoenix-mcp path. Offline fixture is for local skeleton checks.",
        )
        project = st.text_input("Project", value=_default_project(source))
        output_path = st.text_input("Output Markdown", value=str(_default_output(source)))
        gemini_explanation = st.checkbox(
            "Add Gemini explanation",
            value=_gemini_enabled_default(),
            help="Gemini can narrate findings, but cannot change rule IDs, severities, scores, or evidence refs.",
        )
        st.info(
            "MCP mode currently runs only `missing_baseline`. Offline mode still runs the seven placeholder rules."
        )
        phoenix_url = _phoenix_base_url()
        if source == "Phoenix MCP" and _is_hosted_runtime() and _is_localhost_url(phoenix_url):
            st.warning(
                "Cloud Run cannot reach a Phoenix instance on 127.0.0.1. Configure a hosted PHOENIX_BASE_URL."
            )
        st.subheader("System status")
        st.write(f"Selected source: {source}")
        st.write(f"Phoenix base URL: {_redact_url(phoenix_url)}")
        st.write(f"Gemini enabled: {gemini_explanation}")
        st.write(f"Report mode: {'Gemini explanation' if gemini_explanation else 'Deterministic'}")
        run_clicked = st.button("Run audit", type="primary", use_container_width=True)

    if "report_markdown" not in st.session_state:
        st.session_state.report_markdown = ""
        st.session_state.report_name = "tracelitmus-report.md"

    if run_clicked:
        try:
            with st.status("Running audit...", expanded=True) as status:
                st.write(f"Source: {source}")
                st.write(f"Project: {project}")
                st.write(f"Gemini explanation: {'on' if gemini_explanation else 'off'}")
                markdown = _run_selected_audit(
                    source,
                    project,
                    Path(output_path),
                    gemini_explanation=gemini_explanation,
                )
                st.session_state.report_markdown = markdown
                st.session_state.report_name = Path(output_path).name
                status.update(label="Audit complete", state="complete")
        except Exception as exc:
            st.error("Audit failed. The error below is not hidden.")
            st.exception(exc)
            st.code(format_exc(), language="text")

    if st.session_state.report_markdown:
        if "## Gemini Explanation\n\nWarning:" in st.session_state.report_markdown:
            st.warning("Gemini explanation was requested but unavailable. The deterministic report still ran.")
        st.subheader("Report")
        st.download_button(
            "Download Markdown",
            data=st.session_state.report_markdown,
            file_name=st.session_state.report_name,
            mime="text/markdown",
        )
        st.markdown(st.session_state.report_markdown)
    else:
        st.subheader("Ready")
        st.write("Choose a source, enter a project, and run the audit.")
        st.write(f"Session started: {datetime.now().isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
