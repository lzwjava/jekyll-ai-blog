---
audio: false
generated: true
image: false
lang: en
layout: post
title: Private note flag added
translated: false
type: note
---

Done. Here's what was changed in `~/.pi/agent/extensions/note/index.ts`:

| Change | Detail |
| -------- | -------- |
| **`WwQueueEntry` interface** | Added `private?: boolean` field |
| **`enqueue()` function** | Added `isPrivate` parameter, sets `entry.private = true` when passed |
| **`handleNote()` function** | Parses `--private` token, passes `isPrivate` to `enqueue()` |
| **Output message** | Shows `(private)` label when flag is used |
| **Doc comment** | Added `--private` usage examples |

Now `/note --private` from the pi agent enqueues a note with `"private": true` in the queue, and the `ww note process` handler saves it to `/Users/lzwjava/projects/jekyll-ai-blog/private-note` without git push.
