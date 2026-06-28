---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH server setup on Fedora
translated: false
type: note
---

Question: Explain what this bash script does, line by line.

Answer:

This sets up SSH access on a Fedora/RHEL-family Linux box (uses `dnf`, so not Debian/Ubuntu).

```bash
# Install the OpenSSH server package (the daemon that accepts incoming SSH connections)
sudo dnf install -y openssh-server
```
`dnf` is the package manager. `openssh-server` provides `sshd`. The `-y` auto-confirms. Note: `openssh-clients` (the `ssh` command for *outgoing* connections) is usually already installed — this is the *server* side, so other machines can connect *in*.

```bash
# Enable the service at boot AND start it immediately, in one command
sudo systemctl enable --now sshd
```
`enable` creates the symlink so `sshd` launches on every boot. `--now` also starts it this instant, saving you a separate `systemctl start sshd`. Without `--now`, it'd be enabled but not running until reboot.

```bash
# Verify the daemon is active (look for "active (running)")
sudo systemctl status sshd
```
Shows state, PID, recent log lines. Exit code is 0 if running, non-zero otherwise — useful in scripts via `systemctl is-active sshd`.

```bash
# Print the machine's IP addresses so you know where to SSH to
ip addr show | grep "inet "
```
`ip addr show` dumps all interfaces. `grep "inet "` (trailing space) filters to IPv4 lines only — excludes `inet6`. You'll see something like `inet <IP_ADDRESS>/24` on your LAN interface (e.g. `eth0`/`enp3s0`) plus `127.0.0.1` for loopback. The LAN one is what you connect to.

Then from another machine: `ssh user@<IP_ADDRESS>`.

A few things the script omits that matter in practice:

- **Firewall.** Fedora ships `firewalld` enabled by default, which will block port 22 even with `sshd` running. Add: `sudo firewall-cmd --add-service=ssh --permanent && sudo firewall-cmd --reload`.
- **Cleaner IP lookup.** `ip -4 -br addr` gives a one-line-per-interface summary, or `hostname -I` prints just the IPs space-separated — easier to script around than grepping `ip addr`.
- **Confirm it's listening.** `sudo ss -tlnp | grep :22` proves `sshd` actually bound to the port, which is stronger evidence than `systemctl status`.

For your setup (`lzw@192.168.1.36`), once this runs and the firewall rule is added, you'd reach it from the Air with `ssh lzw@192.168.1.36`. Drop an SSH key in with `ssh-copy-id` to skip password auth entirely.
