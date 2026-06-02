---
audio: false
generated: true
image: false
lang: en
layout: post
title: Excluding Own Visits From Cloudflare Analytics
translated: false
type: note
---

**Question:** Can I install a plugin or extension in Safari (or on my machine) to exclude my own visits from being counted in Cloudflare Web Analytics for my blog?

**Answer:**

Unfortunately, **Cloudflare does not provide an official plugin or built-in feature to exclude your own visits** from Web Analytics. According to the Cloudflare community, natively excluding your own visits from Cloudflare Web Analytics is not currently possible within the dashboard itself.

However, there are several practical workarounds depending on your setup:

---

## Method 1: Use an Ad Blocker (Easiest for Safari)

The Cloudflare Web Analytics beacon script (`https://static.cloudflareinsights.com/beacon.min.js`) is blocked by ad blockers such as uBlock Origin and privacy-focused browsers like Brave. This means if you install an ad blocker on your Safari, it will prevent the beacon from firing and your visits won't be counted.

- **Safari on Mac:** Install [AdGuard for Safari](https://adguard.com/en/adguard-safari/overview.html) or enable Safari's built-in **Intelligent Tracking Prevention**. Many filter lists (like EasyPrivacy) already block `cloudflareinsights.com`.
- **iOS Safari:** Use a content blocker app (e.g., AdGuard, 1Blocker) from the App Store and enable it in Safari Settings → Extensions.

> ⚠️ Note: Cloudflare is aware that the analytics beacon is blocked by ad blockers. However, Cloudflare's **edge analytics** (available to Pro/Business/Enterprise plans) cannot be blocked because they measure every request at the network level. So this only works for the JS beacon-based Web Analytics (the free version).

---

## Method 2: Block via `/etc/hosts` or DNS on Your Machine

On your Mac, you can block the Cloudflare analytics domain at the system level:

1. Edit `/etc/hosts` as root:
   ```
   sudo nano /etc/hosts
   ```
2. Add this line:
   ```
   0.0.0.0 cloudflareinsights.com
   0.0.0.0 static.cloudflareinsights.com
   ```
3. Save and flush DNS cache:
   ```
   sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
   ```

This will block the beacon from all browsers on your machine.

---

## Method 3: Modify Your Blog's Code (localStorage Flag)

A developer-friendly approach is to create a private route (e.g., `/donottrack`) on your blog that sets a `localStorage` flag. When the flag is present, the Cloudflare Analytics script is not appended to the page, preventing your visits from being tracked. Regular visitors who never hit this route are unaffected.

The logic would look like this in JavaScript:

```javascript
if (!localStorage.getItem("notrack")) {
  // append Cloudflare beacon script normally
  const script = document.createElement("script");
  script.src = "https://static.cloudflareinsights.com/beacon.min.js";
  script.setAttribute("data-cf-beacon", '{"token": "YOUR_TOKEN"}');
  document.body.appendChild(script);
}
```

Visit `/donottrack` once to set the flag, and your browser will stop sending analytics data on future visits. You can also add a button to clear the flag (`localStorage.removeItem("notrack")`) if you ever want to re-enable tracking for yourself.

---

## Summary Table

| Method | Effort | Works on Safari | Blocks All Browsers |
|---|---|---|---|
| Ad blocker extension | Low | ✅ Yes | ❌ Per browser |
| `/etc/hosts` block | Medium | ✅ Yes | ✅ Whole machine |
| localStorage flag in code | Medium-High | ✅ Yes | ✅ Per device (once set) |

The **ad blocker** is the fastest solution. The **`/etc/hosts`** method is the most system-wide. The **localStorage** approach is the most elegant if you control the blog's source code.

---

**References:**

- [Cloudflare Community – Excluding own visits](https://community.cloudflare.com/t/how-to-eclude-my-own-visits-from-web-analytics/812198)
- [Cloudflare Web Analytics FAQ](https://developers.cloudflare.com/web-analytics/faq/)
- [Hide your own visits from Cloudflare Analytics with JavaScript](https://www.shedloadofcode.com/blog/hide-your-own-site-visits-from-cloudflare-analytics-with-javascript/)
