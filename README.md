# RMCT Public-Data Capability Classification
Public-data-driven Regional Manufacturing Capability Taxonomy for manufacturing capability visibility and partner discovery.
# RMCT Public-Data Capability Classification

This repository provides reproducibility materials for the study:

**Public-data-driven Regional Manufacturing Capability Taxonomy for manufacturing capability visibility and partner discovery**

The project develops a Regional Manufacturing Capability Taxonomy (RMCT) for identifying, classifying and representing manufacturing capabilities from public data sources. The empirical setting is the West Midlands manufacturing ecosystem in the UK. The repository supports reproducibility of the taxonomy construction, controlled vocabulary development, company-level capability profiling, and benchmarking analyses reported in the manuscript.

## 1. Project Overview

Manufacturing supply chains require reliable information about where relevant production capabilities are located and how they can be accessed. Public industrial classifications such as SIC codes provide broad activity information, but they do not describe the specific capabilities that matter for supplier discovery, such as manufacturing processes, materials, certifications, engineering support, digital capability, commercial readiness, or sustainability-related practices.

This project treats regional manufacturing capability classification as a public-data-driven decision aid for supplier discovery and supply chain visibility. It uses public company records and manufacturer website text to construct firm-level capability profiles and evaluate whether RMCT improves capability-specific search compared with practical baselines.

## 2. Research Objectives

The repository supports the following research objectives:

1. Construct a theoretically grounded manufacturing capability taxonomy from prior literature.
2. Cross-check the taxonomy against independently extracted public website capability concepts.
3. Build a controlled vocabulary and thesaurus for normalising heterogeneous website language.
4. Generate company-level capability profiles from public website evidence.
5. Benchmark RMCT against practical alternatives, including SIC codes, keyword-only search, and single-dimension capability baselines.
6. Support expert validation and reproducibility without redistributing full raw website text.

## 3. Repository Structure

```text
RMCT-public-data-capability-classification/
├── README.md
├── LICENSE
├── requirements.txt
├── environment.yml
├── .gitignore
│
├── data/
│   ├── README_data.md
│   ├── public_company_frame_sample.csv
│   ├── capability_evidence_spans.csv
│   ├── rmct_controlled_vocabulary.csv
│   ├── rmct_company_profiles_anonymised.csv
│   ├── benchmark_briefs.csv
│   ├── benchmark_results_aggregate.csv
│   └── hashes/
│       └── website_document_hashes.csv
│
├── code/
│   ├── 01_preprocess_public_web_text.py
│   ├── 02_extract_capability_terms.py
│   ├── 03_build_rmct_vocabulary.py
│   ├── 04_create_company_profiles.py
│   ├── 05_benchmark_retrieval.py
│   └── 06_expert_validation_metrics.py
│
├── notebooks/
│   ├── rmct_taxonomy_construction.ipynb
│   ├── rmct_website_cluster_validation.ipynb
│   └── rmct_benchmarking.ipynb
│
├── outputs/
│   ├── figures/
│   └── tables/
│
└── docs/
    ├── data_availability_statement.md
    ├── code_availability_statement.md
    ├── public_website_data_ethics_statement.md
    └── reproducibility_protocol.md


## 4. Data Sources
The study uses two public-data sources:
Company population frame
A Companies House-derived population frame of manufacturers in the West Midlands region.

Manufacturer public websites
Publicly accessible manufacturer websites were scraped and processed to extract capability-related evidence.

The full raw and cleaned website texts are not redistributed in this repository. Instead, the repository provides derived research data that support verification while reducing copyright and privacy risks.

## 5. Data Availability and Sharing Approach
This repository shares derived and reproducibility-oriented data only. These include:
company identifiers;
website URLs where available;
crawl dates;
document hashes;
extracted capability evidence spans;
RMCT preferred labels;
alternative labels;
broader RMCT dimensions;
narrower capability categories;
anonymised company-level capability profiles;
aggregate benchmarking results.
The repository does not share:
full raw website HTML;
full cleaned website text;
personal contact details;
email addresses;
phone numbers;
contact-form content.
This approach allows the analysis to be checked without redistributing full website content.

## 6. RMCT Dimensions
The RMCT framework classifies manufacturing capability using eight first-level dimensions:
Code	RMCT Dimension
D1	Production Process Capability
D2	Material Capability
D3	Quality, Testing and Certification Capability
D4	Sector and Application Experience
D5	Engineering, Product Development and Industrialisation Support
D6	Digital Production and Automation Capability
D7	Commercial and Delivery Readiness
D8	Sustainability and Circular Production Practices

These dimensions were developed through literature-derived concept clustering, public website concept extraction, empirical cross-checking and controlled vocabulary construction.

## 7. Method Summary
The analysis pipeline consists of six main stages:
Public website text preprocessing
Website text is cleaned, normalised and prepared for capability extraction.

Capability concept extraction
Literature-derived concepts and independently extracted website concepts are used to identify candidate capability dimensions and terms.

Semantic clustering
Sentence-BERT embeddings, UMAP dimensionality reduction and HDBSCAN clustering are used to identify semantic clusters of manufacturing capability concepts.

Controlled vocabulary construction
Preferred labels, alternative labels, broader dimensions and narrower categories are constructed to normalise heterogeneous website language.

Company-level capability classification
Each company website is matched against the RMCT vocabulary to produce a structured capability profile.

Validation and benchmarking
RMCT-based classification is benchmarked against practical alternatives using population coverage, capability specificity and supplier-search noise reduction.

## 8. Reproducibility
The main scripts are provided in the code/ folder:
Script	Purpose
01_preprocess_public_web_text.py	Clean and prepare public website text
02_extract_capability_terms.py	Extract candidate manufacturing capability terms
03_build_rmct_vocabulary.py	Build the RMCT controlled vocabulary and thesaurus
04_create_company_profiles.py	Generate company-level RMCT capability profiles
05_benchmark_retrieval.py	Benchmark RMCT against comparison methods
06_expert_validation_metrics.py	Calculate expert validation metrics

The notebooks in notebooks/ provide a transparent workflow for taxonomy construction, website-cluster validation and benchmarking.
## 9. Software Environment
The project was developed in Python. Core packages include:
pandas
numpy
scikit-learn
sentence-transformers
umap-learn
hdbscan
matplotlib
seaborn
rank-bm25
openpyxl
See requirements.txt and environment.yml for environment details.

## 10. Ethical and Legal Notes
This project uses publicly accessible company website information for research purposes. The analysis focuses on manufacturing capability information intentionally disclosed by firms, such as processes, materials, certifications, sectors served and engineering services.
To reduce privacy and copyright risks:
full website texts are not redistributed;
personal names, email addresses and phone numbers are removed where detected;
only short evidence spans and derived capability labels are shared;
document hashes are provided to support verification without releasing full text.
Further details are provided in:
docs/data_availability_statement.md
docs/public_website_data_ethics_statement.md
docs/reproducibility_protocol.md

## 11. Citation
If you use this repository, please cite the associated manuscript:
Author(s). Year.   Manuscript under preparation.

A full citation will be added after publication.

## 12. Contact
For questions about the repository or associated manuscript, please contact the corresponding author.

