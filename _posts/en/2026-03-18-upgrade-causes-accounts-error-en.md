---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upgrade Causes No Available Accounts Error
translated: false
type: note
---

**Question:** After upgrading to version 2.1.78, Claude starts reporting a "no available accounts" error. The "Claude Max" group has issues while "CC-逆向渠道B" works. What happened?

**Answer:**

The upgrade to version 2.1.78 (as shown in the example in the project's upgrade guide) pulled in recent changes from the main branch of the claude-relay-service. These updates include significant improvements to account routing, error handling, cooldown logic, and validation rules. This is the most likely cause of the sudden "no available accounts" error appearing only in the "Claude Max" group.

Key changes that triggered the issue (based on the latest releases around March 2026):
- Account blocking reasons are now surfaced clearly in the UI (previously hidden or misdiagnosed).
- Fixes for false 429 rate-limit flagging and 503 backoff behavior, plus configurable cooldown TTLs.
- Updates to how team accounts, 1M context flags (`allow1mContext`), and free-tier misidentification are handled — these can suddenly mark previously working accounts as unavailable.
- Removal of old hard restrictions on models/context windows, now relying on admin/API-key settings instead.

"Claude Max" is probably a group using official Anthropic OAuth accounts or a specific pool that got hit by the stricter/corrected validation. In contrast, "CC-逆向渠道B" (your reverse/proxy channel) uses a different set of accounts or proxy settings that were not affected by the same routing blocks.

The dashboard you shared shows very low usage ($0.1052 today) and recent timestamps (03/18/2026), which matches a fresh post-upgrade state where accounts may have been auto-flagged during the restart.

**How to fix it quickly:**
1. Go to the web management UI (usually `/web` on your server).
2. Select the "Claude Max" group → check the "routing-block reasons" column (it now shows exact error type, status code, and remaining cooldown).
3. Click "Reset Status" on affected accounts.
4. Verify each account's proxy settings and `allow1mContext` flag (if using 1M models).
5. Restart the service (`npm run service:restart:daemon`) and test again.

If the block reasons point to upstream Anthropic errors, you may need to add per-account cooldown overrides in `.env` or the Admin UI. The "CC-逆向渠道B" group continuing to work proves the core service is fine — only the "Claude Max" account pool needs attention.

This is a common post-upgrade behavior after the March 2026 account-management refactor; it is not a bug in your setup.

**References:**  
- [https://github.com/Wei-Shaw/claude-relay-service/blob/main/README_EN.md](https://github.com/Wei-Shaw/claude-relay-service/blob/main/README_EN.md)  
- [https://github.com/Wei-Shaw/claude-relay-service/releases](https://github.com/Wei-Shaw/claude-relay-service/releases)