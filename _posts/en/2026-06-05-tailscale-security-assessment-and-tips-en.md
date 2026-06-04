---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale Security Assessment and Tips
translated: false
type: note
---

**Question:** Is my Tailscale setup safe?

**Answer:**

Yes, fundamentally sound. Your setup follows the security model correctly:

**What's secure:**
- **WireGuard encryption** — Tailscale's tunnel is cryptographically solid, peer-to-peer, with forward secrecy. Traffic between your Mac and workstation is encrypted end-to-end by default.
- **Public key SSH auth** — you're using the strongest SSH auth mechanism. No password exposure surface.
- **No inbound exposure** — machines behind NAT are unreachable from the public internet without being part of your tailnet. Tailscale handles NAT traversal internally.
- **Automatic updates** — Tailscale keeps key exchange updated; version mismatch between 1.96.4 and 1.98.x is operationally fine (WireGuard protocol is stable).

**Realistic risks to consider:**

1. **Tailscale account compromise** — if `lzwjava@` credentials leak or Tailscale's backend is breached, an attacker can hijack your tailnet. Mitigate: use a strong passphrase, enable 2FA if Tailscale supports it, rotate auth keys periodically.

2. **Workstation compromise** — if your Ubuntu box (where `tailscaled` runs) is breached, the attacker has access to your private WireGuard key and can impersonate your workstation. Mitigation: keep Ubuntu patched, firewall non-Tailscale ports, run minimal services.

3. **SSH key compromise** — if your SSH private key (used for `ssh lzw@<workstation-ip>`) is stolen from your Mac, the attacker can SSH in. Mitigation: use an SSH agent, consider Ed25519 keys with passphrase protection, monitor `.ssh/authorized_keys` on the workstation for unauthorized additions.

4. **Tailscale's infrastructure** — you're trusting Tailscale Inc. for coordination. They can theoretically see metadata (which devices connect, rough timing). They cannot see encrypted traffic content. This is acceptable for home/personal use; if you run sensitive business workloads, self-hosting WireGuard is the alternative.

**Quick wins:**
- Update both machines to latest Tailscale (`brew upgrade tailscale` on Mac, `sudo apt upgrade tailscale` on Ubuntu).
- Enable MagicDNS in the Tailscale admin console — cleaner than remembering IPs and reduces typos that could hit wrong machines.
- Lock down SSH on your workstation: disable password auth in `/etc/ssh/sshd_config` (you already are, but verify), restrict to public key only.
- Review `~/.ssh/authorized_keys` on the workstation — ensure only your keys are there.

**Bottom line:** Your setup is safer than exposing SSH directly to the internet or using password-based VPNs. It's operationally sound for AI/ML work. The weakest link is human error (losing your passphrase, SSH key carelessness) — not the protocol.
