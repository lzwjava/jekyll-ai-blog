---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Scripts Over Direct Upgrades
translated: false
type: note
---

Question: Is it better to let an LLM help write scripts for Ubuntu release upgrades, rather than having the LLM directly perform the `do-release-upgrade` process?

Answer:

Yes — and your intuition is spot-on. Here's a thorough breakdown of **why `do-release-upgrade` is unsuitable for direct LLM execution**, and **where an LLM genuinely shines** in this workflow.

---

## Why `do-release-upgrade` Is Hard for an LLM to "Do"

`do-release-upgrade` is not a single command — it is a **complex, stateful, interactive orchestration process**. Here's what it actually involves:

### 1. Interactive Prompts at Unpredictable Points

During the upgrade, the tool presents diffs and asks you what to do with modified config files — for example, whether to keep your version of `/etc/ssh/sshd_config` or install the package maintainer's version. These prompts cannot be fully predicted or automated ahead of time without knowing the system's state.

### 2. Multi-Stage Process That Requires Monitoring

The release upgrade is an interactive process that will sometimes stop and ask questions, so you should monitor the upgrade and be available to respond. An LLM cannot reliably "stay present" across a process that may take 30–60+ minutes.

### 3. Dynamic Dependency Resolution

When you run the command, it checks if a new release is available, guides you through the upgrade, resolves package dependencies, and removes obsolete or conflicting software. This resolution is environment-specific and cannot be predicted generically.

### 4. Third-Party PPA Handling

Third-party software repositories and PPAs are disabled during the release upgrade. While software installed from these sources will not be removed, they are the most common cause of upgrade issues. Dealing with these requires knowledge of the specific system.

### 5. SSH Backup Port for Remote Upgrades

If you changed SSH to a non-default port, `do-release-upgrade` opens a second SSH server on port 1022 as a backup in case the main SSH service restarts during the upgrade. This kind of runtime side-effect is hard for an LLM to manage live.

### 6. Recovery From Failures

If apt is in a bad state, you need to run `sudo dpkg --configure -a` followed by `sudo apt --fix-broken install` before retrying the upgrade. Failure modes are diverse and system-specific.

---

## Where an LLM Genuinely Helps: Script Writing

An LLM is excellent at **producing well-structured, repeatable, documented scripts** that a human (or CI/CD pipeline) can review and run. Here is what an LLM can reliably help with:

### Pre-Upgrade Preparation Script

```bash
#!/bin/bash
# Pre-upgrade checklist script (LLM-generated)
set -e

echo "=== Step 1: Update current packages ==="
sudo apt update && sudo apt dist-upgrade -y

echo "=== Step 2: Check if reboot is required ==="
if [ -f /run/reboot-required ]; then
  echo "Reboot required before upgrade. Please reboot and re-run."
  exit 1
fi

echo "=== Step 3: Check disk space ==="
df -h /

echo "=== Step 4: Install upgrade manager ==="
sudo apt install -y update-manager-core

echo "=== Step 5: Backup sources.list ==="
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

echo "=== Ready for: sudo do-release-upgrade ==="
```

### Post-Upgrade Cleanup Script

```bash
#!/bin/bash
# Post-upgrade cleanup (LLM-generated)

echo "=== Remove obsolete packages ==="
sudo apt autoremove -y

echo "=== Re-enable PPAs (review list manually) ==="
ls /etc/apt/sources.list.d/

echo "=== Verify new release ==="
lsb_release -a

echo "=== Remove SSH backup rule if added ==="
sudo ufw delete allow 1022/tcp 2>/dev/null || true
```

---

## The Right Mental Model

| Task | LLM Role |
|---|---|
| Understanding what `do-release-upgrade` does | ✅ Explain thoroughly |
| Writing pre/post-upgrade shell scripts | ✅ Very well suited |
| Generating checklists and runbooks | ✅ Very well suited |
| Answering config file conflict questions | ✅ With context |
| Actually running `do-release-upgrade` live | ❌ Not reliable — interactive, stateful, long-running |
| Handling mid-upgrade failures autonomously | ❌ Too environment-specific |

---

## Summary

`do-release-upgrade` is a **battle-tested orchestration tool** built by Canonical with years of edge-case handling baked in. It becomes less predictable when your system has heavy third-party customization, unusual package selections, or custom-compiled software — in those cases, more manual review of each step is warranted. The best use of an LLM here is as a **script author, checklist generator, and advisor** — not as a live operator. You run the scripts; the LLM helps you write them well.

References:

- [Ubuntu Server Upgrade Documentation](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/)
- [How to Upgrade Ubuntu Server Using do-release-upgrade](https://oneuptime.com/blog/post/2026-03-02-upgrade-ubuntu-server-do-release-upgrade/view)
- [Understanding the do-release-upgrade Command](https://knowledge.buka.sh/understanding-the-do-release-upgrade-command-in-ubuntu-a-beginners-guide/)
