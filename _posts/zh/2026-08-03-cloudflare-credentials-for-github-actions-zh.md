---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向GitHub Actions的Cloudflare凭据
translated: true
type: note
---

问题：这些获取 `CLOUDFLARE_ACCOUNT_ID` / `CLOUDFLARE_API_TOKEN` 并将其接入 GitHub Actions 的仪表盘步骤，对于 `wrangler deploy` 来说正确吗？

回答：是的，这是当前的流程。已对照 Cloudflare 官方文档确认：

**Account ID** — 要找到你的 Cloudflare 账户 ID，请参考“查找账户和区域 ID”。缩小视图以确保选中你的账户（而非某个区域）——右侧边栏显示的 ID 是一个 32 字符的十六进制字符串。

**API Token** — 在 Cloudflare 仪表盘中，进入“账户 API 令牌”页面，选择“创建令牌”，在“权限策略”下打开“自定义”下拉菜单并选择“编辑 Cloudflare Workers”，自定义你的令牌名称，然后将令牌范围限定到特定账户（如果你有多个账户，不要将其保留为“所有账户”）。

**GitHub Secrets** — 与你当前设置完全一致：仓库 → `Settings → Secrets and variables → Actions → New repository secret`，添加 `CLOUDFLARE_ACCOUNT_ID` 和 `CLOUDFLARE_API_TOKEN`。

有一个值得注意的纠正，因为这是一个常见陷阱：不要将 `CLOUDFLARE_API_TOKEN` 的值存储在代码仓库中，因为它允许在你的账户上部署 Workers——应改用 CI/CD 提供商提供的密钥存储功能（这正是你当前的做法）。

两个密钥创建后的最小工作流步骤：

{% raw %}

```yaml
- name: Deploy Worker
  uses: cloudflare/wrangler-action@v4
  with:
    apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
    command: deploy
```

{% endraw %}

或者，如果你在 `run:` 步骤中直接调用 `npx wrangler deploy` 而不是使用 action，只需在该步骤中将两者导出为环境变量：

{% raw %}

```yaml
- name: Deploy
  run: npx wrangler deploy
  env:
    CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

{% endraw %}

Wrangler 会自动识别这两个环境变量名称——无需为 `jekyll-ai-blog` 做额外配置。

参考文档：

- [GitHub Actions · Cloudflare Workers 文档](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/)
- [cloudflare/wrangler-action](https://github.com/cloudflare/wrangler-action)
