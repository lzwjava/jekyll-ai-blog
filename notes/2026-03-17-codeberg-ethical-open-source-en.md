---
audio: false
generated: true
image: false
lang: en
layout: post
title: Codeberg Ethical Open Source Hosting
translated: false
type: note
---

Question: What is a comprehensive introduction to Codeberg?

Answer:

**Codeberg** is a **non-profit**, **community-driven** platform for hosting and collaborating on **free and open-source software** (FOSS) projects. It serves as a popular ethical and privacy-focused alternative to commercial services like **GitHub**.

### Core Facts (as of early 2026)

- **Official website**: <https://codeberg.org>
- **Operator**: Codeberg e.V. — a registered non-profit association (eingetragener Verein) based in **Berlin, Germany**
- **Founded**: September 2018 (public launch January 2019)
- **Software stack**: Built on **Forgejo** (a free, community-maintained soft fork of Gitea)
- **Philosophy**: Put the commons and free software first — no profit motive, no investors, no advertising, no AI-training-by-default on public code

### Main Services

- **Git hosting** with issues, pull/merge requests, project boards, wikis, releases, packages
- **Codeberg Pages** — free static website hosting (`username.codeberg.page` or custom domain)
- **CI/CD runners** (Woodpecker CI) — free minutes for open-source projects
- **Translation platform** (Weblate instance at translate.codeberg.org)
- **Mirroring** support and federation experiments (ActivityPub/ForgeFed related work)

### Key Characteristics Compared to GitHub

| Aspect               | Codeberg                              | GitHub (Microsoft)                     |
|----------------------|---------------------------------------|----------------------------------------|
| Legal structure      | German non-profit e.V.                | For-profit corporation                 |
| Hosting location     | EU (mainly Germany)                   | Mainly USA                             |
| Private repositories | Allowed but **not the primary focus** (limited resources) | Fully supported & core business        |
| Profit model         | Donations + membership fees           | Enterprise plans, Copilot, etc.        |
| Data & privacy       | Strong EU GDPR baseline, no tracking/ads | More data collection & commercialization |
| Community governance | Members of e.V. can vote              | Controlled by Microsoft                |
| Scale (repos)        | ~ hundreds of thousands               | > 1 billion                            |
| Network effects      | Smaller discovery / fewer integrations| Dominant ecosystem                     |

Codeberg deliberately stays smaller and more focused. It prioritizes independence, long-term sustainability, and alignment with free software values over trying to compete on raw scale or enterprise features.

### Who Uses Codeberg?

- Free software projects that want to **leave or avoid** big-tech platforms
- European projects concerned about US jurisdiction (e.g. DMCA takedown risk)
- People/organizations who prefer **non-profit stewardship**
- Projects that value **Forgejo/woodpecker** ecosystem and dislike GitHub's increasing commercialization

### How to Get Started

1. Go to <https://codeberg.org>
2. Register an account (free, no credit card needed)
3. Create or import a repository
4. Optional: join Codeberg e.V. as supporting or active member → gives voting rights and financially helps the platform

Membership is **not required** to use the service — using Codeberg is free for individuals and open-source projects as long as you follow the Terms of Use.

### Strengths

- Genuine non-profit structure
- EU-based (stronger privacy laws)
- Very close to vanilla Forgejo → lightweight & fast
- Active community that cares about software freedom
- No corporate roadmap hijacks

### Limitations (realistic view in 2026)

- Smaller ecosystem → fewer ready-made integrations & actions
- Search & discoverability weaker than GitHub
- CI minutes and storage more limited (donation-dependent)
- Private repos tolerated but not encouraged (public-first philosophy)
- Less "social" visibility for new projects

In short: if you want **GitHub-like functionality without GitHub company**, Codeberg is currently (2026) one of the most mature, stable and ideologically clean options in the FOSS-friendly code forge landscape.

References:

- [Codeberg Official Site](https://codeberg.org/)
- [What is Codeberg? - Documentation](https://docs.codeberg.org/getting-started/what-is-codeberg)
- [Codeberg on Wikipedia](https://en.wikipedia.org/wiki/Codeberg)
- [Codeberg vs GitHub comparisons (various 2025–2026 sources)](https://shyft.ai/tools/compare/codeberg-vs-github)
