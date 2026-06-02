---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 官方Imagen Python代码片段修复
translated: true
type: note
---

你的基本逻辑是正确的，但 **get‑unstuck** 说明略有偏差。以下是根据官方文档示例整理后的版本：

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# ← 设置您的 API 密钥或使用环境变量 GOOGLE_API_KEY / GEMINI_API_KEY
client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_images(
    model="imagen-4.0-generate-preview-06-06",
    prompt="一只正在读报纸的狗",
    config=types.GenerateImagesConfig(
        number_of_images=1,
        # image_size="2K",  # 可选 2K 分辨率；需要更新的 fast-preview 库
        aspect_ratio="1:1",
        safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
        person_generation="ALLOW_ADULT",
    )
)

for i, generated in enumerate(response.generated_images):
    raw = generated.image.image_bytes
    pil = Image.open(BytesIO(raw))  # 将原始字节转换为 PIL 图像
    pil.save(f"output-image-{i+1}.png")
    print(f"已保存图像 {i+1}，大小 {len(raw):,} 字节")
```

虽然 Google 的 Python 代码片段在其 4‑preview 模型中也使用了 `image_size="2K"`，但请注意：

* 您必须运行 `google-genai` v1.28 或更高版本才能在 Imagen 4 模型上支持 `image_size`；
* 否则请省略该字段（默认为固定的正方形像素分辨率 1,024×1,024）（[GitHub][1]）。

---

### 🚩 常见陷阱与修复方法

1. **缺少 PIL 安装**
   如果您安装了 `google-genai` 但没有添加 `Pillow`，`.image.save()` 调用可能会静默失败（或引发 `AttributeError`）。请确保：

   ```bash
   pip install pillow
   ```

2. **没有 API 密钥或选择了错误的服务**
   如果您在没有 API 密钥且没有云凭据的情况下调用 `genai.Client()`，客户端会在调用时因身份验证错误而失败（例如 `"401 UNAUTHENTICATED"`）。对于 Gemini Developer API，请传递 `api_key="…"` 或在 shell 中设置 `GOOGLE_API_KEY`（[GitHub][1]）。

3. **库版本不匹配**
   旧版本的库或遗留的 `google.generativeai` 模块可能不暴露 `generate_images()`，并且可能仍默认使用 *已弃用* 的 generative-ai 接口。请始终确保：

   ```bash
   pip install --upgrade google-genai
   ```

   在旧代码库（`deprecated-generative-ai-python`）中出现的“无法打开输出图像”问题源于这种不匹配，通常在写入损坏的字节后会抛出 `UnidentifiedImageError` 或 `FileNotFoundError`（[GitHub][1]）。

4. **使用 PIL 打开时出现 UnidentifiedImageError**
   如果您看到：

   ```
   PIL.UnidentifiedImageError: cannot identify image file <_io.BytesIO …>
   ```

   这通常意味着响应缓冲区已损坏或不完整。请仔细检查：

   * 您的提示词未被过滤（例如被 RAI 阻止）；
   * 您没有对字节进行 base64 解码（SDK 已经返回原始的 PNG/JPEG 数据）；
   * 您的文件下载没有中途被截断。

---

### ✅ 此修复为何有效

* Google 文档在 2025‑08‑01 的官方代码片段明确使用了：

  ```python
  types.GenerateImagesConfig(image_size="2K")
  ```

  然后通过 `result.image.save(...)` 保存（[Google Cloud][2]）。

* 但其他使用 Imagen 3 模型的指南仅指定了 `number_of_images`、`aspect_ratio` 和安全设置——没有 `image_size`——因为 Imagen 3 不支持该参数（[GitHub][1]）。

遵循上述流程应该能让您解决问题。如果您遇到特定的错误消息（如 HTTP 403、响应中缺少 JSON 键等），请随时贴出来，我会帮您排查下一步。

[1]: https://github.com/google-gemini/generative-ai-python/issues/674?utm_source=chatgpt.com "can not open the output images from imagen API · Issue #674 · google-gemini/deprecated-generative-ai-python · GitHub"
[2]: https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview?utm_source=chatgpt.com "Imagen on Vertex AI | AI Image Generator"
