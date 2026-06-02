---
audio: false
generated: true
image: false
lang: en
layout: post
title: DMIT Firewall ACL Location Guide
translated: false
type: note
---

**Question:** Why can't I find the firewall / ACL section in DMIT.io control panel to open ports 13000-14000, even though I already allowed them in UFW?

**Answer:**

DMIT.io advertises a customizable front-end (external) firewall with ACL rules for all cloud VM instances, but based on current public information and user reports, the exact location and interface for managing these ACL rules in the client control panel may not be prominently visible or could be under a different label than expected (e.g., not always called "Firewall" or "ACL Rules" directly on the main instance page).

Here are the most likely reasons you can't find it and steps to resolve:

1. **Check the correct location in the control panel**
   - Log in to https://www.dmit.io/ or your billing/client area (SolusVM, custom panel, or WHMCS-based portal).
   - Go to **Services** → **My Services** → select your specific cloud instance/VM.
   - Look for tabs or sections like:
     - "Firewall"
     - "Security"
     - "Network"
     - "ACL"
     - "Protection" / "DDoS Protection" / "Front Firewall"
     - "Advanced" or "Additional Features"
   - Some providers hide advanced firewall options under a "Manage" or "Console" button, or in a separate "Security Group" area. If it's not there, it may only appear after certain conditions (e.g., after enabling DDoS protection or on specific plans).

2. **The external firewall might be disabled by default or minimal**
   - On some DMIT plans, the front firewall starts with very permissive rules (allow most inbound) or is mainly for DDoS filtering rather than granular port control.
   - If no custom ACL interface shows, the provider might not offer user-configurable inbound port restrictions beyond basic DDoS settings — meaning external ports are open by default unless blocked by their anti-DDoS layer.

3. **Your issue is almost certainly NOT the DMIT external firewall**
   - You already ran:
     ```
     sudo ufw allow 13000:14000/tcp
     sudo ufw allow 13000:14000/udp
     sudo ufw reload
     ```
     But then saw: **Firewall not enabled (skipping reload)**
   - This means **UFW is currently disabled/inactive** on your VPS. No rules (even allowed ones) are being enforced because the firewall isn't running.
   - **Fix this first** — it's the most common reason ports remain blocked even after adding rules:
     ```
     sudo ufw enable
     ```
     Answer "y" to the prompt (it warns about possibly disrupting SSH — make sure you have console access via the DMIT panel in case of lockout).
     Then reload again:
     ```
     sudo ufw reload
     ```
     Verify status:
     ```
     sudo ufw status verbose
     ```
     You should now see your 13000:14000 rules listed as ALLOW and the firewall as "active".

4. **Test connectivity after enabling UFW**
   - From an external machine, try:
     `telnet your-vps-ip 13000` (or use `nc -zv your-vps-ip 13000` for TCP)
     If it connects, the port is open.
   - If still closed → double-check you're testing the correct public IP (run `curl ifconfig.me` on the VPS).

5. **If you still need/want to configure the DMIT front firewall**
   - Submit a support ticket directly through the client area (under "Support" or "Open Ticket"). Ask:
     "How can I access and configure the customizable front firewall ACL rules for my instance to allow/deny specific inbound ports or ranges?"
   - DMIT support is generally helpful for these questions and can guide you to the exact panel section (or confirm if it's not user-editable on your plan).

**Summary**
- Enable UFW first (`sudo ufw enable`) — that's blocking your ports right now, not DMIT's side.
- The DMIT external ACL interface exists per their site but may be hard to locate or limited; use support if needed.
- Opening a large range like 1000 ports to 0.0.0.0/0 is risky — restrict source IPs if your application allows it.

**References:**

- [DMIT Official Website (mentions customizable ACL front firewall)](https://www.dmit.io/)
