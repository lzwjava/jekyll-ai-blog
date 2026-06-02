---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DevCloud上GPU实例额度超出限制
translated: true
type: note
---

**问题：** 为什么在 AMD DevCloud 上创建 GPU Droplet 时，尝试创建 MI300X x8 实例会显示“this will exceed your droplet limit”？

**回答：**

AMD DevCloud（由 DigitalOcean 基础设施支持）对新用户/未验证账户强制执行**账户级资源限制**。以下是触发该问题的原因：

## 根本原因

### 1. 新账户的默认 Droplet 限制非常低
新的 AMD DevCloud 账户通常初始**限制为 0 或 1 个 Droplet**，或者极低的 **vCPU/RAM 配额**。MI300X x8 方案消耗：
- 160 vCPUs
- 1,920 GB RAM
- 2x NVMe 磁盘

仅此一项就远超大多数默认配额。

### 2. GPU Droplet 有单独的配额层级
GPU 资源与常规计算资源分开管理。即使你的通用 Droplet 限制没问题，**GPU 专属限制**通常默认为 0，除非你申请访问权限或完成账单验证。

### 3. 账单/验证未完成
按 ~$1.99/GPU/小时 × 8 GPUs = **$15.92/小时**计算，AMD DevCloud 可能要求：
- 确认有效付款方式
- 完成账户身份/组织验证
- 明确申请配额提升

---

## 如何解决

### 选项 A：请求提升配额
前往你链接的个人资料页面：`devcloud.amd.com/account/profile?i=cd3419`

查找：
- **“Request Limit Increase”** 或 **“Quota”** 板块
- 提交支持工单，说明你的使用场景（模型训练、研究等）

### 选项 B：直接联系 AMD DevCloud 支持
AMD DevCloud 设有支持渠道 — 说明：
- 你的使用场景（LLM 训练、MI300X 工作负载）
- 预计使用时长/周期
- 你已完成账单验证

### 选项 C：通过 API 检查当前限制（如果基于 DigitalOcean）
```bash
# 如果他们暴露了兼容 DO 的 API
curl -X GET "https://api.devcloud.amd.com/v2/account" \
  -H "Authorization: Bearer YOUR_API_TOKEN" | jq '.account.droplet_limit'
```

---

## 针对你使用场景的实用说明

如果你正在训练 GPT-2 规模模型或运行 MI300X 工作负载，MI300X x8（总计 1.5TB VRAM）非常庞大 — 目前 ROCm 堆栈对 PyTorch 支持良好。但 AMD DevCloud 免费/试用账户是故意设置限制的。你可能需要：

1. **发送邮件**说明使用场景以解锁 GPU 配额
2. **升级到付费/已验证层级**（如果尚未操作）
3. 从 **MI300X x1** 开始（如果可用），测试你的配额是否允许创建任何 GPU Droplet，然后再逐步升级

该限制消息是后端硬限制 — 除非由团队提升配额，否则无法绕过。
