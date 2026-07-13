"""
01_preprocess_public_web_text.py

Purpose
-------
Prepare public manufacturer website text for RMCT capability classification.

This script is a reproducibility template. The manuscript does not redistribute
full raw website texts. If researchers have permission to use their own website
corpus, they can place an input CSV at data/private/website_texts.csv with:

    company_id, url, crawl_date, raw_text

The script outputs cleaned text metadata and document hashes. It does not write
full cleaned text to the public data folder.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("data/private/website_texts.csv")
DEFAULT_OUTPUT = Path("data/hashes/website_document_hashes.csv")


def clean_text(text: str) -> str:
    """Lightweight cleaning used before capability matching."""
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", " ", text)
    return text.strip().lower()


def quality_flag(cleaned_text: str) -> str:
    """Classify website text usability by length."""
    n = len(cleaned_text)
    if n >= 3000:
        return "usable_rich"
    if n >= 800:
        return "usable"
    if n >= 200:
        return "short_but_usable"
    return "very_short"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def main(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}. "
            "Create this file locally if you have permission to process full website text."
        )

    df = pd.read_csv(input_path)
    required = {"company_id", "raw_text"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["cleaned_text"] = df["raw_text"].map(clean_text)
    df["company_text_length"] = df["cleaned_text"].str.len()
    df["quality_flag"] = df["cleaned_text"].map(quality_flag)
    df["sha256_document_hash"] = df["cleaned_text"].map(sha256_text)

    safe_cols = [
        c
        for c in [
            "company_id",
            "url",
            "crawl_date",
            "quality_flag",
            "company_text_length",
            "sha256_document_hash",
        ]
        if c in df.columns
    ]
    out = df[safe_cols].copy()
    out["hash_algorithm"] = "SHA-256"
    out["text_shared_in_repository"] = "no"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(out)} hash records to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    main(args.input, args.output)
