---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 谷歌Imagen 4预览指南
translated: true
type: note
---

要使用 Google Imagen 4 Preview 0606，您需要通过 Google 的 Vertex AI 平台访问，因为这是一个专为文生图设计的生成式 AI 预览服务。以下是基于现有信息的逐步指南：

### 如何使用 Google Imagen 4 Preview 0606

1. **访问 Vertex AI**：
   - **平台**：Imagen 4 Preview 0606 可在 Google Cloud 的 Vertex AI 上使用。您需要拥有 Google Cloud 账户才能开始。
   - **注册**：如果没有账户，请在 [cloud.google.com](https://cloud.google.com) 注册并设置项目。请确保启用计费，因为这是可能产生费用的预览服务（定价详情可在 Vertex AI 定价页面的 Imagen 部分找到）。[](https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate-preview-06-06)[](https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-fast-generate-preview-06-06)
   - **导航至 Vertex AI**：登录后，前往 Google Cloud Console 中的 Vertex AI 部分，找到生成式 AI 工具。

2. **设置环境**：
   - **身份验证**：使用 Google Cloud 凭据验证您的账户。您可以使用以下命令生成访问令牌：

     ```bash
     gcloud auth print-access-token
     ```

   - **项目和位置**：设置您的 Google Cloud 项目 ID 和位置（例如 `us-central1`）。示例：

     ```bash
     export GOOGLE_CLOUD_PROJECT=your-project-id
     export GOOGLE_CLOUD_LOCATION=us-central1
     ```

3. **使用 Imagen 4 模型**：
   - **API 访问**：Imagen 4 Preview 0606 可通过 Vertex AI API 访问。使用模型端点 `imagen-4.0-generate-preview-06-06`。您可以使用 cURL 或 Google Gen AI SDK for Python 以编程方式与其交互。
   - **cURL 请求示例**：

     ```bash
     curl -X POST \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json; charset=utf-8" \
     "https://${GOOGLE_CLOUD_LOCATION}-aiplatform.googleapis.com/v1/projects/${GOOGLE_CLOUD_PROJECT}/locations/${GOOGLE_CLOUD_LOCATION}/publishers/google/models/imagen-4.0-generate-preview-06-06:predict" \
     -d '{"instances": [{"prompt": "A cat reading a book"}], "parameters": {"sampleCount": 1}}'
     ```

     这将返回一个 base64 编码的图像。[](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)
   - **Python SDK 示例**：

     ```python
     from google import genai
     from google.genai.types import GenerateImagesConfig
     client = genai.Client()
     image = client.models.generate_images(
         model="imagen-4.0-generate-preview-06-06",
         prompt="A dog reading a newspaper",
         config=GenerateImagesConfig(image_size="2K")
     )
     image.generated_images[0].image.save("output-image.png")
     print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
     ```

     这将生成一个图像并将其保存为 PNG 文件。[](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)

4. **构建有效提示**：
   - **提示结构**：为获得最佳效果，请使用详细且具体的提示。包括主体、环境、艺术风格（例如，写实、抽象）、情绪和构图元素（例如，相机角度）。示例：“一幅未来主义城市日落的生动图形插图，赛博朋克风格，带有霓虹灯和戏剧性的低角度视角。”
   - **技巧**：
     - 精确描述：模糊的提示可能导致不可预测的结果。
     - 避免无意义的输入（例如，随机表情符号），因为它们可能产生不一致的输出。
     - 如果需要，指定文本，因为 Imagen 4 改进了字体渲染能力。[](https://deepmind.google/models/imagen/)[](https://replicate.com/blog/google-imagen-4)
   - **负面提示**：您可以使用负面提示来排除不需要的元素（例如，如果不想图像中有文字，可使用“no text”）。[](https://docs.aimlapi.com/api-references/image-models/google/imagen-4-preview)

5. **探索变体**：
   - Imagen 4 Preview 0606 有多个变体，如 **Fast**（速度提升高达 10 倍，针对批量生成优化）和 **Ultra**（与提示对齐度更高，适合专业用途）。请检查这些变体是否在您的 Vertex AI 界面中可用，并根据需求选择（例如，快速原型制作使用 Fast，高质量输出使用 Ultra）。[](https://fal.ai/models/fal-ai/imagen4/preview)[](https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-fast-generate-preview-06-06)

6. **审查输出和安全功能**：
   - **输出格式**：图像以标准格式（如 PNG 或 JPEG）生成，分辨率最高为 2K。[](https://fal.ai/models/fal-ai/imagen4/preview)
   - **SynthID 水印**：所有图像都包含一个不可见的数字水印，以标识其为 AI 生成，确保透明度。[](https://deepmind.google/models/imagen/)[](https://developers.googleblog.com/en/imagen-4-now-available-in-the-gemini-api-and-google-ai-studio/)
   - **内容限制**：Imagen 4 使用过滤机制来减少有害内容，但可能难以处理复杂构图、小面孔或居中图像。请查阅 Google 的使用指南以了解内容限制。[](https://deepmind.google/models/imagen/)[](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)

7. **替代平台**：
   - Imagen 4 也可在第三方平台上使用，如 Replicate、fal.ai 或 AI/ML API，这些平台可能提供更简单的界面或沙盒环境用于测试。例如：
     - **Replicate**：使用提示如“A serene mountain landscape at sunset, hyperrealistic style.”运行 Imagen 4。请查阅 Replicate 的文档以了解 API 密钥和使用方法。[](https://replicate.com/blog/google-imagen-4)[](https://replicate.com/google/imagen-4-fast)
     - **fal.ai**：使用他们的 API 发出请求，例如：

       ```javascript
       const result = await fal.subscribe("fal-ai/imagen4/preview", {
           input: { prompt: "A serene mountain landscape at sunset, hyperrealistic style" }
       });
       console.log(result.images[0].url);
       ```

       定价各不相同（例如，Standard 为 $0.05/图像，Fast 为 $0.04/图像，Ultra 为 $0.06/图像）。[](https://fal.ai/models/fal-ai/imagen4/preview)
   - **Gemini 应用或 Google Workspace**：Imagen 4 已集成到 Gemini 应用、Google Slides、Docs 和 Vids 中，可直接在工作流中生成图像。例如，在 Google Docs 中，您可以生成图像以说明文档。[](https://www.stablediffusion.blog/imagen4)

8. **测试和迭代**：
   - 在集成到生产环境之前，在沙盒环境（例如 Google AI Studio，提供有限的免费测试）中试验提示。[](https://developers.googleblog.com/en/imagen-4-now-available-in-the-gemini-api-and-google-ai-studio/)
   - 通过平台的仪表板监控 API 使用情况和成本，因为预览服务可能支持有限或功能会变化。[](https://fal.ai/models/fal-ai/imagen4/preview)

### 补充说明

- **定价**：请查看 Vertex AI 定价页面了解 Imagen 4 的成本（例如，Standard 为 $0.04/图像，Ultra 为 $0.06/图像）。[](https://developers.googleblog.com/en/imagen-4-now-available-in-the-gemini-api-and-google-ai-studio/)[](https://fal.ai/models/fal-ai/imagen4/preview)
- **限制**：Imagen 4 可能难以处理模糊提示、小面孔或完美居中的构图。使用清晰、结构化的提示以获得最佳效果。[](https://deepmind.google/models/imagen/)
- **可用性**：作为预览服务，功能和支持可能会变化。请查看 Google Cloud 的发布阶段说明以获取更新。[](https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate-preview-06-06)[](https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-fast-generate-preview-06-06)

如需详细文档，请访问 [Vertex AI Imagen 页面](https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview) 或 [Google Developers Blog](https://developers.googleblog.com)。对于 API 访问，请参阅 [x.ai/api](https://x.ai/api) 以获取通用 AI API 指南，但具体的 Imagen 4 详细信息在 Google Cloud 上。[](https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate-preview-06-06)[](https://developers.googleblog.com/en/imagen-4-now-available-in-the-gemini-api-and-google-ai-studio/)

如果您在特定平台或使用案例上需要帮助，请告诉我！
