---
audio: false
generated: true
image: false
lang: en
layout: post
title: Embed Videos in GitHub README
translated: false
type: note
---

**Question:** How do I properly display/embed a video in a GitHub README?

**Answer:**

The key problem with your current approach is that **GitHub does NOT render `<video>` tags pointing to `raw.githubusercontent.com`** in README files. It simply shows a broken player or nothing. GitHub only renders videos that are hosted on its own asset CDN (`github.com/user-attachments/assets/...`).

Here are the working methods, from most recommended to least:

---

## ✅ Method 1: Drag & Drop Upload (Best & Easiest)

This is the officially supported way. Open your README for editing on GitHub's web editor, then drag and drop your `tot.mp4` file directly into the editor. GitHub will automatically upload it and generate a URL like `https://github.com/lzwjava/Tree_Of_Thought/assets/{id}/....mp4`.

Using a URL in the format `https://github.com/user-attachments/assets/${UUID}` works, but `https://github.com/${user}/${repo}/raw/main/some/path/demo.mp4` does NOT work for video embedding.

**Steps:**

1. Go to your repo on GitHub → click the pencil ✏️ to edit `README.md`
2. Drag `tot.mp4` from your local machine into the text editor area
3. Wait for the upload — GitHub will insert a line like:

```markdown
https://github.com/lzwjava/Tree_Of_Thought/assets/XXXXX/XXXXXXXX.mp4
```

4. Wrap it in a `<video>` tag or use it directly:

```html
<video src="https://github.com/lzwjava/Tree_Of_Thought/assets/XXXXX/XXXXXXXX.mp4" controls width="100%"></video>
```

5. Commit and save — the video player will render in your README.

> **Note:** File size limit is 10 MB for free GitHub plans and 100 MB for paid plans.

---

## ✅ Method 2: Clickable Thumbnail (Fallback — No Size Limit)

If your video is too large, use a thumbnail image that links to the video file:

```markdown
[![Watch the video](https://raw.githubusercontent.com/lzwjava/Tree_Of_Thought/main/thumbnail.png)](https://raw.githubusercontent.com/lzwjava/Tree_Of_Thought/main/tot.mp4)
```

This uses Markdown to create an image link — clicking the thumbnail opens the raw video file. You need a thumbnail image (e.g., `thumbnail.jpg`) committed to the repository.

---

## ❌ Why Your Current Approach Doesn't Work

```html
<video src="https://raw.githubusercontent.com/lzwjava/Tree_Of_Thought/main/tot.mp4" controls width="100%"></video>
```

GitHub's markdown rendering does not support embedding videos directly with the `<video>` tag pointing to raw repository file paths — this is a known GitHub limitation.

---

## Summary Table

| Method | Works in README? | Size Limit |
|---|---|---|
| Drag & drop upload (GitHub CDN URL) | ✅ Yes | 10–100 MB |
| `raw.githubusercontent.com` `<video>` tag | ❌ No | — |
| Clickable thumbnail → raw link | ✅ Yes (no autoplay) | No limit |
| YouTube embed thumbnail | ✅ Yes | No limit |

**Recommended action:** Use Method 1 — drag and drop `tot.mp4` into the GitHub web editor to get a proper CDN link.

**References:**

- [bobbyhadz.com - How to embed a Video into GitHub README.md](https://bobbyhadz.com/blog/embed-video-into-github-readme-markdown)
- [GitHub Community Discussion - Readme.md videos not working](https://github.com/orgs/community/discussions/19403)
- [amonxu.com - How to embed a video into GitHub README](https://amonxu.com/2024/05/23/en/2024-05-23-How-to-embed-a-video-into-GitHub-README/)
- [GeeksforGeeks - How to Embed a Video Into GitHub README.md](https://www.geeksforgeeks.org/git/how-to-embed-a-video-into-github-readme-md/)
