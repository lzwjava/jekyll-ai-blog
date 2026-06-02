---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sync Spring UAT Branches & Code
translated: false
type: note
---

Here’s a collection of best practices and patterns you can mix-and-match to keep your three UAT branches in sync, keep your history clean, and handle country-specific code in a Spring app—plus a bit on where AI can help.

---

## 1. Branching & synchronization

1. **Trunk-based with short-lived feature branches**

   * Keep a single **main** (or **develop**) branch.
   * For each Jira ticket (e.g. FT-103) and country, create feature branches named:

     ```
     feature/FT-103-cn
     feature/FT-103-sg
     feature/FT-103-tw
     ```
   * When work is ready, merge back into **main**, then cherry-pick or merge into each `uat_cn`, `uat_sg`, `uat_tw`.
   * Benefit: merges into main happen once; country branches only pick up what they need.

2. **Regular syncing of UAT branches**

   * Schedule a daily (or per-build) job to rebase each `uat_*` onto `main` so they don’t drift too far.
   * Automate it in CI (e.g. a GitHub Action that rebases `uat_cn` every night).

3. **Use pull-requests + review enforcement**

   * Require a PR for every feature-branch → main merge.
   * Ensure the “FT-xxx” ticket is in the branch name and in the PR title/description.

---

## 2. Commit-message conventions & squashing

1. **Conventional-style with JIRA key**

   ```
   FT-103: fix null-pointer in customer lookup
   ```

2. **Micro-commit → squash at merge time**

   * During feature work, developers commit as they go:

     ```
     FT-103 #1: initial wiring of service beans
     FT-103 #2: add validation logic
     FT-103 #3: update error handling
     ```
   * On PR merge, use “Squash and merge” to collapse all FT-103 commits into one concise commit:

     ```
     FT-103: customer-service validation and error handling
     ```

3. **Numbering within a ticket**

   * If tracking multiple distinct steps in the same ticket, numbering (`#1`, `#2`) is fine during dev.
   * Once merged, squash everything into a *single* FT-103 commit; the history stays tidy and each ticket is one logical change.

4. **Automate commit-lint**

   * Use a Git hook or CI plugin (e.g. [commitlint](https://commitlint.js.org)) to enforce `FT-\d+` at the start of every message.
   * Optionally enforce a scope: `FT-103(sg): …`.

---

## 3. Handling country-specific code in Spring

1. **Profiles & conditional beans**

   * Define a Spring profile per country: `@Profile("cn")`, `@Profile("sg")`, `@Profile("tw")`.
   * In `application-cn.yml`, `application-sg.yml`, etc., set country-specific properties.
   * At startup, pass `--spring.profiles.active=cn` (or sg, tw) to pick the right beans.

2. **Strategy pattern / plugin modules**

   * Create an interface `PaymentProcessor` with three implementations (`CnPaymentProcessor`, etc.).
   * Use `@Component` + `@Profile` or a factory that picks the bean based on a runtime flag.

3. **Resource bundles / feature flags**

   * If differences are small (e.g. date formats, endpoint URLs), keep one code path and externalize differences in property files or a feature-flag service.

4. **Separate modules (if large)**

   * For very divergent logic, split into sub-modules:

     ```
     /core
     /country-cn
     /country-sg
     /country-tw
     ```
   * The main app pulls in only the active country module at build/deploy time.

---

## 4. Separating tasks by author vs by ticket

* **By ticket, not author.** Tasks should be unitized around *features* (Jira IDs), not the person.
* If multiple devs work on FT-103, they collaborate on the same branch or use topic branches off of it—but ultimately merge back into the single FT-103 branch.
* Author metadata stays in the commit author field; you don’t need to squash by author.

---

## 5. Putting AI to work

1. **Commit-message generation**

   * Tools like GitHub Copilot or OpenAI can suggest clean, conventional commit messages from your diff.
   * Integrate a pre-commit hook that runs `ai-commit --preview` to draft the message for review.

2. **PR description & changelog**

   * Use an AI assistant to summarize all commits under a ticket into a coherent PR description or release note:

     > “Summarize the changes in feature/FT-103 into bullet points.”

3. **Code review assistance**

   * AI-powered linters (SonarQube with AI plugins, DeepCode) can point out issues in country-specific code paths.

4. **Automating cherry-picks/rebases**

   * Write a small script (or use a low-code platform) that, when FT-103 lands on `main`, automatically cherry-picks it into each `uat_*` and opens PRs for any merge conflicts.

---

### Putting it all together

1. **Develop on** `feature/FT-XXX-<cn/sg/tw>`.
2. **Commit freely** (numbered steps OK), referencing the JIRA key.
3. **Open a PR** → main; choose **Squash-and-merge** so that each FT-XXX is one clean commit.
4. **CI job** automatically rebases/merges that commit into each `uat_cn`, `uat_sg`, `uat_tw`.
5. **Spring profiles** at runtime pick the correct country logic—no code duplication in three branches.
6. **AI tools** help enforce commit style, summarize PRs, and manage merges.

This workflow keeps your history tidy, ensures each ticket is traceable to a single commit across all environments, separates country logic at runtime instead of in Git history, and leverages AI where it adds the most value.
