---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multi-Step HEIC to Markdown Workflow
translated: false
type: note
---

Great question. You're essentially asking: how do I encode a repeatable multi-step CLI workflow (HEIC→JPG, compress, strip EXIF, inject into markdown) into a reusable skill that an agent like Hermes can invoke reliably?

Here's the architecture I'd use:

---

## The Skill Pattern for Image Processing + Markdown Injection

A "skill" in your agent context is really three things:

1. **A SKILL.md** — declarative spec the agent reads to understand what tools/steps to use
2. **A shell script or Python script** — the actual executable logic
3. **A prompt template** — how the agent calls it with parameters

---

### Step 1: Write the executable script

```bash
# ~/scripts/add_images_to_post.sh
#!/usr/bin/env bash
set -euo pipefail

# Usage: add_images_to_post.sh <heic_dir> <post_md> <section_name>
HEIC_DIR="$1"
POST_MD="$2"
SECTION="$3"
OUT_DIR="$(dirname "$POST_MD")/images/$(basename "$POST_MD" .md)"

mkdir -p "$OUT_DIR"

for heic in "$HEIC_DIR"/*.HEIC "$HEIC_DIR"/*.heic; do
  [ -f "$heic" ] || continue
  base=$(basename "$heic" | sed 's/\.[Hh][Ee][Ii][Cc]//')
  jpg="$OUT_DIR/${base}.jpg"

  # Convert HEIC → JPG
  magick "$heic" "$jpg"

  # Strip location/EXIF metadata
  exiftool -all= -overwrite_original "$jpg"

  # Compress to ~500KB (iterative quality reduction)
  quality=85
  while [ $(stat -f%z "$jpg") -gt 512000 ] && [ $quality -gt 20 ]; do
    magick "$jpg" -quality $quality "$jpg"
    quality=$((quality - 10))
  done

  echo "Processed: $jpg ($(du -sh "$jpg" | cut -f1))"
done

# Build markdown image block for section
IMG_BLOCK=""
for jpg in "$OUT_DIR"/*.jpg; do
  rel_path="${jpg#$(dirname "$POST_MD")/}"
  IMG_BLOCK+="![](${rel_path})\n\n"
done

# Inject after ## $SECTION header
python3 - <<PYEOF
import re, sys

md = open("$POST_MD").read()
section_pattern = rf"(## $SECTION\n)"
replacement = r"\1\n$IMG_BLOCK\n"
new_md = re.sub(section_pattern, replacement, md, count=1)

if new_md == md:
    # Section doesn't exist — append it
    new_md += f"\n## $SECTION\n\n$IMG_BLOCK\n"

open("$POST_MD", "w").write(new_md)
print("Injected images into $POST_MD under ## $SECTION")
PYEOF
```

Dependencies: `imagemagick`, `exiftool` (both `brew install imagemagick exiftool`).

---

### Step 2: Write the SKILL.md

```markdown
# skill: add-images-to-post

## Purpose
Convert HEIC photos → JPG, compress to ~500KB, strip EXIF/location,
and inject them into a markdown post under a named section.

## When to use
User says: "add images to post", "insert photos", "convert HEIC to jpg for blog",
or provides a directory of images and a .md file path.

## Parameters
- heic_dir: directory containing .HEIC files (e.g. ~/Downloads/c1)
- post_md: absolute path to the markdown file
- section: section heading name to inject under (e.g. "Porridge")

## Steps
1. Run: ~/scripts/add_images_to_post.sh <heic_dir> <post_md> <section>
2. Verify output with: ls -lh <out_dir>/*.jpg
3. Show the injected markdown block to the user for confirmation
4. Optionally open the markdown file for review

## Tools required
- imagemagick (brew install imagemagick)
- exiftool (brew install exiftool)

## Output
- Converted JPGs in <post_dir>/images/<post_name>/
- Markdown file updated with image references under ## <section>
```

Save this to `/mnt/skills/user/add-images-to-post/SKILL.md` (or wherever your agent loads skills from — check your Hermes config).

---

### Step 3: How your agent invokes it

The key insight is that your agent (Hermes) reads SKILL.md at the start of relevant tasks. The trigger is matching the user's intent to the skill description. So in your `available_skills` config, register it:

```yaml
skills:
  - name: add-images-to-post
    description: |
      Convert HEIC photos to JPG, compress, strip EXIF, inject into markdown post.
      Trigger when user mentions adding images to a blog post or converting HEIC files.
    location: ~/skills/add-images-to-post/SKILL.md
```

Then Hermes will:

1. Read the SKILL.md
2. Extract parameters from your natural language request
3. Call the shell script with the right args
4. Report back

---

### The compounding pattern

Once you have 5–10 skills like this, you get:

```
User intent → agent reads skill → runs script → done
```

With zero ambiguity. The skill file is the spec. The script is the implementation. This is exactly how Claude Code's internal tools work — the model reads tool descriptions and maps intent to invocation.

For your use case specifically, I'd also add a `--dry-run` flag to the script that shows what it *would* do without modifying files — agents love having a safe preview step before committing writes.
