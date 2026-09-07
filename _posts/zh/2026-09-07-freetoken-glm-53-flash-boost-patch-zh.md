---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FreeToken GLM-5.3-Flash 增强补丁
translated: true
type: note
---

这是 **freetoken-ox-boost** —— 一个针对推理服务器 [FreeToken](https://github.com/FlashML-org/FreeToken) v0.1.2 的补丁/插件仓库。它不包含上游代码，仅包含补丁和新文件。

**它的作用：** 添加了对 GLM-5.3-Flash（MoE，NVFP4）的支持，并针对在 **单块 RTX PRO 6000 Blackwell 96 GB GPU** 上运行该模型时，通过 PCIe Gen5 将专家权重卸载到主机内存的场景，提供了一系列性能优化。

**主要成果：**
- 单流解码：**17.8 → 36.7 tok/s（约 2 倍提升）**，零质量损失（与 HF 参考实现逐 bit 一致，48/48 步骤）
- MoE 专家缓存命中率约 84%，小提示词的首 token 生成时间（TTFT）为 0.59 秒，232K 上下文时预填充约 1030 tok/s
- 并发扩展性不佳（4 路并发时聚合约 49 tok/s），因为 GLM-5.3-Flash 的路由非常扁平——并发请求无法共享专家获取，因此 PCIe 带宽成为瓶颈

**值得注意的特性：**
- **视觉支持**（图像 + 视频输入），通过检查点的 0.6B ViT 塔实现，使用 OpenAI/Anthropic 风格的端点
- 使用基数缓存键中的像素内容哈希对媒体请求进行**前缀缓存**
- 一个已定位根因的**混合基数缓存损坏 bug**（缺少 KDA 轨道快照写入导致约 10% 的缓存命中被损坏），并通过基于重计算的写入器及防御措施修复

**布局：**
- `patches/` —— 针对 FreeToken v0.1.2 的 53 个逐文件统一差异
- `overlay/` —— 19 个新文件（GLM-5.3-Flash 模型代码、视觉、4 个 Triton 内核、预取/LFU 缓存）
- `install.sh` —— 版本检查 → 预演 → 应用 → 编译
- `examples/` —— 生产启动脚本
- `MANIFEST.md` —— 功能 → 文件 → 开关 → 测量数据映射

基于 Apache-2.0 许可，与上游相同。