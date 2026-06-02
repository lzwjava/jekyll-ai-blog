---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Open Source Trunk Based Development Examples
translated: false
type: note
---

Question: Can you provide some examples of open-source GitHub projects that use Trunk-Based Development for learning purposes?

Answer:

Trunk-Based Development (TBD) emphasizes short-lived branches (or none at all) and frequent integration into a single main branch (the "trunk") to enable fast feedback, reduce merge conflicts, and support continuous delivery. While many large-scale open-source projects approximate TBD through high-velocity contributions, direct commits, and CI/CD pipelines, pure examples are rarer in OSS due to the distributed nature of contributors. Below are curated GitHub projects that either explicitly adopt TBD, demonstrate it effectively, or serve as learning resources (e.g., via documentation or structure). I've focused on active repos with clear workflows you can study through their commit history, PR patterns, and configs.

### 1. **Flipt** (github.com/flipt-io/flipt)

- **Why learn from it?** An open-source feature flag system designed explicitly for TBD and GitOps. It treats feature flags as code, enabling trunk commits without breaking production. Study their CI/CD setup and how they use flags to hedge releases—ideal for seeing TBD in action with real-time deployments.
- **Key to explore:** Short-lived PRs, automated tests on every push to main, and their docs on integrating with trunk workflows.
- **Stars:** ~5k+ | Language: Go

### 2. **Ripissue** (github.com/cwnt/ripissue)

- **Why learn from it?** An OSS tool for transitioning from GitFlow to TBD, used by the maintainers in their own workflows. It automates rebasing and merging to keep branches ephemeral. Perfect for hands-on learning: fork it, simulate a team setup, and observe how it enforces trunk hygiene.
- **Key to explore:** Workflow YAML files in `.github/workflows` and commit history showing daily trunk integrations.
- **Stars:** ~100+ (growing) | Language: Go

### 3. **Hexagonal Architecture TBD Demo** (github.com/gergely-nagymeyer/hexagonal-architecture-trunk-based)

- **Why learn from it?** A Java project showcasing TBD with feature toggles and Branch by Abstraction. It's built as a learning example using Spring Boot, Docker, and GitHub Actions—great for seeing how to handle larger refactors without long branches.
- **Key to explore:** Use of Togglz for flags and the repo's README on applying TBD patterns in DDD/hexagonal setups.
- **Stars:** ~200+ | Language: Java

### 4. **Abstract Feature Branch Gem** (github.com/paulhammant/abstract_feature_branch)

- **Why learn from it?** A Ruby gem implementing Branch by Abstraction and feature toggles for TBD. It's a practical toolkit for OSS contributors; examine how it enables concurrent development on trunk without isolation.
- **Key to explore:** Rails integration examples and tests that run on trunk commits to prevent breaks.
- **Stars:** ~50+ | Language: Ruby

### 5. **Awesome Trunk-Based Dev** (github.com/cgbystrom/awesome-trunk-based-dev)

- **Why learn from it?** Not a codebase, but a curated list of TBD resources with links to more projects, talks, and tools. Use it as a gateway: it points to real-world OSS examples like Google's monorepo practices (though not fully public).
- **Key to explore:** Sections on scaling TBD in distributed teams and OSS-specific adaptations.
- **Stars:** ~300+ | Language: N/A (curated list)

To dive deeper, clone these repos and run `git log --graph --oneline main` to visualize the trunk's linear history (minimal branching). Pair with tools like GitHub Actions for CI on main. For broader inspiration, check trunkbaseddevelopment.com, which references scaled OSS-like setups at Google/Facebook. Start with Flipt if you're into Go/infra—it's the most production-ready example.

References:

- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- [GitHub Topics: trunk-based-development](https://github.com/topics/trunk-based-development)
- [Awesome Trunk-Based Dev](https://github.com/cgbystrom/awesome-trunk-based-dev)
- [Flipt on X](https://x.com/devhunt_/status/1720093931902554448)
- [Ripissue on X](https://x.com/gubasso777/status/1811602748523102598)
