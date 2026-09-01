# Final Capstone — Presentation Package

**14 slides · 15 minutes · Meqdad Muhana · DSB FT2**
*Bank Customer Churn Prediction*

---

# PART 1 — Structure at a glance

| # | Slide | Time | Covers which requirement |
|---|-------|------|--------------------------|
| 1 | Title | 20 sec | — |
| 2 | Introduction | 60 sec | ✅ Introduction on your topic |
| 3 | Problem Statement & Aim | 90 sec | ✅ Problem framing |
| 4 | Data Summary | 70 sec | ✅ What data, what records represent |
| 5 | EDA — The Two-Month Drain | 100 sec | ✅ Key findings |
| 6 | EDA — Data Quality & Hidden Signal | 80 sec | ✅ Key findings |
| 7 | Modeling Approach | 80 sec | ✅ Features, preprocessing, model types |
| 8 | Model 1 — Logistic Regression | 90 sec | ✅ All 4 sub-requirements |
| 9 | Model 2 — Random Forest | 90 sec | ✅ All 4 sub-requirements |
| 10 | Model 3 — XGBoost | 90 sec | ✅ All 4 sub-requirements |
| 11 | Model Comparison & Best Model | 90 sec | ✅ Summary table + which is best and why |
| 12 | Business Implications | 70 sec | ✅ Business implications |
| 13 | Limitations & Improvements | 70 sec | ✅ Limitations + potential improvements |
| 14 | Questions | 10 sec | — |

**Total ≈ 17 min of slide time budget, script is ~13 min of speaking.** That leaves room to
slow down. You have 15 minutes maximum, so finishing at 13 is safe.

**Why 14 slides:** the four sample decks ranged from 11 to 23. The Conclusion requirement
has five separate parts, so it is split across slides 11–13 rather than crammed into one.

---

# PART 2 — Content of each slide

## SLIDE 1 — Title
**Predicting Customer Churn in Retail Banking**
*Finding customers who are about to leave, before they go*
Meqdad Muhana | Data Science Bootcamp — DSB FT2, Bahrain 2026
Bottom strip: `28,382 customers · 18.53% churn · Binary Classification`

---

## SLIDE 2 — Introduction

**The topic**
A retail bank's savings accounts are one of its main sources of funding. When a customer
quietly drains their balance and goes dormant, the bank loses that funding — and because
nobody formally closes a savings account, the bank usually finds out only after the money
has gone.

**Three stat boxes:** `28,382 customers` · `21 columns` · `18.53% churn`

**What we have on each customer**
- **Who they are** — age, gender, occupation, dependents, time with the bank
- **Where they bank** — city and branch
- **What their money is doing** — balances and transactions across 2 months and 2 quarters

---

## SLIDE 3 — Problem Statement & Aim

**The problem**
18.53% of savings customers churn. The retention team currently calls customers almost at
random — wasting effort on people who were never going to leave, and missing the ones who do.

**The aim**
Classify every savings customer as **high risk** or **low risk** of churning, using their
profile and recent transaction behaviour, so the retention team contacts only the customers
who are actually about to leave.

**Success metrics**

| Metric | Target | Why |
|---|---|---|
| **Recall (churn)** | **≥ 0.70** | Catch at least 7 in 10 real churners |
| **ROC-AUC** | **≥ 0.80** | Ranks risk correctly, not fooled by imbalance |
| Precision / F1 | monitored | Keeps the call list realistic |
| ❌ Accuracy | **not used** | A do-nothing model already scores 81.5% |

---

## SLIDE 4 — Data Summary

**Source:** Kaggle — Bank Customer Churn Data · single CSV · 28,382 × 21

**Each record is one savings-account customer**, with:
- **6 customer columns** — vintage, age, gender, dependents, occupation, net-worth tier
- **2 location columns** — city (1,605 codes), branch (3,185 codes)
- **6 balance columns** — current, previous month, previous 2 quarters
- **4 transaction columns** — money in and money out, this month and last
- **1 date column** — last transaction
- **Target:** `churn` — 1 = left, 0 = stayed

**Data quality out of the box**
- 0 duplicate rows
- 3,871 visible missing values across 4 columns
- Money columns extremely skewed — one customer holds **5.9 million** against a median of **3,281**

---

## SLIDE 5 — EDA Key Finding: Churn is a Two-Month Drain

**Median values — customers who stayed vs customers who churned**

| | Stayed | Churned | |
|---|---|---|---|
| Balance 2 quarters ago | 3,383 | 3,206 | *nearly identical* |
| Balance last quarter | 3,508 | **3,721** | *churners held more* |
| Money out — last month | 43 | **838** | **19× higher** |
| Money out — this month | 22 | **1,120** | **51× higher** |
| Balance now | 3,643 | **1,541** | *collapsed to under half* |

> **Churn is not sudden. It is a visible drain over about two months.**
> Act when the withdrawals spike — not after the balance is gone.

**Who leaves:** self-employed **19.84%** · 1–3 dependents **~22%** vs 17.42% with none ·
net worth barely matters (17.9% – 19.2%)

---

## SLIDE 6 — EDA Key Finding: Data Quality & The Hidden Signal

**Three problems the data hid**

| Found | Detail |
|---|---|
| **3,223 hidden nulls** | Missing dates stored as the **text** `'NaT'` — `.isnull()` reported none |
| **806 impossible ages** | Minimum age was **1 year old** |
| **10 impossible dependents** | Up to **52**, with a gap in the data from 9 straight to 25 |

**And the missingness was informative** — customers with no transaction date churn at
**9.28%**, against **19.72%** for those who have one.

**The correlations looked useless — but they were not**

| Feature | Raw | After log transform |
|---|---|---|
| `current_month_debit` | 0.048 | **0.236** |
| `previous_month_debit` | 0.073 | **0.200** |

Skew up to **143** was breaking the correlation. The signal was always there.

**Chi-Square:** all 3 categorical features significant (p < 0.05) — `occupation` strongest at χ² = 56.95

**Zero rows were deleted.**

---

## SLIDE 7 — Modeling Approach

**Feature engineering — 5 new features measuring *change*, not level**
`balance_drop_pct` · `balance_change` · `debit_to_balance` · `net_flow_current` · `quarter_decline`

**Preprocessing pipeline (`ColumnTransformer`)**
- **Skewed money columns** → median impute → **Yeo-Johnson** *(handles negative overdrafts; log and Box-Cox cannot)*
- **Normal numeric** → median impute → **StandardScaler**
- **Categorical** → most-frequent impute → **OneHotEncoder(drop='first')**
- **High-cardinality** branch & city → **frequency encoding** *(avoids ~4,800 new columns)*

**Feature selection:** 6 balance columns correlated up to **0.994** → 4 dropped ·
`quarter_decline` dropped (correlation 0.0001) → **24 final features**

**Handling the 18.53% imbalance** — compared 3 methods on Model 1:
`class_weight='balanced'` (4.4×) · SMOTE · RandomOverSampler

**Split:** 75/25 with `stratify=y` — both sets hold exactly 18.53%

**3 model types × base + tuned = 6 models**, plus a `DummyClassifier` baseline

---

## SLIDE 8 — Model 1: Logistic Regression (tuned)

**What we did:** `GridSearchCV`, scored on **recall**, `StratifiedKFold(cv=5)`
**Best parameters:** `C=0.01` · `penalty='l1'` · `class_weight='balanced'`

*L1 regularisation shrank 10 of the 24 features to exactly zero — the model selected its own features.*

**Performance vs base**

| | Base | **Tuned** | Change |
|---|---|---|---|
| Recall | 0.421 | **0.720** | **+0.299** ✅ |
| ROC-AUC | 0.815 | 0.815 | — |
| Precision | 0.708 | 0.486 | −0.222 |
| F1 | 0.528 | 0.580 | +0.052 |

**Churners caught: 553 → 947** out of 1,315

**Features that influenced the model (coefficients)**

| Feature | Coefficient |
|---|---|
| `balance_drop_pct` | **−1.009** |
| `debit_to_balance` | +0.305 |
| `no_last_txn` | −0.255 |
| `previous_month_debit` | +0.139 |

---

## SLIDE 9 — Model 2: Random Forest (tuned)

**What we did:** `GridSearchCV`, scored on **recall**, `StratifiedKFold(cv=5)`
**Best parameters:** `max_depth=6` · `min_samples_leaf=20` · `n_estimators=200` · `class_weight='balanced'`

*Both constraints stop the trees memorising the training data.*

**Performance vs base**

| | Base | **Tuned** | Change |
|---|---|---|---|
| Recall | 0.592 | **0.703** | **+0.111** ✅ |
| ROC-AUC | 0.834 | **0.839** | +0.005 |
| Precision | 0.638 | 0.512 | −0.126 |
| F1 | 0.614 | 0.593 | −0.021 |

**Features that influenced the model (importances)**

| Feature | Importance | |
|---|---|---|
| `balance_drop_pct` | **0.393** | **engineered** |
| `current_balance` | 0.181 | original |
| `balance_change` | 0.103 | **engineered** |
| `debit_to_balance` | 0.089 | **engineered** |
| `net_flow_current` | 0.065 | **engineered** |

> **One engineered feature drives 39% of the decisions. Four of the top five are ones we built.**

---

## SLIDE 10 — Model 3: XGBoost (tuned)

**What we did:** `GridSearchCV`, scored on **recall**, `StratifiedKFold(cv=5)`
**Best parameters:** `n_estimators=200` · `max_depth=3` · `learning_rate=0.05` · `scale_pos_weight=4.40`

*XGBoost has no `class_weight`; `scale_pos_weight` does the same job.*
*Low learning rate + shallow trees = many small corrections, which generalise better.*

**Performance vs base**

| | Base | **Tuned** | Change |
|---|---|---|---|
| Recall | 0.624 | **0.700** | **+0.076** ✅ |
| ROC-AUC | 0.816 | **0.842** | **+0.026** ⭐ |
| Precision | 0.558 | 0.516 | −0.042 |
| F1 | 0.589 | 0.594 | +0.005 |

**Highest ROC-AUC of all 10 runs.**

**Features that influenced the model (importances)**

| Feature | Importance |
|---|---|
| `balance_drop_pct` | **0.498** |
| `no_last_txn` | 0.062 |
| `balance_change` | 0.039 |
| `current_month_debit` | 0.036 |

---

## SLIDE 11 — Model Comparison & Best Model

| Model | Accuracy | **Recall** | Precision | F1 | **ROC-AUC** |
|---|---|---|---|---|---|
| Baseline (most frequent) | 0.815 | 0.000 | 0.000 | 0.000 | 0.500 |
| A. Logistic Regression | 0.807 | **0.720** | 0.486 | 0.580 | 0.815 |
| B. Random Forest | 0.821 | 0.703 | 0.512 | 0.593 | 0.839 |
| **C. XGBoost** | **0.823** | 0.700 | **0.516** | **0.594** | **0.842** |

**All three met both targets.** ✅ recall ≥ 0.70 ✅ ROC-AUC ≥ 0.80

### ✅ Best model: XGBoost

**XGBoost wins 4 of the 5 metrics.** Logistic Regression wins only recall, by 0.020.

**What that 0.020 costs:**

| | Churners caught | Wasted calls |
|---|---|---|
| Logistic Regression | **947** | 1,002 |
| XGBoost | 920 | **863** |

**27 more churners for 139 more wasted calls — a bad trade.**

**And ROC-AUC decides it:** the retention team gets a list *ordered by risk* and works down
it. ROC-AUC measures exactly how good that ordering is. XGBoost is best (0.842).

---

## SLIDE 12 — Business Implications

**From zero to seven in ten.** A do-nothing baseline found **0** churners. The final model
finds **~7 in every 10**.

**On the test set of 7,096 customers**

| | |
|---|---|
| Real churners | 1,315 |
| Identified | **920** |
| Flagged for contact | **1,783 — about 25% of customers** |

A quarter of the customer base is a list a retention team can actually work through.

**The insight is usable even without the model**

> Churn is a **two-month drain**. The trigger should be the **rate of balance decline**, not
> the balance level. A customer whose balance falls sharply against their own normal is at
> risk however much money they still hold.

**How the bank would use it**
1. Score every customer monthly
2. Rank by churn probability
3. Send the top ~25% to the retention team, highest risk first
4. Track who stays, and retrain as new data arrives

---

## SLIDE 13 — Limitations & Improvements

**Limitations**

| | |
|---|---|
| **No source documentation** | Dataset has no published provenance — internal checks all indicate real bank records, but this could not be formally verified |
| **Snapshot, not full history** | Only 2 months and 2 quarters per customer |
| **No context on *why*** | No complaints, competitor offers, or life events |
| **Churn definition unknown** | We know *that* a customer churned, not the exact rule used |
| **Precision ~0.52** | About half of flagged customers would not have churned |
| **30% of churners missed** | 395 customers in the test set |
| **Trees are harder to explain** | XGBoost gives importances, not per-customer reasons like a coefficient |

**Potential improvements**
- Longer transaction history, and the bank's actual churn definition
- Customer service records — complaints and contact history
- Test on live customers before full deployment
- Estimate what a saved customer is worth, so the model can be tuned on **money** rather than a recall target

---

## SLIDE 14 — Questions

**Thank you**
Questions & Discussion

Small recap strip: `XGBoost · Recall 0.700 · ROC-AUC 0.842 · Both targets met`

---

# PART 3 — Prompt for Manus AI

> Copy everything inside the box and paste it into Manus AI.

```
Create a presentation deck in 16:9 widescreen format.

============================================================
CRITICAL CONSTRAINT — READ THIS FIRST
============================================================
Output EXACTLY 14 SLIDES. Not 15. Not 20. Exactly 14.

DO NOT ADD any slide that is not listed below. Specifically, DO NOT add:
- an agenda, overview, or table-of-contents slide
- a background, context, or "why this matters" slide
- a methodology, roadmap, or timeline slide
- a separate summary or key-takeaways slide
- any divider, section-break, or transition slide
- a second thank-you slide (slide 14 already is one)

DO NOT SPLIT any slide into two slides. Many slides below contain a table
AND bullet points together — keep them on ONE slide. Make tables compact
so everything fits.

If you think a slide is missing or the deck feels incomplete, DO NOT ADD IT.

When you finish, COUNT THE SLIDES. If the number is not exactly 14,
delete the extra slides.
============================================================

=== DESIGN RULES (apply to all 14 slides) ===
- Style: clean, modern, professional, corporate banking.
- Colours: deep navy (#0F2A44) for titles, white background, teal (#1B9AAA)
  as the accent for key numbers. Use soft red (#C0392B) ONLY for the churn
  numbers on slide 5 and the "not used" row on slide 3.
- Font: clean sans-serif (Inter, Lato or Calibri).
- Minimum 15pt body text, 28pt slide titles.
- Short bullets only, maximum 12 words each. NO paragraphs anywhere.
- Make every number and percentage BOLD and in the accent colour.
- Small slide number in the bottom right of every slide.
- Simple flat icons only. No clipart, no cartoons, no photos of people.
- IMPORTANT: on every slide, make sure tables do not overflow. Reduce table
  font size before you let anything get cut off.

=== SLIDE 1 : TITLE ===
Centred title slide.
IMPORTANT: make the title text box span the FULL width of the slide (0.5 inch
margin each side) so the title fits on ONE line and never wraps or overlaps
the subtitle.
Main title: "Predicting Customer Churn in Retail Banking"
Subtitle: "Finding customers who are about to leave, before they go"
Presenter line: "Meqdad Muhana | Data Science Bootcamp - DSB FT2, Bahrain 2026"
Bottom line in teal: "28,382 customers · 18.53% churn · Binary Classification"
Add one simple flat icon of a bank building above the title.

=== SLIDE 2 : INTRODUCTION ===
Title: "Introduction"
TOP - a short paragraph block titled "THE TOPIC":
"A retail bank's savings accounts are a main source of funding. When a customer
quietly drains their balance and goes dormant, the bank loses that funding. And
because nobody formally closes a savings account, the bank finds out only after
the money has gone."
MIDDLE - three large stat boxes in a row (big number, small label underneath):
  "28,382" / "customers"
  "21" / "columns"
  "18.53%" / "churn rate"
BOTTOM - heading "What we know about each customer", 3 bullets:
- "Who they are - age, gender, occupation, dependents, time with the bank"
- "Where they bank - city and branch"
- "What their money is doing - balances and transactions over 2 months and 2 quarters"

=== SLIDE 3 : PROBLEM STATEMENT & AIM ===
Title: "Problem Statement & Aim"
TOP LEFT (50%) - box titled "THE PROBLEM":
"18.53% of savings customers churn. The retention team calls customers almost at
random - wasting effort on people who were never leaving, and missing the ones
who do."
TOP RIGHT (50%) - box titled "THE AIM":
"Classify every customer as high risk or low risk of churning, so the retention
team contacts only those who are actually about to leave."
BOTTOM - full width, a compact 4-row table titled "SUCCESS METRICS":
  Header: Metric | Target | Why
  Row 1: "Recall (churn)" | "= 0.70 or higher" | "Catch 7 in 10 real churners"
  Row 2: "ROC-AUC" | "= 0.80 or higher" | "Ranks risk correctly"
  Row 3: "Precision / F1" | "Monitored" | "Keeps the call list realistic"
  Row 4: "Accuracy" | "NOT USED" | "A do-nothing model already scores 81.5%"
Style row 4 in grey with a small red cross icon.

=== SLIDE 4 : DATA SUMMARY ===
Title: "Data Summary"
TOP - one line: "Source: Kaggle - Bank Customer Churn Data | Single CSV file |
28,382 rows x 21 columns"
MIDDLE - heading "Each record is one savings-account customer", 6 bullets:
- "6 customer columns - vintage, age, gender, dependents, occupation, net worth"
- "2 location columns - city (1,605 codes), branch (3,185 codes)"
- "6 balance columns - current month, previous month, previous two quarters"
- "4 transaction columns - money in and money out, this month and last"
- "1 date column - last transaction"
- "Target: churn (1 = left the bank, 0 = stayed)"
BOTTOM - a highlighted box titled "DATA QUALITY", 3 short bullets:
- "0 duplicate rows"
- "3,871 visible missing values across 4 columns"
- "Money columns extremely skewed - one customer holds 5.9 million vs a median of 3,281"

=== SLIDE 5 : EDA KEY FINDING - THE TWO-MONTH DRAIN ===
Title: "Key Finding: Churn is a Two-Month Drain"
MAIN ELEMENT - a 5-row comparison table, large and central:
  Header row (navy background, white text): (blank) | Stayed | Churned | 
  Row 1: "Balance 2 quarters ago" | "3,383" | "3,206" | "nearly identical"
  Row 2: "Balance last quarter" | "3,508" | "3,721" | "churners held more"
  Row 3: "Money out - last month" | "43" | "838" | "19x higher"
  Row 4: "Money out - this month" | "22" | "1,120" | "51x higher"
  Row 5: "Balance now" | "3,643" | "1,541" | "collapsed to half"
Make the "Churned" values in rows 3, 4 and 5 BOLD and soft red.
BELOW THE TABLE - a full-width teal band with white text:
"Churn is not sudden. It is a visible drain over about two months."
Under the band, small grey text:
"Act when the withdrawals spike, not after the balance is gone."
BOTTOM - one line: "Who leaves: self-employed 19.84% | 1-3 dependents ~22% vs
17.42% with none | net worth barely matters (17.9% - 19.2%)"

=== SLIDE 6 : EDA KEY FINDING - DATA QUALITY & HIDDEN SIGNAL ===
Title: "Key Finding: The Data Was Hiding Its Own Signal"
TOP LEFT (50%) - heading "Three problems the data hid", a compact 3-row table:
  Header: Found | Detail
  "3,223 hidden nulls" | "Missing dates stored as the TEXT 'NaT'"
  "806 impossible ages" | "Minimum age was 1 year old"
  "10 impossible dependents" | "Up to 52, with a gap from 9 straight to 25"
  Below it, one line: "And the missingness was informative: no transaction date
  = 9.28% churn vs 19.72% with one."
TOP RIGHT (50%) - heading "The correlations looked useless - but were not",
a compact 2-row table:
  Header: Feature | Raw | After log
  "current_month_debit" | "0.048" | "0.236"
  "previous_month_debit" | "0.073" | "0.200"
  Below it, one line: "Skew up to 143 was breaking the correlation."
BOTTOM - full width, two short lines:
"Chi-Square: all 3 categorical features significant (p < 0.05), occupation strongest"
"Zero rows were deleted during cleaning."

=== SLIDE 7 : MODELING APPROACH ===
Title: "Modeling Approach"
LEFT COLUMN (50%) - heading "FEATURE ENGINEERING", one line:
"5 new features measuring CHANGE, not level:"
then 5 short items in a small box:
"balance_drop_pct | balance_change | debit_to_balance | net_flow_current |
quarter_decline"
Then heading "FEATURE SELECTION", 2 bullets:
- "6 balance columns correlated up to 0.994 - dropped 4"
- "quarter_decline dropped (correlation 0.0001) - 24 final features"
RIGHT COLUMN (50%) - heading "PREPROCESSING PIPELINE (ColumnTransformer)",
4 bullets:
- "Skewed money columns - Yeo-Johnson (handles negative overdrafts)"
- "Normal numeric - StandardScaler"
- "Categorical - OneHotEncoder(drop='first')"
- "Branch & city - frequency encoding (avoids 4,800 new columns)"
BOTTOM - full width highlighted band, 2 lines:
"Imbalance (18.53%): compared class_weight='balanced' (4.4x), SMOTE, RandomOverSampler"
"Split 75/25 with stratify=y | 3 model types x base + tuned = 6 models, plus a baseline"

=== SLIDES 8, 9 AND 10 : USE THE EXACT SAME LAYOUT ===
Layout for each of these three model slides:
- Slide title at the top.
- A thin strip under the title showing "WHAT WE DID" and the best parameters.
- LEFT COLUMN (50%): a bordered box titled "PERFORMANCE vs BASE MODEL"
  containing a 4-row table with columns: Metric | Base | Tuned | Change
- RIGHT COLUMN (50%): a bordered box titled "FEATURES THAT INFLUENCED THE MODEL"
  containing a small table.
- A note line at the bottom.
Make the "Tuned" column values bold and teal. Make the recall row stand out.

--- SLIDE 8 CONTENT ---
Title: "Model 1: Logistic Regression (tuned)"
WHAT WE DID strip: "GridSearchCV scored on recall, StratifiedKFold cv=5 |
Best: C=0.01, penalty='l1', class_weight='balanced'"
PERFORMANCE table:
  Header: Metric | Base | Tuned | Change
  "Recall" | "0.421" | "0.720" | "+0.299"
  "ROC-AUC" | "0.815" | "0.815" | "no change"
  "Precision" | "0.708" | "0.486" | "-0.222"
  "F1" | "0.528" | "0.580" | "+0.052"
FEATURES table (title "Coefficients"):
  Header: Feature | Coefficient
  "balance_drop_pct" | "-1.009"
  "debit_to_balance" | "+0.305"
  "no_last_txn" | "-0.255"
  "previous_month_debit" | "+0.139"
BOTTOM note: "Churners caught: 553 to 947 out of 1,315. L1 regularisation shrank
10 of the 24 features to zero, so the model selected its own features."

--- SLIDE 9 CONTENT ---
Title: "Model 2: Random Forest (tuned)"
WHAT WE DID strip: "GridSearchCV scored on recall, StratifiedKFold cv=5 |
Best: max_depth=6, min_samples_leaf=20, n_estimators=200, class_weight='balanced'"
PERFORMANCE table:
  Header: Metric | Base | Tuned | Change
  "Recall" | "0.592" | "0.703" | "+0.111"
  "ROC-AUC" | "0.834" | "0.839" | "+0.005"
  "Precision" | "0.638" | "0.512" | "-0.126"
  "F1" | "0.614" | "0.593" | "-0.021"
FEATURES table (title "Feature importances"):
  Header: Feature | Importance | Origin
  "balance_drop_pct" | "0.393" | "engineered"
  "current_balance" | "0.181" | "original"
  "balance_change" | "0.103" | "engineered"
  "debit_to_balance" | "0.089" | "engineered"
  "net_flow_current" | "0.065" | "engineered"
BOTTOM note, in a highlighted teal band: "One engineered feature drives 39% of the
decisions. Four of the top five features are ones we built ourselves."

--- SLIDE 10 CONTENT ---
Title: "Model 3: XGBoost (tuned)"
WHAT WE DID strip: "GridSearchCV scored on recall, StratifiedKFold cv=5 |
Best: n_estimators=200, max_depth=3, learning_rate=0.05, scale_pos_weight=4.40"
PERFORMANCE table:
  Header: Metric | Base | Tuned | Change
  "Recall" | "0.624" | "0.700" | "+0.076"
  "ROC-AUC" | "0.816" | "0.842" | "+0.026"
  "Precision" | "0.558" | "0.516" | "-0.042"
  "F1" | "0.589" | "0.594" | "+0.005"
FEATURES table (title "Feature importances"):
  Header: Feature | Importance
  "balance_drop_pct" | "0.498"
  "no_last_txn" | "0.062"
  "balance_change" | "0.039"
  "current_month_debit" | "0.036"
BOTTOM note: "Highest ROC-AUC of all 10 runs. XGBoost has no class_weight, so
scale_pos_weight does the same job."

=== SLIDE 11 : MODEL COMPARISON & BEST MODEL ===
Title: "Model Comparison & Best Model"
TOP - a 4-row comparison table, full width:
  Header (navy): Model | Accuracy | Recall | Precision | F1 | ROC-AUC
  "Baseline (most frequent)" | "0.815" | "0.000" | "0.000" | "0.000" | "0.500"
  "A. Logistic Regression" | "0.807" | "0.720" | "0.486" | "0.580" | "0.815"
  "B. Random Forest" | "0.821" | "0.703" | "0.512" | "0.593" | "0.839"
  "C. XGBoost" | "0.823" | "0.700" | "0.516" | "0.594" | "0.842"
Highlight the XGBoost row with a light teal background.
Under the table, one line in green: "All three met both targets: recall 0.70+ and
ROC-AUC 0.80+"
BOTTOM LEFT (50%) - heading "BEST MODEL: XGBoost", 2 bullets:
- "Wins 4 of the 5 metrics"
- "Logistic Regression wins only recall, by 0.020"
BOTTOM RIGHT (50%) - a small 2-row table titled "What that 0.020 costs":
  Header: Model | Churners caught | Wasted calls
  "Logistic Regression" | "947" | "1,002"
  "XGBoost" | "920" | "863"
  Below it, one line in bold: "27 more churners for 139 more wasted calls - a bad trade."

=== SLIDE 12 : BUSINESS IMPLICATIONS ===
Title: "Business Implications"
TOP - a large highlighted statement:
"From zero to seven in ten. A do-nothing baseline found 0 churners. The final model
finds about 7 in every 10."
MIDDLE LEFT (45%) - a small 3-row table titled "On 7,096 test customers":
  "Real churners" | "1,315"
  "Identified by the model" | "920"
  "Flagged for contact" | "1,783 (about 25%)"
  Below it: "A quarter of the customer base is a list a team can actually work through."
MIDDLE RIGHT (55%) - heading "How the bank would use it", 4 numbered bullets:
1. "Score every customer monthly"
2. "Rank by churn probability"
3. "Send the top 25% to the retention team, highest risk first"
4. "Track who stays, and retrain as new data arrives"
BOTTOM - full width teal band with white text:
"The trigger should be the RATE of balance decline, not the balance level."

=== SLIDE 13 : LIMITATIONS & IMPROVEMENTS ===
Title: "Limitations & Potential Improvements"
LEFT COLUMN (55%) - heading "LIMITATIONS", a compact 6-row table:
  Header: Limitation | Impact
  "No source documentation" | "Provenance could not be formally verified"
  "Snapshot, not full history" | "Only 2 months and 2 quarters per customer"
  "No context on why" | "No complaints, competitor offers, or life events"
  "Churn definition unknown" | "We know that a customer churned, not the rule used"
  "Precision about 0.52" | "Half of flagged customers would not have churned"
  "30% of churners missed" | "395 customers in the test set"
RIGHT COLUMN (45%) - heading "POTENTIAL IMPROVEMENTS", 4 bullets:
- "Longer transaction history and the bank's actual churn definition"
- "Customer service records - complaints and contact history"
- "Test on live customers before full deployment"
- "Estimate what a saved customer is worth, so the model can be tuned on money
  instead of a recall target"

=== SLIDE 14 : QUESTIONS ===
Centred closing slide.
Large text: "Thank You"
Below it: "Questions & Discussion"
At the bottom, a small teal strip:
"XGBoost · Recall 0.700 · ROC-AUC 0.842 · Both targets met"

============================================================
FINAL CHECK BEFORE YOU FINISH
============================================================
1. Count the slides. If it is not exactly 14, delete the extras.
2. Confirm slide 1's title sits on ONE line and does not overlap the subtitle.
3. Confirm slides 8, 9 and 10 use an IDENTICAL layout.
4. Confirm no table overflows its slide and no text is cut off.
5. Confirm you did NOT add an agenda, summary, or extra thank-you slide.
============================================================
```

---

# PART 4 — Speaking script

**1,900 words.** Timing depends on your pace:

| Your pace | Time |
|---|---|
| 150 wpm (normal) | **12.7 min** ✅ |
| 140 wpm | **13.6 min** ✅ |
| 130 wpm (slow) | **14.6 min** ⚠️ tight |
| 120 wpm (very slow) | 15.8 min ❌ over |

**Time yourself once.** If you land over 14 minutes, cut the two marked ⚡ lines on slides 6
and 7 — that saves about 40 seconds. Pause at every full stop.

---

## SLIDE 1 — Title *(15 sec)*

> Hello everyone. My name is Meqdad.
>
> My capstone is about **bank customer churn** — when a customer stops using their account
> and leaves the bank.
>
> My goal was to find these customers **before** they go.

---

## SLIDE 2 — Introduction *(45 sec)*

> A bank makes money from the deposits sitting in savings accounts.
>
> The problem is that nobody closes a savings account officially. They just take their money
> out slowly and go quiet. So the bank finds out **after** the money is gone.
>
> My dataset has twenty-eight thousand customers and twenty-one columns. Eighteen point five
> percent of them churned.
>
> For each customer I know who they are, where they bank, and most importantly **what their
> money is doing** over the last two months and two quarters.

---

## SLIDE 3 — Problem Statement & Aim *(70 sec)*

> Almost nineteen percent of customers leave. And right now the retention team calls people
> almost randomly. So they waste time on customers who were never leaving, and miss the real
> ones.
>
> My aim is to classify every customer as high risk or low risk, so the team only calls the
> people who are actually about to go.
>
> My main metric is **recall**. Recall answers one question: out of all the customers who
> really left, how many did I find? My target was seventy percent.
>
> My second metric is **ROC-AUC**, which measures how well the model ranks customers by risk.
>
> And look at the last row. I do **not** use accuracy.
>
> This matters. Eighty-one percent of customers do not churn. So a model that says "nobody
> leaves" is already eighty-one percent accurate — but it finds zero churners. It is useless.

---

## SLIDE 4 — Data Summary *(50 sec)*

> My data comes from Kaggle. One CSV file, twenty-eight thousand rows, twenty-one columns.
>
> **Each row is one savings-account customer.**
>
> Six columns describe the customer. Two describe location. Six are account balances at
> different times. Four are transactions — money in and money out. One is the date of their
> last transaction.
>
> The target is churn — one if they left, zero if they stayed.
>
> No duplicate rows, and about three thousand nine hundred missing values.
>
> And the money columns are extremely skewed. One customer holds almost **six million**,
> while a normal customer holds about three thousand. That customer caused me problems later.

---

## SLIDE 5 — EDA: The Two-Month Drain *(85 sec)*
### ← Your best slide. Slow down. Point at the table.

> This is my most important finding.
>
> The left column is customers who **stayed**. The right column is customers who **left**.
>
> Two quarters ago, both groups look almost the same.
>
> Last quarter, the customers who left actually had **more** money than everyone else. So at
> this point you cannot tell them apart.
>
> Now look at the money going **out**.
>
> Last month, the leavers took out **nineteen times more**. This month, **fifty-one times
> more**.
>
> And their balance has collapsed to less than half.
>
> So here is the finding. **Churn is not sudden. It is a slow drain over about two months.**
>
> This is very useful. The bank should act **when the withdrawals start** — not after the
> account is empty.
>
> ⚡ Quickly on who leaves. Self-employed customers churn most. Customers with dependents churn
> more. But net worth barely matters — rich customers leave too, and they take more money
> with them.

---

## SLIDE 6 — EDA: Data Quality & Hidden Signal *(60 sec)*

> Now the data problems.
>
> ⚡ Three thousand missing dates were **hidden** — saved as text, so Python did not count them
> as missing. Eight hundred customers had an impossible age; the youngest was **one year
> old**.
>
> But the missing dates were not random. Customers with no date churned at nine percent,
> against nineteen percent for those with one. So even the missing data told me something.
>
> Now the part I like most.
>
> At first, all my correlations looked useless. The strongest was only zero point zero seven.
>
> But that was wrong. Remember the customer with six million? That one customer was
> **breaking the calculation**.
>
> After a log transform, the same column went from zero point zero five up to zero point two
> four. Five times stronger.
>
> The signal was always there. It was hidden by the skew.
>
> And I deleted **zero** rows during cleaning.

---

## SLIDE 7 — Modeling Approach *(65 sec)*

> Now how I built the models.
>
> First, feature engineering — the most important step.
>
> The raw columns tell you **how much** money a customer has. But churn is about **change**.
> So I built five new features that measure movement instead of level.
>
> The most important is **balance drop percent** — how far a balance fell compared to
> **that customer's own** normal level.
>
> On the right is preprocessing. Skewed money columns get a Yeo-Johnson transform. I used
> Yeo-Johnson and not a log, because some balances are negative — real overdrafts — and log
> cannot handle negative numbers.
>
> For branch and city I used frequency encoding. There were over three thousand branch codes.
> One-hot encoding would have created almost five thousand columns. So instead I replaced
> each code with the **number of customers in that branch**.
>
> Then three model types, each run twice — a base version and a tuned version.

---

## SLIDE 8 — Model 1: Logistic Regression *(70 sec)*

> Model one is Logistic Regression — my simplest model.
>
> I tuned it with GridSearchCV, scored on **recall**, not accuracy.
>
> The best settings used L1 regularisation. And something interesting happened — L1 shrank
> **ten of my twenty-four features to exactly zero**. The model chose its own features.
>
> Recall went from zero point four two, up to **zero point seven two**. Almost thirty points.
>
> In real numbers: the base model found five hundred fifty-three churners. The tuned model
> found **nine hundred forty-seven**. Almost four hundred more customers the bank can try to
> keep.
>
> On the right are the coefficients. The strongest by far is **balance drop percent**, at
> minus one point zero. It is negative because the further a balance falls, the higher the
> risk.

---

## SLIDE 9 — Model 2: Random Forest *(75 sec)*

> Model two is Random Forest. It builds many decision trees and averages their votes.
>
> The best settings were max depth six, and minimum twenty customers per leaf. Both are
> strong limits. By default a Random Forest grows until every leaf is pure, which means it
> memorises the training data. These limits force it to generalise.
>
> Recall went from zero point five nine to **zero point seven zero**.
>
> Now the right side is my favourite part of the project.
>
> These are the feature importances — what the model actually used.
>
> Number one is **balance drop percent**, at zero point three nine. **One feature drives
> thirty-nine percent of all the model's decisions** — more than twice the next one.
>
> And look at the origin column. **Four of the top five features are ones I built myself.**
> They did not exist in the original data.
>
> So this confirms my EDA finding, completely independently.

---

## SLIDE 10 — Model 3: XGBoost *(70 sec)*

> Model three is XGBoost. It also builds trees, but one after another — each tree fixes the
> mistakes of the one before it.
>
> XGBoost has no class weight setting. It uses **scale pos weight** instead, which does the
> same job. I set it to four point four.
>
> The best settings were a low learning rate with shallow trees — the normal recipe for
> boosting. Many small careful corrections work better than a few big ones.
>
> Recall went from zero point six two to **zero point seven zero**. This model gained least
> from tuning, but only because it started strongest.
>
> And most importantly — **the ROC-AUC is zero point eight four two. The highest of all ten
> models.**
>
> And again **balance drop percent** is the top feature — this time at almost fifty percent.
>
> Three different algorithms, all agreeing on the same feature.

---

## SLIDE 11 — Model Comparison & Best Model *(80 sec)*

> Now the comparison.
>
> At the top is the baseline. Eighty-one percent accuracy — but look at the recall. **Zero.**
> It found no churners at all. That is the number every model had to beat.
>
> Then my three tuned models. **All three met both targets.**
>
> So which is best?
>
> **XGBoost wins four of the five metrics.** Logistic Regression only wins recall, by zero
> point zero two.
>
> Is that difference important? Look at the bottom right.
>
> Logistic Regression catches nine hundred forty-seven churners. XGBoost catches nine hundred
> twenty. So Logistic Regression finds **twenty-seven more**.
>
> But Logistic Regression wastes one thousand and two calls. XGBoost wastes eight hundred
> sixty-three.
>
> So: twenty-seven more churners, for **one hundred thirty-nine more wasted calls.** A bad
> trade.
>
> And one more reason. The retention team gets a list **sorted by risk**, and works down it
> until they run out of time. ROC-AUC measures how good that sorting is — and XGBoost is best.
>
> **So my final model is XGBoost.**

---

## SLIDE 12 — Business Implications *(55 sec)*

> What does this mean for the bank?
>
> Before this project, the bank had no way to know who was leaving. A do-nothing model finds
> **zero** churners. My model finds about **seven out of every ten**.
>
> On the test set there were one thousand three hundred fifteen real churners. My model found
> nine hundred twenty.
>
> And it flagged about **twenty-five percent** of the customer base to contact.
>
> That matters. A quarter of the customers is a list a retention team can actually work
> through. It is realistic.
>
> On the right is how they would use it — score everyone monthly, rank by risk, send the top
> twenty-five percent to the team, then track who stays and retrain.
>
> And the simplest message from this whole project: **watch the rate of decline, not the
> balance level.**

---

## SLIDE 13 — Limitations & Improvements *(55 sec)*

> Now, honestly, the limitations.
>
> The dataset has no official source documentation. Everything indicates real bank data, but
> I could not formally verify it.
>
> I only have two months and two quarters per customer. A longer history would help.
>
> And most important — **I do not know why customers leave.** I have no data on complaints,
> competitor offers, or life events. I can only see the money moving.
>
> On the model side, my precision is about fifty percent — so about half the customers I flag
> would not have left. And I still miss thirty percent of the real churners.
>
> For improvements, the biggest would be a longer transaction history and customer service
> records.
>
> And the best improvement would be to find out **how much a saved customer is actually
> worth** — then I could tune the model on real money instead of a recall target.

---

## SLIDE 14 — Questions *(10 sec)*

> That is my project.
>
> Thank you for listening. I am happy to take any questions.

---

# Presenting tips

- **Practise with a timer.** If you finish at 13 minutes, that is perfect. You have 15.
- **Slides 5, 9 and 11 are your strongest moments.** Slow down on those three.
- **Do not read the slides.** The audience can read. Tell them the story.
- **Say the plain meaning first**, then the technical name — "money going out of the
  account" before "debits".
- If you are running late, **cut slide 6's data-quality bullets** and go straight to the
  correlation point. That saves about 30 seconds.

---

# Likely questions and answers

**"Why not use accuracy?"**
> "Because eighty-one percent of customers do not churn. A model that predicts nobody leaves
> is already eighty-one percent accurate, but it finds zero churners. It looks good and
> means nothing."

**"Why did you not delete the outliers?"**
> "In banking, the outlier is the high-value customer. If I delete the person with six
> million in their account, I delete exactly the customer the bank cannot afford to lose.
> So I transformed the data instead of deleting rows."

**"Your correlations are very weak."**
> "They looked weak because the money data is extremely skewed. One customer has almost six
> million, and that breaks the correlation calculation. After a log transform they became
> about five times stronger, and my engineered feature reached minus zero point three three."

**"Why Yeo-Johnson and not a log transform?"**
> "Because some balances are negative — those are real overdrafts. Log and Box-Cox cannot
> handle negative numbers. Yeo-Johnson can."

**"Why did you choose XGBoost when Logistic Regression had higher recall?"**
> "Because the difference was only twenty-seven customers, but it cost one hundred
> thirty-nine extra wasted calls. And XGBoost has the best ROC-AUC, which matters because
> the retention team works down a ranked list."

**"What is ROC-AUC?"**
> "It measures how well the model ranks customers by risk, across every possible cut-off
> point. Recall depends on where you set the threshold. ROC-AUC does not — so it tells you
> the quality of the model itself."

**"Why three models? Why not SVM or KNN?"**
> "I chose one model from each major family — a linear model, a bagging model, and a
> boosting model. That gives three genuinely different approaches, instead of three
> variations of the same idea."

**"What is frequency encoding?"**
> "Branch code has over three thousand values. I replaced each code with the number of
> customers in that branch. So instead of a meaningless ID number, the model sees the size
> of the branch."

**"How would you deploy this?"**
> "Score every customer once a month, rank them by probability, and send the top twenty-five
> percent to the retention team. Then track how many stay, and retrain the model as new data
> comes in."
