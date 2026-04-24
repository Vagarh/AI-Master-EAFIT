
## 2026-04-18 - [Strict Input Validation for External APIs]
**Vulnerability:** External API wrapper functions (`fetch_pdb_data` and `run_blast_search`) lacked strict input sanitization, exposing potential SSRF or injection vulnerabilities via malicious parameters to third-party endpoints.
**Learning:** This application wraps remote biological databases (NCBI BLAST and RCSB PDB) directly passing parameters to URLs and remote executors without validation. Without restricting inputs strictly to expected sets (e.g. alphanumeric IDs or valid sequence strings), untrusted input can manipulate endpoint calls.
**Prevention:** Apply strict Regular Expression validations over inputs before integrating them into API calls.

## 2024-05-24 - [Fix insecure file upload handling and DoS risk]
**Vulnerability:** The `read_any` file upload function lacked validation on file sizes, file extensions, and allowed uploading of binary files parsed as CSV (bypassing Pandas type checks due to lack of a null byte check).
**Learning:** External files read via pandas `read_csv` and `read_excel` functions need strict security checks to avoid excessive resource consumption (DoS) and potential arbitrary parsing of binaries as text.
**Prevention:** Always enforce file extension whitelists, check max file size bounds against a reasonable limit (like 25MB), and validate that text-like formats like CSV are free of unexpected null bytes (`\x00`).

## 2026-04-20 - [Multiple Security Enhancements]
**Vulnerability:** Found missing email format validation, a missing timeout on external API requests (DoS risk), and unsanitized parameters in an HTML anchor tag generation (XSS risk).
**Learning:** In applications using the Streamlit framework, helper functions that return HTML (like `create_download_link`) or interface with external resources must include proper sanitization (e.g. `html.escape`) and explicit configurations (e.g., `timeout=10` in `requests`). Furthermore, email wrappers need strict format checks to prevent injection attacks.
**Prevention:** Apply input sanitization when injecting variables into HTML strings, set timeouts on all network calls, and utilize RegEx for validating structured data like email addresses.

## 2026-04-24 - [Secure Subprocess Execution]
**Vulnerability:** The `run_command` utility in `Proyecto_Agente/setup.py` used `subprocess.run(..., shell=True)` which is a major command injection risk if arguments ever become unsanitized, and an anti-pattern.
**Learning:** Helper scripts often wrap `subprocess` with `shell=True` for convenience when passing string commands. When moving to `shell=False`, legacy string inputs must be split. `shlex.split()` safely converts these string commands to the required list format without breaking existing code.
**Prevention:** Default to `shell=False` for all `subprocess.run` calls, use list arguments, and prefer `sys.executable -m pip` to invoke module execution safely and reliably.
