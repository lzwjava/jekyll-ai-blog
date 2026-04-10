---
audio: false
generated: true
image: false
lang: en
layout: post
title: HTTP and HTTPS Node.js Logging
translated: false
type: note
---

**Question:** Give me the command about NODE options to log HTTP and HTTPS logs, related to npm install --verbose.

**Answer:**

To enable detailed logging of **HTTP** and **HTTPS** requests made by Node.js (including those triggered during `npm install`, such as fetching packages from the registry), use the built-in `NODE_DEBUG` environment variable.

### Primary Command for HTTP/HTTPS Logging
Run this before your npm command (on Unix-like systems like Linux/macOS):

```bash
NODE_DEBUG=http,https npm install --verbose
```

On Windows (Command Prompt):

```cmd
set NODE_DEBUG=http,https && npm install --verbose
```

On Windows (PowerShell):

```powershell
$env:NODE_DEBUG="http,https"; npm install --verbose
```

### What This Does
- `NODE_DEBUG=http` → Logs all outgoing/incoming HTTP client and server activity (requests, responses, headers, sockets, etc.).
- `NODE_DEBUG=https` → Logs HTTPS-specific activity (TLS handshakes, secure connections).
- Combining them with a comma (`http,https`) enables both.
- `--verbose` (or `--loglevel verbose`) adds extra npm-level details, including some HTTP fetch info at the "http" loglevel.

You can also include more modules for broader debugging:

```bash
NODE_DEBUG=http,https,http2,tls npm install --verbose
```

### Additional Useful NODE_OPTIONS
You can pass Node.js flags via the `NODE_OPTIONS` environment variable (npm supports this for lifecycle scripts too):

```bash
NODE_DEBUG=http,https NODE_OPTIONS="--trace-warnings" npm install --verbose
```

Or combine with npm's own HTTP logging level:

```bash
NODE_DEBUG=http,https npm install --loglevel=http --verbose
```

### Tips
- This output can be very verbose — redirect it to a file if needed:  
  `NODE_DEBUG=http,https npm install --verbose > npm-http.log 2>&1`
- These logs help debug network issues like registry connectivity, proxy problems, SSL errors, or slow downloads.
- `NODE_DEBUG` works for any Node.js process, not just npm.

This is the standard, built-in way to get low-level HTTP/HTTPS logs without installing extra packages.

**References:**
- https://nodejs.org/api/cli.html (Node.js command-line options and environment variables)
- https://docs.npmjs.com/cli/v9/using-npm/logging (npm logging levels including "http")