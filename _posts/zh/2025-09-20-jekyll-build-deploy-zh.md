---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 自动化Jekyll构建与部署流程
translated: true
type: note
---

你可以完全在 GitHub Actions 中实现：在运行器上构建网站，然后将目标仓库检出到子文件夹，并将 `_site/` 目录的内容推送过去。

以下是可添加到**源**仓库（存放 Python 脚本和 Jekyll 内容的地方）的即用工作流：

{% raw %}

```yaml
# .github/workflows/build-and-deploy.yml
name: 构建并部署 Jekyll 到外部仓库

on:
  push:
    branches: [ main ]
  workflow_dispatch:

# 我们将使用 PAT 来推送到目标仓库
permissions:
  contents: read

jobs:
  build-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: 检出源仓库
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 设置 Ruby 环境
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true

      - name: 安装 Jekyll 依赖
        run: |
          bundle install --jobs 4 --retry 3

      - name: 设置 Python 环境
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 安装 Python 依赖
        if: hashFiles('requirements.txt') != ''
        run: pip install -r requirements.txt

      - name: 运行本地工作流管道（CI 模式）
        env:
          # 在此添加脚本所需的所有密钥
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        run: |
          # 运行与脚本编排完全相同的步骤。
          # 如果愿意，可以直接调用脚本：
          python scripts/workflow_local.py
          # 或者，如果更喜欢明确的步骤：
          # python scripts/generate/update_notes_link.py
          # python scripts/translation/update_lang.py --max_files 9 --model gemini-flash --commits 1000
          # python -m unittest discover -s tests/workflow
          # python scripts/release/update_release.py

      - name: 构建 Jekyll（到 _site 目录）
        run: |
          # 如果你的 Python 模块在其他地方设置了 DEFAULT_DESTINATION，你仍然可以在这里覆盖。
          bundle exec jekyll build --destination _site

      - name: 检出目标仓库
        uses: actions/checkout@v4
        with:
          repository: lzwjava/lzwjava.github.io   # <-- 你的 DESTINATION_REPO_URL 目标
          token: ${{ secrets.WORKFLOW_ACCESS_TOKEN }}      # <-- 具有 "repo" 范围的 PAT
          path: destination
          fetch-depth: 0

      - name: 同步构建后的网站到目标仓库
        run: |
          mkdir -p destination/_site
          rsync -av --delete _site/ destination/_site/
          cd destination
          # 可选：确保 Pages 不会再次处理 Jekyll
          touch _site/.nojekyll

          git config user.name  "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          if [ -n "$(git status --porcelain)" ]; then
            git add -A
            git commit --amend --no-edit
            # 如果你的目标分支使用其他名称（例如 gh-pages），请调整分支
            git push --force-with-lease origin HEAD:main
          else
            echo "No changes to deploy."
          fi

      - name: （可选）上传构建后的网站产物
        uses: actions/upload-artifact@v4
        with:
          name: site
          path: _site
```

{% endraw %}

### 需要设置的内容

* **用于推送目标的 PAT**：在你的 GitHub 账户上创建一个经典的 Personal Access Token，需具有 `repo` 范围（或使用一个细粒度令牌，授予对目标仓库的写入权限）。将其作为 `WORKFLOW_ACCESS_TOKEN` 保存在源仓库的设置中（即 `Settings → Secrets and variables → Actions → New repository secret`）。
* **分支和仓库名称**：在 `检出目标仓库` 步骤中，将 `repository:` 设置为外部仓库（可以是公开或私有的）。在推送命令中，设置你想要部署到的分支（通常是 `main` 或 `gh-pages`）。
* **GitHub Pages 设置**（如果你要从目标仓库提供服务）：在该仓库的 **Settings → Pages** 中，选择正确的 **Branch**（例如 `main` / root），并根据需要保留 `CNAME`/自定义域名。
* **历史记录预期**：部署步骤会修改最新提交并使用 `--force-with-lease`；请确保该分支专门用于部署产物，因此重写历史记录是可接受的。

### 关于你的 Python 脚本的说明

* 在 CI 中你不需要 `open_destination_repo_in_browser()`，所以保持原样即可；它在这里不会被调用。工作流会直接从运行器推送。
* 在 CI 中你也不需要 `push_destination_repo()`。工作流处理第二次检出和推送，因此你可以保持脚本在本地运行时不作更改。
* 如果你的 `build_site()` 写入到不同的 `DEFAULT_DESTINATION`，你仍然可以通过运行上面显示的显式 Jekyll 构建步骤来覆盖，该步骤会写入到 `_site/`。部署步骤会从 `_site/` 进行同步。

### 目标仓库是私有的？

* 没问题。GitHub Pages 仅服务于公共仓库（或在启用了 Pages 的组织中的公共分支），但如果你的目标只是出于某种原因将产物推送到私有仓库，上述方法仍然有效。如果你确实需要 Pages 托管，请确保目标仓库/分支配置为提供 Pages 服务（在需要的地方设为公开），或者使用替代主机（例如 Cloudflare Pages、Netlify）并部署到那里。

就是这样——你现在可以在 GitHub 的运行器上构建，并将 `_site/` 推送到云中的另一个仓库。
