---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Pro Plan Features Explained
translated: false
type: note
---

**Question:** What do each of the GitHub Pro plan features mean?

**Answer:**

Here is a plain-English explanation of every item listed on the GitHub Pro plan:

---

### ✅ Included Features

**1. Required Reviewers (in private repos)**
You can enforce that one or more specific people must approve a pull request before it can be merged. In Free, this is only available on public repos. Pro unlocks it for private repos too.

**2. Protected Branches (in private repos)**
You can lock important branches (e.g. `main`) so no one can push directly or merge without passing certain rules (like CI checks or required reviews). Again, Free only has this for public repos.

**3. Repository Insights (in private repos)**
A built-in analytics dashboard showing contributor activity, commit frequency, traffic, and code frequency graphs — useful for tracking project health in private repos.

**4. Wikis (in private repos)**
A built-in documentation wiki attached to your repo (like a lightweight knowledge base), unlocked for private repos. Free users can only use Wikis on public repos.

**5. Pages (in private repos)**
GitHub Pages lets you host a static website directly from a repository. Pro lets you do this for private repos; Free only allows it on public repos.

**6. Code Owners (in private repos)**
A `CODEOWNERS` file lets you designate who automatically gets tagged as a required reviewer when certain files or directories are changed in a PR. Unlocked for private repos on Pro.

**7. 3,000 Minutes for GitHub Actions**
GitHub Actions is the built-in CI/CD system (run tests, build, deploy automatically). Pro gives you **3,000 free minutes per month** on GitHub-hosted runners, vs. 2,000 on Free.

**8. 2GB of GitHub Packages Storage**
GitHub Packages is a package registry (host npm, Docker, Maven packages etc. alongside your code). Pro raises the storage limit to **2 GB**, vs. 500 MB on Free.

**9. 180 Core-Hours of Codespaces Compute**
GitHub Codespaces is a cloud-based VS Code dev environment — you spin up a fully configured machine in the browser. Pro includes **180 core-hours/month** (e.g., ~90 hours on a 2-core machine, ~45 hours on a 4-core machine).

**10. 20GB of Codespaces Storage**
The disk space available for your Codespaces environments (stored files, Docker layers, etc.) is **20 GB/month** on Pro.

---

### ❌ Not Included

**GitHub Copilot Pro**
Copilot (the AI code completion / chat assistant) is a **separate add-on subscription** — it is not bundled with the GitHub Pro account plan. As of 2026, Copilot Pro costs $10/month on top of your base plan, so you need to purchase it separately.

---

### Quick Summary Table

| Feature | GitHub Free | GitHub Pro |
| --- | --- | --- |
| Required reviewers | Public only | ✅ Private too |
| Protected branches | Public only | ✅ Private too |
| Wikis / Pages / Code Owners | Public only | ✅ Private too |
| Actions minutes | 2,000/mo | 3,000/mo |
| Packages storage | 500 MB | 2 GB |
| Codespaces compute | 120 core-hrs | 180 core-hrs |
| Codespaces storage | 15 GB | 20 GB |
| Copilot | ❌ (free tier only) | ❌ (paid add-on) |

---

**References:**

- [GitHub's Plans – GitHub Docs](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
- [GitHub Copilot Pricing 2026](https://nocode.mba/posts/github-copilot-pricing)
