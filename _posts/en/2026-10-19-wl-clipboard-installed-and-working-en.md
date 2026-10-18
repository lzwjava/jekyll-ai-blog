---
audio: false
generated: true
image: false
lang: en
layout: post
title: wl-clipboard installed and working
translated: false
type: note
---

`wl-clipboard` is now installed and working:

```bash
wl-copy --version
# wl-clipboard 2.2.1
```

You can now use clipboard commands in Wayland:

- **Copy text to clipboard:**
  ```bash
  echo "hello" | wl-copy
  ```

- **Copy file contents:**
  ```bash
  cat file.txt | wl-copy
  ```

- **Paste from clipboard:**
  ```bash
  wl-paste
  ```

- **Copy image:**
  ```bash
  wl-copy < image.png
  ```

Everything is ready. Do you need any code in this directory updated to use `wl-copy`/`wl-paste`?