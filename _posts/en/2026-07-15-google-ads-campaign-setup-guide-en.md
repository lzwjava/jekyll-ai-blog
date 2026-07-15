---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google Ads campaign setup guide
translated: false
type: note
---

No file attached — "this" isn't landing on anything. What are you trying to advertise? Your AI consulting business, a specific product (like Fun Live successor or one of your CLI tools), or something else?

Once I know that, I can walk you through the actual campaign setup — but here's the skeleton regardless since Google Ads campaign creation is the same structure no matter the product:

**Campaign creation flow (Google Ads UI, no way around it — no CLI/API shortcut for the initial setup wizard):**

1. **Objective** — pick "Sales," "Leads," "Website traffic," or "Awareness." For a consulting/dev-services business, **Leads** is usually right (you want form fills/contact, not direct checkout).
2. **Campaign type** — Search (intent-based, people typing "AI consulting" etc.) vs Performance Max (broad, automated, eats budget fast, less control) vs Display. For B2B technical services, **Search** gives you the most control and best signal-to-noise.
3. **Conversion goal** — attach a conversion action (form submit, call, etc.) before you spend a dollar, or Smart Bidding has nothing to optimize against.
4. **Targeting** — geo (countries/regions you actually want clients from), language.
5. **Budget & bidding** — start with Manual CPC or Maximize Clicks if you have <$1500 total lifetime spend on the account (Smart Bidding needs conversion volume to learn — with low volume it'll just burn budget).
6. **Ad groups & keywords** — tight, one-theme ad groups. E.g. separate ad group for "GPU model training consulting" vs "AI agent development" — don't lump them.
7. **Ad copy** — Responsive Search Ads: 15 headlines, 4 descriptions, let Google mix. Include exact keyword phrases in at least 3 headlines.
8. **Extensions** (now called "assets")** — sitelinks, callout, structured snippets. These are free real estate in the ad and improve CTR meaningfully.

If you tell me what you're promoting and the target market (China domestic, US, global?), I'll draft the actual ad groups, keyword list, and headline/description copy — that's the part worth spending time on, the console clicking is mechanical.
