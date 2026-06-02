---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Llama 服务器在 MI300X 上运行
translated: true
type: note
---

**服务器已启动！** 以下是完整状态：

---

## llama-server：在端口 8080 上运行

**模型：** Qwen3.5-122B-A10B-UD-IQ1_M（总参数122B / 约10B活跃MoE）
**文件大小：** 37 GB（IQ1_M 量化）
**显存：** 总计 196,288 MiB / 空闲 194,606 MiB — 空间充足

### 性能

| Metric | Speed |
|---|---|
| Prompt processing | **77.4 t/s** |
| Token generation | **91.2 t/s** |

### 服务器配置

| 设置项 | 值 |
|---|---|
| 上下文 | 32,768 tokens（4个插槽） |
| GPU层数 | 99（全部在MI300X上） |
| 线程数 | 16 |
| 内存 | mlocked（无交换） |
| API | 与OpenAI兼容，地址 `http://165.245.137.138:8080/v1` |
| 进程PID | 292080 |

### API使用

```bash
curl http://165.245.137.138:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "Qwen3.5-122B-A10B-UD-IQ1_M",
    "messages": [{"role": "user", "content": "Your prompt here"}],
    "max_tokens": 500
  }'
```

模型已加载并启用了推理/思考能力（Qwen3.5默认设置）——你将在最终答案之前获得 `reasoning_content` 中的思维链。凭借在122B MoE上91 t/s的生成速度，MI300X运行非常强劲。
