---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Clash Proxy Successors and Linux Support
translated: false
type: note
---

Clash, a rule-based proxy tool similar to Shadowsocks, had its original repository deleted by the author in 2023 due to regulatory pressures in China. The community has continued development through forks and successors like Clash.Meta (now officially called Mihomo), which is widely regarded as the most reliable and actively maintained replacement. It supports Linux binaries, including for Ubuntu, and includes features like DNS over HTTPS (DoH), tunneling, and rule-based routing.

For a reliable GitHub repository on Linux/Ubuntu, I recommend the main continuation project. Here's a summary of the top options based on community adoption, updates, and Linux support:

### Recommended Repositories
- **MetaCubeX/mihomo (Clash.Meta Core)**: This is the primary successor to Clash, forked and maintained by the community after the original deletion. It offers full proxy functionality, frequent updates, and pre-built binaries for Linux (x86_64 and arm64). Ubuntu compatibility is excellent, with binaries tested across versions 18.04+. It's open-source, ad-free, and highly customizable via YAML config files.
  - GitHub: https://github.com/MetaCubeX/mihomo
  - Why reliable: Over 14k stars, active community, and binaries include GeoIP databases for routing. Direct download links for Linux CLI binaries in the releases section.
  - Installation for Ubuntu: Download the latest "mihomo-linux-amd64" binary from releases, make it executable (`chmod +x mihomo`), and run it. Requires a config.yaml file with proxy rules. [1][2]
  - Alternatives if the core doesn't suit:
    - **CarlDegio/verge**: A Tauri-based GUI wrapper for Clash.Meta, providing an intuitive dashboard for Linux (Ubuntu included). Builds on Mihomo under the hood for stability.
      - GitHub: https://github.com/CarlDegio/verge
      - Why reliable: GUI support for desktop, over 2k stars, easy profile switching, and system tray icon. Download AppImage for Ubuntu. [3]
    - **chen08209/FlClash**: Multi-platform client (including Linux binaries) based on Clash.Meta. Focuses on simplicity and ad-free design, with a simple interface for configuration.
      - GitHub: https://github.com/chen08209/FlClash
      - Why reliable: Lightweight, supports Ubuntu via deb/AppImage builds, and integrates Mihomo bindings. [4]
  - For legacy backups: Kuingsmile/clash-core offers archived builds of the pre-deletion core, with releases for Linux downloads if you prefer an unmaintained but historical version. [5]

### Additional Notes
- **Installation Tips**: Ensure you have libc (glibc 2.17+) for Ubuntu. Use tools like `systemd` or `screen` to run as a background service. Verify downloads against SHA256 hashes for security.
- **Reliability Criteria**: These repos have active contributed, large user bases (high stars/forks), and avoid the risks of abandoned projects post-2023. Clash.Premin (likely a typo for Premium) is a paid fork but not as open-source focused.
- **Legal/Usage Reminder**: Clash is for bypassing censorship; ensure compliance with local laws, as its use can attract attention in restricted regions.
- If you need a UI or specific features (e.g., multi-platform), verge or FlClash are more user-friendly than the core Mihomo CLI. For details, check each repo's README. If issues arise, the Mihomo repo has extensive documentation. [6][7][1][8]

If none fit or you need a step-by-step guide for Ubuntu, provide more details!

Citations:
[1] https://github.com/djoeni/Clash.Meta
[2] https://discussion.fedoraproject.org/t/rhbz-2305079-review-request-clash-meta-a-rule-based-network-proxy-tool-aka-mihomo/146312
[3] https://github.com/CarlDegio/verge
[4] https://github.com/chen08209/FlClash
[5] https://github.com/Kuingsmile/clash-core/releases
[6] https://github.com/fengwz17/Clash-For-Ubuntu
[7] https://news.ycombinator.com/item?id=38126160
[8] https://github.com/hiddify/Clash.Meta
