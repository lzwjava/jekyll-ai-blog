---
audio: false
generated: true
image: false
lang: en
layout: post
title: Using GitHub Crates with Cargo
translated: false
type: note
---

**Question:** How do you configure `Cargo.toml` to pull crates directly from GitHub instead of crates.io, so they compile in an enterprise environment where the registry is blocked?

**Answer:**

## 1. Direct GitHub dependency in `Cargo.toml`

```toml
[dependencies]
# By branch
serde = { git = "https://github.com/serde-rs/serde", branch = "master" }

# By tag
serde = { git = "https://github.com/serde-rs/serde", tag = "v1.0.197" }

# By exact commit (most reproducible — prefer this in enterprise)
serde = { git = "https://github.com/serde-rs/serde", rev = "9b868ef831b32de" }
```

## 2. If GitHub is also blocked — vendor the deps locally

```bash
# On a machine with internet access:
cargo vendor

# This creates a `vendor/` directory with all source code
# Then commit it, or copy it to the enterprise machine
```

Then add to `.cargo/config.toml` (project-level or `~/.cargo/config.toml`):

```toml
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
```

Now `cargo build` reads from `vendor/` — zero network calls.

## 3. If you can reach an internal mirror (Artifactory / Cloudsmith / etc.)

```toml
# .cargo/config.toml
[source.crates-io]
replace-with = "internal-mirror"

[source."internal-mirror"]
registry = "https://artifactory.corp.example.com/cargo"
```

## 4. Mixed: some from GitHub, some vendored

You can combine both. Cargo resolves in priority order. To patch a specific crate (e.g., override a transitive dep without changing every consumer):

```toml
# Cargo.toml
[patch.crates-io]
ring = { git = "https://github.com/briansmith/ring", rev = "fabd88f" }
```

`[patch]` is the cleanest way to override transitive dependencies — you don't touch each crate's own `Cargo.toml`, just the workspace root.

## 5. Workspace-wide patching (monorepo / multi-crate setup)

```toml
# workspace root Cargo.toml
[patch.crates-io]
tokio = { git = "https://github.com/tokio-rs/tokio", branch = "master" }
```

All crates in the workspace inherit this patch automatically.

## Quick decision tree

```
Can reach GitHub?
├── Yes → git = "https://github.com/..." in [dependencies] or [patch.crates-io]
└── No
    ├── Can reach internal registry? → [source] replace-with in config.toml
    └── Fully airgapped → cargo vendor + commit vendor/
```

## Gotcha: `Cargo.lock` matters

Always commit `Cargo.lock` in enterprise environments. Without it, `rev`-less git deps can silently pick up new commits. With `rev = "..."` + committed lockfile you get fully reproducible builds.
