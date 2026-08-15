---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ComfyUI：启动与成长
translated: true
type: note
---

## 问题：ComfyUI入门——起源与发展

## 答案

![Image](https://images.openai.com/static-rsc-4/wvbULrX1mxPAhbmMD3g98WBNKaWxHcrgAEAeC8rtgPpukT8wPMEaVdEtzuxVBbc-54ita3_hoQYBVUvK3kCSqAk2rxNIC8zSh2OR5uGFDuYIA5ZY8cY4ic5pPXkEcbK3iT-T2Fvz_yTmFlccaG7S9OQFYNcpa-w10M4pP96nqZ71P0G1S123M1wKeO96cm5g?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/suN64f4kWXL2H7mvE0_A5SFZ62MLPOsCXhDiWD7WBEda_VZ93JvOqeu07OtPpeK5KL9T8zRnStt7vzN2cxsIBAnsR6hdI6TEAYv8k8l7uQlu_SNNaQyOQ8a88NDaEIC9tLQfZA5IDJazQoNT_4HuaVLjjCZYw5Ju4emznrIVM35_2Datqhq8SvLKos1R0BIH?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/9fejpdhQrZsn-jUNpm8VFiOp6lkNAPwDdYcsPA5UNjiNFV4hzI_Wkv19b8PX-7c87qaJhmg2Gn_HU1INn0XVNE5qpemgwPBGDi_uOm9JDR_5alq1W3ljT02Xyr_VsC45ScLXgV9-otonfRenDIzOVmIsHLVhcPUMFmcMTCWl1A5PCBDGtYiI1sIpUavA6Txa?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Hlkgx06CaCt-pks1tQ7yAbUC-xwEMwa2Rzg6Op7MDuxP4uDkA7zLgdjOGIFQKsge_R8oApprbAP77PkvQjRYzIOWiuWcBauAgW8_QTEFRdieULP6UV4J8TBhsv4SBSDP74-j4M0i0oz7Q2b_zPWojGVtaqdsRWYQVHIemlP8Zb_D34dVcTwTo461AEgVUxSk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/DyjM3FwbRRbqm2uUq_Gil3iD7VMeBUdlt8VBOvfYCtXfP98RvhHOnIUcGkLRduRDQ-ebKWuNiwCq0r5wCJ5XP5y3KJMhby9sWwhzStDrVE5p6ymUZWdXFSBQFKvOlWbrjZol0wyoe9WOKw5jc9fAHgR3MgyJJIOYCx-7ApL8t9RbFiQ1_oVRJPScRL_O10Lc?purpose=fullsize)

## 什么是ComfyUI？

ComfyUI 是一个**基于节点的视觉AI生成引擎**。它允许你将扩散管道构建为图结构：

```
文本提示
    |
    v
CLIP 文本编码器
    |
    v
潜在噪声
    |
    v
UNet / DiT 降噪器
    |
    v
VAE 解码器
    |
    v
图像
```

不同于将所有操作隐藏在"生成"按钮背后，ComfyUI 直接展示了实际的计算图。

核心理念：

> "AI图像生成是一个程序。节点图是该程序的视觉编程语言。"

官方仓库将其描述为一个具有图/节点界面的模块化扩散引擎，支持图像、视频、3D、音频工作流以及 API。（[GitHub][1]）

---

# 1. ComfyUI之前：Stable Diffusion 的爆发

时间线：

### 2022年——Stable Diffusion 发布

Stability AI 以开源权重发布了 Stable Diffusion。

立刻：

* 研究人员
* 艺术家
* 开发者

开始对其进行修改。

早期生态：

```
Stable Diffusion
       |
       +-- AUTOMATIC1111 WebUI
       |
       +-- 脚本
       |
       +-- notebooks
```

AUTOMATIC1111 Stable Diffusion WebUI 成为主流的用户界面。

问题：

AUTOMATIC1111 设计得像 Photoshop：

```
提示词
负面提示词
步数
CFG
种子
生成
```

对用户友好。

但研究人员和高级用户想要：

```
加载模型
+
编码提示词
+
应用 LoRA
+
ControlNet
+
潜在空间放大
+
面部修复
+
视频插帧
+
自定义模型
```

管道变得过于复杂。

---

# 2. ComfyUI 的诞生

ComfyUI 由名为 **comfyanonymous** 的开发者创建。

最初的动机非常工程化：

> 深入理解 Stable Diffusion 的内部机制，并创建一个用于实验的简洁系统。

早期的 README 明确将目标描述为深入学习 Stable Diffusion 的工作原理，并创建一个灵活的界面。（[GitHub][2]）

第一个突破：

## 将扩散视为计算图

取代：

```
generate()
```

你得到：

```
检查点加载器
        |
        |
CLIP 编码器 ----+
                 |
KSampler <--------+
        |
        |
VAE 解码器
        |
        |
图像
```

每个操作都成为一个节点。

类似理念：

* TensorFlow 图
* PyTorch autograd 图
* Unreal Engine 蓝图
* Blender 节点编辑器

---

# 3. ComfyUI 为何增长如此迅速

其增长并非因为它更美观。

它胜出是因为 AI 生成变得更加复杂。

## 原因一：扩散模型变成了管道

2022年：

```
文本 -> 图像
```

2024年：

```
文本
 |
CLIP
 |
SDXL
 |
LoRA
 |
ControlNet
 |
IP Adapter
 |
AnimateDiff
 |
放大器
 |
面部细化器
 |
视频
```

按钮式界面失效了。

图界面得以生存。

---

## 原因二：开源AI研究人员喜欢控制

研究人员以图的方式思考。

示例：

Stable Diffusion 前向传递：

```
z_t = alpha_t * z_0 + sigma_t * epsilon

epsilon_theta(z_t, t, c)
```

一个采样器：

```
z_{t-1}=调度器(
    z_t,
    epsilon_theta,
    时间步
)
```

ComfyUI 将其暴露出来。

你可以替换：

* 调度器
* 采样器
* 条件控制
* VAE
* 模型模块

而无需重写整个系统。

---

## 原因三：自定义节点创造了生态系统

杀手级功能：

**任何人都可以添加节点。**

示例：

```
ComfyUI
 |
 +-- ControlNet 节点
 |
 +-- AnimateDiff 节点
 |
 +-- IPAdapter 节点
 |
 +-- Flux 节点
 |
 +-- Wan 视频节点
 |
 +-- Hunyuan3D 节点
```

生态系统变得像：

```
PyTorch
   |
   +-- 扩展

ComfyUI
   |
   +-- 自定义节点
```

该仓库已成长为一个非常庞大的开源项目，拥有超过10万颗GitHub星标和数千个分支。（[GitHub][3]）

---

# 4. 发展阶段

## 阶段一：2023年——小众高级用户

用户：

* 机器学习工程师
* Stable Diffusion 研究人员
* 技术艺术家

大多数人仍在使用 AUTOMATIC1111。

---

## 阶段二：2024年——SDXL + ControlNet 时代

爆发。

原因？

SDXL 工作流变得复杂：

```
基础模型
+
优化器
+
ControlNet
+
LoRA
+
放大
```

ComfyUI 成为严肃用户的首选工具。

---

## 阶段三：2025-2026年——多模态AI工作流引擎

它已超越图像领域：

```
图像
 |
视频
 |
3D
 |
音频
 |
智能体
```

现代模型：

* Flux
* Hunyuan Video
* Wan
* Stable Video Diffusion
* Hunyuan3D

自然地被表示为工作流。

ComfyUI 现在定位为通用AI内容创作引擎，而不仅仅是 Stable Diffusion。（[GitHub][1]）

---

# 5. 为什么ComfyUI在技术上很重要

从工程角度来看，ComfyUI 的有趣之处在于它基本上是：

## AI模型的视觉编译器

用户图：

```
A -> B -> C
```

变为执行计划：

```
拓扑排序(图)

执行(节点_1)
执行(节点_2)
执行(节点_3)
```

类似于：

* LLVM IR
* TensorFlow 图执行
* Apache Airflow DAG
* LangGraph 智能体

这种抽象非常强大：

```
模型 = 计算图
工作流 = 程序
节点 = 函数
检查点 = 参数状态
```

---

# 6. 为什么它对AI工程师很重要

对于从事LLM/ML基础设施的人来说，ComfyUI 是一个未来模式的良好范例：

## AI系统变得可组合成图

今天：

```
LLM
 |
工具
 |
检索器
 |
数据库
 |
智能体
```

明天：

```
AI模型组件
       |
       v
工作流图
       |
       v
优化执行
```

相同理念：

* ComfyUI 用于生成式媒体
* LangGraph 用于智能体
* CUDA 图用于GPU执行
* MLIR 用于编译器系统

---

# 我的观点

ComfyUI 是**开源AI基础设施通过可组合性取胜**的最清晰例证之一。

AUTOMATIC1111 的理念是：

> "让 Stable Diffusion 变得简单"

ComfyUI 的理念是：

> "让AI模型变得可编程"

当一项技术成熟时，第二种理念通常会胜出。

参考：

* [ComfyUI GitHub 仓库](https://github.com/comfy-org/comfyui?utm_source=chatgpt.com)
* [ComfyUI 原始仓库文档](https://github.com/commune-ai/comfy?utm_source=chatgpt.com)
* [ComfyUI 发布与架构说明](https://github.com/comfy-org/ComfyUI?utm_source=chatgpt.com)

[1]: https://github.com/comfy-org/comfyui?utm_source=chatgpt.com "GitHub - Comfy-Org/ComfyUI: 最强大且模块化的扩散模型GUI，API和后端，具有图/节点界面。 · GitHub"
[2]: https://github.com/commune-ai/comfy?utm_source=chatgpt.com "GitHub - commune-ai/comfy: 最强大且模块化的稳定扩散GUI，API和后端，具有图/节点界面。 · GitHub"
[3]: https://github.com/comfy-org/ComfyUI?utm_source=chatgpt.com "GitHub - Comfy-Org/ComfyUI: 最强大且模块化的扩散模型GUI，API和后端，具有图/节点界面。 · GitHub"
