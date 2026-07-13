"""
03_build_rmct_vocabulary.py

Purpose
-------
Build a controlled vocabulary from preferred labels and alternative labels.

Input
-----
data/rmct_controlled_vocabulary.csv

Output
------
outputs/tables/rmct_searchable_vocabulary.csv
One row per searchable string mapped to one preferred RMCT label.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


def normalise_term(term: str) -> str:
    term = str(term).lower().strip()
    term = re.sub(r"[^a-z0-9\-\s/]", " ", term)
    term = re.sub(r"\s+", " ", term)
    return term.strip()


def split_alternatives(value: str) -> list[str]:
    if pd.isna(value) or str(value).strip() == "":
        return []
    parts = re.split(r"[;|,]", str(value))
    return [normalise_term(p) for p in parts if normalise_term(p)]


def build_searchable_vocabulary(vocab: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in vocab.iterrows():
        preferred = normalise_term(row["preferred_label"])
        strings = {preferred, *split_alternatives(row.get("alternative_labels", ""))}
        for s in sorted(strings):
            rows.append(
                {
                    "searchable_string": s,
                    "preferred_label": row["preferred_label"],
                    "rmct_term_id": row.get("rmct_term_id", ""),
                    "broader_dimension": row["broader_dimension"],
                    "narrower_category": row["narrower_category"],
                    "string_type": "preferred" if s == preferred else "alternative",
                }
            )
    return pd.DataFrame(rows).drop_duplicates()


def main(input_path: Path, output_path: Path) -> None:
    vocab = pd.read_csv(input_path)
    required = {"preferred_label", "broader_dimension", "narrower_category"}
    missing = required - set(vocab.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    searchable = build_searchable_vocabulary(vocab)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    searchable.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(searchable)} searchable strings to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/rmct_controlled_vocabulary.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/tables/rmct_searchable_vocabulary.csv"))
    args = parser.parse_args()
    main(args.input, args.output)
