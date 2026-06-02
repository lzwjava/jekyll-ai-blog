---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Debug Node.js HTTP and NPM
translated: false
type: note
---

I'll help you with debugging HTTP/HTTPS requests in Node.js and NPM operations.

## NODE_DEBUG for HTTP/HTTPS

The `NODE_DEBUG` environment variable enables internal Node.js debugging output. For HTTP/HTTPS requests:

```bash
# Debug HTTP requests
NODE_DEBUG=http node your-script.js

# Debug HTTPS requests
NODE_DEBUG=https node your-script.js

# Debug both
NODE_DEBUG=http,https node your-script.js
```

This shows you:
- Socket connections and reuse
- Request headers being sent
- Response status codes
- Keep-alive behavior
- Internal state transitions

**Example output** includes details like:
```
HTTP 12345: call onSocket 0 0
HTTP 12345: createConnection localhost:3000 {...}
HTTP 12345: outgoing message end
```

## NPM Debug Logging

For NPM, you can control logging verbosity to see request headers and detailed operations:

```bash
# Maximum verbosity (shows all HTTP requests, headers, etc.)
npm install --loglevel silly

# Or set it globally
npm config set loglevel silly

# Then run any npm command
npm install
```

**Alternative using npm debug flag:**
```bash
npm install --verbose
# or
npm install -d  # debug mode
npm install -dd # even more verbose
```

**To see actual HTTP traffic including headers**, combine with NODE_DEBUG:
```bash
NODE_DEBUG=http,https npm install --loglevel silly
```

This will show you:
- Registry URLs being contacted
- Request/response headers
- TLS/SSL handshakes
- Package resolution details
- Cache operations

**Tip**: Pipe to a file if the output is overwhelming:
```bash
NODE_DEBUG=http,https npm install --loglevel silly 2>&1 | tee npm-debug.log
```

You can reset npm logging back to normal with:
```bash
npm config set loglevel warn
```
