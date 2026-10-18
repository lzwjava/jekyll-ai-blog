---
audio: false
generated: true
image: false
lang: zh
layout: post
title: wl-clipboard 已安装并正常运行
translated: true
type: note
---

`wl-clipboard` 现已安装并正常工作：

```bash
wl-copy --version
# wl-clipboard 2.2.1
```

你现在可以在 Wayland 中使用 clipboard 命令：

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

一切都已就绪。你是否需要更新此目录中的代码以使用 `wl-copy`/`wl-paste`？
