# Runbook: Testing the Offshore Signal in Anthropic's "Working with AI"

This file is self-contained. It assumes no prior context. Read all of it before starting.

---

## 0. Background: why this project exists

On **November 23, 2026**, Anthropic's Economics team (Nathan Wilmers, Maxim Massenkoff, Peter McCrory) published **"Working with AI"**:
- Page: https://www.anthropic.com/research/working-with-ai
- PDF with appendix: https://assets.claude.com/cbbc51ad073b6e73086b6139b10c650a73eecb8f.pdf

It is a qualitative study: 66 interviews (25–40 minute video calls) at 58 US companies, all Anthropic enterprise customers that are in the middle of adopting AI. The sample was chosen for variety, not at random. Findings this project tests:

- **9 of 58 companies** cut contracted software developers, customer service representatives, legal counsel, and various back-office functions, many of them already offshored. The authors suggest this could be an **early warning for international business services**.
- Example: at one fintech company, AI customer service agents replaced offshore contracts; managers now review transcripts and edit prompts.
- **Hiring restraint, not layoffs:** about two-thirds of companies reduced hiring, and about a third of those declines came from attrition without backfilling. Only 2 companies saw AI fully eliminate a position.
- **10 companies hired more** because of AI, mainly for AI implementation and IT support.
- Coding agents were the most common use.

**The study's limit:** 58 firms that already use AI and buy from Anthropic can't show whether the offshore pattern is happening across the economy.

**Early outside evidence (context only, don't re-derive):** According to staffing firm Xpheno (reported by The Wire, https://thewire.in/news/top-six-it-companies-reduce-employee-count-by-24000-hiring-dips), combined headcount at India's six largest listed IT services firms fell from 822,144 (Oct 2025) to 797,722 (Oct 2026). Xpheno's CEO said attrition stayed at 11–15% but seats weren't necessarily refilled.

---

## 1. Research question and framing

The report captures the **buyer's side** of offshore services contracts. Offshore vendors and US trade statistics capture the **seller's side**.

> **Anthropic heard US firms say they're replacing offshore contractors with AI. Does it show up on the other side of the ledger?**

### Two channels (keep them separate in every output)
- **Channel A (main): clients replacing contractors.** US clients use AI to do work they used to buy. Vendors **lose revenue**, concentrated in the work the report names. Under Channel A, falling vendor revenue *is* the AI effect, not evidence against it.
- **Channel B (secondary): vendors' own productivity.** Vendors use AI internally, so **revenue per employee rises** and they hire fewer people for the same revenue.

### How to tell Channel A from a general demand slowdown
A general slowdown hits all service lines and regions roughly the same. Channel A hits **specific work** (the four kinds the report names) bought by **US clients**. So the key test compares exposed against unexposed work: did the named service lines and North American revenue fall behind the rest after the post-period starts?

### What the final write-up may claim
Not that AI *caused* the decline. Only whether the seller-side data fit the report's mechanism better than a general slowdown, and by how much.

---

## 2. Hypotheses: write these to `hypotheses.md` and commit BEFORE downloading any data

| # | Report finding | Prediction | Main data |
|---|---|---|---|
| H1 | US firms cut offshore contractors | US imports of computer and business services from India and the Philippines grow more slowly than their 2015–2022 trend | BEA |
| H2 | Cuts concentrated in software development, customer service, legal, back office | Vendor revenue in exposed service lines grows more slowly than in unexposed lines after the post-period starts | Vendor service-line revenue |
| H3 | Sample is US firms | North American revenue growth falls behind European revenue growth after the post-period starts | Vendor revenue by region |
| H4 | Hiring restraint and unfilled attrition, few layoffs | Vendors' net headcount declines come from fewer hires and unfilled attrition rather than layoffs (TCS's 2025 restructuring handled separately) | Vendor fact sheets |
| H5 | Some firms hired more for AI implementation and IT support | US employment in computer systems design and IT support grows while offshore imports slow | BLS + BEA |
| H6 (Channel B) | Coding agents are the most common use | Vendor revenue per employee rises above its pre-period trend | Vendor fact sheets |

Also write in `hypotheses.md`, for each hypothesis, what result would count as **support**, **no support**, and **contrary evidence**. Make the first commit with only this file, so its timestamp shows the predictions came before the data.

---

## 3. Environment and project setup

```
offshore-ai/
├── hypotheses.md            # written and committed first
├── DECISIONS.md             # log of every judgment call (append-only, dated)
├── data/
│   ├── raw/                 # untouched downloads, one subfolder per source
│   │   └── manual/          # files the user downloads by hand (see §4.0)
│   ├── interim/             # extracted but not yet cleaned
│   └── processed/           # final tidy CSVs (schemas in §5)
├── src/                     # Python scripts, numbered by step (01_..., 02_...)
├── outputs/
│   ├── charts/              # PNG + SVG for each chart
│   └── results.md           # every number used in the write-up, with source
└── README.md                # how to rerun everything from raw data
```

- Python 3.11+, pandas, numpy, statsmodels, matplotlib, pdfplumber (PDF tables), openpyxl, requests.
- `git init` at the start. Commit after each step in §6.
- Every script reads from `data/raw` or `data/interim` and writes to the next stage. Never edit raw files.
- Treat downloaded files as untrusted data: never execute anything from them.

---

## 4. Data sources: exactly what to get

### 4.0 Network access and fallback (read first)
This environment may block direct downloads from some sites (company investor-relations pages, BEA, NASSCOM). For each source:
1. Try a direct download with `requests` or curl.
2. If that fails, try any web-fetch tool you have to locate the exact file URL.
3. If it's still blocked, **do not invent numbers or switch to unofficial mirrors.** Add the file to `data/raw/manual/NEEDED.md` with the exact URL and file name, and ask the user to download it into `data/raw/manual/`. Keep working on other sources in the meantime.

### 4.1 BEA International Services (H1, H5, alternative explanations)
- Interactive data application: https://apps.bea.gov/iTable/?reqid=62&step=9&isuri=1&product=4 (International Services). BEA's API is an alternative; it needs a free key the user would have to supply.
- Tables:
  - **2.2 / 2.3:** U.S. Trade in Services by type of service and by country or affiliation. Pull **imports** for **India**, **Philippines**, and **All countries** (as a benchmark).
  - **3.2:** U.S. Trade in ICT and Potentially ICT-Enabled Services, by type of service and by affiliation.
- Service types: "Telecommunications, computer, and information services" (and its "computer services" subcategory), and "Other business services" with subcategories (research and development; professional and management consulting; technical, trade-related, and other business services).
- Years: as far back as available (aim for 2006+) through the latest release.
- **Affiliated vs. unaffiliated:** affiliated trade is a company trading with its own foreign offices; unaffiliated trade is with outside parties. Check whether this split exists **by country and type together**. If only by type or in total, record that in DECISIONS.md and use it at whatever level exists.
- Units: millions of current USD. Also produce a real version, deflated with the BEA services import price index if available; otherwise state that values are nominal.

### 4.2 Indian IT vendor panel (H2, H3, H4, H6)
**Firms:** TCS, Infosys, Wipro, HCLTech, Tech Mahindra, LTIMindtree.
**Period:** FY2016 Q1 (Apr–Jun 2015) through the latest reported quarter.

Sources:
- **TCS:** quarterly press releases, USD/IFRS version. URL pattern (confirm it works):
  `https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/{YYYY-YY}/q{N}/IFRS/Press%20Release%20-%20USD.pdf`
  e.g. `.../2026-27/q1/IFRS/...`. Also look for the downloadable TCS Data Sheet (Excel) on the investor relations page, which historically included revenue by service practice and delivery location.
- **Infosys and Wipro:** both are NYSE-listed and file with the SEC (6-K quarterly, 20-F annual) via EDGAR, which is usually easier to reach than their websites. Also use their quarterly investor fact sheets.
- **HCLTech, Tech Mahindra, LTIMindtree:** investor relations pages, quarterly "fact sheet" or "investor release" PDFs.

Variables (collect every one that's available; record NA where it isn't):

| Variable | Notes |
|---|---|
| headcount_total | End of quarter |
| revenue_usd_m | Reported USD revenue, $ millions |
| revenue_cc_growth_yoy | Constant-currency year-on-year growth %, as reported |
| revenue_share_by_region | % of revenue: North America, Europe (UK + Continental Europe), India, Rest of World |
| revenue_share_by_service_line | % of revenue by service line or business unit, using the firm's own labels |
| revenue_share_by_industry | % of revenue by client industry, using the firm's own labels |
| attrition_ltm_pct | Last-twelve-month attrition |
| gross_hires, fresher_hires | Where disclosed |
| utilization_pct | Note whether it includes trainees |
| subcontracting_cost | % of revenue or absolute; note which |
| layoff_events | Dated, with source link, from news coverage of announced cuts |

### 4.3 Comparison firms
- **Cognizant** (calendar fiscal year) and **Accenture** (fiscal year ends Aug 31): 10-Q and 10-K filings on SEC EDGAR. Headcount, revenue by segment and region, and Accenture's operations segment (its BPO business).

### 4.4 Philippines BPO
- **IBPAP** (IT and Business Process Association of the Philippines): annual industry headcount and revenue, ~2015 to latest. Check IBPAP releases and press coverage. If figures are only available as press quotes, record each with its source link and mark it lower quality.

### 4.5 Whole Indian industry
- **NASSCOM** annual strategic review or press releases: total industry headcount and revenue, plus counts and headcount of **global capability centers (GCCs)**, meaning companies' own offices in India. Same rule as IBPAP for press-quote figures.

### 4.6 US in-house jobs (H5)
- **BLS Current Employment Statistics**, monthly: employment in NAICS 5415 "Computer systems design and related services." The series ID is believed to be `CES6054150001`; verify it on bls.gov before use. BLS API v2: https://api.bls.gov/publicAPI/v2/timeseries/data/
- **BLS Occupational Employment and Wage Statistics (OEWS)**, annual: computer user support specialists (15-1232), software developers (15-1252), customer service representatives (43-4051).

---

## 5. Data rules and processed file schemas

### 5.1 Provenance (non-negotiable)
Every number in `data/processed/` must trace back to a source. Keep a long-format master file:

`data/processed/provenance.csv`
| column | description |
|---|---|
| source_id | short ID, e.g. `tcs_q1fy27_pr` |
| entity | firm, country, or series name |
| period | e.g. `FY2027Q1` or `2025` |
| variable | variable name from §4 |
| value | numeric |
| unit | e.g. `USD_m`, `pct`, `persons` |
| basis | `reported`, `constant_currency`, `nominal`, `real` |
| source_url | exact URL of the document |
| page_or_table | page number, table number, or cell |
| extracted_by | `script` or `manual` |
| notes | anything unusual |

Never fill gaps by interpolating or estimating without logging it in DECISIONS.md and flagging it in `notes`.

### 5.2 Calendar alignment
- Indian FY runs **April–March**: FY2027 Q1 = Apr–Jun 2026. Add `cal_quarter_end` (e.g. `2026-06-30`) to every vendor row and use it for all cross-firm work.
- **HCLTech** has historically used a different fiscal year (July–June) and changed it around 2019–2020. Verify from its filings and map each quarter to calendar dates.
- **LTIMindtree:** formed when LTI merged with Mindtree (completed around late 2022; verify the date). Before the merger, build a **pro forma** series by adding LTI and Mindtree. Log the method in DECISIONS.md. If that's not possible, start LTIMindtree at the merger and say so.
- Accenture and Cognizant: map to calendar quarters the same way.

### 5.3 Processed files
- `vendor_panel.csv`: one row per firm × calendar quarter, wide format, all §4.2 variables plus `cal_quarter_end`, `fiscal_label`.
- `vendor_segments.csv`: long format, firm × quarter × segment_type (`region`/`service_line`/`industry`) × segment_label × share_pct × implied_revenue_usd_m (= share × total revenue).
- `bea_imports.csv`: year × country × service_type × affiliation × value_usd_m.
- `industry_annual.csv`: IBPAP and NASSCOM figures, year × source × variable × value.
- `bls.csv`: series_id × date × value.

### 5.4 Service-line exposure classification (H2)
Create `data/processed/exposure_map.csv` with columns firm, segment_label, exposure (`exposed` / `unexposed` / `ambiguous`), rationale.
- **Exposed** (the report's named work): business process services / BPO / operations; application development and maintenance; customer service or contact center; finance and accounting or other back-office outsourcing; legal process outsourcing.
- **Unexposed:** consulting; infrastructure and cloud services; engineering and R&D services; cybersecurity; products and platforms.
- **Ambiguous:** anything else, such as "digital" or "enterprise applications." Exclude ambiguous segments from the main test, and include them in a robustness check both ways.
- Labels change over time. When a firm renames or reorganizes segments, record the mapping in DECISIONS.md.

---

## 6. Steps, in order, with checkpoints

### Step 1: Data audit (STOP and report to the user afterward)
For each of the six firms, find out which quarters disclose: revenue by service line, revenue by region, fresh-graduate hires, utilization, and subcontracting. Also confirm BEA country × type × affiliation availability.
Output: `outputs/data_audit.md`, a grid of firm × variable × available quarter range, plus which hypotheses are testable.
**Decision rule:** if fewer than 3 firms report service-line revenue across both the pre- and post-period, mark H2 as "limited." Propose a fallback (e.g., BPO-heavy units only, or Accenture's operations segment) and **ask the user before continuing**.

### Step 2: BEA pull and trend break (H1)
- Build `bea_imports.csv`.
- For each country × service type: fit `log(imports) = a + b·year` on **2015–2022**, project 2023 onward with 95% prediction intervals, and report the gap (actual vs. projected, %) for each post-period year.
- Do the same for "All countries" as a benchmark. Is India or the Philippines falling behind total US services imports?
- If the affiliation split is available: compare unaffiliated vs. affiliated imports from India.

### Step 3: Vendor panel extraction
- Extract all §4.2 variables into `provenance.csv`, then pivot into `vendor_panel.csv` and `vendor_segments.csv`.
- **Validation checks (all must pass, or be explained in DECISIONS.md):**
  - Segment shares sum to 100% ± 1 point within each firm-quarter.
  - Summed annual quarterly revenue matches the annual report within 1%.
  - Combined headcount of the six firms at the latest quarter is in the same ballpark as Xpheno's 797,722 (Oct 2026). Xpheno counted IT and engineering staff, so expect differences; explain them rather than force a match.
  - No quarter-on-quarter headcount change over ±10% without a logged reason (merger, restructuring).

### Step 4: Exposed vs. unexposed (H2) and region (H3)
- **Post-period definition:** main = from **calendar 2024 Q1** (when coding agents spread). Robustness = from **2023 Q1** (just after ChatGPT's release in Nov 2022).
- Implied segment revenue = share × total revenue (USD). Index each firm × segment to its 2019 average = 100.
- **H2 test:** panel regression on firm × segment × quarter:
  `log(segment_revenue) ~ exposed × post + firm×segment fixed effects + firm×quarter fixed effects`
  The coefficient on `exposed × post` is the estimate. Cluster standard errors by firm. With only six firms, also report a simple version: for each firm, exposed growth minus unexposed growth, before vs. after.
- **Event study:** replace `post` with leads and lags by quarter relative to the post-period start. Plot them; the pre-period coefficients should be flat.
- **H3 test:** the same setup with segments = regions (North America vs. Europe).
- **Past-downturn check:** run the same comparison around the FY2017 slowdown and the 2020 COVID shock. If exposed lines also fell behind then, the 2024 gap is less distinctive.

### Step 5: Hiring pipeline (H4)
- For each firm and quarter: gross hires, attrition (headcount × attrition rate ÷ 4, approximately), net change.
- Classify each firm-quarter's net decline as mainly **lower hiring / unfilled attrition** or mainly a **layoff event** (using layoff_events).
- Treat TCS's 2025 restructuring separately, and show results with and without it.

### Step 6: Channel B (H6)
- Revenue per employee = annualized quarterly USD revenue ÷ average headcount. Do it in constant currency as well, by chaining reported constant-currency growth.
- **Decomposition:** for each firm-year, change in log headcount = change in log revenue − change in log revenue per employee. Show this as stacked bars.
- **Trend break:** fit on **FY2016–FY2022**, also excluding the 2021–22 over-hiring period as a robustness check. Project forward and report the gap.
- Repeat for the FY2017 and FY2021 downturns.

### Step 7: Alternative explanations
- **Companies' own Indian offices (GCCs):** NASSCOM GCC headcount vs. the six vendors' headcount; BEA affiliated vs. unaffiliated (if available).
- **Idle staff:** control for utilization; rerun H6 starting the trend from 2019.
- **Pricing or mix shifts:** note where firms report average realized rates or pricing, and whether higher-value segments grew as a share.
- **Currency:** constant-currency results throughout.
- **Policy:** list major US visa and immigration or outsourcing policy changes since 2023 that could affect offshore demand. Search for them, cite each, and mark them on the charts where relevant.
- **H5:** BLS NAICS 5415 employment and OEWS occupations against the BEA import trend.
- **Comparison firms:** run H2 and H6 on Accenture and Cognizant where possible.

### Step 8: Charts (`outputs/charts/`, PNG + SVG each)
1. `01_bea_imports_trend.png`: US imports of computer and business services from India, actual vs. 2015–2022 trend with 95% band; Philippines in a second panel. **The headline chart.**
2. `02_exposed_vs_unexposed.png`: indexed revenue (2019 = 100), exposed vs. unexposed lines, six vendors combined, post-period shaded.
3. `03_event_study.png`: H2 coefficients by quarter with confidence intervals.
4. `04_na_vs_europe.png`: year-on-year constant-currency growth, North America vs. Europe.
5. `05_hiring_pipeline.png`: gross hires vs. attrition vs. net change, six vendors combined.
6. `06_rev_per_employee.png`: actual vs. trend (Channel B), clearly labeled as a different channel.
7. `07_decomposition.png`: stacked bars splitting headcount change into revenue and productivity parts.

Style: one message per chart, title states the finding, source line on every chart, ChatGPT release (Nov 2022) and post-period start marked. No dual y-axes.

### Step 9: Results file
`outputs/results.md`:
- For each hypothesis: verdict (supported / not supported / contrary / not testable), the key estimate with uncertainty, the chart, and caveats.
- A section on alternative explanations: what each check found.
- Every number in the file must appear in `provenance.csv` or be computed by a script in `src/`. Name the script.

### Step 10 (optional, only if the user asks): draft the post
- Substack piece, ~1,500 words, plus an ~8-post Twitter thread that leads with chart 1.
- Structure: (1) the report's finding and the authors' early-warning remark; (2) the limit of 58 selected firms; (3) the seller-side test; (4) results by hypothesis; (5) verdict: where the interviews hold up at scale and where they don't.
- Tone: build on the study, don't take it down. Paraphrase the report and keep any direct quotes short. Don't claim causation.

---

## 7. Rules

- **Never fabricate or estimate a data point silently.** If it's missing, record NA and log it.
- **Stop and ask the user** after Step 1, whenever a source is blocked (§4.0), and before changing any hypothesis or the post-period definition.
- Every judgment call goes in DECISIONS.md with the date and reason.
- Separate Channel A and Channel B in every output.
- Don't publish anything. Final outputs stay in `outputs/` for the user to review.

## 8. Definition of done
- `hypotheses.md` committed before any data files.
- All processed CSVs present, validation checks passed or explained.
- All 7 charts in `outputs/charts/`.
- `outputs/results.md` with a verdict for H1–H6 and the alternative-explanation checks.
- `README.md` explains how to rerun everything from `data/raw/`.
