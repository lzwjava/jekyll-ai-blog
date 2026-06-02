---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 配置Playwright使用指定Chrome可执行文件
translated: true
type: note
---

明白了。您希望在 Windows 系统中配置 **Playwright**，使其通过 `playwright.config.js` 直接启动**特定的 Chrome 可执行文件**，并附带某些**启动选项**（例如 `headless: true`）。

具体操作如下：

---

### 1. 在 Playwright 配置中使用 `executablePath`

默认情况下，Playwright 使用其自带的 Chromium，但如果您想使用**Google Chrome**（您自己安装的版本），则必须告知 Playwright `chrome.exe` 文件的位置。

`playwright.config.js` 配置示例：

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
        // 在 Windows 上，提供 chrome.exe 的完整路径
        channel: undefined, // 确保 channel 未设置，因为我们将使用 executablePath
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless: true,  // 在无头模式下运行
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

### 2. 注意事项

- 在 **Windows** 系统上，Chrome 的通常安装路径为：
  - `C:\Program Files\Google\Chrome\Application\chrome.exe`
  - 或 `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
- 请确保在 JavaScript 字符串中**对反斜杠进行转义**（使用 `\\`）。
- 使用 `headless: true` 来强制启用无头模式。
- 您也可以在 `args` 中传递任何 Chromium 命令行标志。

---

### 3. 运行配置

现在您可以使用以下命令运行测试：

```bash
npx playwright test --project="Google Chrome"
```

---

✅ 这将启动您**特定的 Chrome 可执行文件**，并启用**无头模式**及给定的参数。

---

您是否还需要我演示如何**根据条件切换**使用 Playwright 自带的 Chromium 和您已安装的 `chrome.exe`（例如，用于 CI 与本地开发环境）？
