---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 通过Cron实现Git自动同步
translated: true
type: note
---

要实现从一台笔记本电脑的 Git 推送自动同步更新到另一台笔记本电脑上相同仓库的克隆版本（无需手动执行 `git pull`），仅靠 Git 本身无法实现跨机器的实时“自动”更新——Git 在设计上是基于拉取（pull）的。不过，你可以在第二台笔记本电脑上设置一个定时任务，定期从远程仓库（在你的案例中是 GitHub）获取（fetch）并合并（merge）更改。对于你这样的个人设置来说，这是最简单可靠的方法。

以下是在你的 Mac 上操作的方法（因为你使用的是 MacBook Air）。我们将使用 `cron` 进行调度，因为它内置且轻量。假设两台笔记本电脑都克隆了 `github.com:lzwjava/blog-source` 仓库，并且你处于 `main` 分支。

### 步骤 1：确保第二台笔记本电脑的仓库设置正确
在第二台笔记本电脑上：
1.  导航到你的仓库目录：`cd /path/to/blog-source`
2.  确保它跟踪了远程仓库：`git remote -v`（应该显示 `origin` 是你的 GitHub 仓库）。
3.  如果没有，添加它：`git remote add origin git@github.com:lzwjava/blog-source.git`
4.  获取当前状态：`git fetch origin`
5.  切换到 main 分支：`git checkout main`
6.  设置上游分支：`git branch --set-upstream-to=origin/main main`

测试手动拉取：`git pull origin main`。它应该能像你的输出那样工作。

### 步骤 2：创建自动拉取脚本
创建一个简单的 shell 脚本来安全地处理拉取操作（它会获取更新，检查冲突，如果本地是干净的则进行拉取）。

1.  在你的仓库根目录下，创建 `auto-pull.sh` 文件：
    ```bash:disable-run
    #!/bin/bash
    cd "$(dirname "$0")"  # 切换到仓库目录
    git fetch origin
    if git diff HEAD origin/main --quiet; then
        git pull origin main
        echo "Auto-pull completed: $(date)"
    else
        echo "Warning: Local changes detected. Skipping pull. Resolve manually: $(date)"
        # 可选：发送邮件或通知（见下文）
    fi
    ```

2.  使其可执行：`chmod +x auto-pull.sh`

这个脚本：
-   获取更新但不合并。
-   检查你的本地分支是否是干净的（没有未提交的更改）。
-   仅在安全的情况下拉取；否则发出警告。

### 步骤 3：使用 Cron 进行调度
Cron 会定期运行任务。我们将其设置为每 5 分钟运行一次（根据需要调整，例如每小时）。

1.  打开 crontab 编辑器：`crontab -e`（如果提示，使用 nano：`nano ~/.crontab`）。

2.  在末尾添加这一行（每 5 分钟一次）：
    ```
    */5 * * * * /path/to/blog-source/auto-pull.sh >> /path/to/blog-source/pull-log.txt 2>&1
    ```
    -   将 `/path/to/blog-source` 替换为你的实际仓库路径（例如 `~/blog-source`）。
    -   `>> pull-log.txt` 将输出记录到一个文件中，用于调试。

3.  保存并退出（在 nano 中按 Ctrl+O, Enter, Ctrl+X）。
4.  验证：`crontab -l`（应该显示你添加的行）。
5.  测试：等待 5 分钟，或者临时在 `crontab -e` 中添加 `* * * * *`（每分钟一次）进行测试，然后恢复。

Cron 以你的用户身份运行，因此它会使用你的 SSH 密钥进行 GitHub 认证（就像在你的拉取输出中看到的那样）。

### 可选增强功能
-   **处理冲突/通知**：如果脚本检测到问题，可以添加通知。编辑 `auto-pull.sh` 文件，追加：
    ```bash
    # 如果出现警告，发送 macOS 通知
    osascript -e 'display notification "Git pull skipped due to local changes" with title "Blog Repo Sync"'
    ```
-   **在推送时运行（从第一台笔记本电脑）**：要实现更像“推送”的同步，可以在第一台笔记本电脑上使用 GitHub Actions。创建 `.github/workflows/sync.yml` 文件：
    ```yaml
    name: Auto Sync
    on: [push]
    jobs:
      sync:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Notify (e.g., via webhook to second laptop)
            run: curl -X POST https://your-second-laptop-webhook-endpoint  # 在第二台笔记本电脑上设置一个简单的服务器来接收
    ```
    但这需要在第二台机器上运行一个监听器（例如通过 ngrok + 一个小的 Flask 应用），对于大多数情况来说过于复杂。
-   **频率权衡**：对于博客仓库，每 5 分钟一次是可以的。如果需要实时同步，可以考虑在终端中使用 `watch` 工具（`watch -n 300 git pull`），但 cron 是免手动操作的。
-   **代理说明**：你的输出显示了 HTTP/HTTPS 代理——cron 会继承这些环境变量，所以拉取操作应该能像现在这样工作。

现在，当你从第一台笔记本电脑推送（`git push origin main`）时，第二台电脑将每 5 分钟自动同步一次。检查 `pull-log.txt` 文件查看历史记录。

如果你在 cron 中遇到认证/代理问题，可以在脚本中添加 `export HTTP_PROXY=http://127.0.0.1:7890` 等语句。对于另一台笔记本电脑上的 Windows 系统，请使用任务计划程序（Task Scheduler）代替。
