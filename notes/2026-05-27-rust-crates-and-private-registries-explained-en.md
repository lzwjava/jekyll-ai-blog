---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Crates and Private Registries Explained
translated: false
type: note
---

**Question:** How does the Rust crates ecosystem work, and what is Crates.io? How can enterprises use and host private crate registries?

**Answer:**

## Rust Crates — From First Principles

### What is a Crate?

A **crate** is Rust's compilation unit — the smallest thing `rustc` compiles. Two kinds:

- **Binary crate** — has a `main()`, produces an executable
- **Library crate** — no `main()`, produces a `.rlib` (or `.so`/`.a`) for others to link

A **package** is what Cargo manages — one `Cargo.toml`, one or more crates inside.

```
my-package/
├── Cargo.toml        # package metadata + dependency manifest
├── src/
│   ├── main.rs       # binary crate root
│   └── lib.rs        # library crate root (optional)
└── tests/
    └── integration.rs
```

---

### How Cargo Resolves Dependencies

```toml
# Cargo.toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
```

Cargo does **semver-aware resolution**:

1. Reads `Cargo.toml` across your whole workspace
2. Builds a **dependency graph** (DAG)
3. Runs a **SAT solver** (PubGrub algorithm) to find compatible versions
4. Writes the exact solution to `Cargo.lock`
5. Downloads `.crate` tarballs from the registry
6. Compiles in dependency order

`Cargo.lock` pins exact SHAs — deterministic builds. Commit it for binaries, gitignore it for libraries.

---

### crates.io — The Public Registry

`crates.io` is the official **sparse registry** (as of Cargo 1.68+). The protocol:

```
# Old (git-based index, slow)
https://github.com/rust-lang/crates.io-index

# New sparse index (HTTP, fast)
https://index.crates.io/
```

When you `cargo add serde`, Cargo:

1. Fetches `https://index.crates.io/se/rd/serde` — a JSON file listing all versions + yanked status + checksums
2. Picks best version per semver constraint
3. Downloads `https://static.crates.io/crates/serde/1.0.193/download`
4. Verifies SHA-256 checksum
5. Extracts to `~/.cargo/registry/src/`

---

### Publishing to crates.io

```bash
cargo login <your-api-token>    # from crates.io account
cargo publish --dry-run         # smoke test
cargo publish                   # uploads tarball + updates index
```

Crates are **immutable** once published — you can only `yank` (soft-delete, existing users unaffected, new resolves blocked).

---

## Enterprise Private Registries

This is where it gets practically important. Three main options:

### 1. Cloudsmith / Artifactory / Gemfury (SaaS)

Hosted private registries. JFrog Artifactory is most common in enterprise:

```toml
# .cargo/config.toml
[registries]
my-company = { index = "sparse+https://artifactory.mycompany.com/artifactory/api/cargo/rust-local/index/" }

[net]
git-fetch-with-cli = true
```

```toml
# Cargo.toml
[dependencies]
internal-sdk = { version = "0.1", registry = "my-company" }
```

Auth via `~/.cargo/credentials.toml`:

```toml
[registries.my-company]
token = "Bearer eyJ..."
```

### 2. Kellnr — Self-Hosted Open Source

[Kellnr](https://kellnr.io) is the most popular **self-hosted** option. Written in Rust. Supports sparse protocol.

```bash
docker run -d \
  -p 8000:8000 \
  -v kellnr_data:/opt/kellnr/data \
  -e KELLNR_ORIGIN__HOSTNAME=registry.internal \
  ghcr.io/kellnr/kellnr:latest
```

Then in config:

```toml
[registries]
kellnr = { index = "sparse+http://registry.internal:8000/api/v1/crates/index/" }
```

### 3. Gitea / Forgejo (Built-in Cargo Registry)

Gitea 1.21+ has a **native Cargo registry** — no extra service needed if you already run Gitea for git hosting:

```toml
[registries]
gitea = { index = "sparse+https://gitea.mycompany.com/api/packages/{owner}/cargo/index/" }
```

---

### Workspace Monorepo Pattern (Enterprise Standard)

Large enterprises use **Cargo workspaces** to manage many internal crates:

```
company-platform/
├── Cargo.toml          # workspace root
├── Cargo.lock          # one lock file for everything
├── crates/
│   ├── auth/           # internal library
│   ├── db-client/      # internal library
│   ├── api-server/     # binary
│   └── cli-tool/       # binary
```

```toml
# workspace Cargo.toml
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.dependencies]
# Pin versions once for entire workspace
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

Each member `Cargo.toml` inherits:

```toml
[dependencies]
tokio = { workspace = true }
```

---

### Vendoring — Air-Gapped / Compliance Environments

Banks especially need this — no internet access during CI:

```bash
cargo vendor                    # downloads all deps to ./vendor/
```

Generates `vendor/` dir + config snippet:

```toml
# .cargo/config.toml (auto-generated)
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
```

Commit `vendor/` to git. CI builds with zero network access. Fully auditable supply chain.

---

### Supply Chain Security (Critical for Banks)

```bash
# Audit deps against RustSec advisory database
cargo install cargo-audit
cargo audit

# Check for licenses
cargo install cargo-license
cargo license

# Deny specific licenses or vulnerabilities
# cargo-deny: most powerful
cargo install cargo-deny
cargo deny check
```

`cargo-deny` config:

```toml
# deny.toml
[licenses]
allow = ["MIT", "Apache-2.0", "BSD-3-Clause"]

[advisories]
db-path = "~/.cargo/advisory-db"
db-urls = ["https://github.com/rustsec/advisory-db"]
deny = ["unmaintained", "unsound", "yanked"]
```

This is what mature enterprise Rust setups run in CI — license compliance + CVE gating before any dep lands in production.

---

## Summary

| Need | Tool |
|---|---|
| Public open source | crates.io |
| Self-hosted private registry | Kellnr or Gitea |
| Enterprise SaaS registry | Artifactory / Cloudsmith |
| Air-gapped / compliance builds | `cargo vendor` |
| Monorepo management | Cargo workspaces |
| Security auditing | `cargo-audit` + `cargo-deny` |

Given you're at a bank, the realistic stack is: **Artifactory or Kellnr** as registry + **`cargo vendor`** for regulated CI pipelines + **`cargo-deny`** for license/CVE gating.

**References:**

- [The Cargo Book — Registries](https://doc.rust-lang.org/cargo/reference/registries.html)
- [Kellnr — Self-Hosted Crate Registry](https://kellnr.io)
- [cargo-deny](https://embarkstudios.github.io/cargo-deny/)
- [Sparse Registry Protocol RFC](https://rust-lang.github.io/rfcs/2789-sparse-index.html)
- [RustSec Advisory Database](https://rustsec.org)
