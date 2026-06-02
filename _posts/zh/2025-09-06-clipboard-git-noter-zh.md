---
audio: false
date: 2025-09-06
generated: true
image: false
lang: zh
layout: post
title: 剪贴板至Git笔记保存器
translated: true
type: note
---

完全可以——用 Python + `pyperclip` 就能实现。下面是一个守护进程风格的脚本，它会轮询剪贴板，每当检测到**超过 500 字符的新文本**时，就会将一个 Markdown 笔记写入 Git 仓库并提交（如果配置了推送，还会自动推送）。

### 功能说明

* 每隔约 0.7 秒轮询一次剪贴板。
* 忽略非文本内容和重复内容。
* 创建带日期标记的笔记文件，例如 `notes/2025/09/2025-09-06_001530_8c9a8f.md`。
* 存储一个轻量的 `index.json` 文件记录已保存内容的哈希值，避免重复提交。
* 自动执行 `git init`（如果需要）；提交更改；如果设置了 `PUSH=1`（并且已配置远程仓库/分支），则自动推送。

### 依赖项

```bash
pip install pyperclip
# 仅限 Linux：你还需要在系统层面安装 xclip 或 xsel
```

### 脚本代码

```python
#!/usr/bin/env python3
import os, time, json, hashlib, subprocess, textwrap, datetime, pathlib, sys
from typing import Optional

try:
    import pyperclip
except Exception as e:
    print("Error: pyperclip not installed. Run `pip install pyperclip`.")
    sys.exit(1)

# ---- 配置 ----
REPO_DIR = os.environ.get("CLIP_REPO", os.path.expanduser("~/clipboard-notes"))
NOTES_DIR = "notes"
MIN_LEN = int(os.environ.get("MIN_LEN", "500"))
POLL_SEC = float(os.environ.get("POLL_SEC", "0.7"))
PUSH = os.environ.get("PUSH", "0") == "1"    # 设置 PUSH=1 以启用 `git push`

INDEX_PATH = os.path.join(REPO_DIR, ".clip_index.json")  # 存储已保存笔记的哈希值

# ---- 工具函数 ----
def run(cmd: list[str], cwd: Optional[str] = None, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)

def ensure_repo():
    os.makedirs(REPO_DIR, exist_ok=True)
    git_dir = os.path.join(REPO_DIR, ".git")
    if not os.path.isdir(git_dir):
        run(["git", "init"], cwd=REPO_DIR)
        # 可选：如果你的 git 默认分支不是 main，可以设置默认分支
        # run(["git", "checkout", "-b", "main"], cwd=REPO_DIR, check=False)

def load_index() -> set[str]:
    if os.path.isfile(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_index(hashes: set[str]):
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(list(hashes)), f, ensure_ascii=False, indent=2)

def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="replace")).hexdigest()

def sanitize_for_frontmatter(s: str) -> str:
    # 保持简单；仅转义可能破坏 frontmatter 分隔符的三连字符
    return s.replace("---", "—")

def write_note(content: str, h: str) -> str:
    now = datetime.datetime.now()
    y = f"{now.year:04d}"
    m = f"{now.month:02d}"
    subdir = os.path.join(REPO_DIR, NOTES_DIR, y, m)
    os.makedirs(subdir, exist_ok=True)
    ts = now.strftime("%Y-%m-%d_%H%M%S")
    fname = f"{ts}_{h[:6]}.md"
    path = os.path.join(subdir, fname)

    snippet = content.strip().splitlines()[0][:120]
    fm_title = sanitize_for_frontmatter(snippet if snippet else f"Clipboard note {ts}")

    body = textwrap.dedent(f"""\
    ---
    title: "{fm_title}"
    created: "{now.isoformat(timespec='seconds')}"
    source: "clipboard"
    length: {len(content)}
    hash: "{h}"
    ---

    {content}
    """)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return path

def git_commit(path: str, msg: str):
    rel = os.path.relpath(path, REPO_DIR)
    run(["git", "add", rel], cwd=REPO_DIR)
    # 同时添加索引文件以保持版本控制
    run(["git", "add", os.path.relpath(INDEX_PATH, REPO_DIR)], cwd=REPO_DIR, check=False)
    run(["git", "commit", "-m", msg], cwd=REPO_DIR)

def git_push_if_enabled():
    if not PUSH:
        return
    # 如果配置了默认上游，则推送
    try:
        run(["git", "push"], cwd=REPO_DIR, check=False)
    except Exception:
        pass

def main():
    print(f"[clipwatch] repo: {REPO_DIR} | min_len: {MIN_LEN} | push: {PUSH}")
    ensure_repo()
    seen_hashes = load_index()
    last_text = None

    while True:
        try:
            txt = pyperclip.paste()
        except Exception as e:
            # 在某些系统上，如果剪贴板不可用，paste 操作可能会抛出异常
            time.sleep(POLL_SEC)
            continue

        if isinstance(txt, str):
            # 仅处理新的剪贴板文本
            if txt != last_text and len(txt) >= MIN_LEN:
                h = sha1(txt)
                if h not in seen_hashes:
                    path = write_note(txt, h)
                    seen_hashes.add(h)
                    save_index(seen_hashes)

                    first_line = txt.strip().splitlines()[0] if txt.strip() else ""
                    commit_msg = f"Add clipboard note: {first_line[:60]}… ({len(txt)} chars)"
                    try:
                        git_commit(path, commit_msg)
                        git_push_if_enabled()
                        print(f"[clipwatch] saved: {os.path.relpath(path, REPO_DIR)}")
                    except subprocess.CalledProcessError as e:
                        print("[clipwatch] git error:", e.stderr or e.stdout)

            last_text = txt
        time.sleep(POLL_SEC)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[clipwatch] bye.")
```

### 如何运行

1. 保存为 `clipwatch.py`。
2. 设置你的仓库路径（可选）：

   ```bash
   export CLIP_REPO=~/my-notes
   export PUSH=1          # 可选，如果设置了远程仓库则启用 git push
   python3 clipwatch.py
   ```

### 设置为登录时启动（macOS launchd 示例）

创建 `~/Library/LaunchAgents/com.zw.clipwatch.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
 <dict>
  <key>Label</key><string>com.zw.clipwatch</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/env</string>
    <string>bash</string>
    <string>-lc</string>
    <string>CLIP_REPO="$HOME/clipboard-notes" PUSH=1 python3 "$HOME/clipwatch.py"</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$HOME/clipwatch.log</string>
  <key>StandardErrorPath</key><string>$HOME/clipwatch.err</string>
 </dict>
</plist>
```

然后执行：

```bash
launchctl load ~/Library/LaunchAgents/com.zw.clipwatch.plist
launchctl start com.zw.clipwatch
```

### 注意事项

* Linux：安装 `xclip` 或 `xsel` 以便 `pyperclip` 可以访问剪贴板。
* 此脚本仅监视**文本**内容。图片/富文本会被忽略。
* 注意敏感信息——此脚本会捕获你复制的任何超过阈值长度的内容。如果需要排除某些内容，可以添加简单的阻止规则（例如，如果文本包含 `-----BEGIN PRIVATE KEY-----`，则跳过；或者通过查询活动应用程序来匹配黑名单，在 macOS 上可以使用 `osascript`）。
* 如果你希望按活动应用程序/窗口进行标记（例如，“来自 Safari”），我可以添加该功能。

如果你更倾向于使用 Rust/Go 来构建一个更轻量级的跨平台二进制文件，或者希望文件名规则与你的博客 Jekyll front-matter 相匹配，请告诉我，我可以为你定制。
