---
audio: false
generated: true
image: false
lang: en
layout: post
title: Forcing npm to use a new registry
translated: false
type: note
---

Question: How does `npm --cache <dir> --prefer-online` work, and if `package-lock.json` has old `resolved` URLs pointing to a previous registry, how do you force npm to use a new registry? Why does specifying `--registry` sometimes not work and npm still uses the old one?

Answer:

This is a common pain point in teams that switch private registries (Artifactory, Nexus, Verdaccio, etc.). Let's break it down completely.

---

## 1. How `--cache <dir>` Works

The `--cache <dir>` flag overrides the directory where npm stores its local content-addressable cache (default: `~/.npm` on Unix, `%AppData%\npm-cache` on Windows).

```bash
npm install --cache /tmp/my-cache
```

npm's cache stores:

- **Package tarballs** (`.tgz` files) keyed by content hash (SHA-512)
- **Package metadata** (version info, dependency trees)

The cache is **content-addressable**, meaning files are keyed by their integrity hash, not by URL or registry name. This has an important implication: if the same package exists in both your old and new registry with the same hash, npm may serve it from cache and never even contact the new registry.

---

## 2. How `--prefer-online` Works

`--prefer-online` forces npm to revalidate cached data (with HTTP 304 checks), ignoring any staleness checks, and refreshing the cache with revalidated, fresh data.

In contrast:

- `--prefer-offline` makes npm skip conditional requests (304 checks) for stale cache data, only hitting the network if something is missing from the cache.
- `--offline` forces npm to use the cache or exit entirely, erroring with `ENOTCACHED` if anything isn't cached.

So `--prefer-online` is the "freshest" mode — it always goes out to the network to verify, even if data is cached.

When using `--prefer-online` with no `package-lock.json` and the public registry, there can be a very high number of HTTP requests generated (around 2,800 for a typical project), because npm fetches both up-to-date metadata and package content.

**Combining them:**

```bash
npm install --cache /my/cache/dir --prefer-online
```

This uses a custom cache directory but still goes online to revalidate everything. Useful in CI pipelines where you want a shared cache dir but always want fresh resolution.

---

## 3. Why `--registry` Doesn't Work — The `resolved` Field Problem

This is the core issue. When you run `npm install`, **npm reads `package-lock.json` first**, and each package entry has a `resolved` field baked in:

```json
{
  "lodash": {
    "version": "4.17.21",
    "resolved": "https://old-registry.company.com/lodash/-/lodash-4.17.21.tgz",
    "integrity": "sha512-xxxx"
  }
}
```

Even when specifying `--registry <URL>`, an existing lockfile may supersede this, and npm uses the `resolved` path as the package source. The exact behavior depends on the version of the npm client.

This is highlighted in the npm docs: "If the package has a `package-lock`, or an `npm-shrinkwrap` file, or a yarn lock file, the installation of dependencies will be driven by that."

So **`--registry` on the command line loses to the `resolved` URLs in `package-lock.json`**. The lockfile wins.

---

## 4. How to Force npm to Use a New Registry

### Option A — Delete and Regenerate the Lockfile (Recommended)

Users should delete any existing lockfiles and generate new ones when using a new registry. Remember to commit new and updated lockfiles to the project repository.

```bash
# Set new registry
npm config set registry https://new-registry.company.com

# Remove old lockfile
rm package-lock.json

# Reinstall — new lockfile will use the new registry
npm install
```

**Downside:** This may change transitive dependency versions since npm re-resolves everything from scratch.

### Option B — Find and Replace in `package-lock.json`

If you want to keep exact versions locked but just swap the registry URL:

```bash
# On Linux/Mac
sed -i 's|https://old-registry.company.com|https://new-registry.company.com|g' package-lock.json

# Then install
npm install
```

A find/replace may be the safest and most consistent solution when you need to change registries without altering versions or integrity hashes — the version and integrity fields remain exactly the same; only the `resolved` field changes.

### Option C — Use `.npmrc` for Persistent Registry Config

Create or update `.npmrc` in your project root:

```ini
registry=https://new-registry.company.com
# For scoped packages:
@myorg:registry=https://new-registry.company.com
```

For different registries for different packages, use scope-specific registries: `npm config set @myscope:registry=https://myownregist.ry/packages/`

### Option D — npm 5+ Auto-Switch (Limited)

As of npm 5, if you generated your `package-lock.json` against registry A, and you switch to registry B, npm will try to install the packages from registry B instead of A — but this only applies to *unscoped* packages, and different registries for different unscoped packages are no longer supported.

---

## 5. Summary: Priority Order (What Wins)

| Priority | Source |
|----------|--------|
| 1st (highest) | `resolved` URLs in `package-lock.json` |
| 2nd | `.npmrc` in project directory |
| 3rd | `--registry` CLI flag |
| 4th | `~/.npmrc` user config |
| 5th (lowest) | npm global config |

---

## 6. Common Troubleshooting Checklist

```bash
# Check what registry npm currently sees
npm config get registry

# Check all config sources and what's being applied
npm config list

# Clear npm's cache entirely (forces re-download)
npm cache clean --force

# Then reinstall with explicit registry and prefer-online
npm install --registry https://new-registry.company.com --prefer-online

# If still broken: nuke the lockfile and node_modules
rm -rf node_modules package-lock.json
npm install --registry https://new-registry.company.com
```

---

## Key Takeaway

The most frequent reason `--registry` seems to be "ignored" is that **`package-lock.json` has hardcoded `resolved` URLs that override your registry flag at runtime**. The lockfile is the authoritative source for where packages come from. To truly switch registries, you must either regenerate the lockfile, or do a bulk find-and-replace on the `resolved` field values inside it.

References:

- [npm v5.0.0 Release Blog — prefer-online, prefer-offline, offline flags explained](https://blog.npmjs.org/post/161081169345/v500)
- [Bytesafe Docs — Missing packages / lockfile resolved field superseding registry](https://docs.bytesafe.dev/troubleshooting/missing-packages/)
- [npm/npm GitHub Issue #19578 — package-lock.json resolved field not updating after registry change](https://github.com/npm/npm/issues/19578)
- [npm Official Docs — package-locks](https://docs.npmjs.com/cli/v6/configuring-npm/package-locks/)
- [npm Official Docs — config reference (prefer-online, prefer-offline, cache)](https://docs.npmjs.com/cli/v6/using-npm/config/)
- [DEV Community — Demystifying npm package installation (prefer-online deep dive)](https://dev.to/pavel-zeman/demystifying-npm-package-installation-insights-analysis-and-optimization-tips-4nmj)
