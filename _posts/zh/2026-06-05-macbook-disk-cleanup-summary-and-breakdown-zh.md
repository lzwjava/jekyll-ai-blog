---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MacBook磁盘清理总结与细分
translated: true
type: note
---

这是完整的情况。

```
═══════════════════════════════════════════════════════════════
 磁盘清理摘要 — MacBook Air M2
═══════════════════════════════════════════════════════════════

 之前：已用 364 GB / 总容量 460 GB  |  可用约 1 GB  |  已满 94%  ⚠️
 之后：已用 364 GB / 总容量 460 GB  |  可用 60 GB  |  已使用 86%  ✓

 总计释放：约 95 GB
═══════════════════════════════════════════════════════════════
```

已清理内容（按大小）：

```
 大小     项目                          为何占用大
 ─────────────────────────────────────────────────────────────
 23 GB    .git tmp_pack 文件             10 次被中断的 git gc 操作
          (lzwjava.github.io)           因睡眠/终止中断数周。
                                        纯冗余——安全删除。

 21 GB    ~/.cache/huggingface/          下载的模型权重：
          llama-7b-hf (13 GB)           bge-reranker, bce-embedding,
          gpt2, MiniLM 等                chatglm-6b, DeepSeek-R1。
                                        按需重新下载。

  7 GB    ~/Library/Caches/JetBrains/    IntelliJ/PyCharm 构建缓存、
                                        索引、日志。自动重新生成。

  7 GB    ~/.npm/                        node 项目的 npm 下载缓存。
                                        npm 会重建。

  5 GB    ~/.cache/torch/                PyTorch hub 模型 (torch.hub.load
                                        下载)。自动重新下载。

  3 GB    ~/Library/Caches/Homebrew/     下载的 formula 包。
                                        brew 按需重新下载。

  3 GB    ~/.cache/pre-commit/           Pre-commit 钩子环境
                                        (每个钩子的虚拟环境)。下次运行
                                        时 pre-commit 重新安装。

  3 GB    ~/Library/Caches/pip/          pip wheel/构建缓存。
                                        下次安装时 pip 会重建。

  1 GB    ~/.cache/uv/                   uv 包缓存。
                                        下次同步时 uv 会重建。

  1 GB    ~/Library/Caches/LarkShell/    Lark/飞书桌面端缓存。
```

仍占用空间的内容（可操作）：

```
 大小     项目                          操作建议
 ─────────────────────────────────────────────────────────────
 35 GB    lzwjava.github.io .git/       运行 `git gc --aggressive` 重打包
          (23 个包，2950 万个对象)       成 1 个紧凑包。
          对于 1666 次提交仍然臃肿。     可能再节省 5-10 GB。
          历史可能包含大型二进制文件。

 37 GB    ~/Library/Containers/          WeChat 占 19 GB（聊天
          WeChat 19 GB                   历史、媒体、缓存）。
          Docker 8 GB                   打开 WeChat → 设置 →
          QQ 4.5 GB                     存储 → 管理 → 清理。
          Teams 1 GB                    Docker: docker system prune -a
          Slack 860 MB

 11 GB    ~/Library/Caches 剩余          ms-playwright, go-build,
          （清理后）                     vscode-cpptools, camoufox,
                                        Spotify, Cypress。优先级较低。

 58 GB    ~/projects/（不含 .git）        Qwen2.5-Coder (3.4 GB),
          jekyll-ai-blog (3 GB),
          blog-assets (2.3 GB),
          jdk (2.4 GB) 等。
                                        审查：Air 上是否仍需要所有
                                        克隆的仓库？

  5 GB    ~/Library/Application Sup/     JetBrains 5.4 GB（插件、
          nomic.ai 3.5 GB                本地模型？）。nomic.ai 很可能是
          Steam 1.4 GB                   本地嵌入模型。
          Discord 1.2 GB
```

已保留内容（未触及）：

```
 ✓ 所有项目源代码
 ✓ 所有应用数据与配置
 ✓ Git 仓库（工作树完好）
 ✓ ~/Documents, ~/Desktop, ~/Downloads
 ✓ 所有应用容器（WeChat, Docker 等）
 ✓ HuggingFace 认证令牌
 ✓ 所有环境配置（.env, .zshrc 等）
```

剩余可快速回收空间（如需更多）：

```
 1. 对 lzwjava.github.io 执行 git gc --aggressive     ~5-10 GB
 2. WeChat 存储清理（应用设置）                         ~10-15 GB
 3. Docker 清理（如果在 Air 上不使用）                  ~8 GB
 4. 删除 Air 上不再使用的陈旧仓库                      ~20+ GB
```

需要我处理其中任何一项吗？