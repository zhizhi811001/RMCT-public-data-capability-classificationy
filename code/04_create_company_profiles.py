"""
04_create_company_profiles.py

Purpose
-------
Create company-level RMCT capability profiles by matching searchable vocabulary
strings against authorised local website text.

The public repository contains anonymised example profiles but not full website
text. To reproduce profile construction, use a local input file with:

    company_id, cleaned_text
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


def phrase_count(text: str, phrase: str) -> int:
    """Count exact phrase matches with word boundaries."""
    if not text or not phrase:
        return 0
    pattern = r"(?<![a-z0-9])" + re.escape(phrase.lower()) + r"(?![a-z0-9])"
    return len(re.findall(pattern, text.lower()))


def match_profiles(corpus: pd.DataFrame, searchable: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, company in corpus.iterrows():
        text = str(company.get("cleaned_text", "")).lower()
        for _, term in searchable.iterrows():
            count = phrase_count(text, term["searchable_string"])
            if count > 0:
                rows.append(
                    {
                        "company_id": company["company_id"],
                        "preferred_label": term["preferred_label"],
                        "matched_string": term["searchable_string"],
                        "broader_dimension": term["broader_dimension"],
                        "narrower_category": term["narrower_category"],
                        "match_count": count,
                    }
                )
    return pd.DataFrame(rows)


def main(corpus_path: Path, vocab_path: Path, output_path: Path) -> None:
    corpus = pd.read_csv(corpus_path)
    searchable = pd.read_csv(vocab_path)
    required_corpus = {"company_id", "cleaned_text"}
    required_vocab = {"searchable_string", "preferred_label", "broader_dimension", "narrower_category"}
    if missing := required_corpus - set(corpus.columns):
        raise ValueError(f"Corpus missing columns: {sorted(missing)}")
    if missing := required_vocab - set(searchable.columns):
        raise ValueError(f"Vocabulary missing columns: {sorted(missing)}")

    matches = match_profiles(corpus, searchable)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(matches)} match rows to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=Path("data/private/website_texts_cleaned.csv"))
    parser.add_argument("--vocab", type=Path, default=Path("outputs/tables/rmct_searchable_vocabulary.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs/tables/rmct_company_profile_matches.csv"))
    args = parser.parse_args()
    main(args.corpus, args.vocab, args.output)
