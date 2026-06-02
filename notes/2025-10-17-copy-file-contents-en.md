---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Copy File Contents in Vi
translated: false
type: note
---

## Copying (or Moving) All Content from One File to a New File in Vi

Based on your vi usage, I'll assume you want to select and copy/delete the entire contents of a file, then paste it into a new file. Vi doesn't have a direct "select all" like GUI editors, but you can achieve this efficiently in **command mode** (press `Esc` to ensure you're there). I'll cover both **copy** (leaving original intact) and **cut/delete** (moving content).

### Step-by-Step: Copy All Content to a New File

1. Open your source file:

   ```
   vi oldfile.txt
   ```

2. Yank (copy) the entire file:
   - Type `gg` (go to top of file).
   - Then type `yG` (yank from current position to end of file).
   *Alternative (Vim-specific, works in Red Hat's vim):* Type `:1,$y` and press `Enter` (yanks lines 1 to end).

3. Open the new file:
   - Type `:e newfile.txt` and press `Enter` (creates/opens the new file).

4. Paste the content:
   - Type `p` (pastes after cursor; since it's empty, it pastes at the top).
   *Alternative:* Type `P` to paste before cursor.

5. Save and exit the new file:
   - Type `:wq` and press `Enter`.

The original file remains unchanged.

### Step-by-Step: Delete All Content and Paste into a New File (Move)

This deletes the original content after copying it.

1. Open your source file:

   ```
   vi oldfile.txt
   ```

2. Yank (copy) the entire file first:
   - `gg` then `yG` (or `:1,$y`).

3. Delete all content:
   - Type `gg` (to top).
   - Then `dG` (deletes from current position to end).
   *Alternative:* Type `:%d` and press `Enter` (deletes all lines).
   Save if needed: `:w` (overwrites the now-empty file).

4. Open the new file:
   - Type `:e newfile.txt` and press `Enter`.

5. Paste:
   - Type `p`.

6. Save and exit:
   - `:wq`.

### Quick Tips

- If you accidentally delete without yanking first, use `u` to undo.
- To do this across files without opening a new one each time: Yank in first file, then use `vi newfile.txt`, paste, and save.
- For large files, these commands are fast since vi handles buffers efficiently.

Practice on test files to get the hang of it!

[How to Copy Text to Another File in Vim](https://stackoverflow.com/questions/1239801/how-to-copy-to-the-end-of-the-line-in-vim)
[Vim: Yank (copy) entire file](https://vim.fandom.com/wiki/Yank_%28copy%29_the_entire_file)
