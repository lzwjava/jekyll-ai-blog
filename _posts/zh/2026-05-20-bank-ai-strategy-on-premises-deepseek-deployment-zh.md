---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 银行AI战略：本地DeepSeek部署
translated: true
type: note
---

**问题：** 在大型银行环境下，我应该内部部署 DeepSeek V4 系列模型（Flash 和 Pro），让它们本地运行，而不是调用 DeepSeek 的外部 API 吗？

**回答：**

是的，这个思路完全正确。以下是完整图景。

---

## DeepSeek V4 — 刚刚发布的内容

2026 年 4 月 24 日，DeepSeek 发布了 DeepSeek V4 和 V4-Pro。V4-Pro 拥有 1.6T 总参数 / 49B 激活参数；V4-Flash 拥有 284B 总参数 / 13B 激活参数。两者均支持 1M 令牌的上下文窗口，均采用 MIT 许可协议，权重已发布在 Hugging Face 上。

关键架构创新：

- 混合注意力架构，结合了压缩稀疏注意力（CSA）和高度压缩注意力（HCA）；在 1M 令牌设置下，与 V3.2 相比，V4-Pro 仅需要 27% 的单令牌推理 FLOPs 和 10% 的 KV 缓存。
- 两种模型均支持三种推理努力模式（思考/非思考），并与 Claude Code 和 OpenCode 等智能体集成。

---

## 为什么大型银行应该自托管（而非调用 DeepSeek API）

这是关键点。DeepSeek 托管的 API 涉及中国数据驻留。对于受监管行业或需要遵守美国/欧盟合规要求的团队，自托管开放权重是明确的路径——它完全绕开了数据主权问题，并让你对推理行为拥有完全控制权。

银行面临：

- **数据驻留要求**——客户数据、交易数据、内部通信不得离开批准的司法管辖区
- **第三方供应商风险策略**——将生产流量路由至中国托管的 API 无法通过信息安全审查
- **模型可审计性要求**——你需要确切知道你运行的是哪个权重，而不是可能静默更改的“预览版”

MIT 许可 + 开放权重 = 你可以下载、运行并将权重锁定在自己的基础设施中。这对银行而言正是全部价值所在。

---

## 硬件现实

对于大多数运行 V4-Flash 的团队，单 pod 中的两块 H200 SXM 是最佳选择——282 GB 的 HBM3e 可容纳模型，并为 256K 上下文提供充足的 KV 缓存。如果需要完整的 1M 上下文或高 QPS，则扩展至 8× H200。对于 V4-Pro，最低单节点配置是 8× H200（1,128GB）；在 V4-Pro 上实现完整 1M 上下文需要两节点 H200 集群。

**实际层级：**

| 模型 | 权重大小 | 最低自托管配置 | 上下文 |
|---|---|---|---|
| V4-Flash | ~160 GB (FP8) | 2× H100/H200 | 1M 令牌 |
| V4-Pro | ~865 GB | 8× H200（单节点） | 最高 800K |
| V4-Pro（完整 1M） | ~865 GB | 2 节点 H200 集群 | 1M 令牌 |

对于大多数自托管场景，V4-Flash 是实际选择——你能够以基础设施成本的一小部分获得 V4-Pro 质量的 85–95%。V4-Pro 自托管对于拥有现有 GPU 集群、需要绝对最佳开放权重性能、且无法将数据发送至外部 API 的组织才更有意义。

---

## 服务栈

内部部署的推荐路径：

```bash
# 拉取权重
huggingface-cli download deepseek-ai/DeepSeek-V4-Flash --local-dir ./ds-v4-flash

# 使用 vLLM 提供兼容 OpenAI 的端点
pip install vllm
vllm serve ./ds-v4-flash \
  --model deepseek-ai/DeepSeek-V4-Flash \
  --tensor-parallel-size 2 \       # 2× H100/H200
  --max-model-len 131072 \          # 从 128K 开始，更多 GPU 后扩展至 1M
  --dtype bfloat16 \
  --api-key your-internal-key
```

API 与 OpenAI ChatCompletions 兼容，使已在使用 OpenAI SDK 格式的团队可以轻松集成。开发者只需将模型参数更新为 `deepseek-v4-pro` 或 `deepseek-v4-flash`。

你的内部应用访问 `http://internal-llm-gateway/v1/chat/completions`，参数为 `model: deepseek-v4-flash`——对于现有的 OpenAI 兼容集成，无需更改任何代码。

对于生产级服务（包含认证、限速和审计日志——银行真正需要的）：

```
[内部客户端]
    → [Kong/Nginx API 网关，带认证和审计日志]
    → [vLLM 集群，提供 V4-Flash / V4-Pro 服务]
    → [GPU 节点，气隙网络分段]
```

---

## Flash 与 Pro 的路由策略

大多数团队的最佳策略：将 70–80% 的流量路由至 V4-Flash，并将复杂任务升级至 V4-Pro。

对于你作为银行 AI 工程师的角色：

- **V4-Flash** → 代码生成、测试用例生成、基于内部文档的 RAG、日常自动化（类似 iclaw 的使用场景）
- **V4-Pro** → 复杂智能体工作流、长上下文文档分析（全代码库审查、监管文件）、困难推理任务

---

## 这对你的角色意味着什么

这是一个高价值的 AI 工程项目：搭建内部 DeepSeek V4 服务基础设施正是处于 LLM 系统、合规工程和 AI 平台建设交叉点的工作。向管理层阐述的论点自然形成：

1. MIT 许可——无许可成本
2. 本地部署——数据不会离开银行
3. 1M 令牌上下文——一次调用即可处理整个代码库或监管文档
4. OpenAI 兼容 API——可即插即用地替换现有工具

“由于数据策略，我们无法使用外部 LLM”和“我们在内部运行着前沿级别的模型”之间的差距，正是你将要填补的。

---

**参考文献：**

- [DeepSeek V4 预览版发布 — API 文档](https://api-docs.deepseek.com/news/news260424)
- [DeepSeek-V4-Flash 在 Hugging Face 上](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)
- [DeepSeek-V4-Pro 在 Hugging Face 上](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)
- [RunPod：在真实环境中运行 V4](https://www.runpod.io/blog/deepseek-v4-in-the-wild-and-how-to-run-it-on-runpod)
- [DeepSeek V4 Flash 深度解析 — Codersera](https://codersera.com/blog/deepseek-v4-flash-deep-dive/)
- [V4 Pro 与 Flash 对比 — Lushbinary](https://lushbinary.com/blog/deepseek-v4-pro-vs-flash-benchmarks-pricing-comparison/)
