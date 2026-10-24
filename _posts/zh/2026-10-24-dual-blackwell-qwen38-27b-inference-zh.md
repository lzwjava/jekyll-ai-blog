---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双布莱克韦尔 Qwen3.8-27B 推理
translated: true
type: note
---

本仓库是一个高性能 inference stack，用于在**两块异构 Blackwell GPU**（RTX PRO 6000（96 GB，`GPU0`）和 RTX PRO 5000（72 GB，`GPU1`））上部署 **Qwen3.8-27B**（NVFP4 4-bit 权重），并暴露一个 OpenAI 兼容的 endpoint。这是一个 4 个 commit 的项目，其“实际所做的工作”是一次深刻的性能工程实践。具体来说：

**1. 双服务器 + 自适应路由器部署**（`router/adapd.py`，`scripts/duo.sh`）

- 两个经过修补的 vLLM 0.30.0 服务器（每块卡一个），运行在位于 8090 端口的自定义异步 router 之后。
- **Session 归属**（`--home`）：每个 agent 会话固定到一块卡上，使其 KV cache / GDN state 在轮次间保持热点状态（这使得后续跟进问题只需 2.2–2.6 秒，而无需重新 prefill）。
- **基于 NIXL 的自适应 P/D 分离**（`--home-split` / 默认）：一个长的冷 prefill 可以在*一张*卡上运行，然后 KV（+ GDN state）通过 NIXL（UCX，cuda ipc，实测约 13 GB/s）推送到另一张卡进行 decoding。短请求保持聚合。
- 成本模型路由（每卡常数）、通过链式消息哈希进行的 prefix cache 追踪、seat/KV-fill 记账，以及一个 `GET /router/state` 实时视图。

**2. 自定义 sm_120a CUDA 内核**（`kernels/`，使用 CUDA 13 进行 JIT 构建）

- `fp8attn` — FP8 tensor-core paged extend attention（prefill），496 行代码，有着悠久的 "v13b / v13 / v10h / v10g..." 版本历史。
- `fp4_gemv` — NVFP4 GEMV，用于小 M（decode / MTP verify），数值上精确构造。
- `gdn_defer` — 为推测性解码进行的延迟 Mamba/GDN state 写入。
- 为 MTP drafter 融合 decoding 与 argmax 操作。

**3. 延迟感知调度器**（`vllm/v1/core/sched/qwen38_sched.py`），旨在修复原生 vLLM 的问题：一次 256K 的 prefill（约 14 秒）会阻塞所有 decode。解决方案：decode 优先，当 decode 运行时将 prefill 限制在每步 T_ADD 内，采用 SRPT 排序，为等待的请求保留 token，对齐到 b12x extend 成本锯齿波的分块操作，以及 decode 饥饿 / prefill 份额曲线控制。

**4. 推测性解码** — `duo.sh` 背后的两种布局：

- `apd`：DFlash2 W4A16 drafter（k=7）+ KV 传输，target-cache 2.5 倍卸载。
- `home`：MTP drafter（k=4），使用由 `tools/` 构建的修剪后的 98304 token 草稿词表。

**5. 在 vLLM 之上实现 Claude API 风格的思考预算** — 推理难度层级、思维链隐私清理、每层级的硬性思考上限、答案空间预留以及会话压缩——即，它使 vLLM 的行为类似于专有 agent 平台的 API 语义。

**最终结论**：这是一个验证/测试仓库，证明一个量化的 27B 模型可以在两块*价格相对低廉*的消费级 Blackwell 卡上，以接近交互式的延迟服务长上下文（256K）agent 工作负载——224K 会话的最坏情况冷启动约为 70 秒，后续轮次 2.2–2.6 秒，10 个并发会话的聚合输出约为 376 tok/s。README 中的标题数据显然就是最终的交付成果。
