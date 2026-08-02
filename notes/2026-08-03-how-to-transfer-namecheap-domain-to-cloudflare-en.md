---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Transfer Namecheap Domain to Cloudflare
translated: false
type: note
---

Question: How do I transfer a domain from Namecheap to Cloudflare (registrar transfer, not just DNS)?

Answer:

Two phases: (1) move DNS to Cloudflare first, (2) transfer registration. Cloudflare requires the zone to be **active on Cloudflare** before it'll accept an auth code — you can't transfer registration first.

**Phase 1 — DNS cutover**

```
1. cloudflare.com → Add a site → enter domain → Free plan
2. Review auto-scanned DNS records, fix/add missing ones (MX, TXT/SPF, etc.)
3. Namecheap dashboard → Domain List → Manage → Nameservers → Custom DNS
   → set the two nameservers Cloudflare gave you (e.g. <NS1>.cloudflare.com, <NS2>.cloudflare.com)
4. If DNSSEC is on at Namecheap, disable it first (remove DS record) — mismatched
   DS records will break resolution once nameservers point at Cloudflare
5. Wait for Cloudflare dashboard to show zone status "Active" (usually mins, up to 24h)
```

**Phase 2 — Registrar transfer** (only after zone is Active)

```
1. Domain must be >60 days old at current registrar, unlocked, no pending renewal
2. Namecheap → Domain List → Manage → Sharing & Transfer → unlock domain
3. Same page → request/reveal Auth Code (EPP code), sent to registrant email
4. Cloudflare dashboard → Domain Registration → Transfer Domains → enter domain
5. Paste Auth Code → confirm/verify WHOIS contact info → pay (Cloudflare charges
   at-cost, no markup — usually just the ICANN + registry fee, ~$9-15/yr depending on TLD)
6. Namecheap emails you a transfer confirmation link → click Approve (don't ignore it,
   silence = auto-approve after ~5 days at registry level, but don't rely on that)
7. Transfer completes within a few hours to 5 days
```

Gotchas that bite people:

- WHOIS privacy sometimes needs to be temporarily off depending on registrar (Namecheap usually fine, but check).
- If you skip Phase 1, Cloudflare's "enter auth code" field is literally disabled until zone status = Active.
- Keep Namecheap NS as fallback in a notepad until transfer fully completes — if it fails mid-transfer you don't want to lose DNS control too.

References:

- [Transfer your domain to Cloudflare — Cloudflare Registrar docs](https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/)
- [How to transfer a domain name — Cloudflare Learning Center](https://www.cloudflare.com/learning/dns/how-to-transfer-a-domain-name/)
- [Namecheap to Cloudflare Domain Transfer walkthrough](https://syahnurnizam.com/articles/2025/07/how-to-transfer-your-domain-name-from-namecheap-to-cloudflare/)
