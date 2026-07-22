---
audio: false
generated: true
image: false
lang: en
layout: post
title: Aligned Pi note extension with ww
translated: false
type: note
---

All sorted. Here's what was done:

## Fix Summary

**Problem**: The Pi agent's `/note` extension wrote to `~/.config/pi/note_queue.json` instead of `~/.config/ww/note_queue.json`, and used a different JSON format than what the ww note watcher (`ww note watch`) expects.

### Changes made to `/home/lzw/.pi/agent/extensions/note/index.ts`:

1. **Path**: `~/.config/pi/note_queue.json` → `~/.config/ww/note_queue.json`
2. **Queue format**: Changed from `{entries: [...]}` wrapper to a **plain JSON array** (matching `ww/note/note_queue.py`)
3. **Entry fields**: Now writes entries in the ww-compatible format:
   - `content` (was `text`)
   - `content_hash` — SHA-256 first 12 chars (was a random shortId)
   - `queued_at` — ISO timestamp with seconds precision (was `timestamp`)
   - `status: "pending"` — so the watcher picks it up
   - `type: "note"`, `note_path: null`
   - `id` — now uses content hash (same as ww) instead of random
4. **Dedup**: Added duplicate content check (same hash + pending status) matching ww's behavior
5. **Error handling**: Surfaces errors (like duplicates) to the user

### Migration

Migrated **9 unique entries** from the old pi queue to the correct ww queue (2 duplicates were deduplicated). All entries are `status: "pending"` and ready for the `ww note watch` daemon to process.