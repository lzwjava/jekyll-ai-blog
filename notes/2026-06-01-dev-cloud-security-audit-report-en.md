---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dev Cloud Security Audit Report
translated: false
type: note
---

Got everything. Here's the full report:

```
================================================================
  SECURITY AUDIT REPORT — 129.212.187.36
  AMD Dev Cloud MI300X Droplet
  Scan date: 2026-06-01 12:42 CST
================================================================

OPEN PORTS (from outside)
─────────────────────────────────────────────
  22/tcp   OPEN   SSH (OpenSSH 9.6p1 Ubuntu)
  80/tcp   OPEN   HTTP (Caddy, returns 502)
  All other common ports: CLOSED

INTERNAL-ONLY SERVICES (not exposed)
─────────────────────────────────────────────
  127.0.0.1:5000   amd-metrics-exp (GPU metrics)
  127.0.0.1:2019   Caddy admin API
  *:6601           amd-metrics-exp (blocked by UFW)
  *:50061          gpuagent (blocked by UFW)

FIREWALL (UFW — active)
─────────────────────────────────────────────
  22/tcp    LIMIT    (rate-limited, good)
  80/tcp    ALLOW    (open to world)
  443       ALLOW    (open to world)
  6601      DENY     (metrics blocked)
  50061     DENY     (gpuagent blocked)
  Default:  INPUT policy ACCEPT (dangerous — see below)

FAIL2BAN:  ACTIVE ✓

================================================================
  FINDINGS
================================================================

 [CRITICAL] Root login enabled with no password auth
 ────────────────────────────────────────────────────
  PermitRootLogin yes
  Only pubkey auth works (PasswordAuthentication not set,
  defaults to yes on Ubuntu). If someone adds a password
  or the pubkey leaks, root is fully compromised.

  FIX: Set "PermitRootLogin prohibit-password" or "no"
       Create a non-root user, disable root SSH.

 [HIGH] Only root has a shell
 ────────────────────────────────────────────────────
  Only root:x:0:0 has /bin/bash. Everything runs as root.
  Any service compromise = instant full root.

  FIX: Create a regular user, use sudo.

 [HIGH] HTTP port 80 open to world (Caddy 502)
 ────────────────────────────────────────────────────
  Caddy is running but returns 502 Bad Gateway — no
  backend is configured. Attack surface for:
  - Caddy version fingerprinting
  - Future proxy misconfig
  - Admin API exposure (currently localhost-only, good)

  FIX: If not needed, block port 80 in UFW.

 [MEDIUM] INPUT policy is ACCEPT
 ────────────────────────────────────────────────────
  UFW is active but iptables INPUT default is ACCEPT.
  Any port not explicitly denied is reachable if a
  service binds to 0.0.0.0. The DENY rules for 6601/50061
  are doing the heavy lifting.

  FIX: ufw default deny incoming

 [MEDIUM] X11 Forwarding enabled
 ────────────────────────────────────────────────────
  Unnecessary for a headless GPU server. Minor attack
  surface for X11-based exploits.

  FIX: Set "X11Forwarding no" in sshd_config.

 [LOW] SSH banner reveals OS and version
 ────────────────────────────────────────────────────
  SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.16
  Tells attackers exact version to search CVEs for.

  FIX: Minor risk — keep OpenSSH patched.

 [LOW] Ports 6601/50061 bound to 0.0.0.0
 ────────────────────────────────────────────────────
  Services bind to all interfaces but UFW blocks them.
  If UFW is ever disabled, these are immediately exposed.

  FIX: Bind to 127.0.0.1 if not needed externally.

 [GOOD] Fail2ban is active
 [GOOD] SSH uses pubkey auth (no password prompt)
 [GOOD] GPU metrics / agent ports are UFW-denied
 [GOOD] Caddy admin API is localhost-only

================================================================
  ATTACK SIMULATION SUMMARY
================================================================

  If IP leaks, an attacker sees:
    1. SSH on port 22 — can attempt brute force (limited
       by fail2ban + UFW rate limit). Key-only auth blocks
       password attacks. But root login is allowed.
    2. HTTP on port 80 — Caddy fingerprint, 502 error.
       No app to exploit right now.
    3. Everything else — closed.

  Risk level: MODERATE
  The machine is not wide open, but root SSH + ACCEPT
  default policy means one misconfiguration = game over.

================================================================
  TOP 3 FIXES (10 minutes total)
================================================================

  1. Disable root SSH login:
     sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
     systemctl restart sshd

  2. Default deny incoming:
     ufw default deny incoming
     ufw reload

  3. Block HTTP if unused:
     ufw deny 80/tcp
     ufw reload
```

**Bottom line:** If the IP leaks, the attack surface is small (SSH + dead HTTP), but the **root login + permissive default policy** is the real risk. Fail2ban buys you time, but a determined attacker with a leaked key or a 0-day in OpenSSH 9.6 has a direct path to root on a $2/hr MI300X machine.

Want me to apply the hardening fixes?
