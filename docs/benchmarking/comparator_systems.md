# Comparator Systems for RMCT Benchmarking

This document defines the comparator systems used to evaluate whether the Regional Manufacturing Capability Taxonomy (RMCT) improves public-data-driven manufacturing partner discovery and sourcing search.

The comparators are designed to represent realistic alternatives available to engineers, buyers, procurement specialists and regional manufacturing analysts using public data.

## 1. Evaluation Setting

Let:

- $F=\{f_1,\ldots,f_N\}$ denote the set of manufacturers with usable website text;
- $N=888$ denote the number of firms with usable public website text in the current corpus;
- $B=\{b_1,\ldots,b_Q\}$ denote the set of practitioner-style sourcing briefs;
- $R_{s,q}$ denote the candidate firms retrieved by system $s$ for brief $q$;
- $G_q$ denote the expert-labelled relevant firm set for brief $q$, where available.

All comparator systems use the same public website corpus and the same sourcing briefs.

## 2. SIC Baseline

The SIC baseline represents the existing public industrial classification approach. For each sourcing brief, the closest SIC or process-family category is selected from the Companies House-derived manufacturer population frame. Firms assigned to that SIC family are returned as the candidate supplier pool.

For brief $b_q$, the SIC candidate set is:


$$
R_{\mathrm{SIC},q}=\{f_i \in F : SIC(f_i) \in SIC_q\}
$$


where:

- $SIC(f_i)$ is the SIC or process-family assignment for firm $f_i$;
- $SIC_q$ is the SIC family selected as the closest public classification match for brief $b_q$.

The SIC baseline is expected to provide broad coverage but limited capability specificity because SIC codes describe general economic activity rather than detailed process, material, certification, engineering or delivery capabilities.

## 3. BM25 Lexical Retrieval Baseline

The BM25 baseline represents a strong lexical information retrieval method. The full practitioner brief is treated as a query and matched against the cleaned website text of each firm. BM25 ranks firms according to term frequency, inverse document frequency and document length normalisation.

For brief $b_q$ and firm document $d_i$, the BM25 score is:


$$
BM25(b_q,d_i)=\sum_{t \in b_q} IDF(t)
\cdot
\frac{tf(t,d_i)(k_1+1)}
{tf(t,d_i)+k_1\left(1-b+b\frac{|d_i|}{avgdl}\right)}
$$


where:

- $t$ is a query term;
- $tf(t,d_i)$ is the frequency of term $t$ in firm document $d_i$;
- $|d_i|$ is the length of firm document $d_i$;
- $avgdl$ is the average document length in the corpus;
- $k_1$ and $b$ are BM25 parameters.



BM25 is a stronger comparator than simple keyword search because it accounts for term informativeness and document length. However, it remains lexical and does not provide an explicit capability structure.

## 4. Dense Embedding Retrieval Baseline

The dense embedding baseline evaluates semantic search over public website text. Each practitioner brief and each firm website document are encoded using Sentence-BERT, specifically the `all-MiniLM-L6-v2` model. Firms are ranked by cosine similarity between the brief embedding and firm-document embedding.

Let:

- $e(b_q)$ denote the embedding of brief $b_q$;
- $e(d_i)$ denote the embedding of firm document $d_i$.

The semantic similarity score is:


$$
Sim_{\mathrm{emb}}(b_q,d_i)=
\frac{e(b_q)\cdot e(d_i)}
{\|e(b_q)\|\|e(d_i)\|}
$$


The embedding retrieval result is:


$$
R_{\mathrm{Emb},q}=\operatorname{rank}_{f_i \in F}\left(Sim_{\mathrm{emb}}(b_q,d_i)\right)
$$


This baseline captures semantic similarity beyond exact keyword overlap. However, document-level semantic similarity may retrieve firms whose websites are generally related to the brief without satisfying all required capability constraints.

## 5. LLM-Assisted Retrieval or Classification Baseline

The LLM-assisted baseline evaluates whether a large language model can classify firm relevance to a sourcing brief using the same public website evidence. To maintain reproducibility and avoid uncontrolled web search, the LLM should not browse the internet. Instead, it receives:

1. the practitioner sourcing brief;
2. a standardised company evidence snippet from the same website corpus;
3. a fixed prompt template;
4. a fixed model and decoding configuration.

For each brief-firm pair $(b_q,f_i)$, the LLM returns:


$$
LLM(b_q,e_i) \rightarrow y_{q,i}
$$


where:

- $e_i$ is the evidence snippet for firm $f_i$;
- $y_{q,i}\in\{\text{Relevant}, \text{Partly relevant}, \text{Not relevant}, \text{Unclear}\}$.

The LLM candidate set can be defined as:


$$
R_{\mathrm{LLM},q}=\{f_i \in F : y_{q,i} \in \{\text{Relevant}, \text{Partly relevant}\}\}
$$


This baseline approximates human-like interpretation of noisy public evidence. However, it is more costly, more sensitive to prompt design and less transparent than BM25, embedding retrieval or RMCT-based retrieval.

## 6. RMCT-Based Retrieval

RMCT-based retrieval represents the proposed structured public capability observability approach. Each practitioner brief is mapped to RMCT facets, preferred labels and alternative labels. Firm-level RMCT profiles are then searched to identify companies whose public evidence matches the required capability structure.

For each brief $b_q$, define the RMCT requirement set as:


$$
C_q=\{c_{q1},c_{q2},\ldots,c_{qm}\}
$$


where each $c_{qj}$ is an RMCT concept, such as a process, material, certification, sector application, engineering support capability, digital capability, delivery-readiness attribute or sustainability-related capability.

Each firm $f_i$ has a public capability profile:


$$
P_i=\{p_{i1},p_{i2},\ldots,p_{in}\}
$$


where $P_i$ contains RMCT preferred labels, narrower categories and broader facets detected from public website evidence.

A simple RMCT match score is:


$$
Score_{\mathrm{RMCT}}(b_q,f_i)=
\frac{|C_q \cap P_i|}{|C_q|}
$$


A stricter candidate set can be defined as:


$$
R_{\mathrm{RMCT},q}=\{f_i \in F : C_q \subseteq P_i\}
$$


Where briefs include mandatory and desirable requirements, the score can be weighted:


$$
Score_{\mathrm{RMCT}}(b_q,f_i)=
\frac{\sum_{c \in C_q} w_c \cdot I(c \in P_i)}
{\sum_{c \in C_q} w_c}
$$


where:

- $w_c$ is the weight assigned to requirement $c$;
- $I(c \in P_i)$ equals 1 if firm $f_i$'s RMCT profile contains concept $c$, and 0 otherwise.

RMCT differs from BM25 and dense embedding retrieval because it first normalises website language into a controlled vocabulary and then retrieves firms using structured, multi-dimensional capability requirements.

## 7. Comparator Roles

| Comparator | What it represents | Main strength | Main limitation |
|---|---|---|---|
| SIC baseline | Existing public industrial classification | Broad public coverage | Too coarse for capability-level requirements |
| BM25 lexical retrieval | Strong lexical search over website text | Transparent and reproducible | Limited synonym and capability-structure handling |
| Dense embedding retrieval | Semantic similarity search | Captures related wording | May retrieve semantically similar but capability-incomplete firms |
| LLM-assisted classification | Evidence-based AI judgement | Interprets ambiguous evidence | Costly, prompt-sensitive and less transparent |
| RMCT-based retrieval | Proposed structured capability approach | Multi-dimensional, interpretable and capability-specific | Depends on vocabulary quality and public evidence availability |

## 8. Evaluation Metrics

Where expert relevance labels are available, the comparator systems should be evaluated using:

- precision;
- recall;
- F1;
- precision@k;
- recall@k;
- nDCG@k;
- candidate-set reduction at fixed recall;
- screening effort per relevant firm.

These metrics evaluate RMCT as a decision aid for manufacturing partner discovery rather than only as a classification structure.

