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
