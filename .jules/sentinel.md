## 2026-04-17 - [Input Validation for Bioinformatics API Calls]
**Vulnerability:** The functions `fetch_pdb_data` and `run_blast_search` interacted with external APIs (NCBI and RCSB) but only performed length validation on user inputs (`pdb_id` and `sequence`), leaving them vulnerable to injection and SSRF through malformed or maliciously crafted strings.
**Learning:** In bioinformatics applications, seemingly innocuous inputs like protein sequences or database IDs can be used to construct external API requests. Relying solely on length checks is insufficient defense against SSRF or API injection attacks.
**Prevention:** Always implement strict, regex-based input allowlisting (e.g., alphanumeric only) for parameters that will be interpolated into external API requests.
