---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zone ID Location in Cloudflare Dashboard
translated: false
type: note
---

Question: Why can't I find the Zone ID in Cloudflare under Analytics & Logs > Web Analytics?

Answer: 

The **Zone ID** is **not** located in the **Analytics & Logs** section (including Web Analytics). That area shows traffic statistics, performance metrics, security events, and logs — but it does **not** display account or zone identifiers like the Zone ID.

The Zone ID is a unique identifier for your specific domain (zone) and is found in a different part of the dashboard.

### Correct steps to find your Zone ID (as of 2026, per official Cloudflare docs)
1. Log in to your Cloudflare dashboard at [https://dash.cloudflare.com](https://dash.cloudflare.com).
2. If you have multiple accounts, make sure you've selected the correct one (you'll see your accounts listed; click into the relevant account).
3. Select the specific **domain** (zone) you want the Zone ID for from the list of your websites/domains.  
   → This takes you to the **Overview** page for that domain.
4. On the **Overview** page, scroll down (usually to the bottom of the right-hand sidebar or the main content area).
5. Look for the **API** section (it's typically near the bottom).
6. In the **API** section, you'll see:
   - **Zone ID**: A 32-character hexadecimal string (e.g., `023e105f4ecef8ad9ca31a8372d0c353`).
   - **Account ID**: Also listed nearby.
7. Click **Click to copy** next to the Zone ID to copy it to your clipboard.

**Important notes:**
- You must be viewing the **Overview** page of a specific domain (not the account-level home, not Analytics, not Workers & Pages alone).
- If you're on a Workers & Pages overview (without selecting a domain), you might only see the **Account ID** — that's why some users miss the Zone ID.
- Zone ID only exists for domains you've added to Cloudflare. If no domains are added, there won't be a Zone ID.
- The location has been consistent for years (right sidebar/API section on domain Overview), with no major changes reported in recent docs (last updated Sep 2025).

If you're still not seeing it:
- Double-check you're on the domain's **Overview** tab (not Analytics & Logs).
- Try refreshing the page or switching domains.
- Use the API method as a fallback (requires an API token):
  ```bash
  curl -X GET "https://api.cloudflare.com/client/v4/zones" \
       -H "Authorization: Bearer YOUR_API_TOKEN" \
       -H "Content-Type: application/json"
  ```
  Look for the `id` field in each zone object.

References:  

- [Find account and zone IDs · Cloudflare Fundamentals docs](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids)
- [Cloudflare Community threads confirming location on Overview > API section](https://community.cloudflare.com/t/where-to-find-zone-id/132913)
- [Zone Analytics docs (confirming Analytics section is for metrics, not IDs)](https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics)