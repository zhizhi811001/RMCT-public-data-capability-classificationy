"""
06_expert_validation_metrics.py

Purpose
-------
Calculate agreement and precision metrics from completed expert validation
ratings.

Input
-----
data/expert_validation_sample_completed.csv

Required expert columns:
    expert_1_supported_yes_no_unclear
    expert_2_supported_yes_no_unclear

Ratings should use: yes, no, unclear.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score


RATING_MAP = {
    "yes": "yes",
    "y": "yes",
    "supported": "yes",
    "no": "no",
    "n": "no",
    "not supported": "no",
    "unclear": "unclear",
    "ambiguous": "unclear",
}


def normalise_rating(value: str) -> str:
    value = str(value).strip().lower()
    return RATING_MAP.get(value, value)


def agreement_rate(a: pd.Series, b: pd.Series) -> float:
    valid = a.notna() & b.notna()
    if valid.sum() == 0:
        return float("nan")
    return (a[valid] == b[valid]).mean()


def precision_by_dimension(df: pd.DataFrame) -> pd.DataFrame:
    rating_col = "adjudicated_supported_yes_no_ambiguous"
    if rating_col not in df.columns or df[rating_col].isna().all():
        rating_col = "expert_1_supported_yes_no_unclear"
    tmp = df.copy()
    tmp[rating_col] = tmp[rating_col].map(normalise_rating)
    return (
        tmp.groupby("rmct_dimension", as_index=False)
        .agg(
            n_items=("validation_item_id", "count"),
            n_supported=(rating_col, lambda s: (s == "yes").sum()),
            n_not_supported=(rating_col, lambda s: (s == "no").sum()),
            n_unclear=(rating_col, lambda s: (s == "unclear").sum()),
        )
        .assign(precision=lambda x: x["n_supported"] / x["n_items"])
        .round({"precision": 3})
    )


def main(input_path: Path, output_path: Path) -> None:
    df = pd.read_csv(input_path)
    e1 = df["expert_1_supported_yes_no_unclear"].map(normalise_rating)
    e2 = df["expert_2_supported_yes_no_unclear"].map(normalise_rating)

    valid = e1.notna() & e2.notna() & (e1 != "") & (e2 != "")
    overall = pd.DataFrame(
        [
            {
                "n_items": int(len(df)),
                "n_double_rated_items": int(valid.sum()),
                "agreement_rate": round(agreement_rate(e1, e2), 3),
                "cohens_kappa": round(cohen_kappa_score(e1[valid], e2[valid]), 3)
                if valid.sum() > 0
                else None,
            }
        ]
    )

    by_dim = precision_by_dimension(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        overall.to_excel(writer, sheet_name="Overall Agreement", index=False)
        by_dim.to_excel(writer, sheet_name="Precision by Dimension", index=False)
        df.to_excel(writer, sheet_name="Completed Ratings", index=False)

    print(f"Wrote expert validation metrics to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/expert_validation_sample_completed.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/tables/expert_validation_metrics.xlsx"))
    args = parser.parse_args()
    main(args.input, args.output)
