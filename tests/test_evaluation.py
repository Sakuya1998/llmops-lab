"""评测流水线的确定性单元测试。"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipelines.evaluation.evaluate import evaluate, score  # noqa: E402


def write_jsonl(path: Path, rows: list[dict[str, str]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_fixture_evaluation_passes() -> None:
    root = Path("pipelines/evaluation")
    result = evaluate(
        root / "dataset.jsonl",
        root / "baseline_predictions.jsonl",
        root / "candidate_predictions.jsonl",
        min_accuracy=0.75,
        max_regression=0.10,
    )
    assert result["passed"] is True
    assert result["baseline"]["accuracy"] == 1.0
    assert result["candidate"]["accuracy"] == 1.0


def test_regression_blocks_candidate(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset.jsonl"
    baseline = tmp_path / "baseline.jsonl"
    candidate = tmp_path / "candidate.jsonl"
    write_jsonl(dataset, [{"id": "a", "expected": "correct"}, {"id": "b", "expected": "yes"}])
    write_jsonl(baseline, [{"id": "a", "output": "correct"}, {"id": "b", "output": "yes"}])
    write_jsonl(candidate, [{"id": "a", "output": "wrong"}, {"id": "b", "output": "yes"}])

    result = evaluate(dataset, baseline, candidate, min_accuracy=0.75, max_regression=0.10)
    assert result["passed"] is False
    assert result["candidate"]["accuracy"] == 0.5
    assert result["regression"] == 0.5


def test_duplicate_prediction_id_is_rejected(tmp_path: Path) -> None:
    dataset = tmp_path / "dataset.jsonl"
    predictions = tmp_path / "predictions.jsonl"
    write_jsonl(dataset, [{"id": "a", "expected": "x"}])
    write_jsonl(predictions, [{"id": "a", "output": "x"}, {"id": "a", "output": "x"}])

    with pytest.raises(ValueError, match="重复"):
        score(dataset, predictions)
