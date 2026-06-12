---
audio: false
generated: true
image: false
lang: en
layout: post
title: ww conversation command reference
translated: false
type: note
---

```
ww conversation --help
```

```
Usage: ww conversation <command> [options]

Commands:
  json <name>       Capture conversation JSON from stdin/clipboard
  generate          Generate audio from conversation JSON (Google Cloud TTS)
  notes             Convert conversation JSON files to markdown notes

Options:
  --output-dir DIR  Output directory for audio/JSON files
  --input-dir DIR   Input directory for conversation JSON files
  --type en|cn      Language type for voices (default: en)
  --dry-run         Skip audio generation
  --file FILE       Process a specific JSON file
  --seed N          Random seed for voice selection
```

Typical usage:

```
# Generate audio from a single conversation (English, default)
ww conversation generate --file computer-networks-plus.json \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation

# Generate Chinese voice audio
ww conversation generate --file my-topic.json \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation \
  --type cn

# Dry run — validate without hitting TTS API
ww conversation generate --file my-topic.json \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation \
  --dry-run

# Generate all conversations in a directory
ww conversation generate \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation

# Custom output directory
ww conversation generate --file my-topic.json \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation \
  --output-dir ~/Desktop/audio

# Capture a new conversation JSON interactively
ww conversation json my-new-topic

# Convert conversation JSONs to markdown notes
ww conversation notes \
  --input-dir ~/projects/jekyll-ai-blog/scripts/conversation
```

Defaults:
- `--input-dir` → `scripts/conversation` (relative to cwd)
- `--output-dir` → `~/projects/blog-assets/conversations`
