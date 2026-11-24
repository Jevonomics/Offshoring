# Offshoring & AI: supply-side check

Does the Anthropic "Working with AI" finding (US firms cutting offshore contractors) show up in BEA trade data and Indian IT vendor disclosures?

- Predictions: `hypotheses.md` (pre-registered) · Decisions: `DECISIONS.md` · **Results: `outputs/results.md`** · Validation: `outputs/validation.md` · Charts: `outputs/charts/`

## Rerun
```bash
python3 -m venv .venv && .venv/bin/pip install pandas numpy statsmodels matplotlib pdfplumber openpyxl requests python-dotenv lxml html5lib beautifulsoup4
echo "BEA_API_KEY=...\nBLS_API_KEY=..." > .env
# raw PDFs/XLSX are not committed: see data/raw/MANIFEST.md and data/raw/manual/NEEDED.md (TCS, Infosys need manual download)
for s in 01b_bea_pull 02_bea_build 03_h1_trend 03b_h1_robust 04a_tcs_extract 04b_techm_extract 04c_infosys_extract \
         04d_wipro_fetch 04e_wipro_extract_raw 04f_wipro_extract 04g_hcl_fetch 04h_hcl_extract 04i_ltim_fetch 04j_ltim_extract \
         05_build_panel 06_validate_panel 07_bls_pull 08_h5_bls 09_h6_rpe 10_h3_region 11_h4_hiring 12a_acn_fetch 12b_acn_extract 13_h2_exposure; do
  .venv/bin/python -I src/$s.py; done
```
