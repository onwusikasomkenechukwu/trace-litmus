"""Markdown report rendering."""

from collections import defaultdict
from pathlib import Path

from .models import AuditReport, EvidenceRef


def _template_path() -> Path:
    return Path(__file__).resolve().parents[2] / "templates" / "report.md.j2"


def format_evidence_ref(evidence: EvidenceRef) -> str:
    base = f"{evidence.object_type}:{evidence.object_id}"
    if evidence.label:
        return f"{base} ({evidence.label})"
    return base


def format_evidence_refs(evidence: list[EvidenceRef]) -> str:
    return ", ".join(format_evidence_ref(ref) for ref in evidence)


def _fallback_render(template: str, report: AuditReport) -> str:
    grouped = defaultdict(list)
    for finding in report.findings:
        grouped[finding.rule_id].append(finding)

    sections: list[str] = []
    for rule_id, findings in grouped.items():
        sections.append(f"## {rule_id}")
        for finding in findings:
            sections.extend(
                [
                    f"### {finding.title}",
                    f"- Severity: {finding.severity}",
                    f"- Description: {finding.description}",
                    f"- Evidence: {format_evidence_refs(finding.evidence)}",
                    f"- Recommended fix: {finding.recommended_fix}",
                    "",
                ]
            )
    severity_rows = "\n".join(
        f"- {severity}: {count}" for severity, count in report.severity_counts.items()
    )
    return (
        f"# TraceLitmus Audit Report\n\n"
        f"Project: {report.project_id}\n\n"
        f"Source: {report.source}\n\n"
        f"Reproducibility score: {report.score} / 100\n\n"
        f"Score derivation: {report.score_start} - {report.score_penalty} = {report.score}\n\n"
        f"Severity counts:\n{severity_rows}\n\n"
        f"Generated at: {report.generated_at.isoformat()}\n\n"
        f"Summary: {report.summary}\n\n"
        f"{_fallback_agent_section(report)}"
        f"{chr(10).join(sections)}"
    )


def _fallback_agent_section(report: AuditReport) -> str:
    if report.agent_warning:
        return f"## Gemini Explanation\n\nWarning: {report.agent_warning}\n\n"
    if report.agent_explanation:
        explanation = report.agent_explanation
        finding_items = "\n".join(f"- {item}" for item in explanation.finding_explanations)
        next_step_items = "\n".join(f"- {item}" for item in explanation.prioritized_next_steps)
        return (
            "## Gemini Explanation\n\n"
            "### Executive summary\n\n"
            f"{explanation.executive_summary}\n\n"
            "### Finding explanations\n\n"
            f"{finding_items}\n\n"
            "### Prioritized next steps\n\n"
            f"{next_step_items}\n\n"
        )
    return ""


def render_markdown(report: AuditReport) -> str:
    template_text = _template_path().read_text(encoding="utf-8")
    try:
        from jinja2 import Environment
    except ModuleNotFoundError:
        return _fallback_render(template_text, report)

    grouped = defaultdict(list)
    for finding in report.findings:
        grouped[finding.rule_id].append(finding)
    environment = Environment(autoescape=False, trim_blocks=True, lstrip_blocks=True)
    environment.filters["evidence_ref"] = format_evidence_ref
    environment.filters["evidence_refs"] = format_evidence_refs
    template = environment.from_string(template_text)
    return template.render(report=report, findings_by_rule=dict(grouped))
