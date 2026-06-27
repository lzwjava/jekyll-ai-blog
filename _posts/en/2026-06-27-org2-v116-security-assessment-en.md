---
audio: false
generated: true
image: false
lang: en
layout: post
title: ORG2 v1.1.6 Security Assessment
translated: false
type: note
---

Now I have enough to give you a thorough security assessment. Here's the breakdown:

---

SECURITY ASSESSMENT: ORG2 (ORGII) v1.1.6

VERDICT: Generally well-engineered with some notable concerns. Use it, but understand the tradeoffs.


## What It Is

A Tauri-based desktop app (Rust backend + React frontend) that acts as an agentic development framework. It orchestrates multiple LLM providers (OpenAI, Anthropic, Gemini, Codex, Claude Code, Copilot, etc.) and stores their API keys locally.


## GOOD Security Practices

1. Credential storage: Keys stored at ~/.orgii/credentials.json with 0o600 permissions (owner-only read/write). Atomic write pattern (temp file + rename) prevents corruption.

2. Sensitive file permissions: Dedicated set_sensitive_file_permissions() function used consistently across key vault, proxy CA, connection stores. Cross-platform (Unix 0o600, Windows icacls).

3. MITM proxy CA: Self-signed CA stored in ~/.orgii/proxy/ with proper key file permissions. CA private key is never world-readable.

4. Content Security Policy (CSP): A reasonably strict CSP is configured:
   - default-src 'self'
   - object-src 'none'
   - base-uri 'self'
   - connect-src limited to self, ipc, localhost, and HTTPS

5. Auto-updater: Uses minisign public key verification (signed releases from GitHub).

6. No third-party telemetry/analytics: The "analytics" module is LOCAL session analytics (tool usage, token counts, duration) — not sent to external services by default.

7. Diagnostics upload: Opt-in via environment variables (ORGII_DIAGNOSTICS_ENDPOINT + ORGII_DIAGNOSTICS_TOKEN). If no endpoint is configured, data stays local. Has an offline_mode flag.


## CONCERNS (Ranked by Severity)

### MEDIUM — Broad Shell Execution Permissions

In src-tauri/capabilities/default.json:
```json
{
  "identifier": "shell:allow-execute",
  "allow": [
    { "name": "sh", "cmd": "sh", "args": true },
    { "name": "curl", "cmd": "curl", "args": true },
    { "name": "python3", "cmd": "python3", "args": true }
  ]
}
```
The "args": true means arbitrary arguments. This effectively grants the frontend the ability to run ANY shell command via `sh -c "..."`. This is by design for an agentic tool, but it means if the frontend is compromised (XSS, malicious plugin), an attacker gets full shell access.

### MEDIUM — Very Broad Filesystem Access

From capabilities/default.json:
- fs:allow-home-read-recursive — reads entire home directory
- fs:allow-home-write-recursive — writes anywhere in home directory
- fs:allow-read-file with path: "**" — reads ANY file on the system
- fs:allow-write-text-file with path: "**" — writes ANY text file

Again, by design for an agent, but this is essentially full filesystem access.

### MEDIUM — MITM Proxy Interception

For agents like Cursor, Copilot, and Kiro that don't support custom base URLs, ORGII installs a local MITM proxy with its own CA to intercept and rewrite HTTPS traffic. The code at src-tauri/crates/integrations/src/proxy/certificate_authority.rs generates a root CA that can sign certificates for any domain. This is technically necessary for credential injection but is a powerful capability — if the CA key were compromised, all HTTPS traffic routed through the proxy could be intercepted.

### LOW — CSP Allows Inline Styles and eval-like Constructs

- style-src 'self' 'unsafe-inline' — allows inline CSS (XSS vector for data exfiltration via CSS, though limited)
- script-src 'self' 'wasm-unsafe-eval' — needed for WASM but slightly weakens CSP
- connect-src includes http://127.0.0.1:* and ws://localhost:* — allows connections to any local port

### LOW — Keys Stored as Plaintext JSON

API keys are stored in plaintext at ~/.orgii/credentials.json (protected by 0o600 permissions). This is standard practice for desktop apps (similar to how AWS credentials work), but on a shared machine or if malware runs as your user, the keys are readable.

### INFO — Diagnostics System

There is a diagnostics/telemetry system, but it's well-designed:
- Requires explicit ORGII_DIAGNOSTICS_ENDPOINT env var to upload
- Has offline_mode and diagnostics_level: Off options
- Data is bucketed/sanitized (CPU as ranges, RAM as ranges, durations as ranges)
- Install ID is a random UUID, not tied to personal identity
- Default upload interval is 12 hours

Without the env var set, no data leaves your machine.


## Bottom Line

Yes, you're ok to use it, with these caveats:

1. It's an agent platform — it NEEDS shell and filesystem access to function. That's the whole point. But treat it with the same trust level as running a developer tool with sudo-like access to your home directory.

2. Your API keys are in plaintext at ~/.orgii/credentials.json. Make sure your user account is secured (strong password, full-disk encryption).

3. The MITM proxy is only active when you're using Cursor/Copilot/Kiro CLI agents. If you're only using direct API key providers (OpenAI, Anthropic, etc.), it's not running.

4. No data is sent externally without you explicitly configuring the diagnostics endpoint.

5. The code quality is solid — Rust backend, proper atomic writes, mutex-guarded storage, permission management. This is not a sloppy Electron app.

The security posture is appropriate for a local-first developer tool that orchestrates AI agents. The broad permissions are a necessary consequence of what the product does.
