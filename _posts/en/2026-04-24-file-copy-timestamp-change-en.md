---
audio: false
generated: true
image: false
lang: en
layout: post
title: Timestamps Change on File Copy
translated: false
type: note
---

**Question:**
When copying a file to another file, if the content is the same, will `mtime` stay unchanged while `ctime` changes?

---

**Answer:**

Short answer: **No — both `mtime` and `ctime` usually change when you use `cp`.**

Let’s break it down carefully.

---

## 1. What `cp` actually does

When you run:

```bash
cp source.txt dest.txt
```

`cp` does **not compare content**. It simply:

* Opens/creates `dest.txt`
* Writes data into it (even if identical)
* Updates metadata

---

## 2. What happens to timestamps

### Case A: Destination file is overwritten

Even if the content is identical:

* **`mtime` (modification time)** → ✅ **changes**
  Because the file is rewritten

* **`ctime` (change time)** → ✅ **changes**
  Because metadata (write operation) changed

👉 So your assumption is incorrect:

> ❌ `mtime` does NOT stay the same
> ✅ It will update

---

### Case B: Destination file does NOT exist

A new file is created:

* `mtime` → time of creation (write)
* `ctime` → time of creation

---

### Case C: Using `cp -p` (preserve timestamps)

```bash
cp -p source.txt dest.txt
```

Now behavior changes:

* **`mtime`** → ✅ preserved (same as source)
* **`ctime`** → ❗ still changes

Why?

* `ctime` is controlled by the filesystem
* It updates whenever metadata changes (including setting timestamps)

👉 Important rule:

> You **cannot manually preserve `ctime`**

---

## 3. Key Insight

Even if file content is identical:

* `cp` does not check equality
* Writing = modification → updates `mtime`
* Any metadata change → updates `ctime`

---

## 4. When would `mtime` NOT change?

Only if:

* You **don’t rewrite the file at all**

Example tools that avoid rewriting:

```bash
rsync --ignore-existing
rsync --size-only
rsync --checksum
```

These can skip copying if files are identical.

---

## 5. Summary

| Scenario         | mtime       | ctime       |
| ---------------- | ----------- | ----------- |
| `cp` overwrite   | ✅ changes   | ✅ changes   |
| `cp` new file    | ✅ new time  | ✅ new time  |
| `cp -p`          | ❌ preserved | ✅ changes   |
| No write happens | ❌ unchanged | ❌ unchanged |

---

## 6. Practical Tip

If you want to **avoid unnecessary timestamp changes**, use:

```bash
rsync -a --ignore-existing
```

or

```bash
rsync -a --checksum
```

---

If you want, I can explain why `ctime` is fundamentally unmodifiable at the filesystem level (this is a subtle but important Unix design decision).
