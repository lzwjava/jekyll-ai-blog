---
audio: false
generated: true
lang: zh
layout: post
title: YouTube视频字幕提取方法
translated: true
type: note
---

要获取YouTube视频的所有字幕，请根据您的需求以及选择手动或自动方式，按照以下步骤操作。请注意，视频必须提供字幕（可以是自动生成或创作者上传的）。

### 手动方法（使用YouTube内置的转录功能）

1. **打开视频**：在网页浏览器中访问YouTube并找到目标视频。
2. **检查字幕**：点击视频暂停播放。查看播放器右下角是否有“CC”（隐藏式字幕）图标。如果可见，则表示该视频提供字幕。
3. **打开转录文本**：
   - 向下滚动至视频描述部分，点击“显示更多”。
   - 找到并点击“显示转录”（如有）。这将在视频右侧打开带时间戳和文本的转录面板。
4. **切换时间戳**：点击转录面板右上角的三个垂直点，选择“切换时间戳”以显示或隐藏时间戳。
5. **复制转录文本**：
   - 滚动至转录文本底部，在最后一行文字后点击并按住，然后拖动至顶部以全选文本。
   - 按 `Ctrl + C`（Windows）或 `Command + C`（Mac）复制。
6. **粘贴保存**：打开文本编辑器（如记事本、TextEdit或Word），按 `Ctrl + V` 或 `Command + V` 粘贴文本，并保存为`.txt`文件或您偏好的格式。

**注意**：此方法仅适用于YouTube网站，不适用于移动应用。[](https://www.wikihow.com/Download-YouTube-Video-Subtitles)

### 面向内容创作者（下载自有视频字幕）

如果您是视频所有者，可直接通过YouTube Studio下载字幕：

1. **登录YouTube Studio**：访问 [studio.youtube.com](https://studio.youtube.com)。
2. **选择视频**：点击左侧菜单中的“内容”，然后选择目标视频。
3. **访问字幕**：点击左侧菜单中的“字幕”，选择语言。
4. **下载字幕**：点击字幕轨道旁的三点菜单，选择“下载”。选择格式如`.srt`、`.vtt`或`.sbv`。
5. **编辑使用**：在文本编辑器或字幕编辑器（如Aegisub）中打开下载的文件进行后续使用。

**注意**：您只能下载自己管理频道上视频的字幕文件。[](https://ito-engineering.screenstepslive.com/s/ito_fase/a/1639680-how-do-i-download-a-caption-file-from-youtube)

### 自动方法（使用第三方工具）

如需特定格式（如`.srt`）或下载非自有视频字幕，可使用可靠的第三方工具：

1. **选择工具**：常用工具包括：
   - **DownSub**：免费在线字幕下载工具。
   - **Notta**：提供高准确度的转录和字幕下载服务。[](https://www.notta.ai/en/blog/download-subtitles-from-youtube)
   - **4K Download**：用于提取字幕的桌面应用程序。[](https://verbit.ai/captioning/a-guide-to-downloading-subtitles-and-captions-from-youtube-enhancing-accessibility-and-user-experience/)
2. **复制视频URL**：打开YouTube视频，点击视频下方的“分享”，复制URL。
3. **使用工具**：
   - 将URL粘贴至工具的输入框。
   - 选择所需语言和格式（如`.srt`、`.txt`）。
   - 点击“下载”或“提取”并保存文件。
4. **验证**：打开文件检查准确性，自动生成字幕可能存在错误。

**注意**：请使用可信工具以避免安全风险。部分工具可能含广告或需付费使用高级功能。[](https://gotranscript.com/blog/how-to-download-subtitles-from-youtube)

### 使用YouTube API（面向开发者）

如需批量提取字幕或应用集成，可使用YouTube Data API：

1. **设置API访问**：在[Google Cloud Console](https://console.cloud.google.com)创建项目，启用YouTube Data API v3并获取API密钥。
2. **列出字幕轨道**：使用`captions.list`端点获取视频可用字幕轨道。示例：

   ```
   GET https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=视频ID&key=API密钥
   ```

3. **下载字幕**：使用`captions.download`端点获取特定字幕轨道。示例：

   ```
   GET https://www.googleapis.com/youtube/v3/captions/字幕ID?tfmt=srt&key=API密钥
   ```

4. **限制说明**：
   - 仅可下载自有视频字幕，除非视频所有者已公开字幕。
   - API使用存在配额限制（每条字幕下载约消耗200单位）。[](https://developers.google.com/youtube/v3/docs/captions)[](https://stackoverflow.com/questions/73863672/how-can-i-get-captions-of-a-youtube-video-and-display-it-separately)
5. **替代方案**：部分开发者通过抓取视频页面源码中的定时文本URL（如`https://www.youtube.com/api/timedtext?...`）获取字幕，但该方法不稳定，可能违反YouTube条款并导致IP封禁。[](https://stackoverflow.com/questions/73863672/how-can-i-get-captions-of-a-youtube-video-and-display-it-separately)

### 附加提示

- **语言选择**：若视频提供多语言字幕，可通过“字幕/CC”设置或转录文本下拉菜单选择偏好语言。[](https://riverside.fm/blog/youtube-transcription)
- **自动生成字幕**：因口音、背景噪音或复杂音频可能导致错误，如需精确字幕请审阅编辑。[](https://support.google.com/youtube/answer/6373554?hl=en)
- **无障碍支持**：字幕可提升听障用户访问体验，并通过内容可搜索性优化SEO。[](https://www.descript.com/blog/article/transcript-of-youtube-videos)
- **无可用字幕**：若视频无字幕，可考虑使用Rev、Notta等转录服务通过音频生成文本。[](https://www.rev.com/resources/how-to-download-youtube-subtitles-as-text-files)[](https://www.notta.ai/en/blog/download-subtitles-from-youtube)

### 限制说明

- 并非所有视频都提供字幕，特别是创作者禁用字幕或YouTube自动字幕不支持该语言/音频质量时。[](https://support.google.com/youtube/answer/6373554?hl=en)
- YouTube移动应用不支持查看转录文本，但可通过“CC”按钮启用字幕。[](https://riverside.fm/blog/youtube-transcription)
- 部分第三方工具或API方法可能不适用于自动生成字幕或受限视频。[](https://stackoverflow.com/questions/9611397/how-to-extract-closed-caption-transcript-from-youtube-video)

如果您需要特定视频的字幕或特定格式，请告知我，我将为您提供进一步指导！
