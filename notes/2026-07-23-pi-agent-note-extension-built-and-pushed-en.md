---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pi Agent Note Extension Built and Pushed
translated: false
type: note
---

Here's a full summary of what we did:

---

## 1. Explored the project (`/mnt/data/zz`)
A machine learning data pipeline for downloading, extracting, tokenizing, and analyzing large datasets (FineWeb, Wikimedia, etc.) for model training.

## 2. Studied the Pi Agent extension API
You shared your Hermes `note` plugin (Python), and I read the Pi Agent docs on extensions, session format, and examples (`bookmark.ts`, `summarize.ts`).

## 3. Built a Pi Agent note extension
Wrote `~/.pi/agent/extensions/note/index.ts` — a TypeScript `/note` command that:
- Captures assistant responses from the session
- Strips reasoning tags
- Appends to `~/.config/pi/note_queue.json`
- Supports `N` (response number) and `--title` arguments

## 4. Backed up to `~/projects/config/`
Copied both the extension and `settings.json` to `~/projects/config/pi/agent/` for use on another machine.

## 5. Committed & pushed
```
cd ~/projects/config
git add pi/agent/
git commit -m "add pi agent note extension and settings"
git pull --rebase
git push
```
Pushed to `github.com:lzwjava/config.git` successfully.