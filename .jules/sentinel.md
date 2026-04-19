
## 2026-04-18 - [Strict Input Validation for External APIs]
**Vulnerability:** External API wrapper functions (`fetch_pdb_data` and `run_blast_search`) lacked strict input sanitization, exposing potential SSRF or injection vulnerabilities via malicious parameters to third-party endpoints.
**Learning:** This application wraps remote biological databases (NCBI BLAST and RCSB PDB) directly passing parameters to URLs and remote executors without validation. Without restricting inputs strictly to expected sets (e.g. alphanumeric IDs or valid sequence strings), untrusted input can manipulate endpoint calls.
**Prevention:** Apply strict Regular Expression validations over inputs before integrating them into API calls.

## 2024-05-24 - [Fix insecure file upload handling and DoS risk]
**Vulnerability:** The `read_any` file upload function lacked validation on file sizes, file extensions, and allowed uploading of binary files parsed as CSV (bypassing Pandas type checks due to lack of a null byte check).
**Learning:** External files read via pandas `read_csv` and `read_excel` functions need strict security checks to avoid excessive resource consumption (DoS) and potential arbitrary parsing of binaries as text.
**Prevention:** Always enforce file extension whitelists, check max file size bounds against a reasonable limit (like 25MB), and validate that text-like formats like CSV are free of unexpected null bytes (`\x00`).
