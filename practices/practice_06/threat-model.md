# Threat Model: Mini Shop

Scope: local HTTP server, SQLite in-memory DB, disposable files inside Sandbox root. Clients: alice, bob (customers), staff (employee). LLM assistant suggests tools; server executes.

Assets:
- Customer PII in profiles table.
- Receipts in files/<user>/receipt.txt.
- Operator note private/operator-note.txt (must stay inaccessible over HTTP).
- Orders and prices.

Trust boundaries:
- HTTP client -> server.
- Server -> Sandbox file boundary.
- LLM assistant decision -> server executor.

Main threats and findings:
- T1 SQL injection via /profile and /search string interpolation.
- T2 IDOR: /profile trusts query id; /orders GET returns all; /files allows arbitrary user/path; /admin/export trusts X-Role.
- T3 Price tampering: /orders POST allows client-provided price.
- T4 XSS: /reviews/view renders unescaped HTML.
- T5 Assistant overreach: /assistant/execute tools lack auth; read private files, export profiles, delete tree by customers.
- T6 Prompt injection vector: reviews influence assistant; server must enforce auth regardless of model output.

Mitigations implemented:
- Parameterized SQL for /profile, /search.
- Session-based identity and roles; ignore client id; restrict GET /orders to own; server-side role check for admin/export.
- Server-enforced catalog price; ignore client price.
- Restrict /files to own files for customers; staff may specify; disallow private/.
- Escape reviews to prevent XSS.
- Authorize assistant tools by session; customers limited to own files; staff-only for export/delete.

Residual risks:
- Logs may contain headers; avoid sensitive tokens in logs beyond current scope.
- LLM may still produce unsafe suggestions; server denies execution.

Assumptions:
- Only local loopback; no external network.
- Sandbox guards physical file boundary.
