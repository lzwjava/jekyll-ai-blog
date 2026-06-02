---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Open Source Sharing Guide Essentials
translated: false
type: note
---

Question: How to become more open source? What files and information can we share publicly in open source projects, blogs, etc.?

Answer:

Becoming "more open source" means adopting habits, processes, and a mindset that prioritizes transparency, collaboration, community, and sharing knowledge/code publicly. This applies whether you're an individual developer, a small team, or a company.

### For individual developers or small teams

- **Contribute regularly** to existing open source projects (fix bugs, add features, improve docs, review PRs).
- **Open source your own code** — start with small utilities, configs, or learning projects on GitHub/GitLab.
- **Write publicly** — maintain a **dev blog**, share TILs (Today I Learned), architecture decisions, post-mortems, or tutorials on Medium/Dev.to/your own site.
- **Be transparent in your work** — use public issue trackers even for personal/side projects, discuss design openly.
- **Adopt open practices daily** — use OSI-approved licenses, write good commit messages, respond to issues quickly.
- **Build in public** — share progress updates, roadmaps, decisions on X (Twitter), Mastodon, LinkedIn, or your blog.

### For companies / teams wanting to become more open source

- **Create an open source strategy** — document goals (learning, hiring, ecosystem influence, innovation speed, etc.).
- **Start open sourcing internal tools** — begin with non-core / low-risk libraries, configs, or CLIs (clean them first: remove secrets, sensitive logic).
- **Allow and encourage upstream contributions** — make it easy/legal for employees to contribute to external projects during work hours.
- **Invest in documentation & community** — treat docs as a first-class citizen (many successful OSS companies win via excellent docs).
- **Adopt open processes internally** — use public RFCs, public roadmaps (where possible), open issue trackers for product features.
- **Hire from / reward community** — recognize maintainers, give talk slots, sponsor events, hire active contributors.
- **Publish company blogs about OSS** — write about architecture, scaling stories, open source lessons, security practices, etc.

### Essential files and information to share publicly in open source projects

These are the standard, strongly recommended files in the root of a Git repository:

- **README.md** (most important file)
  Project name, one-paragraph description, why it exists, quick start/install instructions, usage examples, screenshots/GIFs, status (stable/experimental), license link, contribution pointer.

- **LICENSE** (or LICENSE.txt / LICENSE.md)
  The actual license text (MIT, Apache 2.0, GPL, BSD, MPL, etc.). Choose an [OSI-approved license](https://opensource.org/licenses). Without this the project is **not open source**.

- **CONTRIBUTING.md**
  How to contribute: setup dev environment, coding style, commit message format, how to open issues/PRs, what to expect from maintainers, links to Slack/Discord/forum.

- **CODE_OF_CONDUCT.md**
  Usually the [Contributor Covenant](https://www.contributor-covenant.org/) — helps create a welcoming, harassment-free environment.

Other very common / highly recommended files:

- **SECURITY.md** — How to report security issues (private email/security policy link).
- **CHANGELOG.md** or **RELEASE_NOTES.md** — Following [Keep a Changelog](https://keepachangelog.com/) format.
- **.github/** folder containing:
  - ISSUE_TEMPLATE/** — Issue templates
  - PULL_REQUEST_TEMPLATE.md
  - dependabot.yml / funding.yml / workflows/
- **ROADMAP.md** or GitHub Project board — Future plans, helps attract contributors.
- **docs/** folder — Detailed documentation, architecture.md, api.md, tutorials.

### What else can you share publicly (on blog / website / social media)

- Architecture diagrams and decisions (ADRs — Architecture Decision Records)
- Performance benchmarks and comparisons
- Internal tooling (CLI helpers, Git hooks, CI pipelines — sanitized)
- Failure stories / post-mortems
- Scaling stories / "how we handle X million requests"
- Open RFCs / design proposals
- Employee learnings / conference talks slides
- Contributor spotlights / thank-yous

Start small: pick one project → add README + LICENSE + CONTRIBUTING → share it → iterate based on feedback.

References:

- [Starting an Open Source Project (opensource.guide)](https://opensource.guide/starting-a-project)
- [How to Write a Good README (freeCodeCamp)](https://www.freecodecamp.org/news/how-to-write-a-good-readme-file)
- [Setting an Open Source Strategy (Linux Foundation)](https://www.linuxfoundation.org/resources/open-source-guides/setting-an-open-source-strategy)
- [Improve Your Open Source Development Impact (TODO Group)](https://todogroup.org/resources/guides/improve-your-open-source-development-impact)
- [Keep a Changelog](https://keepachangelog.com/)
- [Contributor Covenant](https://www.contributor-covenant.org/)
