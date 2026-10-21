# Shannon Medical Center: Outside-In Quality Analysis

A comparison of Shannon Medical Center (San Angelo, TX; CMS ID 450571) with eight West Texas
regional acute-care hospitals, using public CMS Care Compare data.

**Read the one-page brief:** [Shannon_Quality_Brief.pdf](Shannon_Quality_Brief.pdf)

## Findings

- **Outcomes are a strength.** Shannon is better than the national rate on 4 CMS outcome measures
  (mortality, safety, readmissions) and worse on none, the best net result in the peer group.
- **Cleanliness is the clearest gap.** 15% of surveyed patients said their room was "sometimes" or
  "never" clean, versus 9% nationally and 8% in Texas. Shannon ranks last of 9 on this measure.
- **Doctor communication is the highest in the group** (linear mean score 92).
- **Communication about medicines is low across the region**, not specifically at Shannon:
  7 of 9 hospitals are at 2 stars or below.

## Peer group

Hendrick Medical Center (Abilene), Midland Memorial Hospital, Medical Center Hospital and
Odessa Regional Medical Center (Odessa), Covenant Medical Center and University Medical Center
(Lubbock), Northwest Texas Hospital and BSA Hospital (Amarillo). General acute-care hospitals with
emergency departments; specialty surgical and heart hospitals excluded.

## Data

From [data.cms.gov](https://data.cms.gov/provider-data):

| File | Source dataset | Notes |
|---|---|---|
| `data/hospitals.csv` | Hospital General Information | Overall star rating; counts of outcome measures better/worse than national |
| `data/hcahps.csv` | HCAHPS Patient Survey (hospital level) | Star ratings and linear mean scores, 10/01/2024 to 09/30/2025 |

State and national cleanliness benchmarks come from the HCAHPS state and national files for the
same period.

## Run it

```
pip install duckdb matplotlib
python run.py      # runs the three queries in queries.sql
python charts.py   # rebuilds charts/outcomes.png and charts/cleanliness.png
```

## Limitations

- Public data lags: the survey period ended September 2025.
- HCAHPS is reported hospital-wide; it can't show which unit or campus drives a score.
- Linear scores are rounded, so differences of 1-2 points may not be meaningful.
- Cleanliness here is patient perception, not audit or infection data.

## How this was built

Data gathering, SQL and charts were developed with help from Claude (an AI assistant).
Key figures were checked against the CMS source files.
