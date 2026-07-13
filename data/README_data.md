\# Data README



This folder contains derived research data for the RMCT public-data capability classification study.



The repository does not redistribute full raw website HTML or full cleaned website text. The files in this folder are derived datasets intended to support transparency, auditability and partial reproducibility.



\## Files



| File | Description | Contains full website text? |

|---|---|---|

| `public\_company\_frame\_sample.csv` | A public-data company frame or sample of firms used in the study, including non-sensitive firm identifiers and classification fields where available. | No |

| `capability\_evidence\_spans.csv` | Short evidence spans extracted from public manufacturer websites and linked to RMCT capability labels. | No |

| `rmct\_controlled\_vocabulary.csv` | RMCT preferred labels, alternative labels, broader dimensions and narrower categories used for capability classification. | No |

| `rmct\_company\_profiles\_anonymised.csv` | Company-level RMCT capability profiles generated from public website evidence. | No |

| `benchmark\_briefs.csv` | Procurement or partner-discovery briefs used for benchmarking retrieval and classification performance. | No |

| `benchmark\_results\_aggregate.csv` | Aggregate benchmarking results comparing RMCT with baseline methods. | No |

| `hashes/website\_document\_hashes.csv` | Document-level hashes used to support verification without releasing full website text. | No |



\## Data-Sharing Principle



Only derived and limited research outputs are shared. Full website texts are not redistributed because public manufacturer websites may be protected by copyright, website terms of use and later modification by website owners.



The shared files may include:



\- company identifiers;

\- website URLs where available;

\- crawl dates;

\- document hashes;

\- short evidence spans;

\- RMCT preferred labels;

\- alternative labels;

\- broader RMCT dimensions;

\- narrower categories;

\- aggregate benchmarking results.



The shared files do not intentionally include:



\- full raw website HTML;

\- full cleaned website text;

\- personal names;

\- email addresses;

\- phone numbers;

\- direct contact details;

\- contact-form content.



\## Interpreting Company-Level Profiles



The company-level profiles indicate capabilities that were publicly observable from available website evidence at the time of data collection. They should not be interpreted as complete operational audits of firm capability, capacity, commercial performance or supplier suitability.



Absence of a capability label in the dataset does not necessarily mean that the firm lacks that capability. It may mean that the capability was not publicly visible, not detected by the extraction process, or not represented in the available website text.



\## Evidence Spans



Evidence spans are short text fragments used to support assigned RMCT capability labels. They are included for verification and expert validation, not as a substitute for full website content.



\## Recommended Use



These data may be used to:



\- inspect how RMCT labels were assigned;

\- reproduce company-level capability profiling where possible;

\- reproduce aggregate benchmarking calculations;

\- support expert validation;

\- compare RMCT outputs with alternative classification or retrieval methods.



Users should not use these data for unsolicited marketing or direct commercial targeting.



\## Related Documentation



Please also see:



\- `../docs/data\_availability\_statement.md`

\- `../docs/public\_website\_data\_ethics\_statement.md`

\- `../docs/reproducibility\_protocol.md`

\- `../docs/code\_availability\_statement.md`

