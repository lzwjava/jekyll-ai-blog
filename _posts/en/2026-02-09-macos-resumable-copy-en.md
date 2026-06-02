---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: MacOS Resumable File Copy Explained
translated: false
type: note
---

**Question: How does macOS resumable file copy work, and how does macOS provide this functionality?**

**Answer:**

macOS provides resumable copy functionality in **Finder** starting with **macOS Monterey** (2021) and continuing in later versions like Ventura, Sonoma, and Sequoia. This feature lets you pause or cancel a file/folder copy operation and resume it later from where it stopped, instead of restarting from scratch.

### How to use resumable copy in Finder
1. Start copying large files or folders (Command+C → Command+V or drag-and-drop).
2. While the copy is in progress, click the **X** button in the copy progress window (or press Esc) to cancel/pause it.
3. Finder keeps a **ghosted** (semi-transparent) version of the file/folder at the destination.
4. When you later click this ghosted item, Finder shows two options:
   - **Finish Copying** — continues the copy from where it left off.
   - **Keep Resumable Copy** — leaves the partial/ghosted item for later resumption (useful if you want to finish it another time or after reconnecting an external/network drive).

This works best for local drives, external drives, and sometimes network shares (though network interruptions can be less reliable).

### How it actually works under the hood
Finder does **not** use a simple byte-range copy like HTTP resumable downloads (e.g., Range: bytes=500000- in URLSession). Instead, it relies on these mechanisms:

- The partial files/folders remain on the destination disk exactly as they were when the copy stopped.
- Finder marks the incomplete item with special metadata (an extended attribute like `com.apple.metadata:kMDItemResumableCopy` or similar internal flag).
- When you choose **Finish Copying**, Finder intelligently compares source and destination:
  - Skips already-completed files.
  - Continues copying only missing or incomplete files.
  - For large files that were partially copied, it typically resumes appending data (though this depends on file system and copy engine behavior).
- The ghosted appearance and resume dialog are handled by Finder's internal copy engine (part of the Finder process and macOS file coordination APIs).

Before Monterey, Finder did not support true resuming — interrupting a copy usually meant starting over or manually cleaning up partial files. The resumable feature was a user-requested improvement for large transfers (e.g., terabyte-sized backups to external drives).

### Limitations and notes
- It is not as robust as dedicated tools like `rsync --partial --progress` or third-party apps (Carbon Copy Cloner, SuperDuper), which offer better verification, retry logic, and resume capabilities.
- Network copies (SMB/AFP) can sometimes fail to resume cleanly if the connection drops permanently.
- If the resumable copy becomes stuck (greyed-out and inaccessible), common workarounds include creating an alias to access contents or using Terminal commands to remove the metadata flag (e.g., `xattr -d com.apple.metadata:kMDItemResumableCopy` + resetting creation date).
- For very large or critical transfers, many users still prefer command-line `rsync` or paid tools over Finder's built-in resume.

In summary, macOS Finder's resumable copy is a convenient, built-in convenience feature introduced in Monterey that tracks partial transfers via filesystem metadata and smart comparison logic, allowing you to "keep finishing" interrupted copies without losing already-transferred data.

**References:**

- [https://www.macrumors.com/how-to/pause-copying-file-resume-it-later-monterey/](https://www.macrumors.com/how-to/pause-copying-file-resume-it-later-monterey/)
- [https://apple.stackexchange.com/questions/434544/how-to-remove-the-resumable-copy-flag-of-a-folder](https://apple.stackexchange.com/questions/434544/how-to-remove-the-resumable-copy-flag-of-a-folder)
- [https://discussions.apple.com/thread/253615565](https://discussions.apple.com/thread/253615565)
- [https://developer.apple.com/videos/play/wwdc2023/10006](https://developer.apple.com/videos/play/wwdc2023/10006) (related URLSession resumable transfers, for contrast)
