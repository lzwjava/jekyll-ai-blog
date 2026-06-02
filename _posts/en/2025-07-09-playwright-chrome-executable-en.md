---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Configuring Playwright with Specific Chrome Executable
translated: false
type: note
---

Got it. You want to configure **Playwright** on Windows so that it launches a **specific Chrome executable** with certain **launch options** (like `headless: true`) directly in your `playwright.config.js`.

Here’s how you can do it:

---

### 1. Use `executablePath` in your Playwright config
By default, Playwright uses its bundled Chromium, but if you want **Google Chrome** (your own installation), you must tell Playwright where the `chrome.exe` file is located.

Example `playwright.config.js`:

```js
// playwright.config.js
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

export default defineConfig({
  projects: [
    {
      name: 'Google Chrome',
      use: {
        browserName: 'chromium',
        // On Windows, provide the full path to chrome.exe
        channel: undefined, // make sure channel is unset, since we'll use executablePath
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless: true,  // run in headless mode
        args: [
          '--disable-gpu',
          '--no-sandbox',
          '--disable-dev-shm-usage',
        ],
      },
    },
  ],
});
```

---

### 2. Notes
- On **Windows**, the usual Chrome path is:
  - `C:\Program Files\Google\Chrome\Application\chrome.exe`
  - or `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
- Make sure to **escape backslashes** (`\\`) in JS strings.
- Use `headless: true` to enforce headless mode.
- You can also pass any Chromium CLI flags in `args`.

---

### 3. Run the config
You can now run tests with:

```bash
npx playwright test --project="Google Chrome"
```

---

✅ This will launch your **specific Chrome executable** with **headless mode** and the given arguments.

---

Do you also want me to show you how to **conditionally switch** between bundled Playwright Chromium and your installed `chrome.exe` (e.g. for CI vs local dev)?
