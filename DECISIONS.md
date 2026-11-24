# Decisions Log

This log is append-only. Each entry is dated and gives its reason.

## 2026-11-24

- **Repo layout:** The project lives in the repo root (user's choice), not in an `offshore-ai/` subfolder. Work happens on branch `analysis`, and nothing is pushed.
- **Secrets:** The BEA and BLS API keys are kept in `.env`, which is gitignored. Scripts load them with python-dotenv.
- **Raw binaries are not committed:** PDF and XLSX source documents (≈45 MB+) are gitignored. Each one is listed by URL in `data/raw/MANIFEST.md` and can be re-downloaded with the `src/` scripts. JSON API responses and SEC HTML exhibits *are* committed.
- **SEC User-Agent:** EDGAR requests use the generic `OffshoreAIResearch research-script admin@example.org`, not a personal email.
- **Python:** 3.15 in a local `.venv`, and scripts run with `python -I`.
- **BEA affiliation split:** For India and the Philippines, BEA publishes affiliated vs. unaffiliated only for charges for the use of IP. Computer and business services are split by affiliation only for All countries. So the BEA part of the GCC (companies' own offices) check can only run at the all-countries level, and the India-specific GCC check relies on NASSCOM.
- **BEA Philippines computer services:** 18 of 27 years are suppressed. For H1, use Philippines *other business services* and *all services* as the main series.
- **LTIMindtree is now "LTM":** ltimindtree.com redirects to ltm.com, and documents are branded LTM from FY27. It is treated as the same entity.
- **H2 "limited":** This meets the runbook's Step 1 decision rule (see `outputs/data_audit.md` §4–5). I am waiting for the user's choice of fallback before going further.
- **H2 fallback chosen by the user:** Use all three fallbacks together: (1) vendor proxies (TechM BPS vs. software headcount; HCLTech ITBS vs. ERS/HCLSoftware revenue, with ITBS treated as mostly exposed; Wipro BPS attrition as support), (2) Accenture's split by type of work, (3) BEA India/Philippines by type of service, plus IBPAP. H2 is labeled "limited" throughout. If the combined evidence is weak, the user will decide whether to drop H2 or re-evaluate it. No hypothesis or post-period definition changes.
- **TCS source:** The user-supplied cumulative Data Sheet (Q2 FY27 edition) is the single TCS source. It is treated as untrusted data and read only with openpyxl. TCS's service-practice split ends in FY2017, so it adds nothing to H2's post-period. It is strong for H3 (North America vs. UK/Continental Europe, FY13–FY27) and H6. TCS's attrition definition changes to voluntary-only from 2Q FY26. Mark that break in the data.
- **Infosys sample files:** The user's files are Q1 FY15, Q2 FY19, Q2 FY24, and Q2 FY27 (two differ from the quarters requested; fine for the audit). Infosys service offerings are gone by FY19. With all 6 firms audited, 0 have clean service-line revenue in the post-period, which confirms H2 is "limited". Plan: collect Infosys Q2 and Q4 fact sheets only, since each sheet also reports the previous quarter.
