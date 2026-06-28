---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自托管分析而不暴露家庭IP
translated: true
type: note
---

**问题:** 但要在我的工作站上自托管分析服务，我需要将其暴露到外网，对吗？

**回答:**

是的——跟踪脚本在你的访客浏览器中运行，因此它需要一个公网可访问的 URL 来 POST 事件。你的博客在公网上；分析端点也必须如此。但“暴露”并不意味着要在你的家用路由器上开放端口。更好的方案：

**Cloudflare Tunnel（推荐）** —— 仅从你的工作站到 Cloudflare 边缘的出站连接。无需端口转发，不暴露家庭 IP，免费，并提供真正的 HTTPS 域名。`cloudflared` 守护进程向外拨号，因此你的防火墙在入站方向上保持完全关闭。

```bash
# 在 lzw@192.168.1.36 上
brew install cloudflared   # 或 apt
cloudflared tunnel login
cloudflared tunnel create umami
# 将主机名（需要 Cloudflare 上的域名）映射到本地 Umami
cloudflared tunnel route dns umami analytics.yourdomain.com
cat > ~/.cloudflared/config.yml <<'EOF'
tunnel: umami
credentials-file: /home/lzw/.cloudflared/<UUID>.json
ingress:
  - hostname: analytics.yourdomain.com
    service: http://localhost:3000
  - service: http_status:404
EOF
cloudflared tunnel run umami
```

需要在 Cloudflare 上有一个自定义域名（.com 约 $10/年）。然后你的脚本 src 为 `https://analytics.yourdomain.com/script.js`。

**Tailscale Funnel** —— 类似的出站模型，给你一个 `*.ts.net` 的 HTTPS 主机名，无需购买域名。如果你不想买域名，这是最简单的方案。

```bash
tailscale funnel 3000   # 将本地 :3000 通过 HTTPS 公开暴露
# → https://your-machine.tailXXXX.ts.net
```

注意：Funnel 主机名很丑，且 Tailscale 对 Funnel 带宽有限速——对个人博客的分析流量没问题，但不适合高流量场景。

**诚实的权衡：** 在家庭工作站上运行此服务意味着你的分析可用性取决于机器是否开机、家庭网络是否稳定以及隧道是否保持连接。对于*博客*来说，这很烦人——每当机器重启或 ISP 闪断时，你都会丢失数据。

**我修改后的建议：** 对于分析服务而言，自托管的纯粹性不值得付出脆弱的代价。要么：

1. **Umami Cloud** 免费 hobby 计划或 **GoatCounter** 托管服务——零基础设施，始终在线，仍然注重隐私。把自托管的精力留给那些真正受益于你 GPU 的工作负载（模型训练、推理服务）。
2. 如果你*确实*想自托管，将 Umami 放在一个 $4–6/月的 VPS（Hetzner/Fly.io）上，而不是你的家庭机器上——便宜、始终在线、无需隧道、包含公网 IP。

工作站是你的 ML 设备。不要为了一个页面浏览计数器而消耗它的可用性和排查隧道问题的时间。把家庭自托管留给那些需要 192GB 级硬件或特定用途的事情。
