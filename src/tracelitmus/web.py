"""Thin Streamlit UI for local TraceLitmus demos."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from os import environ
from pathlib import Path
from re import search
from traceback import format_exc
from urllib.parse import urlsplit, urlunsplit

import streamlit as st

from .phoenix_client import load_env_file
from .cli import run_audit, run_mcp_audit


@dataclass
class UiFinding:
    rule_id: str
    title: str
    severity: str
    description: str
    evidence: list[str]
    recommended_fix: str


SEVERITY_TAGS = {
    "critical": "[CRIT]",
    "high": "[HIGH]",
    "medium": "[WARN]",
    "low": "[INFO]",
}


def apply_terminal_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
          --tl-bg: #0a0a0a;
          --tl-panel: #0d120d;
          --tl-primary: #33ff00;
          --tl-secondary: #ffb000;
          --tl-error: #ff3333;
          --tl-border: #1f521f;
          --tl-text: #d6ffd1;
          --tl-muted: #85a985;
          --tl-font: "JetBrains Mono", "Fira Code", Consolas, monospace;
        }

        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
          background: var(--tl-bg) !important;
          color: var(--tl-text) !important;
          font-family: var(--tl-font) !important;
        }

        [data-testid="stAppViewContainer"]::before {
          content: "";
          position: fixed;
          inset: 0;
          pointer-events: none;
          z-index: 9999;
          background: repeating-linear-gradient(
            to bottom,
            rgba(51, 255, 0, 0.025),
            rgba(51, 255, 0, 0.025) 1px,
            transparent 1px,
            transparent 5px
          );
        }

        [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
          background: #070907 !important;
          color: var(--tl-text) !important;
          border-right: 1px solid var(--tl-border);
        }

        h1, h2, h3, h4, p, li, label, span, div {
          font-family: var(--tl-font) !important;
        }

        h1, h2, h3 {
          color: var(--tl-primary) !important;
          letter-spacing: 0;
        }

        .tl-pane {
          border: 1px solid var(--tl-border);
          background: #080b08;
          padding: 0;
          margin: 0 0 1rem 0;
          border-radius: 0;
        }

        .tl-pane-title {
          color: #000;
          background: var(--tl-primary);
          padding: 0.35rem 0.6rem;
          font-weight: 800;
          text-transform: uppercase;
          text-shadow: none;
          overflow-wrap: anywhere;
        }

        .tl-pane-body {
          padding: 1rem;
        }

        .tl-header {
          color: var(--tl-primary);
          font-weight: 700;
          text-transform: uppercase;
          text-shadow: 0 0 5px rgba(51, 255, 0, 0.5);
          overflow-wrap: anywhere;
        }

        .tl-subtitle, .tl-muted {
          color: var(--tl-muted);
        }

        .tl-line {
          border-top: 1px dashed var(--tl-border);
          margin: 0.8rem 0;
        }

        .tl-separator {
          color: var(--tl-muted);
          overflow-wrap: anywhere;
        }

        .tl-tag {
          display: inline-block;
          border: 1px solid var(--tl-border);
          padding: 0.08rem 0.35rem;
          margin: 0.1rem 0.25rem 0.1rem 0;
          color: var(--tl-primary);
          background: #071007;
          white-space: nowrap;
        }

        .tl-tag-solid {
          color: #000;
          background: var(--tl-primary);
          border-color: var(--tl-primary);
          text-shadow: none;
        }

        .tl-tag-warn { color: var(--tl-secondary); border-color: var(--tl-secondary); }
        .tl-tag-err { color: var(--tl-error); border-color: var(--tl-error); }
        .tl-log {
          border-left: 2px solid var(--tl-border);
          padding-left: 0.7rem;
          margin: 0.25rem 0;
          color: var(--tl-text);
          overflow-wrap: anywhere;
        }

        .tl-command {
          color: var(--tl-secondary);
          overflow-wrap: anywhere;
        }

        .tl-score {
          color: var(--tl-primary);
          font-size: 1.35rem;
          font-weight: 700;
          overflow-wrap: anywhere;
        }

        .tl-pre {
          white-space: pre-wrap;
          overflow-wrap: anywhere;
          color: var(--tl-text);
          background: #050805;
          border: 1px solid var(--tl-border);
          padding: 0.7rem;
        }

        .tl-logo {
          color: var(--tl-primary);
          line-height: 1.05;
          white-space: pre;
          overflow-x: auto;
          text-shadow: 0 0 5px rgba(51, 255, 0, 0.5);
          margin: 0 0 0.8rem 0;
        }

        .tl-prompt {
          color: var(--tl-secondary);
          overflow-wrap: anywhere;
        }

        .tl-cursor {
          display: inline-block;
          width: 0.65ch;
          height: 1em;
          margin-left: 0.15rem;
          vertical-align: -0.12em;
          background: var(--tl-primary);
          animation: tl-blink 1s steps(1) infinite;
        }

        .tl-typing {
          display: inline-block;
          overflow: hidden;
          white-space: nowrap;
          max-width: 100%;
          animation: tl-type 1.1s steps(38, end);
        }

        @keyframes tl-blink {
          0%, 49% { opacity: 1; }
          50%, 100% { opacity: 0; }
        }

        @keyframes tl-type {
          from { width: 0; }
          to { width: 100%; }
        }

        .stButton > button, .stDownloadButton > button {
          border-radius: 0 !important;
          border: 1px solid var(--tl-primary) !important;
          background: #071007 !important;
          color: var(--tl-primary) !important;
          font-family: var(--tl-font) !important;
          box-shadow: none !important;
        }

        .stButton > button:hover, .stDownloadButton > button:hover {
          background: var(--tl-primary) !important;
          color: #000 !important;
          text-shadow: none !important;
        }

        .stButton > button:active, .stDownloadButton > button:active {
          transform: translateY(1px);
        }

        .stButton > button::before { content: "[ "; }
        .stButton > button::after { content: " ]"; }
        .stDownloadButton > button::before { content: "[ "; }
        .stDownloadButton > button::after { content: " ]"; }

        input, textarea, [data-baseweb="select"] > div, [role="radiogroup"] {
          border-radius: 0 !important;
          font-family: var(--tl-font) !important;
        }

        input, textarea {
          background: #050805 !important;
          color: var(--tl-primary) !important;
          border: 1px solid var(--tl-border) !important;
        }

        input:focus, textarea:focus, button:focus, [data-baseweb="radio"] div:focus {
          outline: 2px solid var(--tl-secondary) !important;
          outline-offset: 2px !important;
        }

        code, pre {
          color: var(--tl-primary) !important;
          background: #050805 !important;
          border-radius: 0 !important;
          white-space: pre-wrap !important;
          overflow-wrap: anywhere !important;
        }

        [data-testid="stAlert"] {
          border-radius: 0 !important;
          border: 1px solid var(--tl-secondary) !important;
          background: #171107 !important;
          color: var(--tl-text) !important;
        }

        @media (max-width: 760px) {
          .tl-pane-body { padding: 0.75rem; }
          .tl-score { font-size: 1.05rem; }
          .tl-logo { font-size: 0.65rem; }
          .tl-typing { white-space: normal; animation: none; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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


def _status_tag(label: str, *, state: str = "ok") -> str:
    class_name = "tl-tag"
    if state == "warn":
        class_name += " tl-tag-warn"
    elif state == "err":
        class_name += " tl-tag-err"
    elif state == "solid":
        class_name += " tl-tag-solid"
    return f'<span class="{class_name}">{escape(label)}</span>'


def _terminal_pane(title: str, body: str = "") -> None:
    st.markdown(
        f"""
        <div class="tl-pane">
          <div class="tl-pane-title">{escape(title)}</div>
          <div class="tl-pane-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _score_from_markdown(markdown: str) -> int | None:
    match = search(r"Reproducibility score:\s*(\d+)\s*/\s*100", markdown)
    return int(match.group(1)) if match else None


def _score_bar(score: int | None) -> str:
    if score is None:
        return "[....................] n/a"
    filled = max(0, min(20, round(score / 5)))
    return f"[{'#' * filled}{'.' * (20 - filled)}] {score}/100"


def _severity_counts_from_markdown(markdown: str) -> dict[str, str]:
    counts: dict[str, str] = {}
    in_counts = False
    for line in markdown.splitlines():
        if line.strip() == "Severity counts:":
            in_counts = True
            continue
        if in_counts and line.startswith("- ") and ":" in line:
            key, value = line[2:].split(":", 1)
            counts[key.strip()] = value.strip()
            continue
        if in_counts and line.strip():
            break
    return counts


def _agent_section_from_markdown(markdown: str) -> str:
    marker = "## Gemini Explanation"
    start = markdown.find(marker)
    if start < 0:
        return ""
    next_section = markdown.find("\n## ", start + len(marker))
    if next_section < 0:
        return markdown[start:].strip()
    return markdown[start:next_section].strip()


def _parse_findings(markdown: str) -> list[UiFinding]:
    findings: list[UiFinding] = []
    current_rule = ""
    current: dict[str, object] | None = None
    in_gemini = False

    def flush() -> None:
        nonlocal current
        if current and current_rule and current.get("title"):
            raw_evidence = str(current.get("evidence", ""))
            evidence = [item.strip() for item in raw_evidence.split(",") if item.strip()]
            findings.append(
                UiFinding(
                    rule_id=current_rule,
                    title=str(current.get("title", "")),
                    severity=str(current.get("severity", "low")).lower(),
                    description=str(current.get("description", "")),
                    evidence=evidence,
                    recommended_fix=str(current.get("recommended_fix", "")),
                )
            )
        current = None

    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            flush()
            section = stripped[3:].strip()
            in_gemini = section == "Gemini Explanation"
            current_rule = "" if in_gemini else section
            continue
        if in_gemini or not current_rule:
            continue
        if stripped.startswith("### "):
            flush()
            current = {"title": stripped[4:].strip()}
            continue
        if current is None or not stripped.startswith("- "):
            continue
        if stripped.startswith("- Severity:"):
            current["severity"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Description:"):
            current["description"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Evidence:"):
            current["evidence"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Recommended fix:"):
            current["recommended_fix"] = stripped.split(":", 1)[1].strip()
    flush()
    return findings


def _render_status_pane(
    source: str,
    project: str,
    gemini_explanation: bool,
    phoenix_url: str,
) -> None:
    source_state = "ok" if source == "Offline fixture" else "warn"
    phoenix_state = "warn" if _is_localhost_url(phoenix_url) and _is_hosted_runtime() else "ok"
    body = (
        f'<div class="tl-log">{_status_tag("[OK]" if source_state == "ok" else "[WARN]", state=source_state)} '
        f"selected_source={escape(source)}</div>"
        f'<div class="tl-log">{_status_tag("[OK]")} default_project={escape(project)}</div>'
        f'<div class="tl-log">{_status_tag("[OK]" if gemini_explanation else "[WARN]", state="ok" if gemini_explanation else "warn")} '
        f"gemini_enabled={'yes' if gemini_explanation else 'no'}</div>"
        f'<div class="tl-log">{_status_tag("[OK]" if phoenix_state == "ok" else "[WARN]", state=phoenix_state)} '
        f"phoenix_base_url={escape(_redact_url(phoenix_url))}</div>"
        f'<div class="tl-log">{_status_tag("[OK]")} hosted_app_mode=offline-default</div>'
    )
    _terminal_pane("+--- SYSTEM STATUS ---+", body)


def _render_report_pane(markdown: str) -> None:
    score = _score_from_markdown(markdown)
    counts = _severity_counts_from_markdown(markdown)
    count_lines = "".join(
        f'<div class="tl-log">{escape(severity)}={escape(count)}</div>' for severity, count in counts.items()
    )
    _terminal_pane(
        "+--- AUDIT REPORT PANE ---+",
        f'<div class="tl-score">score {escape(_score_bar(score))}</div><div class="tl-separator">============================================================</div>{count_lines}',
    )
    for finding in _parse_findings(markdown):
        tag = SEVERITY_TAGS.get(finding.severity, "[INFO]")
        state = "err" if finding.severity in {"critical", "high"} else "warn" if finding.severity == "medium" else "ok"
        evidence_lines = "".join(f'<div class="tl-log">&gt; {escape(item)}</div>' for item in finding.evidence)
        body = (
            f'{_status_tag(tag, state=state)} {_status_tag(f"[{finding.rule_id}]")}'
            f'<div class="tl-separator">------------------------------------------------------------</div>'
            f'<div class="tl-header">{escape(finding.title)}</div>'
            f'<div class="tl-muted">{escape(finding.description)}</div>'
            f'<div class="tl-separator">------------------------------------------------------------</div>'
            f"{evidence_lines}"
            f'<div class="tl-separator">------------------------------------------------------------</div>'
            f'<div class="tl-command">$ fix --apply "{escape(finding.recommended_fix)}"</div>'
        )
        _terminal_pane("+--- FINDING ---+", body)


def _render_gemini_pane(markdown: str) -> None:
    section = _agent_section_from_markdown(markdown)
    if not section:
        return
    body = (
        f'{_status_tag("[LOCKED]")} deterministic fields immutable'
        '<div class="tl-log">Gemini explains findings but cannot mutate score, severity, rule ID, or evidence refs.</div>'
        '<div class="tl-separator">------------------------------------------------------------</div>'
        f'<div class="tl-pre">{escape(section)}</div>'
    )
    _terminal_pane("+--- GEMINI EXPLANATION LAYER ---+", body)


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
    apply_terminal_theme()
    logo = r"""
 _______ ____   ___   ____ _____ _     ___ _____ __  __ _   _ ____
|_   _|  _ \ / _ \ / ___| ____| |   |_ _|_   _|  \/  | | | / ___|
  | | | |_) | | | | |   |  _| | |    | |  | | | |\/| | | | \___ \
  | | |  _ <| |_| | |___| |___| |___ | |  | | | |  | | |_| |___) |
  |_| |_| \_\\___/ \____|_____|_____|___| |_| |_|  |_|\___/|____/
"""
    _terminal_pane(
        "TRACE_LITMUS://REPRO_AUDIT_CONSOLE",
        f'<pre class="tl-logo">{escape(logo)}</pre>'
        '<div class="tl-header"><span class="tl-typing">BOOTING REPRODUCIBILITY AUDIT CONSOLE</span><span class="tl-cursor"></span></div>'
        '<div class="tl-subtitle">A reproducibility litmus test for Phoenix LLM evaluations.</div>'
        '<div class="tl-separator">============================================================</div>'
        f'{_status_tag("[LOCKED]")} Deterministic evidence core '
        f'{_status_tag("[LLM]", state="warn")} Gemini explanation only '
        f'{_status_tag("[MCP]")} Phoenix local path verified',
    )

    with st.sidebar:
        st.markdown("### +--- CONTROL PANE ---+")
        source_options = ["Offline fixture", "Phoenix MCP"]
        default_source = _default_source()
        st.markdown('<div class="tl-prompt">source@tracelitmus:~$ select --source</div>', unsafe_allow_html=True)
        source = st.radio(
            "Source",
            source_options,
            index=source_options.index(default_source),
            help="Phoenix MCP runs the live @arizeai/phoenix-mcp path. Offline fixture is for local skeleton checks.",
        )
        st.markdown('<div class="tl-prompt">project@tracelitmus:~$ set --project</div>', unsafe_allow_html=True)
        project = st.text_input("Project", value=_default_project(source))
        st.markdown('<div class="tl-prompt">output@tracelitmus:~$ write --markdown</div>', unsafe_allow_html=True)
        output_path = st.text_input("Output Markdown", value=str(_default_output(source)))
        gemini_explanation = st.checkbox(
            "Add Gemini explanation",
            value=_gemini_enabled_default(),
            help="Gemini can narrate findings, but cannot change rule IDs, severities, scores, or evidence refs.",
        )
        st.info("[LOCKED] MCP mode currently runs only `missing_baseline`. Offline mode still runs the seven placeholder rules.")
        phoenix_url = _phoenix_base_url()
        if source == "Phoenix MCP" and _is_hosted_runtime() and _is_localhost_url(phoenix_url):
            st.warning(
                "[WARN] Hosted Phoenix MCP requires a reachable Phoenix endpoint. Local Phoenix at 127.0.0.1 is not reachable from Cloud Run."
            )
        run_clicked = st.button("RUN AUDIT", type="primary", use_container_width=True)

    _render_status_pane(source, project, gemini_explanation, phoenix_url)

    if "report_markdown" not in st.session_state:
        st.session_state.report_markdown = ""
        st.session_state.report_name = "tracelitmus-report.md"

    if run_clicked:
        try:
            with st.status("Running audit...", expanded=True) as status:
                st.write(f"[OK] source={source}")
                st.write(f"[OK] project={project}")
                st.write(f"[OK] gemini={'on' if gemini_explanation else 'off'}")
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
            st.error("[ERR] Audit failed. The error below is not hidden.")
            st.exception(exc)
            st.code(format_exc(), language="text")

    if st.session_state.report_markdown:
        if "## Gemini Explanation\n\nWarning:" in st.session_state.report_markdown:
            st.warning("[WARN] Gemini explanation was requested but unavailable. The deterministic report still ran.")
        _render_report_pane(st.session_state.report_markdown)
        _render_gemini_pane(st.session_state.report_markdown)
        with st.expander("RAW_REPORT.md", expanded=False):
            st.download_button(
                "DOWNLOAD MARKDOWN",
                data=st.session_state.report_markdown,
                file_name=st.session_state.report_name,
                mime="text/markdown",
            )
            st.markdown(st.session_state.report_markdown)
    else:
        _terminal_pane(
            "+--- READY ---+",
            '<div class="tl-log">[OK] Choose a source, enter a project, and run the audit.</div>'
            f'<div class="tl-log">[OK] session_started={escape(datetime.now().isoformat(timespec="seconds"))}</div>'
            '<div class="tl-command">$ tracelitmus audit --source selected --evidence locked</div>',
        )


if __name__ == "__main__":
    main()
