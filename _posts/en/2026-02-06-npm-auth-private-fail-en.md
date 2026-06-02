---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM Auth Failures With Private Registry
translated: false
type: note
---

You're describing a common behavior with npm when using a private registry (like Sonatype Nexus) that requires authentication. Let me break down what's happening:

## When `node_modules` is empty (fresh install)

```bash
npm install
```

- npm tries to download packages directly
- Without proper auth, you get immediate failures
- Error message: `Need: Basic realm "Sonatype Nexus"` (or similar auth challenge)
- Multiple package downloads fail quickly

## When `node_modules` is NOT empty (existing installation)

The behavior is different:

1. **First request: 401 Unauthorized** - npm tries to access the registry
2. **Second request: `npm authCheck`** - npm makes an authentication verification request to a specific endpoint
3. **Then: 500 Internal Server Error** - this might occur if:
   - The auth check endpoint fails
   - There's a server-side issue with credential validation
   - The registry has a misconfiguration

## Why this difference?

When `node_modules` exists, npm performs additional checks before attempting downloads:

- It validates existing packages
- It checks authentication status more thoroughly
- It may try to verify the registry connection first

## Solutions

1. **Configure npm authentication properly:**

   ```bash
   npm config set registry https://your-nexus-url/repository/npm-group/
   npm login --registry=https://your-nexus-url/repository/npm-group/
   ```

2. **Or use `.npmrc` file:**

   ```
   registry=https://your-nexus-url/repository/npm-group/
   //your-nexus-url/repository/npm-group/:_auth=<base64-encoded-credentials>
   ```

3. **Check your credentials format** - Basic auth needs base64 encoding of `username:password`

The 401→500 sequence suggests the registry might be having issues handling the auth check when packages already exist locally.
