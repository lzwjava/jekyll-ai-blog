---
audio: false
generated: true
lang: zh
layout: post
title: 提升yt-dlp音频质量
translated: true
type: note
---

针对您在使用脚本配合 `yt-dlp` 下载 YouTube 视频时对音质不够理想的担忧，我将指导您如何修改脚本以确保始终下载**最佳音质**，无论选择何种视频分辨率（720p 或 480p）。让我们逐步分析并提供清晰的解决方案。

### 理解当前脚本
您的脚本使用 `yt-dlp` 下载 YouTube 视频，允许您指定分辨率（720p 或 480p）。格式选择由 `format_str` 变量控制，该变量传递给 `yt-dlp` 的 `-f` 选项。当前设置如下：

- **720p**：`format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'`
- **480p**：`format_str = 'bestvideo[height<=480]+bestaudio/best[height<=720]'`

在 `yt-dlp` 中：
- `bestvideo[height<=720]` 选择高度不超过 720 像素的最佳视频流。
- `bestaudio` 选择可用的最佳纯音频流（通常是最高码率的音频）。
- `+` 运算符指示 `yt-dlp` 分别下载视频和音频流，然后合并为单个文件。
- `/` 运算符提供备选方案：如果前面的组合（如 `bestvideo[height<=720]+bestaudio`）不可用，则使用后面的格式（如 `best[height<=720]`），即包含视频和音频的最高 720p 单一格式。

由于已包含 `bestaudio`，脚本本应选择最佳可用音质。但您注意到音质"不够好"，让我们探究原因并修复。

### 音质欠佳的可能原因
尽管使用了 `bestaudio`，仍存在潜在问题：
- 备选选项（`best[height<=720]`）可能在极少数情况下被触发（当指定的视频和音频流无法组合时）。该备选选项会选择合并的视频+音频格式，其音质可能较低（例如 128kbps，而非独立的 256kbps 音频流）。
- 对于 480p 的情况，备选项是 `best[height<=720]`，这存在不一致性——它可能下载 720p 视频（而您要求 480p），且该合并格式的音质可能非最佳。

由于 YouTube 通常提供独立的视频和音频流，`bestvideo + bestaudio` 组合几乎总能生效。但为确保最佳音质并避免降级至低质量合并格式，我们需要优化脚本。

### 解决方案：确保最佳音质
为确保 `yt-dlp` 始终下载最佳音质：
1. **使用无备选方案的 `bestaudio`**：强制 `yt-dlp` 下载最佳音频流，同时下载所选分辨率的最佳视频流。如果此组合不可用，程序将报错而非妥协音质——这是可接受的，因为 YouTube 视频几乎总有独立流。
2. **修复 480p 备选方案的不一致性**：将备选项（若保留）与请求的分辨率对齐，但直接移除备选项更简单且符合您的目标。

修改脚本方法如下：

#### 修改后的代码
按以下方式更新脚本中的 `format_str` 定义：

```python
import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos at specified resolution.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--resolution",
        choices=["720p", "480p"],
        default="720p",
        help="Video resolution to download (default: 720p)"
    )
    args = parser.parse_args()

    output_dir = "test"
    os.makedirs(output_dir, exist_ok=True)

    # 更新格式字符串以确保最佳音质
    if args.resolution == "720p":
        format_str = 'bestvideo[height<=720]+bestaudio'
    else:  # 480p
        format_str = 'bestvideo[height<=480]+bestaudio'

    command = [
        "yt-dlp",
        "--cookies-from-browser", "firefox",
        "-f", format_str,
        "-P", output_dir,
        args.url
    ]

    subprocess.run(command)

if __name__ == "__main__":
    main()
```

#### 修改说明
- **720p**：从 `'bestvideo[height<=720]+bestaudio/best[height<=720]'` 改为 `'bestvideo[height<=720]+bestaudio'`。
- **480p**：从 `'bestvideo[height<=480]+bestaudio/best[height<=720]'` 改为 `'bestvideo[height<=480]+bestaudio'`。
- **移除了备选方案（`/best[height<=...]`）**：确保 `yt-dlp` 始终使用最佳音频流（`bestaudio`），避免可能降级至低音质合并格式。

### 为何此方案有效
- **`bestaudio`**：选择最高码率的可用音频流（例如 160kbps 的 Opus 或 256kbps 的 AAC，具体取决于视频），确保最佳音质。
- **无备选方案**：通过移除 `/best[height<=720]`，防止 `yt-dlp` 下载音质较差的合并格式。由于 YouTube 视频通常有独立流，`bestvideo + bestaudio` 应总能成功。
- **分辨率限制**：视频分辨率严格遵循您的选择（720p 或 480p），同时音质最大化。

### 验证结果
为确认您获得了最佳音质：
1. **检查可用格式**：运行 `yt-dlp --list-formats <youtube_url>` 查看特定视频的可用视频和音频流。关注纯音频格式（如 `m4a`、`webm`）及其码率。
2. **监控下载过程**：运行脚本时，`yt-dlp` 会输出正在下载的格式（如 "Downloading video stream (code)" 和 "Downloading audio stream (code)"）。确保其选择了高码率的独立音频流。
3. **测试播放**：播放下载的文件并验证音质。若仍不理想，可能是视频上传者提供的音频质量有限，而非脚本问题。

### 如果失败怎么办？
如果因 `bestvideo[height<=720]+bestaudio` 不可用导致 `yt-dlp` 报错（YouTube 上极罕见），您可以：
- 重新添加备选方案如 `/best[height<=720]'`，但这可能牺牲音质（应避免）。
- 使用 `--list-formats` 检查该特定视频，并针对性调整脚本（但很少需要）。

### 结论
您的脚本现已设置为始终下载最佳可用音质，通过使用无备选方案的 `bestaudio` 配合您选择的视频分辨率。修改后的 `format_str` 值为：

- 720p：`'bestvideo[height<=720]+bestaudio'`
- 480p：`'bestvideo[height<=480]+bestaudio'`

此更改应解决您的问题，确保在您偏好的分辨率范围内获得最高音质。如果音质仍不理想，可能是视频原始上传质量所致，这超出脚本控制范围。请尝试使用并反馈效果！
