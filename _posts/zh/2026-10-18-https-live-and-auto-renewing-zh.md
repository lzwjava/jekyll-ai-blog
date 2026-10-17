---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HTTPS实时与自动续期
translated: true
type: note
---

HTTPS 已启用并自动续期。摘要：

## 当前状态

```
https://web.funlive.io/   → 200 (HTTP/2, TLS 1.2/1.3)
https://web.funlive.io/api/lives/1 → 200
http://web.funlive.io/    → 301 https://web.funlive.io/
```

证书：**Let's Encrypt** `CN=web.funlive.io`，有效期至 **2027-01-13**，证书链已验证（`ssl_verify_result 0`）。移动端站点在 80/8088 端口未受影响（仍为 200）。

## 配置方式（在 VM 上，`/home/lzw/live-server`）

**docker-compose.yml**

- 新增 `certbot` 服务（`certbot/certbot`），挂载两个卷：`letsencrypt` → `/etc/letsencrypt`，`certbot-www` → `/var/www/certbot`（ACME http-01 webroot 验证方式）
- `web`（nginx）发布 `443:443` 端口，并只读挂载上述两个卷

**nginx.conf** — 为 `web.funlive.io` 新增两个配置块：

- `:80` — 从 webroot 卷提供 `/.well-known/acme-challenge/` 路径，其余请求 301 重定向到 HTTPS
- `:443 ssl` + `http2 on` — 完整 SPA 配置 + Mozilla-intermediate TLS 设置；`/api/` 仍代理到 CI4 应用

**`/home/lzw/live-server/renew-certs.sh`** — `docker compose run --rm certbot renew` + nginx 重载。已安装到 crontab：`17 3 * * *`，输出到 `renew-certs.log`。已通过 `certbot renew --dry-run`（成功）和一次真实执行脚本（exit 0）验证。

**GCP** — VM 已有 `https-server` 网络标签，因此现有的 `default-allow-https` 防火墙规则已覆盖 443 端口。无需修改 Namecheap 设置（无需购买付费证书）。

## 仓库已更新（`~/projects/live-web`）

- `deploy/nginx-web.conf` — VM 完整配置的参考副本（已验证除头部注释外字节完全一致）
- `README.md` — 新增 "HTTPS (Let's Encrypt)" 章节，包含续期命令

部署流程不变：`./deploy/deploy.sh`（不会触碰证书；仅重建 + `nginx` 应用配置）。

两个可选后续事项（如需）：

- **HSTS** — 在 `:443` 配置块中添加 `add_header Strict-Transport-Security "max-age=31536000" always;`（安全：仅影响 `web.funlive.io` 主机名）。
- **移动端站点 HTTPS** — 目前没有主机名（在 IP/`localhost` 配置块上提供服务）。如果给它分配域名，我可以复用相同的 certbot 卷。
