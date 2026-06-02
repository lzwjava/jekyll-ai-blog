---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dry Run CLI Design Nuance
translated: false
type: note
---

**Question:** Is `--dry-run` a poor practice in CLI tools? We rarely use it, Git already protects us, and it makes code more complicated — so is it really only worth having for destructive commands like `rm -rf`?

**Answer:**

Your intuition is **partially right**, but the full picture is more nuanced. Here's a structured breakdown:

---

## `--dry-run` is NOT generally poor practice

It is actually considered a **standard CLI design pattern**. The CLI guidelines at clig.dev list `-n, --dry-run` as a standard flag name meaning "do not run the command, but describe the changes that would occur if the command were run."

---

## You're right that it has real costs

The downside is that the `--dry-run` flag pollutes the code a bit. In all the major phases, you need to check if the flag is set, and only print the action that will be taken without actually doing it.

So yes — it **does** add implementation complexity. This is a fair engineering tradeoff.

---

## But it fills a different role than Git

Git protects your **source code history**, not the **side effects** of running a command. `--dry-run` is valuable when a command:

- Uploads files to an SFTP server
- Sends emails / notifications
- Installs/removes system packages
- Syncs directories and deletes files
- Modifies a production database

Git doesn't protect you from those. A developer built a reporting application that reads a database, generates reports, zips them, uploads to SFTP, checks error responses, and sends notification emails — the `--dry-run` flag proved invaluable throughout development and testing, and was used many times a day.

---

## Your `rm -rf` instinct is correct — for one class of commands

CLI guidelines suggest: for "moderate" danger — bigger local changes like deleting a directory, a remote change, or a complex bulk modification that can't be easily undone — you usually want to prompt for confirmation, and consider giving the user a way to "dry run" the operation.

So dry-run is most justified when the operation is:

1. **Irreversible** (can't be undone by Git or any rollback)
2. **Broad in scope** (affects many files, records, or remote systems)
3. **Non-interactive** (runs in scripts, automation, CI/CD)

---

## When dry-run is probably overkill

- Simple read-only commands
- Operations that are already transactional and rollbackable
- Commands that already prompt for confirmation (`y/n`)
- Short scripts where you can just review the code itself

---

## The `ww update` case specifically

`ww update --dry-run` checks for available updates without pulling them. This is a **read-only preview** of what *would* change. This is a legitimately useful pattern — especially in automated pipelines where you want to **detect** if updates are available and alert, without blindly applying them. It's not about fear of `rm -rf`; it's about **controlled automation**.

---

## Summary

| Situation | Dry-run worthwhile? |
|---|---|
| Destructive ops (delete, overwrite) | ✅ Yes |
| Remote side effects (upload, email, deploy) | ✅ Yes |
| Automation / CI pipelines needing previews | ✅ Yes |
| Simple local ops covered by Git | ❌ Probably not |
| Commands with built-in `y/n` confirmation | ❌ Probably not |

The `--dry-run` flag is not for every situation, but when it fits — particularly for command-driven tools that may create changes — it can be quite useful.

**References:**

- [CLI Guidelines — clig.dev](https://clig.dev/)
- [In Praise of --dry-run — Henrik Warne's Blog](https://henrikwarne.com/2026/01/31/in-praise-of-dry-run/)
- [CLI Tools That Support Previews — Nick Janetakis](https://nickjanetakis.com/blog/cli-tools-that-support-previews-dry-runs-or-non-destructive-actions)
- [How to Use --dry-run in Linux — OSTechNix](https://ostechnix.com/linux-dry-run-flag-guide-beginners/)
