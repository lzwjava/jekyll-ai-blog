---
audio: false
generated: true
image: false
lang: en
layout: post
title: npm Dev Script Points to Wrong File
translated: false
type: note
---

Here's the info to raise the issue:

---

## Environment

| Tool | Version |
|------|---------|
| Node.js | v25.3.0 |
| npm | 11.7.0 |
| npx | 11.7.0 |
| Node path | `/opt/homebrew/bin/node` |
| OS | macOS Darwin 25.4.0 |

---

## Issue to Raise

**Title:** `npm run dev` script points to wrong entry file — server never starts

**Description:**

The `dev` script in `package.json` runs `src/index.ts` which is a library export file, not the server. This causes nodemon to start and immediately exit with no server running.

**Steps to reproduce:**
1. `npm install`
2. `npm run dev`
3. Server exits immediately — nothing listening on port 3000

**Expected:** Server starts on `http://localhost:3000`

**Actual:** Process exits cleanly, no server started

**Fix:**
```json
// package.json
"dev": "nodemon --exec ts-node src/server.ts"
```

**Workaround:**
```bash
npx ts-node src/server.ts
```

**Environment:** Node v25.3.0, npm 11.7.0, macOS Darwin 25.4.0

---

You can file this at: https://github.com/sreekanthvaripalli/secure-captcha-plugin/issues
