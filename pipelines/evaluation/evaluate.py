"""使用合成数据演示可重复的候选模型回归门禁；不调用外部模型。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """读取 JSONL，并为无效行提供可定位的错误。"""
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: 无效 JSON：{exc.msg}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: 每行必须是 JSON object")
        rows.append(value)
    return rows


def normalize(text: str) -> str:
    """只做空白与大小写归一化；这不是通用语义评测。"""
    return " ".join(text.strip().casefold().split())


def score(dataset_path: Path, predictions_path: Path) -> dict[str, Any]:
    dataset = read_jsonl(dataset_path)
    predictions = read_jsonl(predictions_path)
    if not dataset:
        raise ValueError("评测数据集不能为空")

    expected_ids = [row.get("id") for row in dataset]
    if any(not isinstance(item, str) or not item for item in expected_ids):
        raise ValueError("数据集每行必须包含非空字符串 id")
    if len(set(expected_ids)) != len(expected_ids):
        raise ValueError("数据集 id 必须唯一")

    predicted: dict[str, str] = {}
    for row in predictions:
        item_id, output = row.get("id"), row.get("output")
        if not isinstance(item_id, str) or not isinstance(output, str):
            raise ValueError("预测每行必须包含字符串 id 和 output")
        if item_id in predicted:
            raise ValueError(f"预测 id 重复：{item_id}")
        predicted[item_id] = output

    expected_set = set(expected_ids)
    extra = set(predicted) - expected_set
    missing = expected_set - set(predicted)
    if extra or missing:
        raise ValueError(f"预测 ID 不匹配；缺少={sorted(missing)}，多余={sorted(extra)}")

    details = [
        {
            "id": row["id"],
            "expected": row["expected"],
            "actual": predicted[row["id"]],
            "passed": normalize(row["expected"]) == normalize(predicted[row["id"]]),
        }
        for row in dataset
        if isinstance(row.get("expected"), str)
    ]
    if len(details) != len(dataset):
        raise ValueError("数据集每行必须包含字符串 expected")
    passed = sum(bool(item["passed"]) for item in details)
    return {
        "dataset": str(dataset_path),
        "predictions": str(predictions_path),
        "total": len(details),
        "passed": passed,
        "accuracy": passed / len(details),
        "details": details,
    }


def evaluate(
    dataset_path: Path,
    baseline_path: Path,
    candidate_path: Path,
    min_accuracy: float,
    max_regression: float,
) -> dict[str, Any]:
    """比较基线和候选版本，并返回是否允许通过质量门禁。"""
    if not 0 <= min_accuracy <= 1 or not 0 <= max_regression <= 1:
        raise ValueError("阈值必须在 0 到 1 之间")
    baseline = score(dataset_path, baseline_path)
    candidate = score(dataset_path, candidate_path)
    regression = baseline["accuracy"] - candidate["accuracy"]
    return {
        "baseline": baseline,
        "candidate": candidate,
        "regression": regression,
        "thresholds": {
            "min_accuracy": min_accuracy,
            "max_regression": max_regression,
        },
        "passed": candidate["accuracy"] >= min_accuracy and regression <= max_regression,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=Path("pipelines/evaluation/dataset.jsonl"))
    parser.add_argument(
        "--baseline", type=Path, default=Path("pipelines/evaluation/baseline_predictions.jsonl")
    )
    parser.add_argument(
        "--candidate", type=Path, default=Path("pipelines/evaluation/candidate_predictions.jsonl")
    )
    parser.add_argument("--min-accuracy", type=float, default=0.75)
    parser.add_argument("--max-regression", type=float, default=0.10)
    parser.add_argument("--report", type=Path, help="可选的 JSON 报告输出路径")
    args = parser.parse_args()

    try:
        result = evaluate(
            args.dataset, args.baseline, args.candidate, args.min_accuracy, args.max_regression
        )
    except (OSError, ValueError) as exc:
        print(f"评测失败：{exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
