---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ads.txt IDs Explained
translated: false
type: note
---

**Question:** Why do publishers need to add numeric/alphanumeric entries to ads.txt, and how does it work?

**Answer:**

## What is ads.txt?

`ads.txt` (Authorized Digital Sellers) is an IAB Tech Lab standard that lets publishers declare **which companies are authorized to sell their ad inventory**. It's a plain text file hosted at the root of your domain (e.g., `yourdomain.com/ads.txt`).

## What Do the Entries Mean?

Each line follows this format:

```
<domain>, <seller_ID>, <relationship>, <certification_ID>
```

Using your example:

```
google.com, pub-6168351539440296, DIRECT, f08c47fec0942fa0
```

| Field | Value | Meaning |
|---|---|---|
| Domain | `google.com` | The ad network/exchange authorized to sell |
| Seller ID | `pub-6168351539440296` | Your unique publisher account ID on that platform |
| Relationship | `DIRECT` or `RESELLER` | How the inventory is being sold |
| Certification ID | `f08c47fec0942fa0` | Optional TAG-certified ID to verify the seller |

## DIRECT vs RESELLER

- **DIRECT** — You have a direct contract with that ad system (e.g., you signed up with Google AdSense directly)
- **RESELLER** — A third party is authorized to resell your inventory through that platform (e.g., a header bidding partner)

## Why Are the IDs Alphanumeric/Long?

The IDs (like `pub-6168351539440296` or `cacb0ecf-f044-478f-acd5-ce83c2d8937f`) are simply **unique account identifiers** assigned by each ad network. They can be:

- Numeric (`2671`)
- Prefixed strings (`pub-XXXX` for Google)
- UUIDs (`cacb0ecf-...` for Admixer)

Each network uses its **own format internally** — there's no universal standard for ID format, only for the line structure.

## How Does It Protect the Ecosystem?

1. **Advertisers/DSPs** crawl your `ads.txt` file before buying inventory
2. They **cross-check** the seller ID against the ad network's own `sellers.json` file
3. If an ID isn't listed → the bid is **rejected** as potentially fraudulent
4. This prevents **domain spoofing** where bad actors fake premium inventory

## The `#nativo`, `#Illumin` Comments

Lines ending with `#nativo` or `#Illumin` are just **human-readable comments** to track which partner/platform added that entry — they have no technical effect.

---

**References:**
- [IAB Tech Lab ads.txt Spec](https://iabtechlab.com/ads-txt/)
- [Google ads.txt Guide](https://support.google.com/admanager/answer/7441288)
- [IAB sellers.json Spec](https://iabtechlab.com/sellers-json/)
