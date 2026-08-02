---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理冗余构建流水线
translated: true
type: note
---

工作流进展顺利（翻译已完成 ✅，正在进行 lint/测试/构建）。

## 答案：是的，清理它们

目前，**每次推送都会触发两个部署器**：

| | GitHub Actions | Workers Builds（仪表盘） |
|---|---|---|
| 触发条件 | ✅ 运行（计划/手动） | ✅ 在**每次推送**时运行 |
| 执行内容 | 翻译 → 构建 → `wrangler deploy`（**提升**到生产环境） | `bundle install && jekyll build` → `wrangler versions upload`（上传版本，**不提升**） |
| 结果 | ✅ 生产环境部署 | ❌ 重复版本混乱 + 浪费构建分钟数 + 冗余的 Jekyll 构建 |

既然 GitHub Actions 现在完成了全部工作（翻译 → 构建 → 部署到 Worker），Workers Builds 就是多余的，并且会在每次推送时与之冲突——导致双重构建、版本混乱和令人困惑的历史记录。

**建议清理**——在 Cloudflare 仪表盘中：

> Worker（`jekyll-ai-blog`）→ **设置 → 构建** → **断开** git 仓库

这将一步移除连接的仓库、构建命令和部署命令。Worker 本身保持不变——GitHub Actions 将继续使用你的 Cloudflare 密钥通过 `wrangler deploy` 更新它。

（如果你希望保留 Workers Builds 作为备用 CI，另一种方法是将它的部署命令改为无操作命令，如 `echo skip`——但说实话，断开连接比维护同一个 Worker 的两条流水线更干净。）

---

我会继续监视运行情况——下一个检查点是 **部署到 Cloudflare Workers** 步骤（在 Jekyll 构建之后），这是关键环节。几分钟后我会再次检查。