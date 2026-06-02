---
audio: false
generated: true
lang: en
layout: post
title: Privacy-Focused Web Analytics Guide
translated: false
type: note
---

Cloudflare Web Analytics is a privacy-focused, free tool designed to help website owners track and understand site performance and visitor behavior without compromising user privacy. Below is a comprehensive guide to setting up and using Cloudflare Web Analytics, based on the latest available information.

### Overview of Cloudflare Web Analytics
Cloudflare Web Analytics provides insights into website traffic, page views, and performance metrics while prioritizing user privacy. Unlike traditional analytics tools that may track personal data or use cookies, Cloudflare’s solution avoids invasive tracking methods like fingerprinting, cookies, or local storage for analytics purposes. It’s suitable for websites of all sizes and can be used with or without Cloudflare’s proxy services.[](https://www.cloudflare.com/web-analytics/)[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)

### Key Features
- **Privacy-First**: Does not collect personal data, use cookies, or track users via IP addresses or user agents, ensuring compliance with privacy regulations like GDPR.[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
- **Two Data Collection Methods**:
  - **JavaScript Beacon**: A lightweight JavaScript snippet collects client-side metrics using the browser’s Performance API. Ideal for detailed Real User Monitoring (RUM) data, such as page load times and core web vitals.[](https://www.cloudflare.com/web-analytics/)[](https://developers.cloudflare.com/web-analytics/about/)
  - **Edge Analytics**: Collects server-side data from Cloudflare’s edge servers for sites proxied through Cloudflare. No code changes are needed, and it captures all requests, including those from bots or users with JavaScript disabled.[](https://www.cloudflare.com/web-analytics/)[](https://developers.cloudflare.com/web-analytics/faq/)
- **Metrics Provided**: Tracks page views, visits, top pages, referrers, countries, device types, status codes, and performance metrics like page load times.[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)[](https://usefathom.com/features/vs-cloudflare-web-analytics)
- **Adaptive Bit Rate (ABR)**: Automatically adjusts data resolution based on data size, date range, and network conditions for optimal performance.[](https://developers.cloudflare.com/web-analytics/about/)
- **Free to Use**: Available to anyone with a Cloudflare account, even without changing DNS or using Cloudflare’s proxy.[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
- **Dashboard and Filters**: Offers an intuitive dashboard to view and filter data by hostname, URL, country, and time range. You can zoom into specific periods or group data for deeper analysis.[](https://www.cloudflare.com/web-analytics/)[](https://www.cloudflare.com/en-in/web-analytics/)
- **Single Page Application (SPA) Support**: Automatically tracks route changes in SPAs by overriding the History API’s `pushState` function (hash-based routers not supported).[](https://scripts.nuxt.com/scripts/analytics/cloudflare-web-analytics)

### Limitations
- **Data Retention**: Limited to 30 days of historical data, which may not suit users needing long-term analytics.[](https://plausible.io/vs-cloudflare-web-analytics)
- **Data Sampling**: Metrics are based on a 10% sample of page load events, which may lead to inaccuracies compared to tools like Plausible or Fathom Analytics.[](https://plausible.io/vs-cloudflare-web-analytics)
- **Inaccuracy Concerns**: Server-side analytics (edge analytics) can include bot traffic, inflating numbers compared to client-side analytics like Google Analytics. Client-side analytics may miss data from users with JavaScript disabled or ad blockers.[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://plausible.io/vs-cloudflare-web-analytics)[](https://markosaric.com/cloudflare-analytics-review/)
- **No UTM Parameter Support**: Currently, query strings like UTM parameters are not logged to avoid collecting sensitive data.[](https://developers.cloudflare.com/web-analytics/faq/)
- **Export Limitations**: No direct way to export data (e.g., to CSV), unlike some competitors like Fathom Analytics.[](https://usefathom.com/features/vs-cloudflare-web-analytics)
- **Basic Analytics**: Lacks advanced features like conversion tracking or detailed user journey analysis compared to Google Analytics.[](https://www.reddit.com/r/webdev/comments/ka8gxv/cloudflares_privacyfirst_web_analytics_is_now/)

### Setting Up Cloudflare Web Analytics
#### Prerequisites
- A Cloudflare account (free to create at cloudflare.com).
- Access to your website’s code (for JavaScript beacon) or DNS settings (for edge analytics if using Cloudflare’s proxy).

#### Setup Steps
1. **Log in to Cloudflare Dashboard**:
   - Go to [cloudflare.com](https://www.cloudflare.com) and log in or create an account.
   - From Account Home, navigate to **Analytics & Logs** > **Web Analytics**.[](https://developers.cloudflare.com/web-analytics/get-started/)

2. **Add a Site**:
   - Click **Add a site** in the Web Analytics section.
   - Enter your website’s hostname (e.g., `example.com`) and select **Done**.[](https://developers.cloudflare.com/web-analytics/get-started/)

3. **Choose Data Collection Method**:
   - **JavaScript Beacon (Recommended for Non-Proxied Sites)**:
     - Copy the provided JavaScript snippet from the **Manage site** section.
     - Paste it into your website’s HTML before the closing `</body>` tag. Ensure your site has valid HTML for the snippet to work.[](https://developers.cloudflare.com/web-analytics/get-started/)[](https://developers.cloudflare.com/web-analytics/faq/)
     - For Single Page Applications, ensure `spa: true` in the configuration for automatic route tracking (hash-based routers not supported).[](https://scripts.nuxt.com/scripts/analytics/cloudflare-web-analytics)
     - Example for Nuxt apps: Use the `useScriptCloudflareWebAnalytics` composable or add the token to your Nuxt config for global loading.[](https://scripts.nuxt.com/scripts/analytics/cloudflare-web-analytics)
   - **Edge Analytics (For Proxied Sites)**:
     - Proxy your website through Cloudflare by updating your DNS settings to point to Cloudflare’s nameservers. This can be done in minutes and requires no code changes.[](https://www.cloudflare.com/en-in/web-analytics/)
     - Metrics will appear in the Cloudflare dashboard under **Analytics & Logs**.[](https://developers.cloudflare.com/web-analytics/faq/)
   - **Cloudflare Pages**:
     - For Pages projects, enable Web Analytics with one click: From **Workers & Pages**, select your project, go to **Metrics**, and click **Enable** under Web Analytics.[](https://developers.cloudflare.com/pages/how-to/web-analytics/)[](https://developers.cloudflare.com/web-analytics/get-started/)

4. **Verify Setup**:
   - Data may take a few minutes to appear in the dashboard. Check the **Web Analytics Sites** section to confirm the site is added.[](https://developers.cloudflare.com/web-analytics/get-started/)
   - If using edge analytics, ensure DNS propagation is complete (may take 24–72 hours).[](https://developers.cloudflare.com/analytics/faq/about-analytics/)

5. **Configure Rules (Optional)**:
   - Set up rules to track specific websites or paths. Use dimensions to categorize metrics (e.g., by hostname or URL).[](https://developers.cloudflare.com/web-analytics/)

#### Notes
- If your site has a `Cache-Control: public, no-transform` header, the JavaScript beacon won’t be injected automatically, and Web Analytics may not work. Adjust your cache settings or manually add the snippet.[](https://developers.cloudflare.com/web-analytics/get-started/)[](https://developers.cloudflare.com/web-analytics/faq/)
- Some ad blockers may block the JavaScript beacon, but edge analytics are unaffected as they rely on server logs.[](https://developers.cloudflare.com/web-analytics/faq/)
- For manual setup, the beacon reports to `cloudflareinsights.com/cdn-cgi/rum`; for proxied sites, it uses your domain’s `/cdn-cgi/rum` endpoint.[](https://developers.cloudflare.com/web-analytics/faq/)

### Using Cloudflare Web Analytics
1. **Access the Dashboard**:
   - Log in to the Cloudflare dashboard, select your account and domain, and go to **Analytics & Logs** > **Web Analytics**.[](https://developers.cloudflare.com/pages/how-to/web-analytics/)[](https://developers.cloudflare.com/analytics/types-of-analytics/)
   - View metrics like page views, visits, top pages, referrers, countries, device types, and performance data (e.g., page load times, core web vitals).[](https://www.cloudflare.com/en-in/web-analytics/)[](https://usefathom.com/features/vs-cloudflare-web-analytics)

2. **Filter and Analyze Data**:
   - Use filters to focus on specific metrics (e.g., by hostname, URL, or country).
   - Zoom into time ranges to investigate traffic spikes or group data by metrics like referrers or pages.[](https://www.cloudflare.com/en-in/web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
   - For advanced users, query data via the **GraphQL Analytics API** to create custom dashboards.[](https://www.cloudflare.com/application-services/products/analytics/)[](https://www.cloudflare.com/en-in/application-services/products/analytics/)

3. **Understand Key Metrics**:
   - **Page Views**: Total times a page is loaded (HTML content-type with successful HTTP response).[](https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics/)
   - **Visits**: Page views from a different referrer (not matching the hostname) or direct links.[](https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
   - **Unique Visitors**: Based on IP addresses, but not stored for privacy reasons. May be higher than other tools due to bot traffic or lack of JavaScript-based deduplication.[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://plausible.io/vs-cloudflare-web-analytics)
   - **Performance Metrics**: Includes page load times, first paint, and core web vitals (client-side only).[](https://usefathom.com/features/vs-cloudflare-web-analytics)

4. **Compare with Other Tools**:
   - Unlike Google Analytics, Cloudflare doesn’t track user journeys or conversions but includes bot and threat traffic, which can inflate numbers (20–50% of traffic for most sites).[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://www.cloudflare.com/insights/)
   - Compared to Plausible or Fathom Analytics, Cloudflare’s data is less granular due to sampling and limited retention.[](https://plausible.io/vs-cloudflare-web-analytics)[](https://usefathom.com/features/vs-cloudflare-web-analytics)
   - Edge analytics may show higher numbers than client-side tools like Google Analytics, which exclude bots and non-JavaScript requests.[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://www.reddit.com/r/CloudFlare/comments/1alzkwm/why_are_my_cloudflare_traffic_stats_so_different/)

### Best Practices
- **Choose the Right Method**: Use the JavaScript beacon for privacy-focused, client-side metrics or edge analytics for comprehensive server-side data if your site is proxied.[](https://www.cloudflare.com/web-analytics/)
- **Combine with Other Tools**: Pair with Google Analytics or privacy-focused alternatives like Plausible or Fathom for deeper insights, as Cloudflare’s analytics are basic.[](https://www.cloudflare.com/insights/)[](https://www.reddit.com/r/webdev/comments/ka8gxv/cloudflares_privacyfirst_web_analytics_is_now/)
- **Monitor Performance**: Use performance metrics to identify slow-loading pages and leverage Cloudflare’s recommendations (e.g., caching optimizations).[](https://developers.cloudflare.com/web-analytics/)
- **Check for Ad Blocker Issues**: If using the JavaScript beacon, inform users to allow `cloudflare.com` or disable ad blockers to ensure data collection.[](https://developers.cloudflare.com/analytics/faq/about-analytics/)
- **Regularly Review Data**: Check the dashboard frequently to spot trends or anomalies, as data is only retained for 30 days.[](https://plausible.io/vs-cloudflare-web-analytics)

### Troubleshooting
- **No Data Showing**:
  - Verify the JavaScript snippet is correctly placed and the site has valid HTML.[](https://developers.cloudflare.com/pages/how-to/web-analytics/)[](https://developers.cloudflare.com/web-analytics/faq/)
  - For edge analytics, ensure DNS is pointing to Cloudflare (propagation may take 24–72 hours).[](https://developers.cloudflare.com/analytics/faq/about-analytics/)
  - Check for `Cache-Control: no-transform` headers blocking automatic beacon injection.[](https://developers.cloudflare.com/web-analytics/get-started/)
- **Inaccurate Stats**:
  - Edge analytics include bot traffic, inflating numbers. Use client-side analytics for more accurate visitor counts.[](https://plausible.io/vs-cloudflare-web-analytics)[](https://markosaric.com/cloudflare-analytics-review/)
  - Data sampling (10%) may cause discrepancies. Consider this when comparing with other tools.[](https://plausible.io/vs-cloudflare-web-analytics)
- **Ad Blocker Issues**: Some browser extensions block the JavaScript beacon. Edge analytics are immune to this.[](https://developers.cloudflare.com/web-analytics/faq/)
- **Missing SPA Metrics**: Ensure SPA support is enabled (`spa: true`) and avoid hash-based routers.[](https://scripts.nuxt.com/scripts/analytics/cloudflare-web-analytics)

### Advanced Usage
- **GraphQL Analytics API**: For custom analytics, query Cloudflare’s API to build tailored dashboards or integrate with other systems. Requires technical expertise.[](https://www.cloudflare.com/application-services/products/analytics/)[](https://www.cloudflare.com/en-in/application-services/products/analytics/)
- **Cloudflare Workers**: Send analytics data to a time-series database for custom processing or use Workers for advanced serverless analytics.[](https://developers.cloudflare.com/analytics/)
- **Security Insights**: Combine with Cloudflare’s Security Analytics to monitor threats and bots alongside visitor data.[](https://www.cloudflare.com/insights/)[](https://developers.cloudflare.com/waf/analytics/security-analytics/)

### Comparison with Alternatives
- **Google Analytics**: Offers detailed user journey tracking and conversions but relies on cookies and JavaScript, which may be blocked. Cloudflare is simpler and privacy-focused but less feature-rich.[](https://developers.cloudflare.com/analytics/faq/about-analytics/)[](https://www.reddit.com/r/webdev/comments/ka8gxv/cloudflares_privacyfirst_web_analytics_is_now/)
- **Plausible Analytics**: Open-source, privacy-first, with unlimited data retention and no sampling. More accurate for unique visitors but requires a paid plan.[](https://plausible.io/vs-cloudflare-web-analytics)
- **Fathom Analytics**: Similar to Plausible, with exportable data and advanced features like campaign tracking. Cloudflare’s free offering is less robust but easier to set up for basic needs.[](https://usefathom.com/features/vs-cloudflare-web-analytics)
- **Jetpack Stats**: WordPress-specific, with limited data retention (28 days) and no user-level tracking. Similar privacy focus but less flexible than Cloudflare.[](https://wordpress.com/support/stats/)

### Additional Resources
- **Official Documentation**: [Cloudflare Web Analytics Docs](https://developers.cloudflare.com/web-analytics/)[](https://developers.cloudflare.com/web-analytics/about/)
- **Setup Guide**: [Enabling Cloudflare Web Analytics](https://developers.cloudflare.com/web-analytics/get-started/)[](https://developers.cloudflare.com/web-analytics/get-started/)
- **FAQ**: [Cloudflare Web Analytics FAQs](https://developers.cloudflare.com/web-analytics/faq/)[](https://developers.cloudflare.com/web-analytics/faq/)
- **Blog Post**: [Cloudflare’s Privacy-First Web Analytics](https://blog.cloudflare.com/privacy-first-web-analytics/)[](https://blog.cloudflare.com/privacy-first-web-analytics/)
- **Community Support**: Check Cloudflare’s community forums for additional help.[](https://developers.cloudflare.com/web-analytics/faq/)

### Conclusion
Cloudflare Web Analytics is an excellent choice for website owners seeking a free, privacy-focused analytics tool with minimal setup. It’s ideal for basic traffic and performance monitoring but may fall short for advanced needs due to data sampling, limited retention, and lack of features like conversion tracking. For deeper insights, consider combining it with tools like Plausible or Fathom Analytics. Always verify setup accuracy and be aware of limitations when interpreting data.

If you need specific assistance with setup or have questions about integrating Cloudflare Web Analytics with your site, let me know!
