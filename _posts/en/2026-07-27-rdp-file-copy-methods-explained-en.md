---
audio: false
generated: true
image: false
lang: en
layout: post
title: RDP File Copy Methods Explained
translated: false
type: note
---

Yes, absolutely! Windows Remote Desktop (RDP) has built-in support for copying files between the remote server and your local machine. Here are the main ways to do it:

## 1. **Enable Drive Redirection** (most common)

Before connecting, configure the RDP client to share your local drives:

1. Open **Remote Desktop Connection** (`mstsc`)
2. Click **Show Options** → **Local Resources** tab
3. Under **Local devices and resources**, click **More**
4. Expand **Drives** and check the drives you want to make available on the remote server (e.g., `Local Disk (C:)`)
5. Connect to the server

Once connected, your local drives will appear in **File Explorer** on the remote server under:

```
This PC > Redirected drives and folders
```

From there, you can copy/paste files just like normal drag-and-drop between the server and your local machine.

## 2. **Copy & Paste (Clipboard)**

RDP also shares the clipboard by default. You can:

- **Copy** a file on the remote server (`Ctrl+C`)
- **Paste** it on your local machine (`Ctrl+V`)

This works for most file types and sizes, though very large files may be slow.

## 3. **mstsc /admin with drive redirection via command line**

You can also set up drive redirection programmatically using the RDP file format (`.rdp`):

```
drive redirect i:drives=C:\
```

## 4. **Alternative: Robocopy or xcopy over mapped drives**

Once drives are redirected, you can use command-line tools like:

```cmd
robocopy \\tsclient\C\path\to\file C:\local\destination file.txt
```

## Notes

- ✅ Works on Windows 10/11 Pro, Enterprise, Server editions
- ✅ The **Remote Desktop Session Host** must allow drive redirection (usually enabled by default on Windows Server)
- ⚠️ Some **corporate/IT-managed servers** may have drive redirection and clipboard disabled via Group Policy for security reasons

If your server **doesn't** allow drive redirection, you'd need alternative methods like:

- `scp` / `rsync` (if SSH is available)
- Shared network folders
- Cloud storage (OneDrive, Dropbox, etc.)
