---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Markdown笔记中的YouTube上传
translated: true
type: note
---

以下是构建并连接的内容：

**已创建：`ww/gen_video/youtube_upload.py`**

- YouTube 上传模块，可从 Markdown 笔记的 YAML 前置元数据中读取标题、描述和标签
- 通过 YouTube Data API v3 使用可续传上传方式将 MP4 文件上传至 YouTube
- 支持 `--public`、`--unlisted`、`--credential`、`--description`、`--tags` 选项
- OAuth 2.0 流程：打开浏览器进行身份验证，令牌缓存至 `~/.google/youtube_token.json`
- 需要将 `client_secret.json` 文件放置于 `~/.google/client_secret.json`（错误信息中有设置说明）

**已修改：`ww/main.py`**

- gen-video 调度逻辑现在会先检查 `upload` 子命令，再回退到原有的视频生成流程
- `ww gen-video <file>` 仍保持原有行为不变
- `ww gen-video upload <note_path> <mp4_path>` 将路由至新的上传模块
- 帮助文本已更新，同时显示两个命令

**已修改：`~/.zsh/completions/_ww`**

- 新增包含 `upload` 条目的 `gen_video_cmds` 数组
- 在子命令调度中为 `gen-video` 新增 case 分支
- 新增 `gen-video upload` 补全功能，支持 `*.md`（笔记）和 `*.mp4`（视频）文件建议

**已安装依赖：**

- 通过 `uv add` 安装 `google-api-python-client`、`google-auth-oauthlib`

**已验证：**

- `ww gen-video upload --help` — 显示正确用法
- `ww gen-video --help` — 保留原有行为
- `ww gen-video upload some_note.md` — 报错：缺少 mp4_path
- `ww gen-video upload /path/to/note.md /nonexistent/video.mp4` — 报错：视频文件不存在
- 主帮助信息（`ww`）显示两个 gen-video 条目

要实际执行上传，你需要：

1. 创建一个 Google Cloud 项目 → 启用 YouTube Data API v3 → 创建 OAuth 2.0 桌面应用凭据
2. 将 JSON 文件保存为 `~/.google/client_secret.json`
3. 运行 `ww gen-video upload notes/your-post.md output.mp4`
