---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Line Ending Control Guide
translated: false
type: note
---

`git config core.autocrlf` controls how Git handles line endings when you check files out of the repository and when you commit them back in. It matters because Windows uses **CRLF** (`\r\n`) for line endings, while Linux and macOS use **LF** (`\n`). Without handling, files may flip between formats depending on who edits them, leading to “dirty” diffs and unnecessary changes.

---

### How it Works

* **When checking out (reading)** a file, Git may convert line endings to match your OS convention (so they look natural in your editor).
* **When committing (writing)** a file, Git may convert line endings back to LF (the cross-platform standard in repos).

---

### Settings

You set it with:

```bash
git config --global core.autocrlf <value>
```

The common values:

* `true`
  Convert **LF → CRLF** on checkout, and **CRLF → LF** on commit.
  Best for **Windows developers** editing code in Windows editors.

* `input`
  Do **not** modify files on checkout, but convert **CRLF → LF** on commit.
  Best for **Linux/macOS developers** to ensure LF-only repos.

* `false`
  No conversion at all. Git stores and checks out files exactly as-is.
  Best if your team/editor consistently handles line endings.

---

### Typical Recommendations

* **Windows**:

  ```bash
  git config --global core.autocrlf true
  ```

* **Linux/macOS**:

  ```bash
  git config --global core.autocrlf input
  ```

For mixed teams, it’s also good to add a `.gitattributes` file in the repo to enforce consistent line endings, e.g.:

```
* text=auto
```

---

Do you want me to also show you a recommended **`.gitattributes` setup** that works well for cross-platform teams (so you don’t rely only on `core.autocrlf`)?
