---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Hunting for the Bad Byte
translated: false
type: note
---

### Why This Didn't Find the Bad Byte
The `hexdump` output you got matched **the file offset** (`000008d0`), not a `\x8D` byte in the actual content. Grep is text-searching the entire line, and "8d" appears in the hex address (e.g., `08d0`), so it pulled that irrelevant line. The data bytes there (`6f 67 20 ...`) are just normal ASCII for `"og = og_images[i"`, no issues.

### Better Ways to Hunt the `\x8D`
Try these commands in your project directory (next to `_layouts/default.html`). They'll scan the file's bytes directly.

1. **Improved Hexdump (Grep for Byte in Data)**:
   This greps for ` 8d ` (spaces around to match hex bytes, not offsets):
   ```
   hexdump -C _layouts/default.html | grep ' 8d '
   ```
   - If it finds something, you'll see the offset (left column) and surrounding bytes. Note the offset, then jump to that position in your editor (e.g., VS Code: Ctrl+G > byte offset / 16 for line approx.).
   - Example output if hit: `00001234  ...  8d  20  61  62  ... |... ab...|`

2. **Use `xxd` (Often Better Than Hexdump)**:
   macOS has `xxd` built-in:
   ```
   xxd _layouts/default.html | grep 8d
   ```
   - Similar: Matches "8d" in hex bytes. If no output, the byte isn't there (rare, but possible if it's in another file).

3. **Binary Grep (Direct Byte Search)**:
   ```
   grep -a -o -P '\x8d' _layouts/default.html | hexdump -C
   ```
   - This extracts exact matches to the byte and dumps them in hex. If empty, no `\x8D`.

4. **Ruby One-Liner (Precise Position)**:
   As I suggested before—run this to get byte index:
   ```
   ruby -e "File.open('_layouts/default.html', 'rb') { |f| f.read.each_byte.with_index { |b, i| puts \"Found at byte #{i}: #{b.chr(Encoding::ASCII_8BIT).inspect}\" if b == 0x8D } }"
   ```
   - Outputs like: `Found at byte 1234: "\x8D"`. Then edit: Open file, go to char ~1234 (or line = 1234/80-ish), and delete the invisible char (it might look like nothing; select/delete around it).

### If No Matches?
- The `\x8D` might be in a **different file** (e.g., a post in `_posts/` rendered via `{{ content }}` in the layout). Scan the whole site:
  ```
  find . -name "*.md" -o -name "*.html" | xargs grep -l $'\x8D'
  ```
  (Or use the Ruby script on each suspect.)
- Or it's a BOM/invisible at file start: Open in editor, delete first line if empty, re-save UTF-8.

Once you zap it, run `bundle exec jekyll serve --incremental` again. If still stuck, paste the output from one of these commands (or the Ruby one), and we'll nail it.

[Hexdump Tips for Byte Hunting](https://unix.stackexchange.com/questions/38331/finding-bad-characters-in-hex-dump)
