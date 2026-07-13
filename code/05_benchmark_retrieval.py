"""
05_benchmark_retrieval.py

Purpose
-------
Compute aggregate benchmark indicators for RMCT-style supplier search.

This script works with public aggregate benchmark files. It calculates
candidate-set reduction for each procurement brief where baseline and RMCT
candidate counts are available.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def candidate_set_reduction(baseline_count: float, rmct_count: float) -> float:
    if baseline_count <= 0:
        return float("nan")
    return (1 - rmct_count / baseline_count) * 100


def main(input_path: Path, output_path: Path) -> None:
    df = pd.read_csv(input_path)
    required = {"brief_id", "baseline_system", "baseline_candidate_count", "rmct_candidate_count"}
    if missing := required - set(df.columns):
        raise ValueError(
            "This script expects a benchmark input with columns: "
            f"{sorted(required)}. Missing: {sorted(missing)}"
        )

    df["candidate_set_reduction_percent"] = df.apply(
        lambda r: candidate_set_reduction(r["baseline_candidate_count"], r["rmct_candidate_count"]),
        axis=1,
    )

    summary = (
        df.groupby("baseline_system", as_index=False)
        .agg(
            n_briefs=("brief_id", "nunique"),
            mean_baseline_candidate_count=("baseline_candidate_count", "mean"),
            mean_rmct_candidate_count=("rmct_candidate_count", "mean"),
            mean_candidate_set_reduction_percent=("candidate_set_reduction_percent", "mean"),
        )
        .round(2)
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Brief Level Results", index=False)
        summary.to_excel(writer, sheet_name="Baseline Summary", index=False)

    print(f"Wrote benchmark workbook to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/benchmark_results_aggregate.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/tables/benchmark_retrieval_summary.xlsx"))
    args = parser.parse_args()
    main(args.input, args.output)
