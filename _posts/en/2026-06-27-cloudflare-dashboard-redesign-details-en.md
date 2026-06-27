---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare Dashboard Redesign Details
translated: false
type: note
---

Question: Did Cloudflare recently update to a new UI/dashboard interface?

Let me verify this rather than guess.Yes. Cloudflare rolled out a major dashboard redesign — their biggest visual overhaul since 2010.

The core change: they got rid of the My Websites page. Instead, in the upper left of the interface after you login is a drop-down menu that allows you to pick your site. The motivation was scale — the old UI fell over for users managing hundreds or thousands of domains, forcing them to manage accounts through the API instead. Matthew Prince framed it as needing an interface that could scale to accommodate all the new things Cloudflare can do today, and the things planned for the future.

Beyond the global shell redesign, several sub-dashboards got reworked on a rolling basis:

- AI got promoted to a top-level sidebar section (Feb 19, 2026) — AI now has its own top-level section in the Cloudflare dashboard sidebar, so you can find AI features without digging through menus, alongside navigation, onboarding, and accessibility fixes.
- Workers KV (Jan 20, 2026) — an updated dashboard UI with new styling, a streamlined homepage for namespaces and key operations, consistent with the rest of the dashboard UI updates, plus an improved analytics view.
- Security Overview dashboard (~May 2026) introduced Security Action Items, which surface vulnerabilities and misconfigurations ranked by severity as critical, moderate, or low priority.
- Turnstile/challenge pages were also redesigned (Feb 2026) for a unified, WCAG 2.2 AAA-compliant UI.

So it's not one single switch — it's a coordinated design-system migration where the main dashboard shell changed and individual products are being restyled to match it over time.

References:

- [CloudFlare's New Dashboard](https://blog.cloudflare.com/cloudflares-new-control-panel/)
- [Redesigning Cloudflare](https://blog.cloudflare.com/redesigning-cloudflare/)
- [AI dashboard experience improvements](https://developers.cloudflare.com/changelog/post/2026-02-19-ai-dashboard-experience-improvements/)
- [New Workers KV Dashboard UI](https://developers.cloudflare.com/changelog/post/2026-01-20-kv-dash-ui-homepage/)
- [Cloudflare Security Overview Dashboard (InfoQ)](https://www.infoq.com/news/2026/05/cloudflare-security-dashboard/)
