---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mihomo 在 Fedora 上设置完成
translated: true
type: note
---

全部完成。Mihomo 正在 Fedora 机器上运行：

```
HTTP proxy:  127.0.0.1:7890
SOCKS proxy: 127.0.0.1:7891
Mixed:       127.0.0.1:7892
API:         0.0.0.0:9090
```

**测试结果：**
- Cloudflare 204: ✅ (代理正常工作)
- Google: ✅ (HTTP 200)
- 出口 IP: `69.63.219.52` (通过你的 Hysteria2 代理，非直连)

**我的操作：**
1. 在 Air 上下载 mihomo v1.19.27 RPM (从 GitHub 下载慢，因为在中国)，通过 scp 传到 Fedora
2. 解压 RPM 内容 (避免使用 sudo)，将二进制文件安装到 `~/bin/mihomo`
3. 从 `~/.config/mihomo/config.yaml` 复制配置 (与 Air 相同)
4. 从 Air 复制 `geoip.metadb` (避免慢速下载)
5. 将 DNS 端口从 53 改为 1053 (无需 root 权限)
6. 使用 `nohup ~/bin/mihomo -d ~/.config/mihomo` 启动

**在 Fedora 机器上使用代理：**
```bash
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
```

或者使用单条命令：`curl -x http://127.0.0.1:7890 https://google.com`

注意：mihomo 通过 `nohup` 运行，而非 systemd 服务。如果机器重启，它会停止。需要我设置一个 systemd 服务以实现自动启动吗？