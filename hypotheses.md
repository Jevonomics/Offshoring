# Pre-registered Hypotheses

Written 2026-11-24, before any data was downloaded. This file is committed alone so that its timestamp shows the predictions came before the data.

**Question:** Anthropic heard US firms say they're replacing offshore contractors with AI ("Working with AI," Nov 23, 2026). Does it show up on the supply side?

**Channels**
- **Channel A (main): clients replace contractors.** US clients use AI for work they used to buy, so offshore vendors lose revenue, mostly in the work the report names. Under Channel A, falling vendor revenue *is* the AI effect.
- **Channel B (secondary): vendors' own productivity.** Vendors use AI themselves, so revenue per employee rises.

**Periods**
- Pre-period trend window: 2015–2022 (vendor fiscal years FY2016–FY2022).
- Post-period, main: from calendar 2024 Q1, when coding agents spread. For annual data, 2024 onward.
- Post-period, robustness: from calendar 2023 Q1, just after ChatGPT's release in Nov 2022.
- I will not change these definitions after seeing the data without first logging the change and the reason in DECISIONS.md.

**Exposed work** (named in the report): BPO and operations, application development and maintenance, customer service and contact centers, finance and accounting and other back-office work, legal process outsourcing.
**Unexposed work:** consulting, infrastructure and cloud, engineering and R&D, cybersecurity, products and platforms.

---

## H1: Trade trend break (Channel A)
**Report finding:** US firms cut offshore contractors.
**Prediction:** US imports of computer services and other business services from India and the Philippines grow more slowly than their 2015–2022 log-linear trend in the post-period. They also fall behind the same trend gap for US imports from all countries.
**Data:** BEA International Services.

- **Support:** In 2024 and later, actual imports from India and/or the Philippines fall below the projected trend, and at least one year falls outside the 95% prediction interval. The shortfall is larger than the all-countries benchmark's.
- **No support:** Actual imports stay within the 95% prediction interval, or the shortfall is no bigger than the all-countries benchmark's.
- **Contrary:** Imports from India and the Philippines run above trend, or above the benchmark, in the post-period.

## H2: Exposed vs. unexposed service lines (Channel A)
**Report finding:** The cuts were concentrated in software development, customer service, legal, and back-office work.
**Prediction:** After the post-period starts, vendor revenue in exposed service lines grows more slowly than in unexposed lines. The test is the coefficient on `exposed × post` < 0 in a regression with firm×segment and firm×quarter fixed effects.

- **Support:** The coefficient is negative and significant at 10% or better (standard errors clustered by firm, with caution given only six firms). The simple per-firm differences go the same way for most firms (at least 4 of 6, or a majority of the firms that report this data). The pre-period event-study coefficients are flat.
- **No support:** The coefficient is near zero or not significant, or the per-firm results are split.
- **Contrary:** The coefficient is significantly positive, meaning exposed lines grew faster than unexposed lines.
- **Diluted support:** If exposed lines fell behind by a similar amount in the FY2017 or 2020 downturns, a negative coefficient counts only as weak support.

## H3: North America vs. Europe (Channel A)
**Report finding:** The report's sample is US firms.
**Prediction:** After the post-period starts, vendor revenue growth from North American clients falls behind growth from European clients. This uses the same regression design as H2, with region in place of service line.

- **Support:** The `NorthAmerica × post` coefficient is negative and significant at 10% or better, and points the same way for most firms.
- **No support:** It is near zero or not significant.
- **Contrary:** North American revenue grows significantly faster than European revenue after the post-period starts.

## H4: Hiring restraint, not layoffs (Channel A)
**Report finding:** Firms showed hiring restraint and left attrition unfilled. There were few layoffs.
**Prediction:** Vendors' net headcount declines in the post-period come mainly from fewer gross and fresh-graduate hires against steady attrition, not from announced layoffs. TCS's 2025 restructuring is analyzed separately.

- **Support:** Most firm-quarters with declining headcount (excluding TCS's 2025 restructuring) are classified as lower hiring or unfilled attrition. Attrition stays near its usual range while hires fall.
- **No support:** Headcount is not declining, or there isn't enough hiring and attrition data to classify the declines.
- **Contrary:** Most of the declines come from dated layoff events.

## H5: Partial move in-house (Channel A)
**Report finding:** Some firms hired more because of AI, mainly for AI implementation and IT support.
**Prediction:** In the post-period, US employment in computer systems design (NAICS 5415) and in IT support occupations grows at or above its 2015–2022 trend while offshore imports fall behind trend (H1).

- **Support:** US IT and support jobs are at or above trend while imports from India and the Philippines are below trend.
- **No support:** Both US jobs and offshore imports are below trend, which looks like a general slowdown in demand.
- **Contrary:** US IT jobs fall behind trend while offshore imports hold up.

## H6: Vendor revenue per employee (Channel B)
**Report finding:** Coding agents were the most common use of AI.
**Prediction:** Vendor revenue per employee, in constant currency, rises above its FY2016–FY2022 trend in the post-period.

- **Support:** Revenue per employee is above trend, outside the 95% prediction interval, for most firms. The rise is larger than in the FY2017 and FY2021 downturns, and it holds up when the trend excludes the 2021–22 over-hiring period and when it starts from 2019.
- **No support:** Revenue per employee stays within the trend band, or the rise is no larger than in past downturns.
- **Contrary:** Revenue per employee falls below trend.

---

## What the write-up may claim
It cannot claim that AI *caused* any change. It can say only whether the seller-side data fit the report's mechanism better than a general slowdown in demand, and by how much.
