"""Command line interface for TraceLitmus."""

from argparse import ArgumentParser
from datetime import UTC, datetime
from os import environ
from pathlib import Path
from typing import Any

from . import audit_rules
from .agent import attach_agent_explanation
from .models import AuditFinding, AuditReport, EvidenceRef, PhoenixDataset, PhoenixExperiment, PhoenixPromptVersion
from .phoenix_client import PhoenixMCPClient, PhoenixMCPError
from .report import render_markdown

SEVERITY_ORDER = ("critical", "high", "medium", "low")
SEVERITY_PENALTIES = {
    "critical": 20,
    "high": 12,
    "medium": 6,
    "low": 2,
}


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="tracelitmus")
    subcommands = parser.add_subparsers(dest="command", required=True)
    audit = subcommands.add_parser("audit")
    audit.add_argument("--project", required=True)
    audit.add_argument("--offline", action="store_true")
    audit.add_argument("--source", choices=("offline", "mcp"), default="offline")
    audit.add_argument("--gemini-explanation", action="store_true")
    audit.add_argument("--output", required=True)
    return parser


def _score_findings(findings: list) -> tuple[int, int, dict[str, int]]:
    severity_counts = {severity: 0 for severity in SEVERITY_ORDER}
    for finding in findings:
        severity_counts[finding.severity] += 1
    penalty = sum(
        severity_counts[severity] * SEVERITY_PENALTIES[severity] for severity in SEVERITY_ORDER
    )
    score = max(0, 100 - penalty)
    return score, penalty, severity_counts


def _write_report(path: str, report: AuditReport) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown(report), encoding="utf-8")
    return output_path


def run_audit(
    project: str,
    offline: bool,
    output: str,
    *,
    gemini_explanation: bool = False,
) -> Path:
    client = PhoenixMCPClient(offline=offline)
    payload = client.load_offline_fixture()

    experiments = [PhoenixExperiment(**item) for item in payload["experiments"]]
    prompt_versions = [PhoenixPromptVersion(**item) for item in payload["prompt_versions"]]
    datasets = [PhoenixDataset(**item) for item in payload["datasets"]]
    project_id = next((item["id"] for item in payload["projects"] if item["name"] == project), project)

    findings = []
    findings.extend(audit_rules.detect_missing_seed(experiments))
    findings.extend(audit_rules.detect_prompt_drift(experiments, prompt_versions))
    findings.extend(audit_rules.detect_dataset_drift(experiments, datasets))
    findings.extend(audit_rules.detect_missing_baseline(experiments))
    findings.extend(audit_rules.detect_metric_ambiguity(experiments))
    findings.extend(audit_rules.detect_no_statistical_support(experiments))
    findings.extend(audit_rules.detect_weak_sample_size(experiments))
    score, penalty, severity_counts = _score_findings(findings)

    report = AuditReport(
        project_id=project_id,
        source="Offline fixture",
        score=score,
        score_start=100,
        score_penalty=penalty,
        severity_counts=severity_counts,
        findings=findings,
        summary="Offline fixture audit: seven deterministic placeholder rules, typed evidence references, and source-verified MCP architecture notes.",
        generated_at=datetime.now(UTC),
    )
    attach_agent_explanation(report, enabled=gemini_explanation)

    return _write_report(output, report)


def _dataset_name_for_project(project: str) -> str:
    return environ.get("PHOENIX_DATASET_NAME") or f"{project}-dataset"


def _extract_examples(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        if isinstance(raw.get("examples"), list):
            return raw["examples"]
        data = raw.get("data")
        if isinstance(data, dict) and isinstance(data.get("examples"), list):
            return data["examples"]
        if isinstance(data, list):
            return data
    if isinstance(raw, list):
        return raw
    return []


def _find_dataset(raw_datasets: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for dataset in raw_datasets:
        if dataset.get("name") == name or dataset.get("id") == name:
            return dataset
    available = ", ".join(str(item.get("name") or item.get("id")) for item in raw_datasets) or "none"
    raise PhoenixMCPError(f'Dataset "{name}" was not found through MCP. Available datasets: {available}')


def _fallback_weak_sample_size_finding(
    dataset: PhoenixDataset,
    examples: list[dict[str, Any]],
    experiments: list[PhoenixExperiment],
) -> AuditFinding:
    evidence = [EvidenceRef(object_type="dataset", object_id=dataset.id, label=f"{len(examples)} examples")]
    if experiments:
        evidence.append(EvidenceRef(object_type="experiment", object_id=experiments[0].id, label="linked experiment"))
    for example in examples[:2]:
        example_id = example.get("id")
        if example_id:
            evidence.append(EvidenceRef(object_type="dataset_example", object_id=str(example_id), label="sample"))
    return AuditFinding(
        rule_id="weak_sample_size",
        severity="medium",
        title="Dataset sample is too small for a confident MCP-backed audit",
        description="The MCP-retrieved dataset has too few examples to support a robust reproducibility claim.",
        evidence=evidence,
        recommended_fix="Seed or select a dataset with enough examples for a reproducibility comparison.",
    )


def run_mcp_audit(
    project: str,
    output: str,
    *,
    gemini_explanation: bool = False,
) -> Path:
    dataset_name = _dataset_name_for_project(project)
    with PhoenixMCPClient(source="mcp", offline=False) as client:
        raw_projects = client.list_projects(limit=100, include_experiment_projects=True)
        raw_datasets = client.list_datasets(limit=100)
        dataset = client.normalize_dataset(_find_dataset(raw_datasets, dataset_name))
        raw_examples = client.get_dataset_examples(dataset_id=dataset.id)
        examples = _extract_examples(raw_examples)
        raw_experiments = client.list_experiments_for_dataset(dataset_id=dataset.id, limit=100)
        experiments = [
            client.normalize_experiment(item, sample_size=len(examples))
            for item in raw_experiments
        ]

    if experiments:
        findings = audit_rules.detect_missing_baseline(experiments)
        summary = (
            "TraceLitmus inspected the Phoenix project, retrieved its dataset and experiment records "
            "through Phoenix MCP, and found one reproducibility risk: a candidate experiment reports "
            "metrics without linking to the baseline run needed for a valid comparison."
        )
    else:
        findings = [_fallback_weak_sample_size_finding(dataset, examples, experiments)]
        summary = (
            "Phase 1 MCP audit: no experiments were returned, so the fallback weak_sample_size "
            "rule fired from MCP-retrieved dataset examples."
        )

    score, penalty, severity_counts = _score_findings(findings)
    matching_project = next(
        (item for item in raw_projects if item.get("name") == project or item.get("id") == project),
        None,
    )
    project_id = str(matching_project.get("id")) if matching_project else project
    report = AuditReport(
        project_id=project_id,
        source="Phoenix MCP",
        score=score,
        score_start=100,
        score_penalty=penalty,
        severity_counts=severity_counts,
        findings=findings,
        summary=summary,
        generated_at=datetime.now(UTC),
    )
    attach_agent_explanation(report, enabled=gemini_explanation)
    return _write_report(output, report)


def main() -> None:
    args = _build_parser().parse_args()
    if args.command == "audit":
        source = "offline" if args.offline else args.source
        if source == "mcp":
            path = run_mcp_audit(
                project=args.project,
                output=args.output,
                gemini_explanation=args.gemini_explanation,
            )
        else:
            path = run_audit(
                project=args.project,
                offline=True,
                output=args.output,
                gemini_explanation=args.gemini_explanation,
            )
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
