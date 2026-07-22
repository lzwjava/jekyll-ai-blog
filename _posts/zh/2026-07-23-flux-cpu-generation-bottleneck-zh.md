---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flux CPU生成瓶颈
translated: true
type: note
---

## 问题：解释这次 Flux CPU 运行中的最终生成阶段和性能瓶颈

这部分是 **VAE 解码 + 清理 + 保存阶段**。关键的一行：

```
generate_image completed in 526.73s
```

意思是：

**一张 1024×1024 的 FLUX.1-schnell 图像在 CPU 上耗时约 8 分 47 秒。**

模型加载不是问题，计算才是。

---

## 1. VAE 后端缓冲区

```
model manager prepared params backend buffer
(94.57 MB, 138 tensors, RAM)
```

这是 VAE 模型。

现在管线如下：

```
Flux Transformer
        |
        v
latent image
        |
        v
VAE decoder
        |
        v
RGB pixels
```

VAE 很小：

```
94.57 MB 权重
```

相比之下，Flux：

```
Flux transformer:
6389 MB

VAE:
95 MB
```

---

## 2. VAE 计算缓冲区

```
vae compute buffer size: 6657.00 MB(RAM)
```

这部分很有趣。

VAE 权重很小，但**临时激活内存**很大。

类似于神经网络推理：

```
权重
+
激活值
+
工作空间
```

对于 VAE：

```
权重:
95 MB

工作空间:
6657 MB
```

为什么？

因为解码过程：

```
latent
  |
  | 上采样
  |
  v
高分辨率特征图
  |
  v
1024x1024 RGB
```

会产生很大的中间张量。

---

## 3. VAE 解码时间

```
computing vae decode graph completed, taking 37.20s
```

所以：

```
VAE:
37 秒
```

总时间：

```
526 秒
```

仅占：

```
37 / 526

≈ 7%
```

Flux transformer 才是真正的瓶颈。

---

## 4. 总生成过程分解

大致如下：

```
文本编码:
2.2s

Flux transformer:
~487s

VAE:
37s

----------------
总计:
526s
```

架构：

```
Prompt
 |
 | 2 秒
 v
CLIP
 |
 v

Flux Transformer Q4
 |
 | ~8 分钟
 v

latent

 |
 | 37 秒
 v

VAE

 |
 v

PNG
```

---

## 5. 为什么 Flux 在 CPU 上慢

Flux 模型：

```
12B 参数
3072 隐藏层大小
24 个注意力头
57 个 transformer 块
```

即使量化后：

```
6.4GB 权重
```

但每个 token 都需要 transformer 计算。

1024×1024：

```
image_seq_len = 16384
```

这意味着注意力操作覆盖：

```
16384 个 token
```

与运行长上下文 LLM 非常相似。

举例：

Llama：

```
8192 个文本 token
```

Flux：

```
16384 个图像 token
```

计算量巨大。

---

## 6. 为什么 GPU 会彻底改变现状

你的 RTX 4070：

```
CUDA 核心:
5888

VRAM:
12GB
```

你的模型：

```
Flux Q4:
6.4GB

计算:
2.3GB

VAE:
~1GB

总计:
<10GB
```

刚好能装下。

预期差异：

CPU：

```
526 秒
```

GPU：

可能：

```
20-60 秒
```

取决于 CUDA 后端。

---

## 7. 当前运行本质上是“图像领域的 llama.cpp”

这个设置类似于：

```
llama.cpp
+
7B Q4 模型
+
CPU 推理
```

但用于图像生成。

GGUF 行：

```
flux1-schnell-Q4_0.gguf
```

意思是：

```
LLM 量化思路
        |
        v
图像扩散模型
```

同样的权衡：

```
FP16:
质量高 + 速度快 + 内存大

Q4:
内存小 + 速度慢
```

---

## 8. 下一步优化路径

对于你的 RTX 4070，我不会在 CPU 模式下运行它。

检查编译选项：

```bash
./stable-diffusion --version
```

或：

```bash
ldd ./stable-diffusion | grep cuda
```

你希望看到：

```
GGML_CUDA=ON
```

编译：

```bash
git clone https://github.com/leejet/stable-diffusion.cpp
cd stable-diffusion.cpp

cmake -B build \
  -DSD_CUDA=ON

cmake --build build --config Release -j
```

然后运行：

```bash
./build/bin/sd-cli \
  -m flux1-schnell-Q4_0.gguf \
  --cfg-scale 1 \
  --steps 4
```

你应该会看到：

```
VRAM:
~9000 MB
```

而不是：

```
VRAM:
0 MB
RAM:
6784 MB
```

---

这段日志其实是一个很好的演示：**Flux Q4 已经跨越了 12GB 消费级 GPU 可以本地运行 12B 图像模型的临界点。** 现在的问题不再是模型大小，而是如何将计算转移到 GPU 上。