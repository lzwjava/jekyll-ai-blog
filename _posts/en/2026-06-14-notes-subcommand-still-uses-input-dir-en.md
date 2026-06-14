---
audio: false
generated: true
image: false
lang: en
layout: post
title: Notes subcommand still uses --input-dir
translated: false
type: note
---

Here's the analysis:

=== Conversation Subcommands: --input-dir vs positional file ===

The commit 7f3f368 changed `ww conversation generate` from `--input-dir` (batch all JSONs in a dir) to a positional `file` arg (single file). Here's the status of all 5 subcommands:

1. json     (json.py)     - positional `filename` arg  ✅ No --input-dir
2. generate (generate.py) - positional `file` arg      ✅ Fixed in 7f3f368
3. notes    (notes.py)    - still uses `--input-dir`    ⚠️  See below
4. to-video (video.py)    - positional file (sys.argv)  ✅ No --input-dir
5. to-image (image.py)    - positional file (sys.argv)  ✅ No --input-dir

=== Only `notes` still uses --input-dir ===

notes.py line 78-82:
    parser.add_argument("--input-dir", default="scripts/conversation", ...)

But this is arguably intentional — `notes` iterates ALL .json files in a directory
and converts each to a markdown note. It's a batch-by-design command.

However, if you want consistency with `generate` (single file arg), it could be
refactored to accept a single file OR a directory. The `generate` command before
7f3f368 also had the "process all files in dir" batch mode, and you removed it.

=== video.py has a local var named `input_dir` but it's NOT a CLI flag ===

video.py line 139: `input_dir = os.path.dirname(input_path) or "."`
This is just extracting the parent directory from the positional file arg.
No `--input-dir` flag exists. ✅ Clean.

=== Summary ===

Only `ww conversation notes` has the `--input-dir` pattern. All others use
positional file args. Want me to refactor `notes` to match — accept either
a single file or a directory as a positional arg?
