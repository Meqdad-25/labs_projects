# Which Startups Raise Again?

**A data-driven screen for selecting seed-stage startups most likely to raise again.**

*Author: Meqdad · Project 2: Exploratory Data Analysis*

---

## Problem Statement

A venture capital firm struggles to reliably select seed-stage startups that will eventually secure follow-on funding, leaving it with a portfolio of stalled companies. This project analyzes historical Crunchbase funding data across industry category, geography, funding round counts, and timing to identify the patterns most associated with startups that successfully raise additional capital — and to refine the firm's $10M seed-stage investment criteria.

---

## Executive Summary

Venture firms make money when the startups they back at seed stage go on to raise larger follow-on rounds. A startup that raises seed money and never raises again has *stalled* — the capital is spent and the investor's stake is unlikely to return. This project asks a narrow, answerable question: **which kinds of seed-stage startups have historically gone on to raise again?**

Working from a Crunchbase dataset of ~49,000 companies, the analysis first cleaned substantial data-quality issues (~4,900 fully blank rows, a funding column stored as text, and corrupt funding dates), then narrowed to the **13,839 companies that raised a seed round** — the only population the firm's decision applies to. Success was defined as raising more than one funding round (`follow_on`). The headline result frames the entire problem: **only 41.2% of seed-stage startups ever raised again — nearly six in ten stalled.**

Three factors separate winners from stallers. **Industry** is the strongest single lever: seed startups in Finance (60%), Health Care (54%), Biotechnology (53%), and SaaS (52%) advanced far above the 41.2% baseline, while Apps (26%) and Fashion, E-Commerce, and Marketplaces (~35%) fell well below. **Geography** compounds it: US startups advanced at 50% and dominate the data, while Chile (13%) and India (29%) lagged badly. **Timing** provides an operational rule: the median follow-on round arrives in ~10 months and 90% of advancing companies raise again within two years. Critically, following on **predicts real success** — companies that advanced were acquired at roughly double the rate and closed at roughly half the rate of those that stalled, confirming the metric is meaningful rather than arbitrary.

Combining the two strongest levers — winning markets *and* winning geographies — lifts the follow-on rate from **41.2% to 60.9%**. Applied to a $10M fund (~33 seed cheques at the $300K median), this screen would historically have raised the number of advancing companies from ~14 to ~20 — about **seven additional advancing companies from the same capital.**

Chart Example:

![Follow-on rate by industry](presentation/images/market_chart.png)

---

## File Directory

| Path | Description |
|:---|:---|
| `README.md` | This file — project overview, findings, and recommendations. |
| `code/startup_investment_eda.ipynb` | The full analysis: data cleaning, EDA across all four factors, and the combined screen. |
| `data/startup_investments.csv` | Original Crunchbase dataset (as provided). |
| `data/startup_investments_clean.csv` | Cleaned dataset produced by the notebook (49,436 rows). |
| `presentation/startup_investments.pdf` | Non-technical slide deck of the findings. |

---

## Data & Data Dictionary

**Source:** Startup Investments dataset from Crunchbase (https://www.crunchbase.com), provided as `startup_investments.csv`. A historical snapshot covering ~49,000 companies worldwide.

**Analysis population:** 13,839 seed-stage companies (`seed > 0`).

Key columns used in the analysis (full dictionary in the notebook, Section 6):

| Feature | Type | Source | Description |
|:---|:---|:---|:---|
| `market` | string | Original | Primary industry category. |
| `country_code` | string | Original | 3-letter ISO country code of headquarters. |
| `status` | string | Original | Operating status: operating, acquired, or closed. |
| `funding_rounds` | float | Original | Total number of funding rounds raised. |
| `seed` | float | Original | Seed funding amount (USD); defines the population. |
| `first_funding_at` / `last_funding_at` | datetime | Original | Dates of first and most recent funding rounds. |
| `follow_on` | boolean | Engineered | Target: `True` if the company raised more than one round. |
| `avg_gap_days` | float | Engineered | Estimated average days between rounds. |

---

## Conclusions & Recommendations

1. **Tilt the $10M toward proven categories** — Finance, Health Care, Biotechnology, SaaS, and enterprise/analytics software. Deprioritize consumer Apps, Fashion, and generic E-Commerce.
2. **Weight toward strong ecosystems** — favor US-headquartered startups and secondary hubs (Japan); apply extra scrutiny where historical follow-on rates are a fraction of the US rate (e.g. Chile, India).
3. **Adopt a two-year follow-on checkpoint** — don't judge a company stalled before ~12 months, but if it hasn't raised again within 24 months, mark the investment inactive.
4. **Expected impact** — this screen would historically have improved the fund's hit rate from ~14 to ~20 advancing companies per $10M, a ~48% increase from the same capital.

---

## Areas for Further Research

- **Correlation, not causation:** the screen identifies favorable odds, not guarantees; founder and team quality are not in the data.
- **Survivorship / coverage bias:** Crunchbase self-reports, so quiet failures are under-represented.
- **Next steps:** model time-to-follow-on with survival analysis, incorporate founder/team data.

---

## Sources

- **Dataset:** Startup Investments (Crunchbase) — https://www.crunchbase.com
- **Tools:** Python 3 · pandas · NumPy · Matplotlib · Seaborn