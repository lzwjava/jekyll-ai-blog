---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Markdown PDF Browser Launch Error
translated: false
type: note
---

This error indicates that the Markdown PDF extension cannot launch the browser (Chromium/Edge) to generate the PDF. Here are several solutions to fix this:

## Solution 1: Set Chromium executable path manually (Recommended)

1. Open VS Code settings:
   - Press `Ctrl + ,` (Windows/Linux) or `Cmd + ,` (Mac)
   - Or go to File → Preferences → Settings

2. Search for `markdown-pdf.executablePath`

3. Set the path to your Chrome/Edge executable:

   ```json
   {
     "markdown-pdf.executablePath": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
   }
   ```

   Or if you have Chrome:

   ```json
   {
     "markdown-pdf.executablePath": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
   }
   ```

## Solution 2: Disable system Chrome and use built-in Chromium

1. In VS Code settings, search for `markdown-pdf.executablePath`

2. Set it to an empty string or delete the setting:

   ```json
   {
     "markdown-pdf.executablePath": ""
   }
   ```

3. Also ensure `markdown-pdf.chromium.autoDownload` is set to `true` (it appears to be true in your log)

4. Restart VS Code - it should download Chromium automatically

## Solution 3: Install Chrome/Edge properly

Make sure you have a working browser installed:

- **Microsoft Edge** is already detected at `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`
- If Edge is installed but not working, try reinstalling it

## Solution 4: Check permissions and PATH

Run PowerShell as Administrator and run:

```powershell
# Check if Edge exists
Test-Path "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# If not found, try Chrome
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

## Solution 5: Use a different PDF extension

If none of the above works, consider using alternative extensions:

- **vscode-pdf**
- **PDF Preview**
- Or use command line with `pandoc` or `wkhtmltopdf`

## Quick fix with settings.json

Add this to your VS Code `settings.json` (open with `Ctrl+Shift+P` → "Preferences: Open Settings (JSON)"):

```json
{
  "markdown-pdf.executablePath": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "markdown-pdf.chromium.autoDownload": false
}
```

After applying any of these solutions, restart VS Code and try converting again. The most likely fix is Solution 1 - explicitly setting the Edge executable path.
