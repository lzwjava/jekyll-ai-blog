#!/usr/bin/env python3
import os, time, json, hashlib, subprocess, textwrap, datetime, pathlib, sys, re
from typing import Optional

# Import utilities from create_note_utils
sys.path.append(os.path.join(os.path.dirname(__file__)))
from create_note_utils import clean_grok_tags, clean_content

try:
    import pyperclip
except Exception as e:
    print("Error: pyperclip not installed. Run `pip install pyperclip`.")
    sys.exit(1)

# ---- Config ----
REPO_DIR = os.environ.get("CLIP_REPO", os.path.expanduser("~/clipboard-notes"))
NOTES_DIR = "notes"
MIN_LEN = int(os.environ.get("MIN_LEN", "500"))
POLL_SEC = float(os.environ.get("POLL_SEC", "0.7"))
PUSH = os.environ.get("PUSH", "0") == "1"  # set PUSH=1 to enable `git push`

INDEX_PATH = os.path.join(REPO_DIR, ".clip_index.json")  # stores hashes of saved notes


# ---- Utilities ----
def run(
    cmd: list[str], cwd: Optional[str] = None, check=True
) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)


def ensure_repo():
    os.makedirs(REPO_DIR, exist_ok=True)
    git_dir = os.path.join(REPO_DIR, ".git")
    if not os.path.isdir(git_dir):
        run(["git", "init"], cwd=REPO_DIR)
        # Optional: set default branch if your git default is not main
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
    # keep it simple; escape only triple-dashes fence risk
    return s.replace("---", "—")


def write_clipwatch_note(content: str, h: str) -> str:
    """Create a simplified note using create_note_utils but maintaining clipwatch structure"""
    from create_note_utils import (
        create_filename,
        format_front_matter,
        write_note,
        clean_grok_tags,
        clean_content,
    )

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    # Clean content
    content = clean_grok_tags(content)
    content = clean_content(content)

    # Generate quick filename based on first line + hash
    first_line = content.strip().splitlines()[0][:40] if content.strip() else "clip"
    safe_title = re.sub(r"[^a-zA-Z0-9-]", "", first_line.lower().replace(" ", "-"))
    short_title = f"{safe_title}-{h[:6]}"

    # Create clipwatch-compatible path
    y = f"{now.year:04d}"
    m = f"{now.month:02d}"
    subdir = os.path.join(REPO_DIR, NOTES_DIR, y, m)

    # Use clipwatch-style filename format
    ts = now.strftime("%Y-%m-%d_%H%M%S")
    fname = f"{ts}_{h[:6]}.md"
    path = os.path.join(subdir, fname)

    # Create clipwatch-specific front matter (keeping old format)
    snippet = content.strip().splitlines()[0][:120]
    fm_title = sanitize_for_frontmatter(snippet if snippet else f"Clipboard note {ts}")

    front_matter = f"""---
title: "{fm_title}"
created: "{now.isoformat(timespec='seconds')}"
source: "clipboard"
length: {len(content)}
hash: "{h}"
---"""

    # Use create_note_utils for file writing but with our custom format
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{front_matter}\n\n{content}\n")

    return path


def git_commit(path: str, msg: str):
    rel = os.path.relpath(path, REPO_DIR)
    run(["git", "add", rel], cwd=REPO_DIR)
    # also add index to keep it versioned
    run(
        ["git", "add", os.path.relpath(INDEX_PATH, REPO_DIR)], cwd=REPO_DIR, check=False
    )
    run(["git", "commit", "-m", msg], cwd=REPO_DIR)


def git_push_if_enabled():
    if not PUSH:
        return
    # Push to default upstream if configured
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
            # On some systems paste can throw if clipboard is not available
            time.sleep(POLL_SEC)
            continue

        if isinstance(txt, str):
            # Only process new clipboard text
            if txt != last_text and len(txt) >= MIN_LEN:
                h = sha1(txt)
                if h not in seen_hashes:
                    path = write_clipwatch_note(txt, h)
                    seen_hashes.add(h)
                    save_index(seen_hashes)

                    first_line = txt.strip().splitlines()[0] if txt.strip() else ""
                    commit_msg = (
                        f"Add clipboard note: {first_line[:60]}… ({len(txt)} chars)"
                    )
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
