---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX.2 图像生成工作流
translated: true
type: note
---

问题：解释 `download_flux.py`、`run_flux.py` 和 `/workspace` 文件。

答案：

这是一个典型的 **Hugging Face Diffusers FLUX.2 图像生成工作流**：

```
/workspace
├── download_flux.py     # 下载模型权重
├── run_flux.py          # 加载模型 + 生成图像
├── FLUX.2-dev/          # 下载的模型检查点
├── venv/                # Python 虚拟环境
└── lost+found/          # 文件系统恢复目录
```

流程如下：

```
HuggingFace
    |
    | snapshot_download()
    v
/workspace/FLUX.2-dev
    |
    | Flux2Pipeline.from_pretrained()
    v
GPU 内存（部分）
    |
    | pipe(prompt)
    v
flux_output.png
```

---

## 1. `download_flux.py`

功能：

**从 Hugging Face 下载 FLUX.2-dev 模型文件到本地磁盘。**

```python
import os, time, subprocess
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
```

这将更改 Hugging Face 端点：

正常情况下：

```
https://huggingface.co
```

变为：

```
https://hf-mirror.com
```

在 huggingface.co 较慢或无法访问时很有用。

---

### 导入下载器

```python
from huggingface_hub import snapshot_download
```

`snapshot_download()` 下载整个 Hugging Face 仓库。

类似于：

```bash
git clone https://huggingface.co/black-forest-labs/FLUX.2-dev
```

但针对模型文件进行了优化。

---

### 下载

```python
path = snapshot_download(
    "black-forest-labs/FLUX.2-dev",
    local_dir="/workspace/FLUX.2-dev",
    resume_download=True,
    local_dir_use_symlinks=False
)
```

含义：

源：

```
black-forest-labs/FLUX.2-dev
```

目标：

```
/workspace/FLUX.2-dev
```

示例结构：

```
FLUX.2-dev/
├── model_index.json
├── scheduler/
├── text_encoder/
├── transformer/
├── vae/
└── tokenizer/
```

模型并非单个文件。

扩散模型由多个组件组成：

```
             提示词
               |
               v
        文本编码器
               |
               v
       条件向量
               |
               v
随机噪声 ---> Transformer ---> VAE 解码器
               |
               v
            图像
```

---

### 断点续传

```python
resume_download=True
```

如果中断：

```
50GB 模型
已下载 30GB
网络失败
```

重新开始会继续：

```
30GB -> 50GB
```

而不是重新开始。

---

### 检查大小

```python
subprocess.run(["du", "-sh", path])
```

等价于：

```bash
du -sh /workspace/FLUX.2-dev
```

示例：

```
大小: 80G
```

---

# 2. `run_flux.py`

功能：

**加载 FLUX.2-dev 并生成图像。**

---

## 环境设置

```python
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
```

同样的镜像设置。

---

## 导入 PyTorch + Diffusers

```python
import torch
from diffusers import Flux2Pipeline
```

`Flux2Pipeline` 是高级推理封装。

它将以下组件组合起来：

```
Flux Transformer
+
文本编码器
+
VAE
+
调度器
+
分词器
```

统一成一个 API。

---

## 加载模型

```python
pipe = Flux2Pipeline.from_pretrained(
    "/FLUX.2-dev",
    torch_dtype=torch.bfloat16
)
```

注意：

你的模型路径：

```
/FLUX.2-dev
```

而不是：

```
/workspace/FLUX.2-dev
```

这意味着你的镜像可能已经挂载了：

```
/FLUX.2-dev
```

检查方法：

```bash
ls -lh /FLUX.2-dev
```

如果没有，请改为：

```python
pipe = Flux2Pipeline.from_pretrained(
    "/workspace/FLUX.2-dev",
    torch_dtype=torch.bfloat16
)
```

---

## 为什么使用 bfloat16？

```python
torch_dtype=torch.bfloat16
```

FLUX 非常大。

FP32：

```
1 个参数 = 32 位
```

BF16：

```
1 个参数 = 16 位
```

内存：

```
FP32:
200 亿参数 × 4 字节
≈80GB

BF16:
200 亿参数 × 2 字节
≈40GB
```

几乎减少一半显存。

---

# 3. CPU 卸载

```python
pipe.enable_sequential_cpu_offload()
```

这是关键行。

如果不使用：

```
GPU 显存：

文本编码器
+
Transformer
+
VAE

全部加载

=> 内存不足
```

使用卸载后：

```
CPU 内存
 |
 |
 v

文本编码器
      |
      v
GPU
      |
      v
移除

Transformer
      |
      v
GPU
      |
      v
移除

VAE
      |
      v
GPU
```

每次只有一个组件保留在 GPU 上。

权衡：

|       |            |
| ----- | ---------- |
| 显存  | 大幅降低   |
| 速度  | 变慢       |
| 内存  | 升高       |

适用于 Radeon 7900 / MI300 / 小显存显卡。

---

# 4. 生成图像

```python
prompt = "一只穿着宇航服的可爱猫咪在火星上，数字艺术"
```

文本提示词。

---

```python
image = pipe(
    prompt=prompt,
    num_inference_steps=28,
    guidance_scale=3.5,
).images[0]
```

扩散循环：

开始：

```
随机噪声

x_T
```

28 步：

```
x_T
 |
 v
去噪
 |
 v
x_27
 |
 v
...
 |
 v
x_0
```

最终：

```
潜变量
 |
 VAE 解码器
 |
 RGB 图像
```

---

## `num_inference_steps`

```python
num_inference_steps=28
```

步数越多：

```
10 步
快速
质量较低

50 步
较慢
质量较高
```

28 是一个合理的默认值。

---

## `guidance_scale`

```python
guidance_scale=3.5
```

控制提示词遵循程度。

较低：

```
2
|
更具创造性
服从性较弱
```

较高：

```
8+
|
强烈遵循提示词
有时会出现伪影
```

FLUX 通常比 Stable Diffusion 更喜欢较低的 CFG。

---

## 保存

```python
image.save("/workspace/flux_output.png")
```

输出：

```
/workspace/flux_output.png
```

---

# 5. `venv`

```
venv/
```

Python 虚拟环境。

通常包含：

```
venv/
├── bin/python
├── bin/pip
└── lib/python3.12/site-packages/
```

激活：

```bash
source venv/bin/activate
```

然后：

```bash
python run_flux.py
```

使用隔离的包。

---

# 6. `lost+found`

```
lost+found/
```

正常的 Linux 文件系统目录。

由 `ext4` 创建。

用于：

```bash
fsck
```

在磁盘损坏后恢复孤立文件。

忽略它。

---

## 针对你的 AMD Radeon 云环境

鉴于你之前的服务器：

```
AMD Radeon 云
ROCm 7.2.1
AMD GPU
```

需要检查的重要项：

```bash
rocminfo | head
```

以及：

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.version.hip)"
```

预期输出：

```
True
7.2.x
```

然后：

```bash
python run_flux.py
```

应该会使用 ROCm。

这里的设计专门是为了让巨大的 FLUX 模型在有限的显存上运行，通过使用 `enable_sequential_cpu_offload()` 以速度换取内存。
