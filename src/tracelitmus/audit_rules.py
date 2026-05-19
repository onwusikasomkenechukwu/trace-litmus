"""Placeholder audit rules for Phase 0."""

from collections.abc import Sequence

from .models import AuditFinding, EvidenceRef, PhoenixDataset, PhoenixExperiment, PhoenixPromptVersion


def _ref(object_type: str, object_id: str, label: str | None = None) -> EvidenceRef:
    return EvidenceRef(object_type=object_type, object_id=object_id, label=label)


def detect_missing_seed(experiments: Sequence[PhoenixExperiment]) -> list[AuditFinding]:
    target = next((item for item in experiments if "seed" not in item.metrics), experiments[0])
    return [
        AuditFinding(
            rule_id="missing_seed",
            severity="high",
            title="Experiment seed is not recorded",
            description="The run cannot be replayed deterministically because no seed is attached to the experiment metadata.",
            evidence=[
                _ref("experiment", target.id, "seed missing from metrics"),
                _ref("dataset", target.dataset_id, "experiment dataset"),
                _ref("metadata", "seed", "missing metadata key"),
            ],
            recommended_fix="Record random seeds and sampler configuration in Phoenix experiment metadata.",
        )
    ]


def detect_prompt_drift(
    experiments: Sequence[PhoenixExperiment],
    prompt_versions: Sequence[PhoenixPromptVersion],
) -> list[AuditFinding]:
    candidate_prompt_id = prompt_versions[1].id if len(prompt_versions) > 1 else prompt_versions[0].id
    experiment = next(
        (item for item in experiments if item.prompt_version_id == candidate_prompt_id),
        experiments[-1],
    )
    baseline = prompt_versions[0]
    candidate = prompt_versions[1] if len(prompt_versions) > 1 else prompt_versions[0]
    return [
        AuditFinding(
            rule_id="prompt_drift",
            severity="critical",
            title="Prompt version changed across comparable runs",
            description="Comparable experiments point at different prompt versions, so score movement cannot be assigned to the model or dataset alone.",
            evidence=[
                _ref("experiment", experiment.id, "comparison run"),
                _ref("prompt_version", baseline.id, baseline.version_tag or "baseline prompt"),
                _ref("prompt_version", candidate.id, candidate.version_tag or "candidate prompt"),
            ],
            recommended_fix="Pin a prompt version or tag, then rerun the comparison under the same prompt.",
        )
    ]


def detect_dataset_drift(
    experiments: Sequence[PhoenixExperiment],
    datasets: Sequence[PhoenixDataset],
) -> list[AuditFinding]:
    experiment = experiments[-1]
    first_dataset = datasets[0]
    second_dataset = datasets[1] if len(datasets) > 1 else datasets[0]
    return [
        AuditFinding(
            rule_id="dataset_drift",
            severity="high",
            title="Dataset version changed between experiments",
            description="Experiments are being compared across dataset versions, which makes regressions hard to attribute.",
            evidence=[
                _ref("experiment", experiment.id, "candidate run"),
                _ref("dataset", first_dataset.id, first_dataset.version),
                _ref("dataset", second_dataset.id, second_dataset.version),
            ],
            recommended_fix="Compare against a fixed dataset version, then run a separate dataset-change analysis.",
        )
    ]


def detect_missing_baseline(experiments: Sequence[PhoenixExperiment]) -> list[AuditFinding]:
    target = next(
        (
            item
            for item in experiments
            if "baseline" not in item.id
            and not item.metrics.get("baseline_experiment_id")
            and not item.metadata.get("baseline_experiment_id")
            and not item.metadata.get("baseline_experiment")
            and not item.metadata.get("reference_experiment_id")
        ),
        experiments[0],
    )
    return [
        AuditFinding(
            rule_id="missing_baseline",
            severity="medium",
            title="No baseline experiment is linked",
            description="The experiment reports metrics without naming the baseline run it should be compared against.",
            evidence=[
                _ref("experiment", target.id, "missing baseline_experiment_id"),
                _ref("metadata", "baseline_experiment_id", "missing metadata key"),
            ],
            recommended_fix="Store a baseline experiment ID in metadata for every candidate run.",
        )
    ]


def detect_metric_ambiguity(experiments: Sequence[PhoenixExperiment]) -> list[AuditFinding]:
    target = next((item for item in experiments if item.metrics.get("metric_definition") in (None, "")), experiments[0])
    return [
        AuditFinding(
            rule_id="metric_ambiguity",
            severity="medium",
            title="Metric definition is ambiguous",
            description="A reported score lacks a clear rubric, direction, or evaluator identity.",
            evidence=[
                _ref("experiment", target.id, "ambiguous evaluator output"),
                _ref("metric", "accuracy", "missing rubric or direction"),
                _ref("metadata", "metric_definition", "empty value"),
            ],
            recommended_fix="Attach metric direction, rubric text, evaluator version, and threshold to the experiment.",
        )
    ]


def detect_no_statistical_support(experiments: Sequence[PhoenixExperiment]) -> list[AuditFinding]:
    target = next((item for item in experiments if "confidence_interval" not in item.metrics), experiments[0])
    return [
        AuditFinding(
            rule_id="no_statistical_support",
            severity="medium",
            title="Score lacks statistical support",
            description="The result has no confidence interval, variance estimate, or significance note.",
            evidence=[
                _ref("experiment", target.id, "no confidence interval"),
                _ref("metric", "accuracy", "no uncertainty estimate"),
                _ref("metadata", "sample_size", str(target.sample_size)),
            ],
            recommended_fix="Compute and store uncertainty, including confidence intervals or bootstrap estimates.",
        )
    ]


def detect_weak_sample_size(experiments: Sequence[PhoenixExperiment]) -> list[AuditFinding]:
    target = min(experiments, key=lambda item: item.sample_size)
    return [
        AuditFinding(
            rule_id="weak_sample_size",
            severity="low",
            title="Sample size is too small for a confident claim",
            description="The experiment uses a small sample, so a pass or fail conclusion would be fragile.",
            evidence=[
                _ref("experiment", target.id, "smallest sample"),
                _ref("metadata", "sample_size", str(target.sample_size)),
            ],
            recommended_fix="Increase the sample size or mark the result as directional only.",
        )
    ]
