---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Note Plugin Setup Summary
translated: false
type: note
---

## Note Plugin — Full Setup Summary

### What was done

**1. Installed Fcitx5** (previous session)

- `apt install fcitx5 fcitx5-chinese-addons im-config`
- Set as default input method via `im-config -n fcitx5`
- Config at `~/.config/fcitx5/` — keyboard-us + pinyin, shuangpin mode enabled

**2. Note plugin — already existing, updated**

- The plugin lives in two places:
  - `~/.hermes/plugins/note/` — Hermes reads from here (user plugins dir)
  - `~/projects/config/hermes/plugins/note/` — your config repo (source of truth)
- The live version in `~/.hermes/plugins/note/` was an older copy (May 23)
- Updated `__init__.py` to the July version which has:
  - Reasoning tag stripping (``, etc.)
  - Dotenv loading from `~/projects/ww/.env`
  - LLM title generation via ww's `openrouter_client`
  - Auto git commit + push via `gitmessageai`
  - Fallback sys.path insert for ww when not pip-installed
- Updated `plugin.yaml` to match

**3. Plugin already enabled** in `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
  - note
```

**4. Dependencies installed** (into Hermes venv at `~/.hermes/hermes-agent/venv/`):

- `ww` package — installed via `uv pip install --no-deps -e ~/projects/ww`
- `pyperclip` — for clipboard operations
- `python-dotenv` + `requests` — already in Hermes venv

Did NOT install `ww`'s full dependency tree (torch, cudnn, whisperx, playwright — 2GB+) since only `ww.note.create_note_from_content` and `ww.github.gitmessageai` are needed.

**5. Verified:** Plugin listed as `enabled` in `hermes plugins list`. Import tested successfully.

### How `/note` works

In a Hermes CLI session:

```
/note                         # save last assistant response
/note 3                       # save 3rd response back
/note --title "My Title"      # custom title
/note --dir ~/my-notes        # custom directory
/note 2 --title "Foo" --dir ~/notes
```

Pipeline:

1. Strips reasoning tags (`...`)
2. Prompts LLM (via `ww.llm.openrouter_client`) for a 6-word title
3. Writes `~/notes/<date>-<slug>-en.md` with YAML frontmatter
4. Runs `gitmessageai` to auto commit + push

### Files involved

| File | Role |
| ------ | ------ |
| `~/.hermes/plugins/note/__init__.py` | Plugin entry point (updated) |
| `~/.hermes/plugins/note/plugin.yaml` | Plugin metadata (updated) |
| `~/.hermes/config.yaml` line 642 | Plugin enabled list |
| `~/projects/ww/ww/note/create_note_from_clipboard.py` | Note creation logic |
| `~/projects/ww/ww/note/create_note_utils.py` | Title gen, frontmatter, file ops |
| `~/projects/ww/ww/github/gitmessageai.py` | Auto git push |
| `~/projects/ww/.env` | Config (MODEL, BASE_PATH, OPENROUTER_API_KEY) |
| `~/.config/fcitx5/profile` | Fcitx5 input method config |
| `~/.config/fcitx5/conf/pinyin.conf` | Pinyin engine (shuangpin mode) |
