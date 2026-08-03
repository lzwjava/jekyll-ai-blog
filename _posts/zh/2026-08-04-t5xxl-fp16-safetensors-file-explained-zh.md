---
audio: false
generated: true
image: false
lang: zh
layout: post
title: T5XXL FP16 Safetensors 文件解析
translated: true
type: note
---

问题：`t5xxl_fp16.safetensors` 是什么？监控它的 shell 命令有何含义？

答案：

`t5xxl_fp16.safetensors` 是一个**模型权重文件**。文件名透露出以下信息：

```
t5xxl_fp16.safetensors
│ │    │
│ │    └── FP16 精度（16位浮点数）
│ └─────── XXL 版本（超大 T5 模型）
└───────── T5 文本编码器系列
```

它通常是图像生成模型（尤其是 **FLUX.1 / FLUX.2** 管线）所使用的 **T5-XXL 文本编码器**。

架构：

```
用户提示词
    |
    v
文本分词器
    |
    v
T5-XXL 编码器
（约 47 亿参数）
    |
    v
文本嵌入
    |
    v
扩散 Transformer（FLUX）
    |
    v
图像
```

例如：

```
"a cyberpunk city at night"
          |
          v
    T5-XXL FP16
          |
          v
  语义文本表示
          |
          v
      FLUX 模型
          |
          v
     生成的图像
```

---

### 为什么它大约有 9.8GB？

你的命令检查的是：

```bash
9787841024
```

字节。

换算：

```
9787841024 / 1024 / 1024
≈ 9335 MB
≈ 9.1 GB
```

T5-XXL 模型大约有：

```
参数：
约 47 亿

FP16：
每个参数 2 字节

47 亿 × 2
≈ 9.4 GB
```

因此大小相符。

---

### 你的 shell 命令

```bash
for i in $(seq 1 20); do
```

循环 20 次：

```
i = 1
...
i = 20
```

---

每 30 秒：

```bash
size=$(stat -c%s /mnt/data/zz/flux/models/t5xxl_fp16.safetensors)
```

获取当前文件大小。

示例：

```
size=5000000000
```

表示当前下载进度为 5GB。

---

计算百分比：

```bash
pct=$(( size * 100 / 9787841024 ))
```

示例：

```
5GB / 9.8GB

≈ 51%
```

---

打印进度：

```bash
echo "t=$((i*30))s: $(( size / 1024 / 1024 )) MB ($pct%)"
```

示例输出：

```
t=30s: 5120 MB (52%)
t=60s: 7000 MB (71%)
t=90s: 9787 MB (99%)
```

---

检查完成：

```bash
if [ "$size" -ge 9787841024 ]; then
    echo "DONE"
    break
fi
```

当文件达到预期大小时：

```
DONE
```

退出循环。

否则：

```bash
sleep 30
```

等待 30 秒后再次检查。

---

在你的 FLUX 设置中，完整的模型栈可能如下：

```
models/
├── flux2-dev.safetensors       # 扩散 Transformer
├── t5xxl_fp16.safetensors      # 文本编码器（约 9GB）
├── clip_l.safetensors          # CLIP 文本编码器
└── vae/
    └── ae.safetensors          # 图像解码器
```

内存需求大致：

```
T5-XXL FP16        ~10GB 显存/内存
FLUX Transformer   ~23-60GB 显存（取决于模型）
VAE                ~0.3GB
```

这就是为什么 FLUX.1-dev / FLUX.2-dev 在 12GB 或 16GB 的 GPU 上难以运行。卸载（`cpu_offload`、sequential offload）可将部分内容在 CPU 内存和 GPU 显存之间移动。

参考资料：

* Hugging Face FLUX 模型生态系统
* Black Forest Labs FLUX 模型
* Google Research T5 架构