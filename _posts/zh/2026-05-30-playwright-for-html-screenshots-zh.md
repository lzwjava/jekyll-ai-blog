---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于HTML截图的Playwright
translated: true
type: note
---

**问题：** 对于描述的 HTML→截图流程，在 [lzwjava/ww](https://github.com/lzwjava/ww) 中，无头浏览器步骤应使用哪个 Python 库？Camoufox、原始 CDP 还是其他？

**答案：**

针对你的用例——渲染本地 HTML → 截图 → 裁剪——这**并非爬虫/反爬问题**，因此选择可以简化为更简单的轴：**渲染保真度 vs. 依赖重量 vs. 控制级别**。以下是分析：

---

## 技术栈决策树

```
需要反爬指纹伪装？
├── 是 → Camoufox (Firefox 分支，此处大材小用)
└── 否 → 是否需要像素级完美的 Chrome 渲染？
    ├── 是，仅本地 → playwright (Chromium)
    └── 是，需要视口/PDF 控制 → playwright + CDP 会话
```

你的用例是**本地 HTML → 截图**，无需认证，无爬虫检测。正确答案是 **Playwright (Python)**，原因如下：

---

## 方案 1：Playwright —— 推荐

Playwright 是 Browserbase 内部使用的库（也是其抽象层）。你可以直接使用：

```python
# pip install playwright && python -m playwright install chromium
from playwright.sync_api import sync_playwright

def html_to_screenshot(html_path: str, output_path: str, width: int = 720):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": 800})
        page.goto(f"file://{html_path}")

        # 获取精确的内容高度
        height = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": width, "height": height})

        # 全页截图，无需 ImageMagick 裁剪
        page.screenshot(path=output_path, full_page=True)
        browser.close()
```

关键技巧：**在截图前将视口设为内容宽度** → 完全省去 ImageMagick 裁剪步骤。`full_page=True` 处理纵向范围。

如需导出 PDF（替代 PNG/JPG）：

```python
page.pdf(path="output.pdf", width="720px", print_background=True)
```

---

## 方案 2：原始 CDP —— 当 Playwright 不够用时

CDP 是一组 API，通过 WebSocket 连接暴露正在运行的 Chromium 浏览器，使外部工具能够编程式打开标签页、执行 JavaScript、拦截网络请求及捕获屏幕截图。Playwright 和 Puppeteer 底层均使用 CDP。

当你需要以下场景时，可通过 `pychrome` 或 `nodriver` 直接使用原始 CDP：

- 你需要附加到**已运行的 Chrome**（例如，已登录状态的日常浏览器会话）
- 你需要 Playwright 未暴露的底层协议访问（例如，带特定裁剪区域的 `Page.captureScreenshot`，或 `Emulation.setDeviceMetricsOverride`）

```python
# pip install pychrome
import pychrome, base64

browser = pychrome.Browser(url="http://127.0.0.1:9222")  # Chrome --remote-debugging-port=9222
tab = browser.new_tab()
tab.start()
tab.Page.navigate(url=f"file:///path/to/file.html")
tab.wait(2)

# 按精确尺寸捕获
result = tab.Page.captureScreenshot(
    format="png",
    clip={"x": 0, "y": 0, "width": 720, "height": 3008, "scale": 1}
)
with open("out.png", "wb") as f:
    f.write(base64.b64decode(result["data"]))
```

CDP 的 `clip` 参数**完全等同于你的 ImageMagick 裁剪**——你可以完全省去后处理步骤。

---

## 方案 3：Camoufox —— 并非此处的合适工具

Camoufox 是一个为 AI 代理定制的 Firefox 分支。它无头、不可检测，并针对大规模运行进行了优化。其价值在于为爬取受保护网站提供指纹伪装。在无头模式下运行未来仍可能被检测；建议使用虚拟显示缓冲区。

对于你的流程：本地 HTML 文件，无需认证，无爬虫检测 → Camoufox 增加零价值，反而需要你下载 Firefox 二进制文件及 Xvfb 依赖。跳过它。

---

## 对 `ww` 的建议

使用 **Playwright** 作为库，并通过以下改进流程省去 ImageMagick 步骤：

```python
# 在 ww 中：render_html_screenshot(html_path, out_path, content_width=720)
from playwright.sync_api import sync_playwright
from pathlib import Path

def render(html_path: str, out_path: str, width: int = 720, fmt: str = "jpeg"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": 100})
        page.goto(f"file://{Path(html_path).resolve()}")
        page.wait_for_load_state("networkidle")  # 等待 Google Fonts 等加载
        h = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": width, "height": h})
        page.screenshot(
            path=out_path,
            full_page=True,
            type=fmt,
            quality=95 if fmt == "jpeg" else None,
            clip={"x": 0, "y": 0, "width": width, "height": h}
        )
        browser.close()
```

`wait_for_load_state("networkidle")` 至关重要——它会等待 Google Fonts（Noto Sans SC）完全加载后再截图。缺少它会导致使用后备字体。

---

## 总结表格

| 库 | 引擎 | 用例适配度 | 额外依赖 |
|---|---|---|---|
| **Playwright** | Chromium/Firefox/WebKit | ✅ 本地 HTML → PNG/JPG | 最小 |
| **原始 CDP** | Chromium | ✅ 附加到运行中的 Chrome，精确裁剪 | `pychrome` 或 `nodriver` |
| **Camoufox** | Firefox 分支 | ❌ 仅用于反爬抓取 | Firefox 二进制文件 + Xvfb |
| **Selenium** | 任意 | ❌ 过时，负担较重 | WebDriver 二进制文件 |

选择 Playwright。它正是 Browserbase 所抽象的工具——去掉中间层，在 `ww` 中直接掌控渲染。

**参考文献：**

- [Playwright Python 文档](https://playwright.dev/python/docs/intro)
- [Chrome DevTools 协议概述](https://chromedevtools.github.io/devtools-protocol/)
- [Camoufox GitHub](https://github.com/daijro/camoufox)
- [browser-use: 从 Playwright 迁移到 CDP](https://browser-use.com/posts/playwright-to-cdp)
