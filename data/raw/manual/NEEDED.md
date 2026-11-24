# Files to download by hand

tcs.com and infosys.com return HTTP 403 to every automated request (curl and the web-fetch tool). Please download these in a browser and save them into this folder (`data/raw/manual/`). Any file names are fine. Add a subfolder per firm if that helps.

## Round 1: finish the audit (small)
For each of **Q2 FY27 (Jul–Sep 2026), Q2 FY24, Q2 FY20, and Q1 FY16**:

**TCS: ✅ DONE.** The user supplied the cumulative Data Sheet (`TCS-Data-Sheet-Q2FY27.xlsx`, FY05–Q2 FY27). Nothing more is needed. Original request:
https://www.tcs.com/investor-relations/financial-statements
- The quarterly **press release, USD / IFRS version**. The expected path, not verified, is `https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/{YYYY-YY}/q{N}/IFRS/Press%20Release%20-%20USD.pdf`
- The **TCS Data Sheet** (Excel), if it's offered. The latest copy may include history going back several years.

**Infosys: Round 1 ✅ DONE** (`infosys_2015.pdf` = Q1 FY15, `infosys_2019.pdf` = Q2 FY19, `infosys_2024.pdf` = Q2 FY24, `infosys_2027.pdf` = Q2 FY27).
https://www.infosys.com/investors/reports-filings/quarterly-results.html
- The quarterly **Fact sheet** (PDF or Excel), plus the **"Investor sheet"/metrics** file if it's separate.

## Round 2: Infosys only. Fact sheet for **Q2 and Q4** of each fiscal year (each sheet also shows the previous quarter)
URL pattern: `https://www.infosys.com/investors/reports-filings/quarterly-results/{YYYY-YYYY}/q{N}/documents/fact-sheet.pdf`
Name them `infosys_q{N}fy{YY}.pdf`. Needed: Q2 and Q4 for FY16, FY17, FY18, FY19 (Q4 only), FY20, FY21, FY22, FY23, FY24 (Q4 only), FY25, FY26. That's about 20 files. If any URL doesn't work, skip it and tell me.
