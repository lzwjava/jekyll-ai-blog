---
audio: true
generated: false
image: false
lang: zh
layout: post
title: Google Text-to-Speech API 入门教程
translated: true
type: post
---

我计划将 Yin Wang 的一些文章转换成音频。为此，我正在尝试使用 Google Text-to-Speech API。以下是一些由 ChatGPT 提供的教程，帮助你完成这一过程。完成后，我会将音频上传到这里。

---

### 步骤 1：设置 Google Cloud 账户

1. 创建 Google Cloud 账户
   如果你还没有 Google Cloud 账户，前往 [Google Cloud Console](https://console.cloud.google.com/) 注册。

2. 创建一个新项目
   - 在 Google Cloud Console 中，点击顶部左侧的项目下拉菜单。
   - 选择 New Project，为项目命名并创建。

3. 启用 Text-to-Speech API
   - 访问 [Google Cloud Text-to-Speech API 页面](https://cloud.google.com/text-to-speech)。
   - 点击 Enable，为你的项目启用 API。

4. 创建 API 凭证
   - 在 Cloud Console 中，导航到 APIs & Services > Credentials。
   - 点击 Create Credentials，选择 Service Account。
   - 按照提示创建服务账户，并确保 下载 JSON 格式的私钥文件。
   - 安全地保存此 JSON 文件，因为它将在身份验证时使用。

---

### 步骤 2：安装 Google Cloud SDK 和客户端库

1. 安装 Google Cloud SDK
   如果尚未安装 [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)，请根据操作系统的安装指南进行安装。

2. 安装 Python 客户端库
   如果使用 Python，运行以下命令安装 `google-cloud-texttospeech` 库：

   ```bash
   pip install google-cloud-texttospeech
   ```

---

### 步骤 3：设置认证

在与 Google Cloud Text-to-Speech API 交互之前，需要通过指定凭证文件的位置来进行认证。运行以下命令：

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/Users/lzwjava/Downloads/google_credentials_service_account.json"
```

将路径替换为你的服务账户 JSON 密钥文件的实际位置。

---

### 步骤 4：实现文本到语音转换

现在，你可以使用 Google Cloud Text-to-Speech API 将文本转换为语音。以下是一个 Python 示例，演示如何实现：

```python
from google.cloud import texttospeech

def text_to_speech(text, output_filename):
    # 初始化 Text-to-Speech 客户端
    client = texttospeech.TextToSpeechClient()

    # 设置合成输入
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 选择语音参数
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # 如果需要，可以更改为其他语言
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # 可选择男性或女性
    )

    # 设置音频配置
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3  # 可选 MP3 或 LINEAR16 (WAV)
    )

    # 执行文本到语音请求
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 将音频内容写入文件
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

    print(f"音频内容已写入 {output_filename}")


# 示例使用
article_text = """
在此粘贴你的文章内容。确保文章格式正确，且不超过 API 限制。
"""
output_file = "output_audio.mp3"

# 调用函数
text_to_speech(article_text, output_file)
```

---

### 步骤 5：运行脚本

1. 将脚本保存为 `text_to_speech.py`。
2. 运行脚本：

   ```bash
   python text_to_speech.py
   ```

这将从提供的文本生成音频文件（`output_audio.mp3`）。

---

### 步骤 6：服务账户密钥

你的服务账户密钥应该如下所示：

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "your-private-key",
  "client_email": "your-service-account-email@your-project-id.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your-client-cert-url"
}
```

---

### 步骤 7：生成新的服务账户密钥（如果需要）

如果你的凭证文件与示例不同，可能需要在 Google Cloud Console 中创建一个新的服务账户密钥。

创建新服务账户密钥的步骤：
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)。
2. 导航到 IAM & Admin：
   - 在左侧边栏，点击 IAM & Admin > Service Accounts。
3. 创建新服务账户（如果你还没有创建）：
   - 点击顶部的 Create Service Account。
   - 输入服务账户名称，并授予适当的角色（如 Viewer 或 Text-to-Speech API User）。
   - 点击 Create。
4. 生成密钥：
   - 创建服务账户后，点击该账户。
   - 转到 Keys 标签，点击 Add Key > Create new key。
   - 选择 JSON 作为密钥类型，然后下载密钥文件。

---

### 示例音频输出

一旦一切设置完成，音频输出文件将在此处提供：
[下载音频文件](assets/audios/output-audio.mp3)。

---

### 结论

借助 Google Cloud Text-to-Speech API，文本转换为自然语音既简单又高效。无论你是构建需要语音输出的应用程序，还是仅仅是进行文本到语音的实验，该 API 提供了强大的功能。请查看文档，了解更多选项，如语音选择和语言支持！
