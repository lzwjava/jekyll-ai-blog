---
audio: false
generated: false
image: false
lang: en
layout: post
title: Automated Draft for Blog Management with VSCode Restart
translated: false
type: post
---

The script you've provided is designed to automate the process of publishing draft blog posts in a structured manner. It is particularly useful for bloggers or content creators who manage their posts as drafts before they are ready to be published. Here's an extended introduction to give more context about the script:

## Introduction

Managing a blog or any content-driven website often involves creating and storing drafts before they are ready to be published. This script is tailored to streamline the workflow of moving draft posts to a designated publishing directory, specifically for a static site generator setup, such as those using Jekyll or similar frameworks.

The script performs the following key tasks:

```python
import os
import datetime
import glob
import shutil
import sys
import subprocess
import time

def publish_drafts_to_posts():
    """Checks for draft files created today and moves them to the _posts/en directory."""
    today = datetime.date.today()
    date_str = today.strftime('%Y-%m-%d')

    drafts_dir = '_drafts'
    posts_en_dir = "original"

    if not os.path.exists(drafts_dir):
        print(f"Drafts directory '{drafts_dir}' does not exist. No files to publish.")
        return

    if not os.path.exists(posts_en_dir):
        os.makedirs(posts_en_dir)

    # Pattern to find files in drafts directory starting with today's date and ending with -en.md
    pattern = os.path.join(drafts_dir, f"{date_str}-*-en.md")

    found_files = glob.glob(pattern)

    if not found_files:
        print(f"No draft files found in '{drafts_dir}' starting with '{date_str}' to publish.")
        return

    for file_path in found_files:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(posts_en_dir, file_name)

        try:
            shutil.move(file_path, destination_path)
            print(f"Moved '{file_name}' from '{drafts_dir}' to '{posts_en_dir}'.")
        except Exception as e:
            print(f"Error moving '{file_name}': {e}")

    restart_vscode()

def restart_vscode():
    print("Restarting VSCode gracefully to prevent accidental re-creation of draft files...")
    try:
        if sys.platform == 'win32':
            # Graceful close without /f
            os.system('taskkill /im Code.exe /t')
            time.sleep(3)  # Delay for cleanup
            subprocess.Popen(['code', '.'])  # Reopen
        elif sys.platform == 'darwin':
            # Use AppleScript for graceful quit
            os.system('osascript -e \'quit app "Visual Studio Code"\'')
            time.sleep(3)
            subprocess.call(['open', '-a', 'Visual Studio Code', '.'])
        elif sys.platform.startswith('linux'):
            # SIGTERM for graceful termination
            os.system('killall code')
            time.sleep(3)
            subprocess.Popen(['code', '.'])
        else:
            print("Unsupported platform for restarting VSCode.")
    except Exception as e:
        print(f"Error during restart: {e}. Please manually restart VSCode.")

if __name__ == "__main__":
    publish_drafts_to_posts()
```
