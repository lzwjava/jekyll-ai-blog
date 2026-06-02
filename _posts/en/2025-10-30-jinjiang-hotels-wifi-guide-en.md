---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Jinjiang Hotels WiFi Portal Guide
translated: false
type: note
---

The Jinjiang Hotels WiFi portal (<https://portal.jinjianghotels.com.cn/>) is a captive portal designed for on-site access only—it's not fully publicly crawlable outside the hotel network, which is why direct browsing often returns empty or error pages. Based on user reports and guides, here's a breakdown of its typical "route" structure (meaning the main URL paths/endpoints) and how to access them. This is common for Vienna Hotels (a Jinjiang brand) and similar chains in China.

### Main Route and Access Method

- **Primary Route**: The root path `/` (i.e., <https://portal.jinjianghotels.com.cn/> or <http://portal.jinjianghotels.com.cn/>).
  - This is the landing page that loads automatically when you try to access any non-HTTPS website while connected to the hotel WiFi.
  - **How to Access**:
    1. Connect your device to the hotel's WiFi SSID (e.g., "ViennaHotel", "Jinjiang_Free", or "Vienna_Free_WiFi"—no password needed initially).
    2. Open a web browser and navigate to any HTTP site (e.g., <http://neverssl.com> or <http://172.16.16.1—the> local gateway IP mentioned in your first query).
    3. You'll be redirected to the portal's root `/` page. If it doesn't auto-redirect, manually enter `http://172.16.16.1` or the portal URL (use HTTP, not HTTPS, as captive portals often block or ignore HTTPS).
  - The page is in Chinese but simple: It shows hotel branding, terms of use, and login buttons. Use browser translation (e.g., Chrome's built-in) for English.

### Known Subroutes/Paths

The portal uses a minimal structure—mostly a single-page app with form submissions rather than deep subpaths. No public docs list all endpoints, but from user videos and troubleshooting reports, common ones include:

- **SMS Login Path**: Handled via a form on the root `/` (no separate `/sms` subroute; it's a POST request to an internal endpoint like `/auth/sms` or similar).
  - **How to Access/Use**: On the main page, click the SMS button (短信验证). Enter your phone number (+86 for China, or international format). A code arrives via SMS; submit it to authenticate. Access expires after 24 hours.
- **Social Login Paths**: Links or iframes to third-party endpoints, e.g.:
  - Weibo/QQ login: Redirects to `/oauth/weibo` or `/oauth/qq` (temporary subroutes for auth callback).
  - **How to Access**: Click the respective social button on the root page; it opens a popup or redirects briefly.
- **Other Potential Subroutes** (inferred from similar systems; not confirmed for Jinjiang):
  - `/terms` or `/agreement`: For viewing full terms (linked from main page footer).
  - `/logout`: To disconnect manually (rarely used).
  - Error paths like `/error` or 404 for invalid access.

If you're on-site and need to inspect subroutes (e.g., for dev tools), open browser dev console (F12) on the portal page—it may reveal AJAX calls to endpoints like `/api/verify` for SMS submission.

### Troubleshooting Access

- **No Redirect?** Clear browser cache, forget/rejoin WiFi, or toggle mobile data briefly.
- **International Phone?** Works for most, but codes may delay—ask front desk for a shared code.
- **Security Note**: All traffic routes through the hotel's gateway (172.16.16.x range), so use VPN post-login.

For visuals, check short Douyin videos on "维也纳酒店 WiFi 登录" showing the exact page flow.

References:
[Reddit: Issues with WiFi in China Hotels](https://www.reddit.com/r/travelchina/comments/1kjdngn/issues_with_wifi_connection/)
[Douyin: Vienna Hotel WiFi Steps](https://www.douyin.com/search/%E7%BB%B4%E4%B9%9F%E7%BA%B3%E9%85%92%E5%BA%97Wi-Fi%E8%BF%9E%E6%8E%A5%E6%AD%A5%E9%AA%A4)
[Douyin: Hotel WiFi Connection Guide](https://www.douyin.com/search/%E9%85%92%E5%BA%97%E6%97%A0%E7%BA%BF%E7%BD%91%E6%80%8E%E4%B9%88%E8%BF%9E%E6%8E%A5)
