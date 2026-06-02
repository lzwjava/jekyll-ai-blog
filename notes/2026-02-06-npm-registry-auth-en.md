---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: NPM Registry Authentication Guide
translated: false
type: note
---

Yes, you can use `npm config set` to configure authentication for npm registries. Here's how it works:

## Basic Usage

```bash
# For _authToken (recommended)
npm config set //registry.npmjs.org/:_authToken "your-token-here"

# For _auth (legacy)
npm config set //registry.npmjs.org/:_auth "base64-encoded-credentials"
```

Note the syntax: it's `//registry.org/:_auth` (with a colon before `_auth`), not `//registry.org/_auth`.

## Difference between _auth and _authToken

**`_authToken`** (modern approach):
- Accepts a plain authentication token directly
- Used by most modern registries (npm, GitHub Packages, etc.)
- The token is stored as-is in your `.npmrc` file
- Example: `//registry.npmjs.org/:_authToken=npm_abc123xyz...`

**`_auth`** (legacy approach):
- Requires base64-encoded credentials in the format `username:password`
- Older authentication method, less commonly used today
- You need to encode it yourself: `echo -n "username:password" | base64`
- Example: `//registry.npmjs.org/:_auth=dXNlcm5hbWU6cGFzc3dvcmQ=`

## Practical Example

For a private registry like GitHub Packages:

```bash
npm config set //npm.pkg.github.com/:_authToken "ghp_yourGitHubToken"
```

For scoped packages, you might also need:

```bash
npm config set @yourscope:registry https://npm.pkg.github.com
```

Most modern workflows use `_authToken` since it's simpler and works with token-based authentication systems. The `_auth` method is mainly for legacy systems that still use username/password authentication.
