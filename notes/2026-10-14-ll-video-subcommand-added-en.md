---
audio: false
generated: true
image: false
lang: en
layout: post
title: ll video subcommand added
translated: false
type: note
---

Everything is committed and pushed — `main` is now in sync with `origin/main`.

## Summary: `ll video` added

**New files:**
- `src/video_ops.rs` (~1450 lines) — 18 commands + 21 unit tests
- `src/cli.rs` — shared flag/positional parsing, now used by both `image` and `video` modules

**Modified:** `src/main.rs` (dispatch), `src/image_ops.rs` (uses shared CLI helpers), `README.md` (Video tools section)

### Commands

| Group | Commands |
|---|---|
| Inspect | `info <file>…` (streams, codecs, fps, `--json`) |
| Cut & join | `screenshot`, `frames` (`--fps`/`--every` sequences), `trim` (stream copy / `--reencode`), `concat`, `reverse` |
| Audio | `audio` (mp3/m4a/wav/flac/opus by extension), `mute`, `volume` (`-v 0.5` / `-v -6dB`) |
| Transform | `resize`, `crop`, `rotate`, `flip`, `speed` (audio follows via chained `atempo`) |
| Export | `convert` (h264/hevc/vp9/av1/copy + `--crf`/`--preset`/`--fps`), `gif` (palette-optimised), `gif2video`, `sprite` (contact sheet) |

### Design notes

- **ffmpeg/ffprobe-driven** — transcoding in pure Rust isn't realistic; the module shells out but every command **echoes the exact ffmpeg line** it runs, and `--dry-run` prints without executing. Missing binaries produce a friendly install hint.
- **Pure builder functions** — `build_trim`, `build_screenshot`, `atempo_chain`, `parse_crop_geometry`, etc. are decoupled from I/O, so the arg construction is unit-tested without touching ffmpeg.
- **Convenience**: times accept `90` / `1:30` / `01:02:03.5`, output dirs auto-created, container codecs picked by extension, negative numbers parse as values.

**Verification:** `cargo build` clean, **38/38 tests pass**, clippy-clean for all new code, plus full end-to-end runs against real generated videos (durations/dimensions verified with `ffprobe`), and an image↔video regression check.

Commits pushed:
```
3c79248 feat: add video subcommand with common operations (ffmpeg-backed)
```