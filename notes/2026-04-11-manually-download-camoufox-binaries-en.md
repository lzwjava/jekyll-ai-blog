---
audio: false
generated: true
image: false
lang: en
layout: post
title: Manually Download Camoufox Binaries
translated: false
type: note
---

I'll search for information about manually downloading Camoufox binaries to help you bypass the slow npm installation.**Question:** Instead of waiting for the slow download during `npm install && npm start` in the `@askjo/camofox-browser` project, can I manually download the Camoufox binaries from the GitHub repository at <https://github.com/apify/camoufox-js>?

**Answer:**

Yes, you can manually download Camoufox binaries, but you should go to the **main Camoufox repository** (not the camoufox-js repo) to get the actual browser binaries.

## Where to Download Camoufox Binaries

The browser binaries are hosted in the **daijro/camoufox** repository's releases page, not in the apify/camoufox-js repository. Here's how to do it:

### Step 1: Go to the Camoufox Releases Page

Visit the main Camoufox releases page and download the appropriate binary for your system.

### Step 2: Choose Your Platform Binary

The latest stable release is **v135.0.1-beta.24** (as of March 15, 2025). Download the file matching your operating system and architecture:

- **Linux x86_64**: `camoufox-135.0.1-beta.24-lin.x86_64.zip`
- **Linux ARM64**: `camoufox-135.0.1-beta.24-lin.arm64.zip`
- **macOS x86_64**: `camoufox-135.0.1-beta.24-mac.x86_64.zip`
- **macOS ARM64**: `camoufox-135.0.1-beta.24-mac.arm64.zip`
- **Windows x86_64**: `camoufox-135.0.1-beta.24-win.x86_64.zip`

### Step 3: Extract and Place the Binary

After downloading, extract the archive and place it in the appropriate cache directory where Camoufox expects to find it. The typical locations are:

- **Linux/macOS**: `~/.cache/camoufox/`
- **Windows**: `%LOCALAPPDATA%\camoufox\`

### Step 4: Run the Fetch Command

After manually placing the binaries, you can run:

```bash
npx camoufox-js fetch
```

This command should detect the existing binaries and skip the slow download.

## Alternative: Use the CLI Fetch Command First

If you want to avoid slow npm postinstall downloads, you can:

1. Install the package without running postinstall hooks:

   ```bash
   npm install --ignore-scripts
   ```

2. Then manually fetch the browser:

   ```bash
   npx camoufox-js fetch
   ```

This gives you more control over the download process and you can retry if it fails.

## Important Notes

- The **apify/camoufox-js** repository is just a JavaScript wrapper/client library - it doesn't contain the actual browser binaries
- The actual browser binaries are built and released by the **daijro/camoufox** repository
- When you run `npx camoufox-js fetch`, it downloads binaries from the daijro/camoufox releases
- The slow download you're experiencing is because the binary files are large (around 700-800 MB)

**References:**

- [https://github.com/daijro/camoufox/releases](https://github.com/daijro/camoufox/releases)
- [https://github.com/apify/camoufox-js](https://github.com/apify/camoufox-js)
- [https://camoufox.com/](https://camoufox.com/)
