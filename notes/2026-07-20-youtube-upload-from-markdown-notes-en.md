---
audio: false
generated: true
image: false
lang: en
layout: post
title: YouTube Upload from Markdown Notes
translated: false
type: note
---

Here's what was built and wired up:

**Created: `ww/gen_video/youtube_upload.py`**

- YouTube upload module that reads a markdown note's YAML frontmatter for title/description/tags
- Uploads the MP4 to YouTube via the YouTube Data API v3 with resumable upload
- Supports `--public`, `--unlisted`, `--credential`, `--description`, `--tags` options
- OAuth 2.0 flow: opens browser for auth, caches token at `~/.google/youtube_token.json`
- Requires `client_secret.json` at `~/.google/client_secret.json` (setup instructions in error message)

**Modified: `ww/main.py`**

- gen-video dispatch now checks for `upload` subcommand before falling through to the existing video generation
- `ww gen-video <file>` still works exactly as before
- `ww gen-video upload <note_path> <mp4_path>` routes to the new upload module
- Help text updated to show both commands

**Modified: `~/.zsh/completions/_ww`**

- Added `gen_video_cmds` array with `upload` entry
- Added case entry for `gen-video` in the subcmd dispatch
- Added `gen-video upload` completion with file suggestions for `*.md` (note) and `*.mp4` (video)

**Installed dependencies:**

- `google-api-python-client`, `google-auth-oauthlib` via `uv add`

**Verified:**

- `ww gen-video upload --help` — shows proper usage
- `ww gen-video --help` — old behavior preserved
- `ww gen-video upload some_note.md` — error: missing mp4_path
- `ww gen-video upload /path/to/note.md /nonexistent/video.mp4` — error: video not found
- Main help (`ww`) shows both gen-video entries

To actually upload, you'll need to:

1. Create a Google Cloud project → enable YouTube Data API v3 → create OAuth 2.0 Desktop credentials
2. Save the JSON as `~/.google/client_secret.json`
3. Run `ww gen-video upload notes/your-post.md output.mp4`
