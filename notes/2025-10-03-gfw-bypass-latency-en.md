---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Optimizing GFW Bypass and Latency
translated: false
type: note
---

Thanks for sharing your setup and experiences—sounds like a thoughtful evolution from your initial proxy script and VPN combo to the Macau SIM approach for direct cellular access. It's great to hear it's been working well for the past couple of months, especially with the Python script automating proxy selection (prioritizing Singapore for AI tools) and sticking with zhs.cloud for the VPN on your laptop. The SIM data bundle (Macau card at 150 CNY/mo for 20GB plus extras) seems like a solid mobile workaround for bypassing GFW restrictions without constant app overhead.

Your findings on the Macau SIM being fastest for GFW-banned sites make sense—direct cellular IP from Macau often skirts geopolitical blocks better than HK or mainland options, especially for services like ChatGPT or Claude that have regional restrictions. Routing specific enablers (e.g., ChatGPT to USA proxies) in Shadowrocket is a clever tweak, but yeah, the blanket proxy delay on every network request is a common pain point on iOS. Shadowrocket (or Surge) can get laggy if it's intercepting too much traffic, leading to higher latency on apps like Twitter/X even if they're not fully blocked.

Here's some feedback and suggestions based on your notes—focusing on optimizations while keeping things practical:

### Shadowrocket Optimizations
- **Rule Refinement for Less Delay**: Instead of a broad proxy-everything setup, try tightening your rules to minimize intercept. For example, use the following flow in Shadowrocket's config:
  - **DIRECT**: Default for local/regional traffic (e.g., WeChat, Baidu).
  - **Proxy/Reject**: Whitelist only the high-priority GFW-banned domains (e.g., allowlist ChatGPT, Claude, Google, and a few others to route through USA proxies).
  - Example rules (in a `.conf` file):
    ```
    [Rule]
    DOMAIN-KEYWORD,chatgpt.com,PROXY
    DOMAIN-KEYWORD,claude.ai,PROXY
    DOMAIN-KEYWORD,google.com,PROXY
    DOMAIN-KEYWORD,twitter.com,PROXY  # Only if ChatGPT/etc. tie into it
    MATCH,DIRECT  # Catch-all to direct non-blocked traffic away from proxy
    ```
    This way, only select sites/apps hit the USA proxy chain, reducing overall delay. You can generate or edit these in Clash or Shadowrocket managers like Stash or Quantumult X for easier customization.
- **Test Latency**: After adding rules, run speed tests (e.g., via Fast.com or Ookla) with Shadowrocket on/off. If delays persist, consider lowering the proxy chain length—one hop (e.g., US-dependent proxy) might suffice over multi-tier setups.

### Alternative Tools for Simpler iOS Access
If Shadowrocket's overhead is too much (especially since you mentioned ditching it after a day), here are low-friction options that mirror your direct Macau SIM use:
- **VPN Apps with On-Demand Rules**: Something like ExpressVPN or NordVPN has iOS features for app-specific routing (enable VPN only for ChatGPT, Mistral, etc.), without proxying everything. It integrates with cellular data seamlessly.
- **Clash for iOS (via Apps like Surge or Stash)**: If you like your desktop Python script's logic, port a simplified Clash config to iOS. Use a rule set that starts with "DIRECT" and only proxies select domains—less delay than full proxy, and you can prioritize Singapore/Macau IPs if your provider supports it.
- **Direct Cellular Proxies via SIM**: Since you're leaning into the Macau SIM for Mistral and Grok, that's smart for pure speed. If you need AI tools on mobile, check if Mistral/Grok have any Macau-friendly IPs or try accessing via incognito modes to avoid app-based routing entirely.

### Broader Tips
- **Battery/Latency on iOS**: Prolonged proxy use can drain battery faster. Monitor with built-in tools, and consider scheduled toggles (e.g., proxy only during peak hours).
- **Provider Stability**: zhs.cloud seems reliable for your VPN needs—stick with it for laptop, but double-check for iOS VPN apps if you expand. For SIM, Macau carriers like CTM are solid, but watch for data caps.
- **Long-Term Viability**: Appreciate the caution for when you leave China—couple this with a global eSIM or roaming plan as backup. Keep an eye on policy shifts, as access tools can be ephemeral.

If you run into specific config issues (e.g., sharing your Shadowrocket rules file) or want script tweaks for Clash, feel free to drop more details—I can help troubleshoot without overcomplicating. Stay safe out there! 🚀
