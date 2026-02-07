---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: Gemini 链接复制错误
translated: true
type: note
---

Question: Is it true that when using Gemini, if there is a link or YouTube preview in the response, the copy function in the frontend has issues?

Answer: **Yes, there have been recurring reports of this issue.** Users frequently encounter bugs where the "Copy" button in the Gemini web interface fails to work properly or results in a blank clipboard when the response contains specific interactive elements like **YouTube previews**, **embedded links**, or **Markdown formatting**。

### Why this happens

The issue is typically a **client-side JavaScript bug** in the Gemini frontend。When a response contains a YouTube preview or a rich-text link，the "Copy" script sometimes fails to parse the underlying HTML or Markdown correctly。

* **Clipboard API Conflicts:** Modern browsers often block scripted "Copy" actions if they use older or deprecated APIs，which can happen when the site tries to package complex data (like a video embed) into the clipboard。
* **Markdown Formatting Errors:** Recent reports indicate that even when the copy function "works," it may incorrectly format links as `[URL](URL)` instead of `[Display Text](URL)`，or strip the links entirely。
* **UI False Positives:** The interface may show a "Copied" checkmark even if the clipboard remains empty because the UI state updates before verifying the success of the background clipboard operation。

### Common Workarounds

If you are experiencing this，you can try the following:

* **Manual Selection:** Highlight the text with your cursor and use the keyboard shortcut (**Ctrl+C** on Windows, **Cmd+C** on Mac) instead of clicking the "Copy" button。
* **Copy as Markdown:** Some versions of the interface offer a "Copy as Markdown" option under the three-dot menu，which is sometimes more reliable for responses with links。
* **Paste without Formatting:** Try using **Ctrl+Shift+V** (Windows) or **Cmd+Option+Shift+V** (Mac) when pasting to see if the content was copied but is simply failing to render in your destination app。
* **Incognito Mode:** Occasionally, browser extensions (especially ad-blockers) can interfere with the way Gemini renders YouTube previews and handles the clipboard。

References:

* [Bug in Gemini Business: "Copy link" is blank](https://support.google.com/gemini/thread/389378326)
* [Gemini's copy response function incorrectly formatting Markdown](https://www.reddit.com/r/GeminiAI/comments/1qnshly/geminis_copy_response_function_is_incorrectly/)
* [Gemini Copy & Paste Not Working Discussion](https://www.reddit.com/r/GeminiAI/comments/1o5ehos/gemini_copy_paste_not_working/)

Would you like me to provide a specific prompt you can use to force Gemini to provide text-only links without previews to avoid this bug?