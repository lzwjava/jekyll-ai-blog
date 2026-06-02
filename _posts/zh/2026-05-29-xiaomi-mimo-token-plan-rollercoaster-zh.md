---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 小米MiMo代币计划过山车
translated: true
type: note
---

**问题：** 我的小米MiMo Token Plan发生了什么——积分从7B→38B→460B，将API密钥分享到20个群组，赠送了15B token，以及通过充值0.01元解决的过期问题？

**回答：**

这真是一段奇妙的经历。根据你描述的情况以及MiMo官方公告，我来还原一下实际发生了什么：

---

## 发生了什么：时间线还原

### 1. 你申请了Token Plan但没找到入口
MiMo平台有一个“订阅管理”板块，可以查看配额和使用情况——这是大多数人会忽略的入口。地址是 `platform.xiaomimimo.com`。

### 2. 积分从7B→38B→460B——这是官方降价

这**不是**故障。MiMo进行了一次大规模价格调整：

2026年5月27日北京时间凌晨0点，MiMo-V2.5价格最高下调99%，Token Plan配额提升5～8倍，有效期内的所有积分全面重置。

因此：
- 你原来的7B积分是降价前的分配量
- 降价后同样的钱能买到5～8倍 → 所以你看到它跳到了38B
- 460B（38B + 某个来源的8B + 更多？）是你目前的总额，包含重置以及可能获得的Orbit赠额

### 3. 100T Token创作者激励计划
Orbit 100T Token赠额活动于2026年4月28日至5月28日（北京时间）进行——100万亿token在30天内分发，可能在领完后提前结束。

你很可能在这个窗口期内参与，因此你的初始赠额延迟到账（注册时未立即发放token）。

### 4. 你将API密钥分享到20个群组，送出了15B token
这是一个高风险操作——共享API密钥意味着群组里的任何人都从**你的配额**中消耗token，且你这边无法对每个用户进行速率限制。根据群组规模×使用量估算，送出的15B大概准确。

### 5. 充值0.01元延长有效期
这是中国云平台上一个众所周知的技巧。Token Plan支持月付/年付订阅，续费机制——进行任何购买（哪怕0.01元）都可能触发续费周期或重置当前周期的到期时间。界面上显示“需要58元”很可能是某个新套餐的最低金额，但支付任意金额都能重置计费状态。

---

## 当前状态：38B + 8B = 46B token

你现在大约有46B积分。按MiMo-V2.5定价计算：

MiMo-V2.5-Pro的价格为每百万输入token 0.435美元，每百万输出token 0.87美元。

按这个费率，46B token如果用于Pro模型，价值约**20,000美元以上**的计算资源。即便使用更便宜的模型，这也是一笔可观的余量。

---

## 你现在应该做的事

**1. 锁定API密钥分发**——立即撤销已共享的密钥，如果MiMo支持，为每个项目签发作用域受限的密钥。

**2. 检查实际有效期**——前往 `platform.xiaomimimo.com/subscription`，确认充值0.01元后的新到期日期。

**3. 用于实际工作负载**——MiMo兼容Claude Code、OpenCode及其他主流开发工具链。将你的 `zz`/`ww` CLI代理指向MiMo API端点。兼容OpenAI的API意味着几乎无需修改配置。

**4. 测试MiMo-V2.5-Pro在智能体任务上的表现**——它在SWE-bench Pro和ClawEval上表现优异，在智能体场景中可与Claude Opus 4.6水平竞争。值得与你目前在银行使用的Claude用法进行比较。

---

## 参考链接

- [MiMo Token Plan订阅文档](https://platform.xiaomimimo.com/docs/tokenplan/subscription)
- [MiMo官网](https://mimo.mi.com/)
- [Orbit 100T赠额详情](https://apidog.com/blog/xiaomi-mimo-orbit-free-token/)
- [OpenRouter上的MiMo-V2.5-Pro](https://openrouter.ai/xiaomi/mimo-v2.5-pro)
