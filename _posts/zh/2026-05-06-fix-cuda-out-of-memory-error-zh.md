---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复CUDA内存不足错误
translated: true
type: note
---

**问题：**
在 RTX 4070 GPU 上运行 Whisper 时，如何解决 CUDA 显存不足的错误？

---

**回答：**

你遇到的是一个典型的 GPU 显存问题——不是因为你的 RTX 4070 性能不够，而是因为 **Whisper 搭配 PyTorch 时显存占用会迅速飙升**，尤其是在使用较大模型或处理长音频时。

下面我们来分析问题原因并给出有效的解决方法。

---

# 🔍 错误信息的实际含义

你的错误信息中的关键点：

* GPU 总显存：**约 11.56 GB**
* 已使用：**约 10.39 GB**
* 可用：**约 8.75 MB（基本等于没有）**
* 尝试分配：**14 MB → 失败**

👉 这意味着你的 GPU 已经 **完全占满**，即使是微小的内存分配也会失败。

---

# 🚀 实用解决方案（按效果排序）

## ✅ 1. 使用更小的 Whisper 模型（效果最显著）

如果你当前使用的是：

* `large` → 切换为 `medium` 或 `small`
* `medium` → 尝试 `small` 或 `base`

示例：

```python
import whisper
model = whisper.load_model("small")  # 替代 "large"
```

💡 大致显存占用：

* large：约 10–12 GB ❌（对 4070 来说太大）
* medium：约 5–6 GB ✅
* small：约 2–3 GB ✅

---

## ✅ 2. 强制使用 FP16（半精度）

RTX 4070 对 FP16 支持得很好。

```python
model = whisper.load_model("small", device="cuda")
```

并确保推理时使用 FP16：

```python
result = model.transcribe("audio.mp3", fp16=True)
```

👉 可显著降低显存占用。

---

## ✅ 3. 运行前释放 GPU 显存

你可能存在未释放的显存分配。

运行：

```bash
nvidia-smi
```

如有必要，终止其他进程：

```bash
kill -9 <PID>
```

或者在 Python 中：

```python
import torch
torch.cuda.empty_cache()
```

---

## ✅ 4. 分割长音频（非常重要）

Whisper 内部会按块加载音频，但长音频仍会增加显存占用。

👉 预先将音频分割成较短的片段（例如 30–60 秒）。

可使用以下工具：

* `ffmpeg`
* `pydub`

---

## ✅ 5. 设置 PyTorch 显存配置（根据你的错误提示）

这有助于缓解碎片化问题（虽不直接影响总占用，但仍有用）：

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
```

---

## ✅ 6. 使用 CPU 作为备选方案（稳定但较慢）

如果 GPU 显存太紧张：

```python
model = whisper.load_model("small", device="cpu")
```

👉 运行稳定，只是速度较慢。

---

## ✅ 7. 使用更快/优化的 Whisper 实现

强烈推荐以下替代方案：

### 🔥 Faster-Whisper（显存占用更优）

```bash
pip install faster-whisper
```

```python
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cuda", compute_type="float16")
segments, info = model.transcribe("audio.mp3")
```

👉 使用 **CTranslate2 后端** → 更低显存占用 + 更快速度

---

## ✅ 8. Batch size 设为 1（如适用）

如果你在做批处理推理，请减少 batch size：

```python
batch_size = 1
```

---

# 🧠 关键洞察

你的问题 **不仅仅是模型大小**，还有：

> GPU 已被占用 + Whisper 峰值显存激增

即使是 14MB 的分配都失败了 → 你已经处在显存边缘。

---

# 🏁 推荐配置（最佳平衡）

针对 RTX 4070：

```python
from faster_whisper import WhisperModel

model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16"
)

segments, info = model.transcribe("audio.mp3")
```

👉 这样将：

* 轻松适配显存
* 运行速度快
* 避免显存不足

---

# ⚠️ 如果仍然显存不足

那说明有其他程序在使用 GPU：

运行：

```bash
nvidia-smi
```

检查是否存在：

* Chrome 的 GPU 进程
* 其他机器学习任务
* VSCode / Jupyter 内核

---

# 🧩 总结

你的 RTX 4070 性能足够，但：

* ❌ Whisper large 模型 → 太大
* ❌ GPU 几乎已满
* ✅ 解决方案 = 更小模型 + FP16 + 清理显存

---

如果你愿意，我可以帮你 **针对你的环境优化一整套 Whisper 流水线（实时、批处理、流式等）**。
