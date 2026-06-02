---
audio: false
generated: true
image: false
lang: en
layout: post
title: Security Audit Report for Proxy Server
translated: false
type: note
---

============================================================
  SECURITY AUDIT REPORT: DMIT Proxy Server
  Date: 2026-05-24
============================================================

SERVER:
  Host:          DMIT Los Angeles (Host-By.DMIT.com)
  IP:            [REDACTED]
  Domain:        [REDACTED]
  OS:            Ubuntu (44 days uptime)
  Disk:          20G (46% used)

============================================================
EXPOSED PORTS
============================================================

  TCP:
    22    SSH    OpenSSH 9.6p1 Ubuntu
    80    HTTP   (ACME challenge only)

  UDP:
    443   QUIC   Hysteria2 proxy
    5353  mDNS   openclaw-gateway (see below)

  Firewall: UFW active, default deny inbound ✓
  All other ports: filtered (silent drop)

============================================================
SSH CONFIGURATION
============================================================

  GOOD:
    ✓ Pubkey-only authentication
    ✓ Root login: without-password (key only)
    ✓ Password authentication: disabled
    ✓ MaxStartups: 10:30:100
    ✓ Host keys: ECDSA + ED25519
    ✓ Modern KEX: sntrup761x25519 (post-quantum), curve25519
    ✓ Strong ciphers: chacha20-poly1305, aes256-gcm
    ✓ ETM MACs preferred
    ✓ Terrapin mitigation (kex-strict-s-v00)

  CONCERN:
    ⚠ LoginGraceTime 120s (recommend 30s)
    ⚠ 3 authorized keys for root — audit who has access
    ⚠ OpenSSH 9.6p1 in regreSSHion range (CVE-2024-6387)
      — Verify Ubuntu has patched: dpkg -l openssh-server
      — Exploit practically infeasible on 64-bit

============================================================
HYSTERIA2 PROXY
============================================================

  FIXED (this session):
    ✓ v2.7.1 → v2.9.2 (latest, 2026-05-23 build)
    ✓ Running as `hysteria` user (was root)
    ✓ Managed by systemd, enabled on boot
    ✓ Security sandboxing active (CapabilityBoundingSet,
      NoNewPrivileges)
    ✓ Config permissions 640 root:hysteria (was 644)

  CURRENT STATE:
    Version:      v2.9.2
    Listen:       UDP :443
    Auth:         password [REDACTED]
    TLS cert:     Let's Encrypt ([REDACTED])
    Masquerade:   proxy → [REDACTED]
    Systemd:      enabled + active ✓
    Auto-restart: yes ✓

  REMAINING:
    ⚠ ACME email is placeholder — change to real email
    ⚠ Backup binary at hysteria.bak.v2.7.1 — safe to
      remove after confirming stability

============================================================
OTHER SERVICES
============================================================

  openclaw-gateway:
    PID:     726
    User:    root
    Listen:  UDP 0.0.0.0:5353 (mDNS)
    Status:  Running, exposed on all interfaces

    ⚠ Running as root
    ⚠ mDNS exposed publicly (should be localhost-only
      if only used locally)
    → Investigate whether this needs to be on this server

  qemu-guest-agent:  running (DMIT VM agent, normal)
  watchdog:          running (system watchdog, normal)

============================================================
VULNERABILITY SUMMARY
============================================================

  FIXED THIS SESSION:
    [✓] Hysteria2 running as root in tmux
        → Now hysteria user via systemd
    [✓] Outdated binary (v2.7.1)
        → Upgraded to v2.9.2
    [✓] Config file world-readable (644)
        → Restricted to 640 root:hysteria

  OPEN:
    [!] openclaw-gateway as root on public mDNS
    [~] ACME email placeholder
    [~] fail2ban not installed
    [~] No automatic security updates (unattended-upgrades)
    [~] Stale UFW rules (ports 13000-14000)
    [~] SSH LoginGraceTime 120s

============================================================
RECOMMENDED NEXT STEPS
============================================================

  1. Investigate openclaw-gateway — what is it, does it
     need to run here, can it run as non-root?

  2. Install fail2ban:
     apt install fail2ban && systemctl enable --now fail2ban

  3. Update ACME email in /etc/hysteria/config.yaml

  4. Remove stale UFW rules:
     ufw delete allow 13000:14000/tcp
     ufw delete allow 13000:14000/udp

  5. Enable auto-updates:
     apt install unattended-upgrades

  6. Reduce SSH LoginGraceTime to 30s

============================================================
SCORE
============================================================

  Before fixes:  4/10
  After fixes:   7/10

  The critical issues (root process, no systemd, outdated
  binary) are resolved. Remaining items are hardening
  measures. Server is solid for its purpose.

============================================================
