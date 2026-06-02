---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Real-Time Blog Visit Telegram Notifications
translated: false
type: note
---

Yes, you can set up a system to analyze Cloudflare logs or traffic in near real-time and send Telegram notifications for each blog visit, but it's not straightforward with standard analytics logs alone. Cloudflare's analytics are mostly aggregate (e.g., daily/weekly summaries), and even their Logpush feature (which exports logs) batches data every 1-5 minutes, making it unsuitable for instant per-visit alerts. Instant Logs offers real-time streaming but requires a Business or Enterprise plan and would need custom processing (e.g., via WebSocket and a script) to trigger Telegram messages— that's overkill for most users.

The most practical and real-time approach is using **Cloudflare Workers** to intercept each incoming request to your blog. This runs serverless code on every visit, allowing you to log the event and immediately send a Telegram message via their API. It's free for low traffic (up to 100k requests/day), but high-traffic blogs could hit limits or incur costs—plus, you'd get spammed with notifications, so consider filtering (e.g., only for unique IPs or specific pages).

### Quick Setup Steps
1. **Create a Telegram Bot**:
   - Message @BotFather on Telegram, use `/newbot` to create one, and note the bot token (e.g., `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).
   - Start a chat with your bot, then message @userinfobot to get your chat ID (e.g., `123456789`).
   - Test sending a message via curl:
     ```
     curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage" \
     -H "Content-Type: application/json" \
     -d '{"chat_id":"<YOUR_CHAT_ID>","text":"Test visit!"}'
     ```

2. **Create a Cloudflare Worker**:
   - Log in to your Cloudflare dashboard > Workers & Pages > Create application > Create Worker.
   - Name it (e.g., `blog-visit-notifier`) and deploy the default template.

3. **Add the Notification Code**:
   - Edit the worker's code to intercept requests and send to Telegram. Here's a basic example (replace placeholders):
     ```javascript
     export default {
       async fetch(request, env) {
         // Optional: Log or filter the visit (e.g., only for your blog's homepage)
         const url = new URL(request.url);
         if (url.pathname !== '/') {  // Adjust path as needed
           return fetch(request);  // Skip non-blog pages
         }

         // Send Telegram message (async to avoid blocking)
         const message = `New visit to ${url.origin}! IP: ${request.headers.get('cf-connecting-ip')}, User-Agent: ${request.headers.get('user-agent')}`;
         await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({
             chat_id: env.TELEGRAM_CHAT_ID,
             text: message,
             parse_mode: 'HTML'  // For formatting if needed
           })
         }).catch(err => console.error('Telegram send failed:', err));

         // Proxy the original request to your blog
         return fetch(request);
       }
     };
     ```
     - This runs on every matching request, logs basic visitor info, and sends it via Telegram without delaying the page load.

4. **Configure Environment Variables**:
   - In the worker settings > Variables > Add:
     - `TELEGRAM_BOT_TOKEN`: Your bot token.
     - `TELEGRAM_CHAT_ID`: Your chat ID.
   - Save and redeploy.

5. **Route the Worker to Your Blog**:
   - In Workers settings > Triggers > Add route.
   - Set it to your blog's domain/path (e.g., `yourblog.com/*`).
   - This ensures the worker runs on every visit before hitting your origin server.

6. **Test and Monitor**:
   - Visit your blog— you should get a Telegram ping instantly.
   - Check worker logs in the dashboard for errors. If you hit rate limits (e.g., Telegram's 30 msgs/sec), add debouncing with KV storage.

### Alternatives If Workers Don't Fit
- **For Batched Log Analysis**: Use Logpush to export HTTP request logs to a service like AWS S3 or Google Pub/Sub, then pipe to a tool like Zapier or n8n for Telegram alerts (e.g., summarize hourly visits). Not real-time, though.
- **Integrations**: Tools like Albato or n8n can connect Cloudflare webhooks to Telegram for broader events, but not per-visit.
- **Limitations**: Free Workers have 10ms CPU time per request—fine for this, but scale up if needed. Avoid on high-traffic sites without throttling.

This setup turns your Cloudflare traffic into actionable, instant alerts. If you need code tweaks or help with errors, share more details!

[Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
[Telegram Bot API](https://core.telegram.org/bots/api)
[Cloudflare Instant Logs](https://developers.cloudflare.com/logs/instant-logs/)
