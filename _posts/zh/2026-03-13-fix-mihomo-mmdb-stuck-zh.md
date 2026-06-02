---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 Mihomo MMDB 下载卡住
translated: true
type: note
---

问题：为什么 mihomo 在启动时卡在“Can't find MMDB, start download”？

回答：

## 为什么 Mihomo 在 MMDB 下载时卡住

当你看到这个日志序列：

```
INFO Can't find MMDB, start download
```

...并且它就**卡在那里**，这意味着 mihomo 正在尝试下载 **GeoIP MMDB database**（MaxMind DB 格式，用于 IP 地理位置规则），但是下载**停滞或静默失败**。

---

## 根本原因

### 1. **网络 / 连接问题（最常见）**

mihomo 正在尝试访问远程 URL（通常托管在 GitHub 或 jsDelivr CDN 上）来下载 `Country.mmdb` 或 `geoip.metadb`。如果你的机器：

- 在启动时尚未有互联网访问
- 位于防火墙/代理后面，阻塞了 GitHub raw 文件下载
- 位于 GitHub CDN 缓慢或不可靠的地区

...下载就会挂起，而不会显示超时错误消息。

### 2. **默认下载 URL 被阻塞**

默认 MMDB 来源 URL 通常指向 GitHub releases，在中国和其他一些地区经常被限流或阻塞。

### 3. **没有预存的 MMDB 文件**

如果 mihomo 的工作/配置目录中没有缓存的 MMDB 文件，它**必须**在继续之前下载一个。没有后备方案。

---

## 如何修复

### ✅ 修复 1：手动下载并放置 MMDB 文件

手动下载文件并将其放置在 mihomo 的配置目录中（例如 `~/.config/mihomo/` 或你的 `config.yaml` 所在位置）：

```bash
wget -O ~/.config/mihomo/Country.mmdb \
  https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/country.mmdb
```

然后重启 mihomo。它会找到文件并跳过下载步骤。

---

### ✅ 修复 2：在 `config.yaml` 中设置自定义（更快的）MMDB 下载 URL

添加 `geox-url` 部分，指向更易访问的镜像：

```yaml
geox-url:
  mmdb: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/country.mmdb"
  geoip: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geoip.dat"
  geosite: "https://fastly.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geosite.dat"
```

或者使用其他镜像：

```yaml
mmdb: "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/release/country.mmdb"
```

---

### ✅ 修复 3：切换到 `.dat` 格式（完全跳过 MMDB）

如果你不需要 MMDB，切换到 `geodata-mode: true`，它使用 `.dat` 文件而不是 MMDB：

```yaml
geodata-mode: true
```

这会让 mihomo 使用 `geoip.dat` 和 `geosite.dat` 而不是 MMDB 格式，可能更容易获取。

---

### ✅ 修复 4：在系统级别预下载

如果你将 mihomo 作为系统服务运行（例如在路由器或 Linux 服务器上），服务可能在网络完全启动之前启动。添加启动延迟或在 systemd unit 中添加 `After=network-online.target`：

```ini
[Unit]
After=network-online.target
Wants=network-online.target
```

---

## 总结表格

| 原因 | 解决方案 |
|---|---|
| 无互联网 / 网络未就绪 | 等待，或修复启动顺序 |
| GitHub CDN 被阻塞/缓慢 | 使用 jsDelivr 或备用镜像 URL |
| 无缓存 MMDB 文件 | 手动预下载文件 |
| 想完全避免 MMDB | 使用 `geodata-mode: true` |

参考：

- [mihomo Issue #931 – MMDB update failure](https://github.com/MetaCubeX/mihomo/issues/931)
- [mihomo General Configuration Docs](https://wiki.metacubex.one/en/config/general/)
- [mihomo Issue #1083 – GeoIP MMDB problems](https://github.com/MetaCubeX/mihomo/issues/1083)
