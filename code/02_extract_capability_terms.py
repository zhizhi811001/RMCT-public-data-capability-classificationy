"""
02_extract_capability_terms.py

Purpose
-------
Extract candidate capability terms from locally available website text.

The public repository does not include full website text. This script documents
the extraction logic used in the RMCT workflow and can be run on an authorised
local corpus with columns:

    company_id, cleaned_text
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


MANUFACTURING_CONTEXT_TERMS = {
    "manufacturing",
    "machining",
    "fabrication",
    "casting",
    "forming",
    "welding",
    "assembly",
    "material",
    "quality",
    "certification",
    "engineering",
    "prototype",
    "production",
    "coating",
    "testing",
    "inspection",
    "automation",
    "supply",
}


def normalise_phrase(phrase: str) -> str:
    phrase = str(phrase).lower().strip()
    phrase = re.sub(r"[^a-z0-9\-\s/]", " ", phrase)
    phrase = re.sub(r"\s+", " ", phrase)
    return phrase.strip()


def has_manufacturing_context(phrase: str) -> bool:
    return any(term in phrase for term in MANUFACTURING_CONTEXT_TERMS)


def extract_ngrams(
    corpus: pd.DataFrame,
    text_col: str = "cleaned_text",
    min_df: int = 3,
    max_features: int = 10000,
) -> pd.DataFrame:
    vectorizer = CountVectorizer(
        ngram_range=(1, 4),
        min_df=min_df,
        max_features=max_features,
        stop_words="english",
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9\-/]+\b",
    )
    matrix = vectorizer.fit_transform(corpus[text_col].fillna(""))
    terms = vectorizer.get_feature_names_out()

    term_frequency = matrix.sum(axis=0).A1
    document_frequency = (matrix > 0).sum(axis=0).A1

    rows = []
    for term, tf, df in zip(terms, term_frequency, document_frequency):
        candidate = normalise_phrase(term)
        if not candidate:
            continue
        rows.append(
            {
                "candidate_concept": candidate,
                "term_frequency": int(tf),
                "document_frequency": int(df),
                "n_words": len(candidate.split()),
                "has_manufacturing_context": has_manufacturing_context(candidate),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["document_frequency", "term_frequency"], ascending=False
    )


def main(input_path: Path, output_path: Path) -> None:
    df = pd.read_csv(input_path)
    if "cleaned_text" not in df.columns:
        raise ValueError("Input file must contain a cleaned_text column.")

    concepts = extract_ngrams(df)
    concepts = concepts[concepts["has_manufacturing_context"]].copy()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    concepts.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(concepts)} candidate concepts to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/private/website_texts_cleaned.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/tables/candidate_capability_terms.csv"))
    args = parser.parse_args()
    main(args.input, args.output)
