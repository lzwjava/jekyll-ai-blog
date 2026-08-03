---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决自定义域名DNS冲突问题
translated: true
type: note
---

问题：`lzwjava.com` 在 Cloudflare Worker `jekyll-ai-blog` 上绑定自定义域名失败，提示"已存在外部管理的 DNS 记录（A、CNAME 等）"。

答案：Cloudflare 自定义域名需要拥有该主机名的 DNS 记录（它会自动创建一条指向 Worker 的代理 CNAME/A 记录）。它不会修改非自身创建的记录——由于 `lzwjava.com` 已存在区域根节点的 A/CNAME 记录（来自 Namecheap 的残留记录，或迁移域名服务器前的指向记录），因此会阻止绑定，而非静默覆盖。自定义域名允许您将 Worker 连接到域名或子域名，无需修改 DNS 设置或管理证书。设置自定义域名后，Cloudflare 会自动创建 DNS 记录并签发所需证书。

修复方法（控制台路径）：

```
Cloudflare 控制台 → lzwjava.com 区域 → DNS → 记录
→ 找到 "@"（根节点）的 A 或 CNAME 记录 → 删除
→ Workers 和 Pages → jekyll-ai-blog → 设置 → 域名和路由 → 自定义域名 → 重新添加 lzwjava.com
```

修复方法（CLI 路径，更快速且可脚本化）：

```bash
# 查找区域 ID
export CF_API_TOKEN=<TOKEN>
ZONE_ID=$(curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones?name=lzwjava.com" | jq -r '.result[0].id')

# 列出根节点记录
curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?name=lzwjava.com" | jq '.result[] | {id,type,name,content}'

# 删除冲突记录（从上方获取 ID）
curl -s -X DELETE -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/<RECORD_ID>"
```

然后通过 wrangler.toml/jsonc 重新绑定（这是推荐的路径，因为控制台自定义域名 UI 和 wrangler 都会触发相同的 100117 检查）：

```jsonc
// wrangler.jsonc
{
  "name": "jekyll-ai-blog",
  "routes": [
    { "pattern": "lzwjava.com", "custom_domain": true },
    { "pattern": "www.lzwjava.com", "custom_domain": true }
  ]
}
```

```bash
npx wrangler deploy
```

两个常见易错点：

1. 错误信息中提到的 `override_existing_dns_record` 参数**实际上并未在 wrangler 中实现**——在 CLI 和控制台中均无效。不必浪费时间查找该标志；删除记录是目前唯一可行的方案。
2. 如果 Namecheap 仍以某种方式同步了仅 DNS 记录（一旦域名服务器指向 Cloudflare 则不太可能，但仍需检查），请确认 Namecheap 的域名服务器已完全设置为 `*.ns.cloudflare.com`——如果 Namecheap 仍为权威服务器，Cloudflare 的 DNS 面板将不起作用，自定义域名也完全无法工作，因为 Cloudflare 不拥有该区域。

重试前快速检查：

```bash
dig NS lzwjava.com +short
```

应返回两个 Cloudflare 分配的域名服务器，而非 Namecheap 的。

参考资料：
- [自定义域名 — Cloudflare 文档](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
- [wrangler deploy 中忽略 override_existing_dns_record 标志 · Issue #9878](https://github.com/cloudflare/workers-sdk/issues/9878)
- [主机名已存在外部管理的 DNS 记录 — Cloudflare 社区帖子](https://community.cloudflare.com/t/hostname-already-has-externally-managed-dns-records/788820)