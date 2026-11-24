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

| Layer | Source | Frequency | Variables |
|---|---|---|---|
| Trade flows (main test) | BEA International Services tables: US imports of telecommunications, computer, and information services and other business services, by country (India, Philippines); split by affiliated vs. unaffiliated trade if available | Annual by country; quarterly in total | Import values |
| Vendor panel | Quarterly fact sheets and investor releases: TCS, Infosys, Wipro, HCLTech, Tech Mahindra, LTIMindtree | Quarterly, FY2016 to latest | Headcount, USD and constant-currency revenue, revenue by region and service line, attrition, utilization, fresh-graduate hires, subcontracting costs |
| Comparison firms | Cognizant and Accenture 10-Qs | Quarterly | Same variables, where reported |
| Philippines BPO | IBPAP industry headcount and revenue | Annual | Customer service exposure |
| Whole industry | NASSCOM headcount | Annual | Catches movement from vendors to clients' own Indian offices |
| US in-house jobs | BLS (employment by occupation and industry, plus computer systems design industry employment) | Monthly / annual | Signs of work moving in-house |

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
