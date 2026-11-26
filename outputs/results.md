# Results: does the supply side show US firms swapping offshore contractors for AI?

Run 2026-11-24. Predictions are pre-registered in `hypotheses.md` (commit 90009e9); judgment calls are in `DECISIONS.md`.
Post-period = calendar 2024 Q1 onward (robustness: 2023 Q1 onward). Pre-period trend = 2015–2022.
**Nothing here shows that AI caused anything.** The question is only whether the seller-side data fit the report's mechanism better than a general slowdown in demand.

## Bottom line

The data do **not** show the pattern the Anthropic report's mechanism predicts. Indian IT firms and US imports from India look like a **broad slowdown that then recovered**. They don't look like a targeted cut in the kinds of work AI replaces.

- US imports of computer and business services from India are **above** trend.
- "Exposed" work (outsourcing, BPO, managed services) has **not** fallen behind "unexposed" work (consulting, engineering).
- North American clients have **not** clearly pulled back relative to European ones.
- The one pattern that matches the report, firms holding back hiring rather than laying people off, is also exactly what an ordinary demand slowdown looks like.
- US IT-services jobs are falling well below trend while offshore imports hold up. That is the *opposite* of a shift from offshore contractors to in-house staff.

| | Hypothesis | Verdict | Key number |
|---|---|---|---|
| **Channel A** | H1 Imports fall below trend | **Contrary (India) / fragile (Philippines)** | India computer & business services +24% above trend in 2025, outside the 95% band. Philippines −30%, inside the band, and the sign flips with the trend window |
| | H2 Exposed work lags (**limited data**) | **No support; India trade data contrary** | Pooled vendor proxies: −0.4 pp, p = 0.83. Accenture managed services grew *faster* than consulting. India's exposed trade categories +34% above trend vs +11% for unexposed |
| | H3 North America lags Europe | **No support** | −3.8 log points, p = 0.65. Clean North America firms only: −15, p = 0.18. The 2025–26 drift (−9 in 2026) mostly disappears at a fixed euro rate (−2). TCS constant-currency gap moved *toward* North America |
| | H4 Hiring restraint, not layoffs | **Support, but not diagnostic** | All 20 post-2024 headcount declines outside TCS come from low hiring with normal or low attrition |
| | H5 Partial move in-house | **Contrary** | US computer systems design jobs −13% below trend (all 10 months of 2026 below the band) while India imports are above trend |
| **Channel B** | H6 Revenue per employee rises | **No support** | 0 of 5 firms above the 95% band in the main specification. Average gaps range from −7% (TechM) to +3% (TCS) |

---

## Channel A: clients replacing contractors

### H1. US imports from India and the Philippines vs. trend (BEA, annual, nominal)
*Chart 01. Files: `outputs/h1_trend_gaps.csv`, `outputs/h1_robustness.csv`.*

| 2025 gap vs trend, computer & business services | Trend fitted on 2015–22 (main) | 2015–21 | 2015–19 |
|---|---|---|---|
| India | **+24% (above band)** | +22% (above) | +4% (inside) |
| Philippines | −30% (inside) | −11% (inside) | +36% (inside) |
| All countries (benchmark) | +14% (inside) | +18% (above) | +22% (above) |

- **India:** above its own trend and above the benchmark in the main specification. That meets the pre-registered **contrary** criterion.
  - Caveat: with a pre-COVID trend (2015–19), India is on trend but trails the all-countries benchmark by about 18 points.
  - The result depends on the trend window, because India's computer services dipped in 2020–22 and then rebounded strongly (+42% from 2022 to 2025).
- **Philippines:** the result changes sign with the trend window, so it is **not robust**. Telecom/computer/information services are about 60% below trend.
  - But this drop coincides with a jump in Philippine "business and management consulting" in 2022 (+1.4 bn).
  - That looks like a **reclassification of call-center services between BEA categories**, not lost business.
  - Philippine total services imports are flat since 2022 (7.8 → 8.7 bn). IBPAP reports industry export revenue of **over $40 bn in 2025, up 5%**, with headcount up 4% to 1.9 million. In 2026 it cut its 2028 job forecast from 2.5M to 1.85–2.14M.
- Values are nominal, but the benchmark comparison cancels US-wide price effects. There are only two post-period years.

### H2. Exposed vs. unexposed work. **LIMITED:** no firm reports service lines after 2024, so this uses the three fallbacks the user approved
*Chart 03. Files: `outputs/h2_vendor_proxies.csv`, `outputs/h2_bea_by_type.csv`.*

Each line is "exposed growth minus unexposed growth" (percentage points, YoY). It compares the post-period with 2016–23 using Newey-West standard errors.

| Proxy | Before | After | Change | p |
|---|---|---|---|---|
| Accenture: Managed services − Consulting (local currency) | +1.2 | +3.5 | **+2.3** | 0.30 |
| TechM: BPS − software headcount | +9.5 | +6.9 | −2.6 | 0.52 |
| HCLTech: IT & Business Services − Engineering & R&D revenue | +0.6 | −0.3 | −0.9 | 0.78 |
| **Pooled (series fixed effects)** | | | **−0.4** | **0.83** |

- **Accenture**, the cleanest exposed/unexposed split available: its outsourcing-type work kept growing faster than consulting. The 2023–24 slump was in *consulting*, the unexposed side.
- **TechM and HCLTech:** small negative changes, nowhere near significant.
- **Robustness, without TechM:** software staff are arguably exposed too (software development is on the report's list), so TechM's pair compares two exposed kinds of work. Dropping it, the pooled change is **+0.88 pp (p = 0.66)**, so exposed work still did not fall behind.
- **BEA India by type:** exposed categories (computer services + accounting + legal) are **+34% above trend in 2025**, outside the band. Unexposed categories (R&D + engineering + management consulting) are +11% above. Exposed grew *faster*.
- **BEA Philippines:** exposed categories are far below trend and unexposed far above. Given the apparent 2022 reclassification, I don't treat this as evidence.
- Pre-registered verdict: **no support**. The BEA India split leans contrary.

### H3. North America vs. Europe
*Chart 04. Files: `outputs/h3_regression.csv`, `outputs/h3_currency_regression.csv`, `outputs/h3_currency_event_study.csv`, `outputs/h3_event_study.csv`, `outputs/h3_per_firm.csv`, `outputs/h3_tcs_constant_currency.csv`.*

- **Regression:** log(North America share ÷ Europe share) on `post`, with firm × definition fixed effects. This is equivalent to the pre-registered segment specification. Standard errors are clustered by firm (6 clusters).

| Specification | Coefficient (log pts) | p |
|---|---|---|
| Main (2024+) | −3.8 | 0.65 |
| Post from 2023 | −2.9 | 0.73 |
| Firm-specific trends | −4.7 | 0.27 |
| Clean "North America" firms only (TCS, Infosys, LTI/LTIM) | −15.0 | 0.18 |

- **Event study:** the coefficients drift negative in 2025 (−4.9) and 2026 (−8.8), but every 95% interval includes zero.
- **Per firm:** 5 of 6 firms show North America growing more slowly than Europe after 2024 than before. HCLTech is the exception.
- **Currency confounds this.** The dollar weakened in 2025, which mechanically raises Europe's US$ revenue. TCS reports constant-currency growth by region, which removes that effect: North America's gap vs. Europe went from **−4.0 pp before to −1.5 pp after**, i.e. North America *improved*.
- **Fixed euro rate check** (`src/10b_h3_currency.py`; files `outputs/h3_currency_regression.csv`, `outputs/h3_currency_event_study.csv`). Europe revenue is converted at a constant euro–dollar rate (ECB reference rate, quarterly average). This assumes all Europe revenue is in euros. The firms don't report the euro/pound/other split, and the pound rose less than the euro in 2025, so this may over-correct.

| Event study, log pts vs 2023 | Reported US$ | Half in euros | All in euros |
|---|---|---|---|
| 2025 | −4.9 | −2.8 | −0.8 |
| 2026 | −8.8 | −5.4 | −2.0 |

  - The 2025–26 drift mostly disappears: it lines up with the euro's rise from about $1.05 (2025 Q1) to $1.17 (2025 Q3).
  - The post-2024 average barely moves (−3.8, p = 0.66; clean North America firms −14.6, p = 0.22). At a fixed rate the pre-period years sit *above* 2023 (+3 to +8), so the decline vs. the 2015–22 average comes mainly from 2021–22, before AI coding tools spread.
- Verdict: **no support.** The 2025–26 drift is mostly the exchange rate, and the currency-neutral checks (TCS's own figures and the fixed euro rate) don't show North America falling behind after 2024.

### H4. Hiring restraint vs. layoffs
*Chart 05. Files: `outputs/h4_quarter_classification.csv`, `outputs/h4_period_summary.csv`. Layoff dates: `data/processed/layoff_events.csv`.*

- **Method:** hires are backed out as net change + attrition × average headcount ÷ 4.
- **Classification:** of 24 post-2024 firm-quarters with falling headcount, 20 come from **low hiring with normal or low attrition**. 2 fall in TCS's announced layoff window (≈12,261 people, Jul 2025–Mar 2026, which TCS attributed to "skill mismatch"). 2 are TCS quarters with high attrition, close to its restructuring.
- **Annualized rates, average of 6 firms:**

| Rate | 2016–19 | 2021–22 boom | 2024+ |
|---|---|---|---|
| Hiring | ≈23% | ≈36% | ≈14% |
| Attrition | ≈17% | ≈20% | ≈13% |

  Both fell. Hiring fell more, so headcount is roughly flat.
- **HCLTech fresh-graduate hires:** 26.7k (FY23) → 12.1k (FY24) → 7.8k (FY25) → 11.7k (FY26).
- Verdict: **support, as pre-registered.** But a falling quit rate plus a hiring freeze is also the textbook response to weak demand, so this doesn't separate AI from a slowdown.

### H5. US IT-services jobs (BLS CES, monthly, seasonally adjusted)
*Chart 08. Files: `outputs/h5_bls_gaps.csv`, `outputs/h5_robustness.csv`.*

- **Computer systems design and related services (NAICS 5415):** −5% below trend in 2024, −9% in 2025, **−13% in 2026**. Every month since January 2024 is below the 95% band. The same holds with a pre-COVID trend (−14%).
- **Comparisons:**
  - All professional, scientific and technical services: −4%.
  - Total nonfarm employment: +4% vs. its 2015–22 trend, or −6% vs. 2015–19.
- Verdict: **contrary.** US IT jobs are falling behind trend while India imports are above trend. The report's in-house story predicts the reverse.
- If anything, this fits AI, or a demand shift, hitting **US-based** IT services employment more than offshore delivery.

## Channel B: vendors' own productivity

### H6. Revenue per employee (annualized US$ revenue ÷ average headcount)
*Charts 06 and 07. Files: `outputs/h6_rpe_gaps.csv`, `outputs/h6_decomposition.csv`.*

Average gap vs. trend, 2024 onward:

| Firm | Main (FY16–22) | Excluding the 2021–22 hiring boom | Trend from 2019 |
|---|---|---|---|
| TCS | +3.0% | +1.0% | +11.8% |
| Infosys | −0.7% | +2.0% | −5.2% |
| Wipro | +1.4% | +9.2% | −2.4% |
| HCLTech | −3.6% | −14.4% | +20.1% |
| TechM | −7.3% | −4.1% | −11.8% |

- **Main specification:** no firm is above the 95% band, and results flip sign across trend windows.
- **Decomposition** (TCS, Infosys, HCLTech and TechM combined):
  - Revenue growth fell from about 8% a year before COVID to 2–3.5% in FY24–FY26.
  - Revenue per employee grew 2.5–6% a year in FY24–26. That mostly unwinds the FY21–22 over-hiring, when it fell about 5% a year.
  - So headcount growth went to about zero.
- Verdict: **no support.** Productivity recovered to trend; it did not break above it.

---

## Data quality and caveats

- **Xpheno vs. company reports:** Xpheno says six-firm headcount fell 3% (Oct 2025–Oct 2026). The firms' own reports sum to about 1.64M and show **+0.7%** (Sep 2025–Sep 2026). Xpheno's level is about half the firms' totals, so it must measure something narrower. Its method is unverified. See `outputs/validation.md`.
- **Indian GCCs** (companies' own offices in India): NASSCOM-Zinnov puts their headcount at 2.36M in FY26, up from about 1.9M in FY24, with revenue of $98.4bn.
  - This is a plausible destination for work that would once have gone to vendors. Some "in-house" substitution may be happening *in India*, not in the US.
  - BEA doesn't split affiliated vs. unaffiliated imports by country for these services, so it can't be measured here. See `data/processed/context_sources.csv`.
- **Deviations from the pre-registration** (logged in DECISIONS.md):
  - H6 uses US$ revenue, not constant currency. A constant-currency level series isn't available for all firms, and most revenue is billed in US$.
  - H2 relies entirely on fallbacks.
  - H3 standard errors use 6 clusters, so treat the p-values as rough.
- **Few post-period years:** BEA has only 2 annual post-period observations (2024–25).
- **Data fixes made along the way:**
  - TechM's datasheet has an FY16 row offset.
  - Some HCLTech segment-margin tables shared labels with share tables. They are now screened by a sum-to-100 rule.
  - HCLTech's 2024 region scheme is kept separate from the old one.
