---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Clash TUN Mode Full Tunnel Guide
translated: false
type: note
---

**Question: If using OpenConnect with Clash as a proxy program, how to make Clash work like full tunnel mode, or use OpenConnect but support VMess/Trojan protocol addresses? (with Clash log example showing proxy usage for domains like gvt2.com, openrouter.ai)**

**Answer:** 

OpenConnect is strictly an **SSL VPN client** (for Cisco AnyConnect, Pulse, Juniper, etc. protocols). It does **not** natively support VMess, VLESS, Trojan, or any V2Ray/Xray-based protocols — those are completely different architectures. There is no built-in way in OpenConnect to use a VMess/Trojan server address directly.

Clash (or Clash Meta/Verge/Premium cores) already supports VMess, Trojan, Shadowsocks, etc., natively — that's its main strength.

Your goal seems to be achieving a **full-tunnel-like experience** (everything routed through proxies, similar to a VPN) while using Clash with VMess/Trojan nodes (as in your log: 🐟 漏网之鱼 node handling traffic to openrouter.ai, Google domains, etc.).

### Option 1: Use Clash in TUN mode (recommended for full-tunnel-like behavior on macOS)

Clash's **TUN mode** (available in Clash Premium core, Clash Verge, Clash for Windows Premium, etc.) creates a virtual network interface (like a lightweight VPN) and routes **all** (or selected) system traffic through it — very similar to Cisco AnyConnect full-tunnel mode.

- No need for OpenConnect at all.
- Your VMess/Trojan nodes work directly.
- Bypasses many app-level limitations (e.g., games, UDP-heavy apps, or apps ignoring system proxy).

**How to enable full-tunnel-like mode in Clash on macOS:**

1. Use a Clash client that supports TUN (Clash Verge is popular and free on macOS).
2. In settings → enable **TUN Mode** (sometimes called "Enhanced Mode" or "Service Mode").
   - On first enable, it may ask to install a TUN driver/service (grant permission; it uses system extensions).
3. Set **Mode** to **Global** (all traffic through proxy) or **Rule** (smart routing based on your rules).
4. Disable **System Proxy** (TUN mode doesn't need it — in fact, enabling both can conflict).
5. In your config YAML:
   - Ensure your VMess/Trojan proxies are loaded (via subscription or manual).
   - Add a proxy-group like `PROXY` selecting your 🐟 漏网之鱼 node.
   - For full tunnel: set final rule to `MATCH,PROXY` (or your group).
6. Restart Clash → test with `curl ipinfo.io` or browser (should show proxy IP).

**Pros**: True system-wide routing, supports UDP, low overhead compared to real VPNs.  
**Cons**: Requires admin privileges once, may need to allow kernel extensions (macOS security prompts).

Your log already shows Clash working well in **system proxy** mode — switching to TUN makes it behave more like full-tunnel VPN.

### Option 2: Stick with System Proxy mode (what you're using now)

Your current setup (Clash listening on 7890/7891, system proxy enabled) already proxies TCP traffic for apps that honor system proxy settings (browsers, curl, git over HTTPS, etc.).

- It's **not** full tunnel — UDP, raw sockets, or apps ignoring proxies bypass it.
- To make it "more like full tunnel": Enable **Global** mode in Clash GUI.
- But for git over SSH (or other non-HTTP apps), it still won't proxy unless you force via tsocks/proxychains or env vars (e.g., `all_proxy=socks5://127.0.0.1:7891 git ...`).

### Option 3: If you really need OpenConnect + VMess/Trojan (advanced, not recommended)

You cannot make OpenConnect speak VMess/Trojan directly.

Workarounds (complex):
- Run Clash in TUN mode → then run OpenConnect inside that proxied environment (rarely useful).
- Use ocproxy (lwIP-based SOCKS proxy for OpenConnect) → but still no VMess support.
- Chain: OpenConnect → expose as SOCKS → feed to Clash as an outbound → but pointless since Clash already has better protocols.

Best advice: **Forget OpenConnect** unless connecting to a corporate Cisco/Pulse VPN. For your VMess/Trojan use case (bypassing, ChatGPT, etc.), Clash TUN mode gives you the full-tunnel experience you want without any Cisco compatibility layer.

If your corporate VPN requires Cisco AnyConnect protocol **and** you want VMess/Trojan at the same time: Run Clash TUN first (for general traffic), then connect OpenConnect normally (it may route only VPN subnets, or conflict — test carefully).

References:  

- [Clash Verge TUN Mode Guide](https://github.com/clash-verge-rev/clash-verge-rev)
- [OpenConnect Manual (no VMess/Trojan mention)](https://www.infradead.org/openconnect/manual.html)
- [Clash TUN vs System Proxy Discussion](https://github.com/MatsuriDayo/nekoray/issues/739)
- [ocproxy for OpenConnect SOCKS exposure](https://github.com/cernekee/ocproxy)