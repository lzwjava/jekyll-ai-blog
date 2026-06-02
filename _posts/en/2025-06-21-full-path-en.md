---
audio: false
generated: true
lang: en
layout: post
title: Getting File's Full Path in Ubuntu
translated: false
type: note
---

In Ubuntu, you can get the full path of a file using the `realpath` or `readlink -f` command. For your example with `geckodriver`, you can run:

```bash
realpath ./geckodriver
```

or

```bash
readlink -f ./geckodriver
```

Both will output the full path, e.g.:

```
/home/lzw/bin/geckodriver
```

The `realpath` command is straightforward and commonly used for this purpose. If `realpath` is not installed, you can install it with:

```bash
sudo apt install realpath
```

Alternatively, `readlink -f` is usually available by default as part of coreutils.
