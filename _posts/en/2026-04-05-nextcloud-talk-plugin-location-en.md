---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nextcloud Talk Plugin Source Code Location
translated: false
type: note
---

Question: Where is the source code for the OpenClaw Nextcloud Talk plugin, and is it in the main openclaw GitHub repository?

Answer:

## OpenClaw Nextcloud Talk Plugin — Source Code & Location

You are correct in suspecting it is **not** directly visible in the public GitHub repo in the traditional sense. Here is the full picture:

---

### 1. It Is a Separate Plugin, Not Bundled with Core

Nextcloud Talk ships as a plugin and is not bundled with the core OpenClaw install. This is by design — the channel integration is treated as an optional extension.

---

### 2. How It Is Distributed

The plugin is published as an npm package under the `@openclaw` scope:

```
@openclaw/nextcloud-talk
```

You can install it via the CLI from the npm registry with:
```
openclaw plugins install @openclaw/nextcloud-talk
```
Or, if running from a git checkout locally:
```
openclaw plugins install ./extensions/nextcloud-talk
```

---

### 3. Where the Source Code Lives

The source code is **inside the main `openclaw/openclaw` monorepo** under the `extensions/` folder. From GitHub discussions and community references, the path is:

```
extensions/nextcloud-talk/
```

Key files referenced in community discussions include:
- `extensions/nextcloud-talk/index.ts` — the plugin entry point
- `extensions/nextcloud-talk/src/signature.ts` — webhook signature verification logic

A user noted finding duplicate configs at `~/.openclaw/extensions/nextcloud-talk/index.ts` and `/opt/homebrew/lib/node_modules/openclaw/extensions/nextcloud-talk/index.ts`, confirming that the source indeed lives within the openclaw monorepo's extensions folder.

---

### 4. Why It "Seems" Missing from the Repo

The plugin manifest in the docs describes it this way:

```json
{
  "name": "@openclaw/nextcloud-talk",
  "openclaw": {
    "install": {
      "npmSpec": "@openclaw/nextcloud-talk",
      "localPath": "extensions/nextcloud-talk",
      "defaultChoice": "npm"
    }
  }
}
```

The `localPath` is `extensions/nextcloud-talk`, and when on a git checkout, OpenClaw will offer that local install path automatically instead of pulling from npm.

So the source is in the repo, but it lives in the `extensions/` subdirectory (a monorepo pattern), not at the root level. It is published separately to npm from that folder, which is why searching the repo's top-level may make it appear absent.

---

### 5. Known Issue: Monorepo Workspace Dependencies

There was a known bug where the `@openclaw/nextcloud-talk` npm package had an unresolved `workspace:*` dependency in its `package.json` — a protocol only valid within a monorepo development environment. When publishing to npm, this should be replaced with an actual version number. This confirms the plugin is authored inside the monorepo and then published outward to npm.

---

### Summary

| Item | Detail |
|---|---|
| Source location | `extensions/nextcloud-talk/` inside the main `openclaw/openclaw` GitHub repo |
| npm package | `@openclaw/nextcloud-talk` |
| Bundled with core? | No — must be installed separately |
| Entry point | `index.ts` |
| Signature logic | `src/signature.ts` |

References:

- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)
- [OpenClaw Nextcloud Talk Channel Docs](https://docs.openclaw.ai/channels/nextcloud-talk)
- [OpenClaw Plugin System Docs](https://docs.openclaw.ai/tools/plugin)
- [GitHub Discussion #4198 — nextcloud-talk plugin error](https://github.com/openclaw/openclaw/discussions/4198)
- [GitHub Issue #8145 — workspace dependency bug](https://github.com/openclaw/openclaw/issues/8145)
