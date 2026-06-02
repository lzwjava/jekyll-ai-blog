---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upgrade glibc with PostgreSQL running
translated: false
type: note
---

Question: Should I answer "Yes" or "No" when upgrading glibc while PostgreSQL is running?

Answer:

## Answer: **Yes** — but only after understanding what will happen

This dialog is from the `libc6` (glibc) upgrade process on a Debian/Ubuntu system. Here's what you need to know:

### What the dialog is telling you

- glibc (the GNU C Library) is a core system library used by almost every program.
- Services using NSS (Name Service Switch) — including **PostgreSQL** — need to be restarted after the upgrade to pick up the new library.
- The installer **detected PostgreSQL is running** and is warning you it cannot restart it automatically.

---

### If you answer **Yes**

- The upgrade proceeds immediately.
- PostgreSQL will **continue running** but against the old in-memory glibc.
- You **must manually restart PostgreSQL** afterward:

  ```bash
  sudo systemctl restart postgresql
  ```

- This is the **recommended choice** in most cases if you are okay restarting PostgreSQL right after.

---

### If you answer **No**

- The upgrade is **paused/aborted**.
- You can manually stop PostgreSQL first:

  ```bash
  sudo systemctl stop postgresql
  ```

- Then re-run the upgrade:

  ```bash
  sudo apt-get upgrade
  ```

- Choose this if you need a **controlled maintenance window** or cannot afford any risk of PostgreSQL instability during the upgrade.

---

### Recommendation

| Scenario | Answer |
|---|---|
| Dev/test server, okay to restart PostgreSQL | **Yes** |
| Production server, need zero risk | **No** (stop PostgreSQL first, then re-run) |
| Active connections/transactions running | **No** |
| No active DB connections | **Yes** |

> ⚠️ After answering **Yes**, always remember to run `sudo systemctl restart postgresql` immediately after the upgrade completes.
