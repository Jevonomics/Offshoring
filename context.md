# Research Plan: Does the Offshore Signal in Anthropic's "Working with AI" Show Up at Scale?

## 1. Background

On November 23, 2026, Anthropic's Economics team (Nathan Wilmers, Maxim Massenkoff, Peter McCrory) published "Working with AI," a qualitative study based on 66 interviews (25–40 minute video calls) at 58 US companies, all Anthropic enterprise customers that are in the middle of adopting AI. Findings relevant here:

- **Offshore contractor cuts:** 9 of the 58 companies cut contracted software developers, customer service representatives, legal counsel, and various back-office functions, many of them already offshored. The authors suggest this could be an early warning for international business services.
- **Example:** At one fintech company, AI customer service agents replaced offshore contracts; managers now review transcripts and edit prompts.
- **Hiring restraint, not layoffs:** About two-thirds of companies reported reduced hiring, and about a third of those declines came from attrition without backfilling. Only 2 companies saw AI fully eliminate a position, and 5 pushed out employees who would not adopt AI.
- **Some work moved in-house:** 10 companies hired more because of AI, mainly for AI implementation and IT support.
- **Main use:** Coding agents were the most common use.

**The limitation this project addresses:** The sample was chosen for variety, not at random, and contains only firms that are already adopting AI and are Anthropic customers. It cannot say whether the offshore pattern is happening across the economy.

**Early outside evidence:** According to staffing firm Xpheno, combined headcount at India's six largest listed IT services firms fell nearly 3%, from 822,144 (Oct 2025) to 797,722 (Oct 2026). Xpheno's CEO said attrition stayed at 11–15% but firms haven't necessarily refilled those seats. Tech Mahindra's headcount fell in one quarter even as its deal volumes improved.

## 2. Research question

The report captures the **buyer's side** of offshore services contracts. Offshore vendors and trade data capture the **seller's side**. If US firms are replacing offshore contractors with AI at scale, it should show up there.

> **Anthropic heard US firms say they're replacing offshore contractors with AI. Does it show up on the supply side?**

## 3. Two channels (keep them separate)

- **Channel A: clients replacing contractors (the report's mechanism, main focus).** US clients use AI to do work they used to buy. Offshore vendors **lose revenue**, concentrated in the work the report names.
- **Channel B: vendors' own productivity (secondary).** Vendors use coding agents themselves, so **revenue per employee rises** and they hire fewer people for the same revenue. The report does not describe this directly.

Important: under Channel A, falling vendor revenue *is* the AI effect, not evidence against it. Section 6 explains how to tell it apart from a general demand slowdown.

## 4. Hypotheses (publish before looking at the data)

| # | Report finding | Prediction | Main data |
|---|---|---|---|
| H1 | US firms cut offshore contractors | US imports of computer and business services from India and the Philippines grow more slowly than their pre-2023 trend | BEA |
| H2 | Cuts concentrated in software development, customer service, legal, back office | Vendor revenue slows most in BPO, application development and maintenance, and back office, compared with consulting and infrastructure | Vendor service-line revenue |
| H3 | Sample is US firms | Revenue from North American clients weakens more than revenue from European clients | Vendor revenue by region |
| H4 | Hiring restraint and unfilled attrition, few layoffs | Vendors show fewer fresh-graduate hires and unfilled attrition rather than mass layoffs (TCS's 2025 restructuring handled separately) | Vendor fact sheets |
| H5 | Some firms hired more for AI implementation and IT support | US IT and support jobs grow while offshore imports slow (partial move in-house) | BLS + BEA |
| H6 (Channel B) | Coding agents are the most common use | Vendor revenue per employee rises above its 2015–2022 trend | Vendor fact sheets |

## 5. Data

### 5.1 Trade data: main test (H1, H5)
**BEA International Services tables** (annual by country, ~2010 to latest)
- Tables 2.1–2.4: US imports by type of service and trading partner, for India and the Philippines. Categories: "telecommunications, computer, and information services" and "other business services" (with subcategories such as management consulting and back-office services).
- Table 3.2: ICT and potentially ICT-enabled services (services that can be delivered remotely), by type of service and by affiliation.
- **Shows:** whether US companies are buying less offshore IT and business services. This is the seller-side test of the report's contractor cuts.
- **Affiliated vs. unaffiliated:** affiliated trade is work a company's own foreign office does for its parent; unaffiliated is work bought from outside vendors. This split separates AI replacing contractors from work moving into companies' own offices abroad. **Gap:** the split may only be published in total or by type of service, not by country and type together. Confirm on day 1.
- **Limit:** country detail is annual, so there are only 2–3 data points after AI adoption took off.

### 5.2 Indian IT vendor quarterly panel (H2, H3, H4, H6)
**Firms:** TCS, Infosys, Wipro, HCLTech, Tech Mahindra, LTIMindtree
**Sources:** quarterly press releases (USD versions), investor fact sheets, TCS's downloadable data sheet. FY2016 to latest (~40 quarters per firm).

| Variable | What it shows | Tests |
|---|---|---|
| Total headcount | Size of the offshore workforce | H4, H6 |
| Revenue (USD and constant-currency growth) | Whether clients are buying less, with currency swings removed | H1–H3 |
| Revenue by region | Whether US clients are pulling back more than European ones | H3 |
| Revenue by service line or business unit | Whether the work the report names (software development and maintenance, customer service/BPO, back office) is shrinking faster than consulting and infrastructure | H2 |
| Revenue by client industry | Secondary exposure check (e.g., BFSI vs. manufacturing) | H2 |
| Attrition rate | How many people leave each year | H4 |
| Fresh-graduate hires and gross hires | Whether firms are filling seats that open up | H4 |
| Utilization rate | Share of staff billed to clients; controls for cutting idle staff after the 2021–22 over-hiring | Alternative explanation |
| Subcontracting costs | Whether vendors are cutting their own contractors | H4 |
| Layoff announcements | Separates one-off restructurings (e.g., TCS's ~2% cut) from steady hiring restraint | H4 |

**Computed:** revenue per employee (H6); the headcount change split into revenue and productivity parts; exposed vs. unexposed service-line comparisons.
**Gap (biggest risk to H2):** reporting by service line is inconsistent. TCS's current releases report industry and geography; its older data sheets also reported service practice. Some firms may have stopped reporting service lines or changed definitions. Check first; if it's missing, use BPO-heavy firms or units as stand-ins.

### 5.3 Comparison firms
**Cognizant and Accenture 10-Qs and 10-Ks (SEC EDGAR):** headcount, revenue by segment and region, and Accenture's operations segment (its BPO business).
- **Shows:** whether the pattern holds for US-listed firms with large Indian workforces. If it does, the explanation isn't specific to India.

### 5.4 Customer service work (H1, H2)
**IBPAP (Philippine IT-BPM industry association):** industry headcount and revenue, ~2015 to latest (annual).
- **Shows:** customer service is one of the report's named categories, and the Philippines is the largest offshore call-center market. Slowing growth there is the clearest sign of AI replacing contracted customer service.

### 5.5 Whole Indian industry (alternative explanation)
**NASSCOM:** total Indian tech industry headcount and revenue, plus the number of global capability centers (GCCs: companies' own offices in India) and how many people they employ.
- **Shows:** whether work is disappearing or just moving from vendors to companies' own Indian offices. Vendor headcount falling while GCC headcount rises points to in-house offices, not AI.

### 5.6 US in-house jobs (H5)
**BLS:**
- Current Employment Statistics: employment in computer systems design and related services (monthly).
- Occupational Employment and Wage Statistics: computer support specialists, software developers, customer service representatives (annual).
- **Shows:** whether some offshore work is coming back in-house. The report found 10 companies hiring more for AI implementation and IT support.

### 5.7 Already collected (context)
- Anthropic report and PDF: the findings being tested.
- Xpheno via The Wire: combined headcount of the six firms fell from 822,144 to 797,722 (Oct 2025 to Oct 2026).
- Business Today: Tech Mahindra's headcount fell while its deal volumes improved.

### 5.8 Collection order
1. Vendor service-line disclosures (decides whether H2 can be tested)
2. BEA country tables (headline chart)
3. Vendor quarterly panel: TCS first (downloadable data sheet), then Infosys (most detailed reporting)
4. NASSCOM and IBPAP
5. BLS, Cognizant, and Accenture

## 6. Analysis

**Channel A (main)**
1. **Trade trend break:** Fit a 2015–2022 trend to US imports from India and the Philippines, project it forward, and measure the gap since 2024.
2. **Exposed vs. unexposed work:** A general slowdown hits all service lines and regions roughly the same; AI replacement should hit the report's four named kinds of work and North American clients first. Compare indexed revenue growth by service line and by region, before and after 2024.
3. **Hiring pipeline:** Plot fresh-graduate hiring, attrition, and net headcount to test unfilled attrition directly.
4. **Move in-house:** Compare US IT and support jobs with offshore import growth.

**Channel B (secondary)**
5. **Split the headcount change:** headcount growth ≈ revenue growth − growth in revenue per employee, by firm and year, in constant currency.
6. **Revenue-per-employee trend break:** actual vs. projected from the 2015–2022 trend, with ChatGPT (Nov 2022) and coding agents (2024–25) marked.
7. **Compare with past downturns:** Repeat the analysis for FY2016–17 and FY2020. If revenue per employee also jumped in those downturns, today's jump is ordinary cost-cutting, not AI.

## 7. Alternative explanations to address

- **General demand slowdown (2023–24 tech budget cuts):** handled by the exposed vs. unexposed comparison (step 2).
- **Clients' own offices in India (global capability centers):** US firms moving work from vendors to their own Indian offices would cut vendor revenue without AI. Check NASSCOM whole-industry headcount and BEA's affiliated vs. unaffiliated split. Unaffiliated imports falling while affiliated imports rise suggests in-house offices, not AI.
- **Idle staff cuts after over-hiring in 2021–22:** use utilization rates and start trends from a 2019 baseline, not the 2022 peak.
- **Pricing and mix shifts:** moving to higher-value work raises revenue per employee without automation; partly controlled with service-line data.
- **Currency, visa, and trade policy:** constant-currency figures handle the currency effect; name relevant policy changes explicitly.

**What the post can claim:** not that AI *caused* the decline, but whether seller-side data fit the report's mechanism better than a general slowdown, and by how much.

## 8. Charts (4–5)

1. US imports of computer and business services from India: actual vs. pre-2023 trend (headline chart)
2. Vendor revenue, exposed vs. unexposed service lines, indexed (2019 = 100)
3. North America vs. Europe revenue growth across the six vendors
4. Fresh-graduate hires vs. attrition vs. net headcount
5. Revenue per employee vs. 2015–2022 trend (Channel B)

## 9. Post structure (Substack ~1,500 words; Twitter thread ~8 posts, chart 1 first)

1. The report's finding: 9 of 58 US firms are replacing offshore contractors with AI; the authors flag it as a possible early warning for international business services.
2. The limit: 58 selected firms that are already Anthropic customers can't show whether this is happening at scale.
3. The test: if it is, it shows up in trade data and vendor revenue, concentrated in the work the report names.
4. Results, one hypothesis at a time.
5. Verdict: where the interviews hold up at scale, and where they don't. Tone: build on the study, not a takedown.

## 10. Timeline

| Day | Work |
|---|---|
| 1 | Publish hypotheses; pull BEA data; build vendor quarterly panel |
| 2 | Trade trend break; exposed vs. unexposed comparison; draft charts |
| 3 | Hiring pipeline, move in-house, Channel B analysis; alternative explanations |
| 4 | Write post and thread |

## 11. Sources

- Anthropic, "Working with AI" (Nov 23, 2026): https://www.anthropic.com/research/working-with-ai
- Report PDF and appendix: https://assets.claude.com/cbbc51ad073b6e73086b6139b10c650a73eecb8f.pdf
- The Wire, on Xpheno headcount data: https://thewire.in/news/top-six-it-companies-reduce-employee-count-by-24000-hiring-dips
- Business Today, on Indian IT hiring: https://www.businesstoday.in/technology/news/story/indian-its-hiring-model-is-changingand-ai-is-the-reason-512582-2026-01-23
