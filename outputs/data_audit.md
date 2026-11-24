# Step 1: Data Audit

Run 2026-11-24. This audit covers which data each source discloses and when. It doesn't analyze anything. Scripts are `src/01a`–`01h`. Raw files are listed in `data/raw/MANIFEST.md`.

Legend: ✅ verified from a downloaded document · ⚠️ partial or with caveats · ❌ not disclosed · ❓ not yet verified (source blocked or not checked)

## 1. Source access

| Source | Access | Route |
|---|---|---|
| BEA International Services | ✅ | API (`IntlServTrade`), key in `.env` |
| BLS CES / OEWS | ✅ | API v2. Series `CES6054150001` confirmed as "All employees, computer systems design and related services, SA", data through Oct 2026 |
| SEC EDGAR (Infosys, Wipro, Cognizant, Accenture) | ✅ | `data.sec.gov` and full-text search |
| Wipro (wipro.com) | ✅ | Datasheet PDFs at a predictable URL, Q3 FY23 onward. Earlier quarters are 6-K exhibits on EDGAR |
| Tech Mahindra | ✅ | A single Excel datasheet with **FY2016 Q1–FY2027 Q2** in one file, plus a PDF fact sheet archive |
| HCLTech | ✅ | Investor releases on the site for Q3 FY22–Q2 FY27. Earlier releases aren't linked from the results page and still need to be found |
| LTIMindtree (rebranded **LTM**, ltm.com) | ✅ | JSON document index covering FY2017–FY2027. Some older PDFs are scanned images and will need OCR. **Mindtree before the merger hasn't been checked yet** |
| **TCS** (tcs.com) | ❌ 403 | Blocked for curl and for the web-fetch tool. **Manual download needed** |
| **Infosys** (infosys.com) | ❌ 403 | Blocked for both. EDGAR 6-Ks have only the press release and Ind AS results (industry segments in ₹ crore). **The fact sheet must be downloaded manually** |
| NASSCOM, IBPAP | ❓ | Not checked yet. These come later in the collection order |

## 2. Vendor disclosure grid (Indian FY; FY27 Q2 = Jul–Sep 2026)

| Firm | Service-line revenue | Region revenue | Fresh-graduate hires | Utilization | Subcontracting | Headcount / attrition |
|---|---|---|---|---|---|---|
| **TCS** | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |
| **Infosys** | ❓ (fact sheet blocked) | ❓ | ❓ | ⚠️ in press-release text, e.g. Q1 FY16 "80.2% excl. trainees" | ❓ | ⚠️ attrition appears in press-release text |
| **Wipro** | ⚠️ **FY2016–Q2 FY21 only** ("Service Line Mix": Digital Operations & Platforms = BPO, Cloud & Infra, Data/Analytics/AI, etc.). Dropped after Oct 2020 → **no post-period data** | ⚠️ regions changed in FY21 to "Americas 1 / Americas 2 / Europe / APMEA" (Americas 1+2 ≈ Americas, not North America alone) | ❌ (only occasional mentions in press text) | ✅ net utilization excl. trainees | ❓ possibly in IFRS expense notes | ✅ headcount. ✅ voluntary LTM attrition (IT excl. BPS). ✅ BPS quarterly attrition, latest datasheets |
| **Tech Mahindra** | ❌ revenue. ⚠️ **headcount split: "Software professionals" vs "BPS professionals"**, FY16–FY27 | ⚠️ Americas / Europe / RoW (not North America alone) | ❌ | ✅ IT utilization, incl. and excl. trainees | ❌ | ✅ total, IT LTM attrition |
| **HCLTech** | ⚠️ segments **IT & Business Services / Engineering & R&D / HCLSoftware** (in place by FY20 Q4, still reported Q2 FY27). Older service lines (Applications / Infrastructure / BServ) existed earlier; when they stopped isn't confirmed | ⚠️ "Americas" (FY23); the latest release labels the region "USA". Label change to check | ✅ **freshers added**, net additions | ❓ | ❓ | ✅ LTM attrition (excludes involuntary attrition and BPO) |
| **LTIMindtree / LTM** | ⚠️ LTI only, **before the merger** ("Revenue by Service Offering": ADM & Testing, Enterprise Solutions, …). Not reported after the merger (FY24 on) → **no post-period data** | ✅ **North America** / Europe / RoW | ❌ | ✅ excl. trainees, plus onsite/offshore effort mix | ❌ | ✅ total employees, TTM attrition |

Other notes:
- **HCLTech fiscal year:** the latest documents use April–March quarters. When HCLTech switched from July–June still needs to be confirmed in Step 3.
- **LTIMindtree:** a pro forma series needs Mindtree's own disclosures before the merger. These haven't been located yet.
- **Industry mix:** every firm reports it, but labels were reclassified (TechM in FY22 and FY24, Wipro in FY21). Restated overlaps exist for TechM.

## 3. BEA availability

- **Years:** 1999–**2025** for country × type, which gives only **two post-period years (2024, 2025)** under the main definition, or three under the robustness definition.
- **India:** all types, computer services, other business services, professional and management consulting, technical/trade-related/other business, R&D, and digitally deliverable services. Most series are continuous from 2013. A few years are suppressed ("(D)"), e.g. India computer services 2012.
- **Philippines:** total and other business services are mostly complete. **Computer services are heavily suppressed** (9 of 27 years). Digitally deliverable services exist only for 2006–2012 and 2023–2025.
- **Affiliated vs. unaffiliated by country:** ❌. For India and the Philippines, BEA publishes the split only for *charges for the use of IP*, not for computer or business services. The split by type of service exists only for **All countries**. → The test separating companies' own Indian offices (GCCs) from outside vendors can't use BEA at country level. It has to rely on NASSCOM GCC figures. Logged in DECISIONS.md.

## 4. Which hypotheses can be tested

| Hyp. | Status | Why |
|---|---|---|
| H1 trade trend break | ✅ testable | Nominal, India strong. Philippines computer services weak because of suppression; use Philippines other business services and total. Only 2–3 post-period years |
| **H2 exposed vs. unexposed** | **⚠️ LIMITED (decision rule triggered)** | Of the 4 firms checked, **none** reports clean exposed/unexposed service-line revenue in both the pre- and post-period. Wipro stopped in 2020 and LTI stopped at the merger. HCLTech's IT & Business Services segment mixes applications, infrastructure, and BPO, so the exposure map marks it ambiguous. TCS and Infosys are unknown. Fewer than 3 firms → **limited** |
| H3 North America vs. Europe | ⚠️ testable with caveats | Only LTIMindtree reports North America on its own. TechM and HCLTech report "Americas" (mostly the US). Wipro's regions were redefined in FY21. TCS and Infosys are unknown |
| H4 hiring pipeline | ⚠️ partly testable | Only HCLTech reports fresh-graduate hires so far. Every firm gives headcount and attrition, so hiring can be backed out as Δheadcount + attrition × headcount ÷ 4. Layoff dates come from news coverage |
| H5 move in-house | ✅ testable | BLS verified. BEA as for H1 |
| H6 revenue per employee | ✅ testable for 4 firms now, 6 once TCS and Infosys arrive | USD revenue and headcount are present everywhere checked. A constant-currency series needs reported CC growth, which is available |

## 5. Decision needed (runbook §6 Step 1)

H2 meets the runbook's "limited" rule. Fallback options, in my order of preference:

1. **A combined exposure test from proxies.**
   - Tech Mahindra **BPS vs. software headcount** (FY16–FY27, continuous).
   - HCLTech **IT & Business Services vs. Engineering & R&D / HCLSoftware** revenue. ITBS would be treated as "mostly exposed", which is a judgment call to log.
   - Wipro's **BPS attrition** as supporting evidence.

   This is weaker than service-line revenue, but it covers both periods.
2. **Accenture's revenue by type of work** (Consulting vs. Managed Services, the latter including its Operations/BPO business), from 10-Ks and 10-Qs. Accenture is the cleanest single exposed/unexposed split available. It isn't an Indian vendor, but most of its staff are in India. *Not yet verified on EDGAR.*
3. **Shift the exposure test to the trade level.** Use the BEA India/Philippines breakdown by type of service: computer services and back-office "other business services" vs. R&D and consulting, plus the IBPAP Philippine contact-center series.
4. **Wait for TCS and Infosys fact sheets.** If either reports service lines in the post-period, H2 strengthens. I'm not counting on this.

My recommendation is **1 + 2 + 3 together**, with H2 labeled "limited" in the results. Continuing will also need the manual TCS and Infosys downloads listed in `data/raw/manual/NEEDED.md`.
