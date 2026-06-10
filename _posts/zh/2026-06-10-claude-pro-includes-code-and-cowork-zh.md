---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Pro 包含代码和协作
translated: true
type: note
---

我来查找关于Claude Pro计划包含Claude Code和Claude Cowork的最新信息。  
**问题：** 当我开通Claude Pro计划（Pro，不是Plus；基于账户，不是API）后，我能否使用该账户使用Claude Code？Claude Cowork呢？

**回答：**

两者都可以。您的Pro账户（每月20美元）可直接验证Claude Code和Claude Cowork——无需API密钥，无需控制台计费。

**Claude Code：** 使用Pro和Max计划，您现在可以通过一个统一的订阅，同时访问网页版、桌面版、移动版Claude以及终端中的Claude Code。您只需下载Claude Code并使用您的Claude凭证登录——同一账户，无需单独设置API。Anthropic曾短暂进行A/B测试，将Claude Code从Pro计划中移除（约2%的新订阅者受到影响），但收到社区反馈后已恢复。截至目前，Claude Code包含在Pro计划中。

**Claude Cowork：** 同样包含在内。Anthropic于2026年1月12日首次推出Claude Cowork时，仅向Max订阅者开放……由于需求巨大，四天后（2026年1月16日）Anthropic向所有Pro订阅者开放了Cowork。

您的设置有两个重要注意事项：

**1. 注意您的`ANTHROPIC_API_KEY`环境变量。** 由于您主要通过OpenRouter/API提供商运行大量任务，消耗约10亿token，您很可能已在shell中导出此变量。如果您的系统中设置了ANTHROPIC_API_KEY环境变量，Claude Code将使用此API密钥进行身份验证，而非您的Claude订阅，从而导致产生API使用费用，而非使用订阅中包含的使用量。

要强制使用订阅身份验证，请在启动前取消设置：
```bash
# 一次性操作
env -u ANTHROPIC_API_KEY claude

# 或检查当前设置
echo $ANTHROPIC_API_KEY

# 验证Claude Code使用的身份验证方式
claude  # 然后运行 /status — 显示"Pro"或API计费
```

**2. 共享使用限制。** Pro和Max计划都提供跨Claude和Claude Code共享的使用限制，这意味着两个工具中的所有活动都计入相同的使用限额。对于"小型代码库中的短编码冲刺"而言，Pro的限制窗口很紧张——考虑到您的工作负载，您很快就会达到上限。当达到使用限制时……您可以启用使用额度，在达到包含的使用限制后继续使用Claude Pro计划。该超额消费按标准API费率计费（与Pro/Max计划定价不同）。

**3. Cowork仅在桌面端打开时运行。** Cowork任务仅在您的电脑上Claude桌面应用打开时运行。关闭应用，会话即结束。如果您希望在您的Air上（而非工作站）安排代理运行，这一点很重要。

**底线：** Pro计划以一个统一的基于账户的订阅覆盖了这两者。对于您的token量级，Pro限制会很快产生作用——如果Claude Code成为您的日常工具，配合现有的API支出，Max（5倍/20倍）是更现实的层级。

参考资料：

- [使用您的Pro或Max计划使用Claude Code](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan)
- [Claude Code产品页面](https://claude.com/product/claude-code)
- [什么是Pro计划？](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan)
- [Pro计划中的Claude Code：当前实际包含的内容](https://codeongrass.com/blog/claude-code-pro-plan-whats-included/)