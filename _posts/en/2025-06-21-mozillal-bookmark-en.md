---
audio: false
generated: true
lang: en
layout: post
title: Parse Mozilla Bookmark File
translated: false
type: note
---

The file you're looking at is a **Firefox bookmark backup** in the `.jsonlz4` format. This means it's a **JSON file compressed using the LZ4 compression algorithm**, and it contains your Firefox bookmarks.

### 📁 File Name

```
bookmarks-2025-06-21_10_MU9VVxxx.jsonlz4
```

This is a standard naming pattern for Firefox bookmark backups.

---

## ✅ Goal: How to Parse It

You cannot directly read this file because it's **compressed with LZ4**. You need to:

1. **Decompress** it (LZ4 → JSON)
2. **Pretty-print** or parse the resulting JSON

---

## 🔧 Step-by-step Instructions

### Option 1: Use Python (Recommended)

Install dependencies:

```bash
pip install lz4
```

Then run this Python script:

```python
import json
import lz4.block
import sys

def decompress_jsonlz4(file_path):
    with open(file_path, 'rb') as f:
        # Read the first 8 bytes - header magic
        magic = f.read(8)
        if magic != b'mozLz40\0':
            raise ValueError("Invalid file header - not a JSON-LZ4 file")

        # Read the rest of the file and decompress
        compressed_data = f.read()
        json_bytes = lz4.block.decompress(compressed_data)
        json_str = json_bytes.decode('utf-8')
        return json.loads(json_str)

# Example usage
if __name__ == "__main__":
    import sys
    file_path = sys.argv[1]
    data = decompress_jsonlz4(file_path)
    print(json.dumps(data, indent=4))
```

Save it as `parse_bookmarks.py`, then run:

```bash
python parse_bookmarks.py 'bookmarks-2025-06-21_10_MU9VV5NmyUCq9RTxuMze5iBNh7sKyRPF_ZlV5EpMqZo=.jsonlz4'
```

> 🔍 The output will be a nicely formatted JSON tree of your bookmarks.

---

### Option 2: Use an Online Tool (Quick but Risky with Sensitive Data)

There are tools like:

- [https://arewecompressedyet.com/jsonlz4/](https://arewecompressedyet.com/jsonlz4/)
- Or search for "jsonlz4 decoder"

⚠️ **Warning:** Do not upload sensitive files to online tools unless you're sure they are safe and trustworthy.

---

### Option 3: Use Node.js

If you prefer JavaScript/Node:

```bash
npm install firefox-jsonlz4
```

Or see this repo: <https://github.com/overdodactyl/firefox-jsonlz4>

---

## 📊 What’s Inside?

Once parsed, you'll get a JSON structure like this:

```json
{
  "title": "Bookmarks Menu",
  "children": [
    {
      "title": "Mozilla Firefox",
      "children": [
        {
          "title": "Get Help",
          "uri": "https://support.mozilla.org/products/firefox/"
        },
        ...
      ]
    }
  ]
}
```

You can use this data to:

- Search through old bookmarks
- Migrate bookmarks
- Analyze your browsing/bookmarking habits

---

## ✅ Summary

| Step | Action |
|------|--------|
| 1 | Recognize that `.jsonlz4` is a **compressed JSON file** |
| 2 | Use Python or other tools to **decompress and parse** it |
| 3 | View/export the structured JSON of your Firefox bookmarks |

Let me know if you want to convert this into CSV, HTML, or extract specific URLs!

---

Great question! Let's break down **why Mozilla uses the `.jsonlz4` format** for bookmarks instead of plain JSON, and address your concern about **security**.

---

## 🔍 Why Mozilla Uses `.jsonlz4` Instead of Plain JSON

### ✅ 1. **Compression Efficiency**

- `.jsonlz4` is **JSON data compressed using the LZ4 algorithm**.
- LZ4 is **fast**, **lightweight**, and offers decent compression ratios — ideal for Firefox’s use case.
- This reduces file size significantly (often by **50–70%**), which:
  - Saves disk space
  - Speeds up backups and restores
  - Reduces I/O when reading/writing bookmark files

> 📦 Example: A 2MB plain JSON bookmark file may compress to ~600KB–800KB with LZ4.

---

### ✅ 2. **Performance**

- LZ4 is optimized for **speed over maximum compression**.
- Firefox can quickly compress and decompress these files without noticeable lag.
- Other algorithms like gzip or zstd are more powerful but slower or more complex.

---

### ✅ 3. **Internal Format**

- Firefox doesn’t expose this as a user-facing format; it's used internally for:
  - Bookmarks backups (`bookmarkbackups/`)
  - Session store (`sessionstore-backups/`)
- It's not meant for human editing or interoperability (like exporting for Chrome import).

> For export/import, Firefox provides **plain JSON** via the "Import and Backup" menu.

---

## 🔒 Is `.jsonlz4` Less Secure Than JSON?

No, **not inherently**.

Let’s clarify:

| Aspect | JSON | JSONLZ4 |
|-------|------|---------|
| **Data Format** | Readable text | Binary-compressed |
| **Security** | None built-in | None built-in |
| **Encryption?** | No | No |
| **Tamper Protection?** | No | No |

Both formats are **unencrypted** and **unprotected** by default.

So:

- If someone has access to your Firefox profile, they can read either file.
- Neither format protects sensitive data like URLs or titles.

---

## 💡 So Why Not Use Encrypted or Secure Formats?

Mozilla **does not encrypt local profile data by default**, including:

- Bookmarks
- History
- Cookies
- Passwords

### Here's Why

- **User Experience**: Encryption adds complexity.
- **Recovery**: Users could lose data if they forget passwords.
- **Trust Assumption**: Firefox assumes your system is secure.
- **Alternative Tools Exist**: You can manually encrypt your Firefox profile directory using OS-level tools (e.g., VeraCrypt, BitLocker, etc.).

If you want encrypted profiles:

- Use **Firefox Lockwise** for password encryption.
- Use **third-party tools** to encrypt the entire profile folder.
- Or switch to a portable Firefox on an encrypted USB drive.

---

## 🧠 Bonus Tip: How to Convert `.jsonlz4` → `.json`

You already know how from the previous answer, but here’s a quick recap using Python:

```bash
python parse_bookmarks.py bookmarks-*.jsonlz4 > bookmarks.json
```

Or use this one-liner if you're comfortable in shell + Python:

```bash
cat bookmarks-*.jsonlz4 | python3 -c '
import lz4.block, sys, json
data = sys.stdin.buffer.read()[8:]
print(json.dumps(json.loads(lz4.block.decompress(data)), indent=2))' > bookmarks.json
```

---

## ✅ Summary

| Question | Answer |
|--------|--------|
| **Why `.jsonlz4` instead of JSON?** | Compression, performance, internal use |
| **Is `.jsonlz4` less secure than JSON?** | No — both are unencrypted and readable |
| **Can someone steal my bookmarks?** | Yes, if they have access to your machine |
| **How to make it more secure?** | Encrypt your Firefox profile manually |

---

If you're concerned about privacy or security, the real solution is to **protect access to your computer** or **encrypt your Firefox profile folder**, not just rely on file formats.

Let me know if you'd like help writing a script to automate decryption or encrypting backups!
