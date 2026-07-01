---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 允许访问网站 限制下载功能
translated: true
type: note
---

**问题：** 我们可以允许员工访问 HuggingFace 网站 (huggingface.co)，但屏蔽 HuggingFace CLI/API 的模型下载功能吗？

**回答：**

可以，两者可以干净地分离。网站和下载机制使用不同的端点和认证模式。以下是拆分方法：

## HuggingFace 下载的工作原理

`huggingface_hub` CLI 和 `transformers` 自动下载使用：

- `https://huggingface.co/<model>/resolve/main/<file>` — 实际文件 blob
- `https://cdn-lfs.huggingface.co/` — 用于模型权重的 LFS（大文件存储）
- `https://cdn-lfs-us-1.huggingface.co/` — 美国 CDN 镜像
- API 调用至 `https://huggingface.co/api/models/...`

网页 UI 使用标准 HTML 页面，位于 `https://huggingface.co/` — 同一域名，不同路径。

## 策略选项

### 选项 1：防火墙/代理 URL 路径过滤（最佳）

如果你能控制代理（Squid、nginx、Zscaler、Palo Alto 等）：

```
# 允许浏览 HuggingFace 网站
ALLOW  GET  huggingface.co/*  (HTML 页面、JS、CSS)

# 阻止模型下载路径
BLOCK  GET  huggingface.co/*/resolve/*
BLOCK  GET  huggingface.co/api/*
BLOCK  GET  cdn-lfs.huggingface.co/*
BLOCK  GET  cdn-lfs-us-1.huggingface.co/*
```

**Squid ACL 示例：**

```squid
acl hf_downloads url_regex huggingface\.co/.*/resolve/
acl hf_lfs dstdomain cdn-lfs.huggingface.co cdn-lfs-us-1.huggingface.co
acl hf_api url_regex huggingface\.co/api/

http_access deny hf_downloads
http_access deny hf_lfs
http_access deny hf_api
http_access allow huggingface.co
```

### 选项 2：仅阻止 CDN + LFS 域名（更简单，精度较低）

完全阻止 CDN 子域名——模型权重存储在这些子域名上，而非主域名：

```
BLOCK: cdn-lfs.huggingface.co
BLOCK: cdn-lfs-us-1.huggingface.co
ALLOW: huggingface.co
```

这会破坏 `huggingface-cli download` 和 `snapshot_download()`，而不影响网站。局限：主域名上的 `/resolve/` blob 仍可通过（较小的文件，如分词器配置）。

### 选项 3：在 OS/MDM 级别阻止 HF_TOKEN 环境变量和端点

针对你控制的员工设备——部署策略：

1. 阻止设置 `HF_TOKEN` 或 `HUGGING_FACE_HUB_TOKEN` 环境变量
2. 通过端点防火墙（例如 macOS 上的 Jamf，Windows 上的 Intune）阻止对 `cdn-lfs.*` 的出站连接

```bash
# 通过审计日志检测下载尝试（Linux）
auditctl -a always,exit -F arch=b64 -S connect \
  -F exe=/usr/bin/python3 \
  -k hf_download_attempt
```

### 选项 4：基于 DNS（粗糙，不推荐单独使用）

```
# Unbound / Pi-hole / 企业 DNS
local-zone: "cdn-lfs.huggingface.co." refuse
local-zone: "cdn-lfs-us-1.huggingface.co." refuse
```

有效但员工可通过 DoH 绕过。结合 TLS 检测以增强效果。

## 实际阻断下载的效果

| 你阻止的内容 | 效果 |
| --- | --- |
| `cdn-lfs.huggingface.co` | 阻止权重下载（模型体积的 >99%） |
| 主域名上的 `/resolve/` 路径 | 阻止配置/分词器文件拉取 |
| `/api/models` | 阻止 `huggingface_hub` 元数据查询 |
| `HF_TOKEN` 认证 | 仅阻止受限模型访问 |

## 推荐方案

```
TLS 检测代理（Zscaler/Squid）
  └── ALLOW huggingface.co  (路径: /, /models, /datasets, /spaces — 仅 HTML)
  └── BLOCK huggingface.co/*/resolve/*
  └── BLOCK huggingface.co/api/*
  └── BLOCK cdn-lfs.huggingface.co
  └── BLOCK cdn-lfs-us-1.huggingface.co
```

这样员工可以完全读取模型卡片、文档、排行榜和 Spaces 演示——同时使 `huggingface-cli download` 和 `snapshot_download()` 因连接错误而失败。
