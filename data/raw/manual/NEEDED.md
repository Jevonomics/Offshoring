# Files to download by hand

tcs.com and infosys.com return HTTP 403 to every automated request (curl and the web-fetch tool). Please download these in a browser and save them into this folder (`data/raw/manual/`). Any file names are fine. Add a subfolder per firm if that helps.

## Round 1: finish the audit (small)
For each of **Q2 FY27 (Jul–Sep 2026), Q2 FY24, Q2 FY20, and Q1 FY16**:

**TCS**: https://www.tcs.com/investor-relations/financial-statements
- The quarterly **press release, USD / IFRS version**. The expected path, not verified, is `https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/{YYYY-YY}/q{N}/IFRS/Press%20Release%20-%20USD.pdf`
- The **TCS Data Sheet** (Excel), if it's offered. The latest copy may include history going back several years.

**Infosys**: https://www.infosys.com/investors/reports-filings/quarterly-results.html
- The quarterly **Fact sheet** (PDF or Excel), plus the **"Investor sheet"/metrics** file if it's separate.

## Round 2: full panel (only after Round 1 confirms which file has the data)
All quarters FY2016 Q1 → FY2027 Q2 of the same file type, for both firms.
