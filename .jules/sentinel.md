
## 2026-04-18 - [Strict Input Validation for External APIs]
**Vulnerability:** External API wrapper functions (`fetch_pdb_data` and `run_blast_search`) lacked strict input sanitization, exposing potential SSRF or injection vulnerabilities via malicious parameters to third-party endpoints.
**Learning:** This application wraps remote biological databases (NCBI BLAST and RCSB PDB) directly passing parameters to URLs and remote executors without validation. Without restricting inputs strictly to expected sets (e.g. alphanumeric IDs or valid sequence strings), untrusted input can manipulate endpoint calls.
**Prevention:** Apply strict Regular Expression validations over inputs before integrating them into API calls.
