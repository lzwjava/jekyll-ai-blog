---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GitHub Actions Usage Limits Overview
translated: false
type: note
---

### GitHub Actions Usage Limits

GitHub Actions has tiered limits based on your plan (personal accounts or organizations). These include free monthly minutes for GitHub-hosted runners in private repositories and storage for artifacts. Public repositories and self-hosted runners don't consume these minutes. Limits reset monthly for minutes (storage is ongoing). Overages are billed automatically if you have a valid payment method; otherwise, jobs are blocked after hitting the limit.

#### Included Minutes and Storage by Plan

| Plan                          | Storage | Minutes (per month) |
|-------------------------------|---------|---------------------|
| GitHub Free (personal/org)   | 500 MB | 2,000              |
| GitHub Pro (personal)        | 1 GB   | 3,000              |
| GitHub Team (org)            | 2 GB   | 3,000              |
| GitHub Enterprise Cloud (org)| 50 GB  | 50,000             |

- **Minutes**: Count total job runtime on GitHub-hosted runners (partial time for failed jobs). Multipliers apply: Linux (1x), Windows (2x), macOS (10x). Anyone with write access to a repo uses the repo owner's allowance.
- **Storage**: Based on GB-hours of artifact storage (e.g., uploads/downloads). Logs and summaries don't count.

#### Overage Billing

If you exceed quotas:

- **Minutes**: Charged per extra minute (USD rates for standard Linux runners: $0.008/min; higher for Windows/macOS due to multipliers).
- **Storage**: Charged as GB-months (total GB-hours / 744 hours per month, rounded up).
- Example: On a Team plan, 5,000 extra minutes (3,000 Linux + 2,000 Windows) costs ~$56.

Without a payment method, usage stops at the quota. The error you saw ("recent account payments have failed or your spending limit needs to be increased") means either payments bounced or your **spending limit (budget)** is capping overages.

#### Spending Limits (Budgets)

- These are optional thresholds to control total monthly spend on Actions (and other metered features).
- If set too low, it blocks jobs before hitting quotas.
- **How to check/increase**:
  1. Go to GitHub Settings > Billing & plans.
  2. Under "Budgets and alerts," view or edit your budget for GitHub Actions.
  3. Increase the limit, add a payment method, or remove the budget entirely (unlimited overages, but monitor via alerts).
- Migrated accounts may have auto-generated budgets from old limits—update them to fit your usage.

For full details, check your account's billing dashboard for real-time usage.

[GitHub Actions Billing Documentation](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)
