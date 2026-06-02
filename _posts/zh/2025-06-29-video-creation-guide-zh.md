---
audio: false
generated: true
lang: zh
layout: post
title: 使用Python制作教学视频
translated: true
type: note
---

要创建具有黑色背景和与音频同步字幕的教育类短视频，并使用 DeepSeek API 和 Google Cloud Text-to-Speech API 从文本生成音频，您可以使用 Python 来编排整个过程。以下是分步指南和实现此功能的 Python 脚本。该脚本将：

1. 使用 DeepSeek API 生成或优化脚本（假设您提供教育内容）。
2. 使用 Google Cloud Text-to-Speech API 将脚本转换为音频。
3. 使用 `moviepy` 等库创建带有黑色背景和与音频同步字幕的视频。

### 前提条件

- **DeepSeek API 密钥**：在 [DeepSeek](https://api-docs.deepseek.com/) 注册并获取 API 密钥。
- **Google Cloud Text-to-Speech API**：
  - 设置 Google Cloud 项目并启用 Text-to-Speech API。
  - 创建服务账号并下载 JSON 凭证文件。
  - 安装 Google Cloud Text-to-Speech 客户端库：`pip install google-cloud-texttospeech`。
- **Python 库**：
  - 安装所需库：`pip install openai moviepy requests`。
- **FFmpeg**：确保安装 FFmpeg，以便 `moviepy` 处理视频渲染（从 [FFmpeg 网站](https://ffmpeg.org/) 下载或通过包管理器安装）。

### 步骤

1. **使用 DeepSeek API 生成或优化脚本**：使用 DeepSeek 创建或润色教育脚本，确保其简洁且适合 1 分钟视频。
2. **使用 Google Cloud Text-to-Speech 将文本转换为音频**：将脚本拆分为段落，为每个段落生成音频，并保存为单独的音频文件。
3. **使用 MoviePy 创建视频**：生成带有黑色背景的视频，为每个段落显示与音频同步的字幕，并将它们组合成最终的 1 分钟视频。

### Python 脚本

以下脚本假设您有一个包含教育内容（段落）的文本文件，并生成带有黑色背景和字幕的视频。

```python
import os
from openai import OpenAI
from google.cloud import texttospeech
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, concatenate_videoclips
import requests

# 设置环境变量
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google-credentials.json"  # 更新为您的凭证文件路径
DEEPSEEK_API_KEY = "your_deepseek_api_key"  # 更新为您的 DeepSeek API 密钥

# 初始化 DeepSeek 客户端
deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# 使用 DeepSeek 优化脚本的函数
def refine_script_with_deepseek(script):
    prompt = f"""
    You are an expert scriptwriter for educational videos. Refine the following script to be concise, clear, and engaging for a 1-minute educational video. Ensure it is suitable for spoken narration and fits within 60 seconds when spoken at a natural pace. Split the script into 2-3 short paragraphs for caption display. Return the refined script as a list of paragraphs.

    Original script:
    {script}

    Output format:
    ["paragraph 1", "paragraph 2", "paragraph 3"]
    """
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    refined_script = eval(response.choices[0].message.content)  # 将字符串转换为列表
    return refined_script

# 使用 Google Cloud Text-to-Speech 为每个段落生成音频的函数
def generate_audio(paragraphs, output_dir="audio"):
    client = texttospeech.TextToSpeechClient()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_files = []
    for i, paragraph in enumerate(paragraphs):
        synthesis_input = texttospeech.SynthesisInput(text=paragraph)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-D"  # 自然发音的英语语音
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        audio_file = os.path.join(output_dir, f"paragraph_{i+1}.mp3")
        with open(audio_file, "wb") as out:
            out.write(response.audio_content)
        audio_files.append(audio_file)
    return audio_files

# 创建带有字幕和黑色背景的视频的函数
def create_video(paragraphs, audio_files, output_file="educational_video.mp4"):
    clips = []
    for i, (paragraph, audio_file) in enumerate(zip(paragraphs, audio_files)):
        # 为字幕创建文本剪辑
        text_clip = TextClip(
            paragraph,
            fontsize=40,
            color="white",
            font="Arial",
            size=(1280, 720),  # 标准高清分辨率
            method="caption",
            align="center"
        )
        # 加载音频并获取其持续时间
        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration
        # 设置文本剪辑持续时间以匹配音频
        text_clip = text_clip.set_duration(duration)
        # 创建黑色背景剪辑
        bg_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=duration)
        # 组合文本和背景
        video_clip = CompositeVideoClip([bg_clip, text_clip.set_position("center")])
        # 为视频剪辑添加音频
        video_clip = video_clip.set_audio(audio_clip)
        clips.append(video_clip)

    # 连接所有剪辑
    final_clip = concatenate_videoclips(clips)
    # 写入最终视频
    final_clip.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")
    final_clip.close()
    for clip in clips:
        clip.close()

# 主函数
def main():
    # 示例输入脚本（替换为您的教育内容）
    input_script = """
    Machine learning is a field of artificial intelligence that allows computers to learn from data without being explicitly programmed. It involves algorithms that identify patterns and make predictions. Applications include image recognition, natural language processing, and more. This technology is transforming industries like healthcare and finance.
    """

    # 步骤 1：使用 DeepSeek 优化脚本
    refined_paragraphs = refine_script_with_deepseek(input_script)
    print("优化后的脚本：", refined_paragraphs)

    # 步骤 2：为每个段落生成音频
    audio_files = generate_audio(refined_paragraphs)
    print("生成的音频文件：", audio_files)

    # 步骤 3：创建带有字幕和黑色背景的视频
    create_video(refined_paragraphs, audio_files)
    print("视频已创建：educational_video.mp4")

if __name__ == "__main__":
    main()

```

### 使用方法

1. **设置凭证**：
   - 将 `"path/to/your/google-credentials.json"` 替换为您的 Google Cloud 服务账号 JSON 文件路径。
   - 将 `"your_deepseek_api_key"` 替换为您的 DeepSeek API 密钥。
2. **准备输入脚本**：
   - 在 `main()` 函数中修改 `input_script` 变量，填入您的教育内容。脚本应为包含要转换为视频的完整文本的单个字符串。
3. **运行脚本**：
   - 将脚本保存为 `create_educational_video.py`，并使用 `python create_educational_video.py` 运行。
   - 脚本将：
     - 使用 DeepSeek API 优化脚本，确保其简洁并拆分为 2-3 个段落。
     - 使用 Google Cloud Text-to-Speech 为每个段落生成 MP3 音频文件。
     - 创建带有黑色背景的视频，依次显示每个段落作为字幕，并与相应的音频同步。
4. **输出**：
   - 最终视频将保存为与脚本同一目录下的 `educational_video.mp4`。
   - 每个段落的音频文件将保存在 `audio` 目录中。

### 注意事项

- **DeepSeek API**：脚本使用 `deepseek-chat` 模型优化脚本。确保您的 API 密钥有效且有足够的额度。DeepSeek API 在此用于为视频叙述构建脚本，因为它在文本生成和优化方面表现出色。[](https://www.datacamp.com/tutorial/deepseek-api)
- **Google Cloud Text-to-Speech**：脚本使用 `en-US-Wavenet-D` 语音进行自然发音的英语叙述。您可以通过修改 `VoiceSelectionParams` 中的 `name` 参数来更改语音（有关其他语音选项，请参阅 Google Cloud Text-to-Speech 文档）。
- **MoviePy**：视频以 1280x720 分辨率（高清）创建。您可以调整 `TextClip` 和 `ColorClip` 中的 `size` 参数以获取不同分辨率。
- **时间同步**：脚本通过将文本剪辑持续时间设置为匹配音频持续时间来确保字幕与音频同步。对于 1 分钟视频，DeepSeek 提示会强制脚本简洁。
- **依赖项**：确保 FFmpeg 已安装并可在系统的 PATH 中访问，以便 `moviepy` 正常工作。

### 示例输出

如果您的输入脚本是关于机器学习的，优化后的脚本可能如下所示：

```
["Machine learning, a branch of AI, enables computers to learn from data.",
 "It uses algorithms to find patterns and predict outcomes.",
 "Applications include image recognition and healthcare innovations."]
```

- 每个段落生成一个音频文件（例如 `paragraph_1.mp3`、`paragraph_2.mp3` 等）。
- 最终视频显示黑色背景，白色字幕依次出现，与音频叙述同步。

这种方法简单、经济高效，并能产生适合 YouTube 或教育网站的专业外观教育视频。如果您需要进一步定制（例如不同的字体、字幕样式或附加效果），请告诉我！
