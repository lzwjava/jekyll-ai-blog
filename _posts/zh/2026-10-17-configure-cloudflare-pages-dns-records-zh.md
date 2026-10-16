---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置 Cloudflare Pages DNS 记录
translated: true
type: note
---

For `zhiweisoft.site`，如果您托管在 Cloudflare Pages 上，请不要创建指向猜测的 IP 地址的 A record。Pages 使用 CNAME target，对于根域名，一旦域名配置完成，Cloudflare 可以自动管理该记录。&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages 文档

+1



## 根据您的 DNS 托管位置进行配置

### 情况 1：您使用的是 Cloudflare nameservers

在 [Cloudflare DNS dashboard](https://dash.cloudflare.com/?utm_source=chatgpt.com) 中，选择 `zhiweisoft.site` → DNS → Records。

一旦您在 Pages 项目的 Custom domains 下添加了 `zhiweisoft.site`，Cloudflare 应该会自动创建所需的记录。

预期配置：

| Field        | Value                                                          |
| ------------ | -------------------------------------------------------------- |
| Type         | `CNAME`                                                        |
| Name         | `@`                                                            |
| Target       | 您的 Pages 项目主机名，例如 `your-project.pages.dev`          |
| Proxy status | Proxied                                                        |

如果 Cloudflare 已经创建了所需记录，请不要手动添加 A record。

### 情况 2：您仍在使用 Namecheap DNS

如果您想保留 Namecheap 的 nameservers，A record 无法直接将根域名连接到 Cloudflare Pages。您可以改为使用诸如 `www.zhiweisoft.site` 的子域，在 Pages dashboard 中添加该子域后，使用 CNAME 将其指向您的 Pages 主机名。&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages 文档

+1



一个问题：在 Namecheap 中，Nameservers 字段当前显示什么？

- `Namecheap BasicDNS`
- `Custom DNS` (Cloudflare nameservers)
- 其他

这决定了您应该在哪里配置 DNS 记录。