---
audio: false
generated: true
image: false
lang: en
layout: post
title: Bun Setup and Comparison Guide
translated: false
type: note
---

**Question:** What is Bun? How do you set a custom certificate and registry in Bun? How does it compare to npm?

**Answer:**

## What is Bun?

Bun is an all-in-one JavaScript runtime + package manager + bundler + test runner written in Zig, built on JavaScriptCore (Safari's engine) instead of V8. Key design goals: be fast by default, replace Node.js/npm/webpack/jest in one binary.

**Core components in one binary:**
- Runtime (`bun run`)
- Package manager (`bun install`, `bun add`)
- Bundler (`bun build`)
- Test runner (`bun test`)
- TypeScript/JSX transpiler (no config needed)

---

## Bun vs npm — Direct Comparison

| Feature | Bun | npm |
|---|---|---|
| Written in | Zig | JavaScript/C++ |
| JS Engine | JavaScriptCore | V8 |
| Install speed | ~10–25x faster (binary lockfile, parallel fetches) | Baseline |
| Lockfile | `bun.lockb` (binary) | `package-lock.json` (JSON) |
| Workspace support | Yes | Yes |
| TypeScript | Native, zero config | Needs `ts-node` or compile step |
| `.env` loading | Built-in | Needs `dotenv` |
| Test runner | Built-in (`bun test`, Jest-compatible) | Needs Jest/Vitest |
| Bundler | Built-in | Needs webpack/esbuild/rollup |
| Node.js compat | High (~95%) but not 100% | 100% (it IS Node) |
| Maturity | ~2023–2024 stable, still maturing | Decade-old, battle-tested |

**Install speed** comes from: binary lockfile (no JSON parse), hardlinks instead of copies, parallel HTTP/2 fetches, and Zig's tight syscall usage.

---

## Set Custom Registry

### Global (all packages)
```bash
bun config set registry https://your-registry.example.com
```

Or edit `~/.bunfig.toml`:
```toml
[install]
registry = "https://your-registry.example.com"
```

### Scoped registry (e.g. `@myorg`)
In `bunfig.toml` (project or `~/.bunfig.toml`):
```toml
[install.scopes]
"@myorg" = { registry = "https://npm.myorg.internal", token = "YOUR_TOKEN" }
```

### With auth (npm-style token)
```toml
[install]
registry = "https://your-registry.example.com"

[install.registry]
token = "YOUR_NPM_TOKEN"
# or:
# username = "user"
# password = "pass"
```

---

## Set Custom Certificate (SSL/TLS)

This is the pain point for corporate environments (e.g. your bank's internal proxy with a self-signed CA).

### Option 1 — `caFile` in bunfig.toml
```toml
[install]
caFile = "/path/to/your-ca-bundle.pem"
```

### Option 2 — System trust store
Bun respects the system's CA store on Linux/macOS. Add your cert to the system store:

```bash
# Ubuntu
sudo cp your-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain your-ca.crt
```

### Option 3 — `NODE_EXTRA_CA_CERTS` (Node compat env var)
```bash
export NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem
bun install
```
Bun respects this env var for compatibility.

### Option 4 — Disable TLS verification (dev only, never prod)
```toml
[install]
tlsRejectUnauthorized = false
```

---

## Full `bunfig.toml` Example (corporate setup)

```toml
[install]
registry = "https://nexus.internal.bank.com/repository/npm-proxy/"
caFile = "/etc/ssl/certs/bank-internal-ca.pem"

[install.scopes]
"@bank-internal" = {
  registry = "https://nexus.internal.bank.com/repository/npm-private/",
  token = "YOUR_NEXUS_TOKEN"
}
```

---

## npm equivalent cheatsheet

```bash
# npm                          → bun
npm install                    → bun install
npm install express            → bun add express
npm install -D vitest          → bun add -d vitest
npm run dev                    → bun dev  (or bun run dev)
npm config set registry <url>  → bun config set registry <url>
npx ts-node index.ts           → bun index.ts
npm test                       → bun test
```

---

## Should you switch from npm to Bun?

Given your setup (AI CLI tools, Node scripts, bank proxy environments):

- **Yes for local dev** — `bun install` is noticeably faster, TS just works, `.env` just works
- **Yes for CLI tools** — `bun build --compile` can produce single-file executables
- **Caution in corp environments** — cert/proxy setups need `caFile` or system store; Node.js 100% compat isn't guaranteed for some native addons
- **Not yet for production infra** — if you're containerizing Node.js services at the bank, Node is still safer for 100% compat