---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ubuntu Upgrade Tool Pros and Risks
translated: false
type: note
---

**Question:** Is `do-release-upgrade` a good tool for upgrading Ubuntu?

**Answer:**

Based on your log output, you are upgrading to **Ubuntu 24.04 LTS "Noble Numbat"** from a previous Ubuntu version (likely 22.04 "Jammy"). Here is a comprehensive assessment of `do-release-upgrade` and what to expect:

---

## What is `do-release-upgrade`?

It is Ubuntu's official in-place release upgrade tool. Ubuntu recommends using the `do-release-upgrade` command on Server editions and cloud images, as it can handle system configuration changes that are sometimes needed between releases.

---

## Is it "great"? — The Honest Assessment

### ✅ Pros

- **Official and well-tested**: It is the canonical way to upgrade Ubuntu without a full reinstall.
- **Handles config merges**: It prompts you when your customized config files (like `sshd_config`) differ from new defaults, giving you a choice to keep or replace them.
- **SSH safety net built in**: As seen in your log, it starts an extra SSH daemon on port **1022** — so even if your main SSH connection drops, you can reconnect via the fallback.
- Before making any changes, `do-release-upgrade` first does checks to verify the system is ready to upgrade, and provides a summary before proceeding.
- For a fairly standard server setup, the whole process typically takes around 20–30 minutes.

### ⚠️ Caveats / Risks

- **Running over SSH is risky**: As clearly warned in your log, if your SSH connection drops mid-upgrade, recovery becomes harder. The tool mitigates this by opening port 1022, but you should have a console/recovery option (like a VPS provider's web console or IPMI).
- **Config conflicts require attention**: There can be merge conflicts between your old customized config and the new defaults — for example, between your `sshd_config` and `journald.conf`. You need to decide which version to keep.
- **Third-party PPAs get disabled**: Third-party software repositories and PPAs are disabled during the release upgrade. While software installed from these sources will not be removed, this is the most common cause of upgrade issues.
- **You inherit old defaults**: In-place upgrades mean you will likely inherit the less-secure defaults from the old OS. For example, if SSH was configured with an older protocol version, the upgrade will not automatically enforce newer security defaults.
- **Disk space needed**: A release upgrade involves downloading hundreds of new packages, which can be several gigabytes. Make sure you have enough free disk space and dedicate time to monitor the interactive process.

---

## What You Are Upgrading To (Ubuntu 24.04 Noble)

Anyone upgrading from Ubuntu 22.04 to 24.04 inherits a cumulative change-set that enhances and expands the desktop and server experience built up over 2 years.

Ubuntu 24.04 LTS is the recommended choice for virtually all server workloads, offering a 5-year support window, extensive testing, and broad compatibility with tools like Kubernetes, Docker, and Ansible.

---

## Bottom Line

`do-release-upgrade` is **solid and reliable** for most cases — especially if you have a recovery fallback (console access, backups). It is not "perfect" — edge cases like custom PPAs, modified configs, and mirror-specific quirks (like the `Missing Signed-By` error noted in community reports) can require manual cleanup after. But for a standard system, it works well and is far better than manually reinstalling from scratch.

---

**References:**

- [Ubuntu Official Upgrade Guide](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/)
- [Real-world do-release-upgrade Experience (22.04 → 24.04)](https://waldenperry.com/ubuntu-do-release-upgrade-experience/)
- [5 Options for Ubuntu 20.04 EOL - In-place Upgrade Pros/Cons](https://www.dogsbody.com/blog/5-options-for-ubuntu-20-04-eol-in-april-2025/)
- [Ubuntu 24.04 LTS: 20 Major Changes](https://www.omgubuntu.co.uk/2024/04/ubuntu-24-04-lts-20-changes-to-look-out-for)
- [Ubuntu Release Cycles: LTS vs Interim](https://oneuptime.com/blog/post/2026-03-02-ubuntu-release-cycles-lts-vs-interim/view)
