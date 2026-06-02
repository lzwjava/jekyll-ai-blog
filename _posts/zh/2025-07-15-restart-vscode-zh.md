---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 自动化博客管理草稿与VSCode重启
translated: true
type: post
---

你提供的脚本旨在自动化以结构化方式发布草稿博客文章的过程。它特别适用于博客作者或内容创作者，他们会在文章准备好发布之前将其保存为草稿。以下是脚本的扩展介绍，以提供更多背景信息：

## 介绍

管理博客或任何内容驱动的网站通常涉及在准备好发布之前创建和存储草稿。该脚本旨在简化将草稿文章移动到指定发布目录的工作流程，特别是针对静态站点生成器设置，例如使用Jekyll或类似框架的情况。

该脚本执行以下关键任务：

```python
import os
import datetime
import glob
import shutil
import sys
import subprocess
import time

def publish_drafts_to_posts():
    """检查今天创建的草稿文件并将它们移动到 _posts/en 目录。"""
    today = datetime.date.today()
    date_str = today.strftime('%Y-%m-%d')

    drafts_dir = '_drafts'
    posts_en_dir = "original"

    if not os.path.exists(drafts_dir):
        print(f"草稿目录 '{drafts_dir}' 不存在。没有文件可发布。")
        return

    if not os.path.exists(posts_en_dir):
        os.makedirs(posts_en_dir)

    # 在草稿目录中查找以今天日期开头并以 -en.md 结尾的文件模式
    pattern = os.path.join(drafts_dir, f"{date_str}-*-en.md")

    found_files = glob.glob(pattern)

    if not found_files:
        print(f"在 '{drafts_dir}' 中未找到以 '{date_str}' 开头的草稿文件可发布。")
        return

    for file_path in found_files:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(posts_en_dir, file_name)

        try:
            shutil.move(file_path, destination_path)
            print(f"已将 '{file_name}' 从 '{drafts_dir}' 移动到 '{posts_en_dir}'。")
        except Exception as e:
            print(f"移动 '{file_name}' 时出错：{e}")

    restart_vscode()

def restart_vscode():
    print("正在优雅地重启 VSCode 以防止意外重新创建草稿文件...")
    try:
        if sys.platform == 'win32':
            # 使用 /t 进行优雅关闭
            os.system('taskkill /im Code.exe /t')
            time.sleep(3)  # 延迟清理
            subprocess.Popen(['code', '.'])  # 重新打开
        elif sys.platform == 'darwin':
            # 使用 AppleScript 进行优雅退出
            os.system('osascript -e \'quit app "Visual Studio Code"\'')
            time.sleep(3)
            subprocess.call(['open', '-a', 'Visual Studio Code', '.'])
        elif sys.platform.startswith('linux'):
            # 使用 SIGTERM 进行优雅终止
            os.system('killall code')
            time.sleep(3)
            subprocess.Popen(['code', '.'])
        else:
            print("不支持重启 VSCode 的平台。")
    except Exception as e:
        print(f"重启期间出错：{e}。请手动重启 VSCode。")

if __name__ == "__main__":
    publish_drafts_to_posts()
```
