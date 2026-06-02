---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix MeCab Config File Path
translated: false
type: note
---

Your error

```
RuntimeError: param.cpp(70) [ifs] no such file or directory: /usr/local/etc/mecabrc
```

means **MeCab can't find its configuration file** (`mecabrc`).
On macOS, if you installed MeCab via Homebrew recently, it’s likely installed under `/opt/homebrew/` instead of `/usr/local/`, but the Python binding is still looking for the old `/usr/local/etc/mecabrc` path.

Here’s how you can fix it:

---

### 1. Find where `mecabrc` actually is

Run:

```bash
brew list mecab
```

or:

```bash
find /opt/homebrew -name mecabrc
```

You’ll probably see something like:

```
/opt/homebrew/etc/mecabrc
```

---

### 2. Point MeCab to the correct mecabrc

You can specify the path in your Python code:

```python
import MeCab

t = MeCab.Tagger(f"-r /opt/homebrew/etc/mecabrc -d /opt/homebrew/lib/mecab/dic/ipadic")
print(t.parse("すもももももももものうち"))
```

---

### 3. Or set an environment variable

```bash
export MECABRC=/opt/homebrew/etc/mecabrc
```

Then run your script normally:

```bash
python try_mecab.py
```

---

### 4. If you want to make `/usr/local/etc/mecabrc` work

You can also symlink it:

```bash
sudo mkdir -p /usr/local/etc
sudo ln -s /opt/homebrew/etc/mecabrc /usr/local/etc/mecabrc
```

But the environment variable approach is cleaner.

---

If you want, I can also give you a **Homebrew reinstall + ipadic setup** command so it works without specifying `-r` every time. That way your `try_mecab.py` stays clean.
