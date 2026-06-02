# jekyll-ai-blog

[English](README.md) | 中文

[![Deploy Jekyll](https://github.com/lzwjava/blog-source/actions/workflows/gh-pages.yml/badge.svg)](https://github.com/lzwjava/blog-source/actions/workflows/gh-pages.yml)[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/lzwjava/jekyll-ai-blog)

追求自由与真理之旅途中的思考、随笔与代码。

## 项目统计

| 文件类型 | 数量 |
|-----------|------|
| Python 文件 ([scripts](scripts), 不含 ml) | 323 |
| Python 文件 ([scripts/ml](scripts/ml)) | 191 |
| Python 测试文件 ([tests](tests)) | 23 |
| C 文件 ([c](c)) | 1 |
| Rust 文件 ([rust](rust)) | 3 |
| C++ 文件 ([cpp](cpp)) | 2 |
| Markdown 文件 ([original](original)) | 515 |
| 笔记文件 ([notes](notes)) | 1992 |

## 核心特性

本博客相比标准 Jekyll 主题 jekyll-theme-cayman 有多项增强：

* **AI 驱动翻译：** 利用先进的语言模型进行准确且符合语境的翻译，将内容扩展到全球受众。
* **XeLaTeX PDF 生成：** 集成 XeLaTeX 生成高质量、可打印的 PDF，方便离线阅读和分享。
* **Google Cloud 文字转语音：** 使用 Google Cloud 的文字转语音服务生成文章音频版本，为视障用户和偏好音频内容的用户提升可访问性。
* **增强的 CSS 样式：** 采用精致的自定义 CSS 设计，提供美观且用户友好的体验。
* **MathJax 支持：** 实现 MathJax 渲染复杂的数学表达式和方程式，让技术内容更易理解。
* **夜间模式：** 包含夜间模式选项，减少眼疲劳，在低光环境下提升可读性。
* **灵活的文章选择：** 提供多种文章筛选选项，如按分类或标签筛选，增强导航体验。
* **定期更新：** 确保博客的库和依赖保持最新，以获得最佳性能和安全性。
* **`awesome-cv` 集成：** 使用 `awesome-cv` 直接从博客生成专业简历。
* **RSS 订阅支持：** 通过 `feed.xml` 提供 RSS 订阅源，方便用户订阅。
* **双语内容：** 支持中英文内容，满足不同受众需求。
* **GitHub 工作流自动化：** 实现 GitHub Actions 自动构建、测试和部署，确保流畅的开发流程。
* **自动翻译工作流：** 使用 GitHub Actions 自动将新发布或更新的文章翻译成多种语言。
* **EPUB 支持：** 将 Markdown 转换为 EPUB 格式，适用于电子书阅读器。

## 快速开始

按照以下步骤设置本地 Jekyll 环境：

```shell
gem install jekyll bundler

jekyll new myblog

cd myblog

bundle install

bundle exec jekyll serve

bundle exec jekyll serve --incremental

bundle exec jekyll serve --draft

bundle exec jekyll serve

bundle add webrick

jekyll serve
```

## Markdown 样式

使用 `rougify` 自定义语法高亮：

```shell
rougify help style

rougify style github > _sass/syntax.css

rougify style gruvbox.dark > _sass/syntax.css

rougify style base16.monokai.dark > _sass/syntax.css
```

## 音频和 PDF 流水线

使用以下命令生成音频和 PDF 文件：

```bash
conda activate google-cloud-env

python scripts/audio_pipeline.py --task posts --n 10

python scripts/audio_pipeline.py --task pages

python scripts/audio_pipeline.py --task notes

python scripts/audio_pipeline.py --task notes --n 100

python scripts/pdf_pipeline.py --task pages

python scripts/pdf_pipeline.py --task posts --n 10

python scripts/pdf_pipeline.py --task notes

python scripts/generate_notes_link.py

python scripts/auto-ss-config/upload_configs.py

python scripts/epub_book.py notes

python scripts/epub_book.py _posts/en

python scripts/epub_book.py _posts/ja

python scripts/update_lang.py --file original/2025-02-02-archlinux-en.md --lang ja  --model gemini
```

## 脚本

使用以下命令创建新的草稿文章：

```
python scripts/draft.py <name>
```

## 内容指南

* `-en`：表示英文文章。
* `-zh`：表示中文文章。

`_posts` 和 `pages` 目录支持 `-en` 和 `-zh` 后缀。

`notes` 目录主要包含用于个人学习的英文内容，不需要翻译。

## 参考

[语法高亮与 Jekyll](https://mcpride.github.io/posts/development/2018/03/06/syntax-highlighting-with-jekyll/)
