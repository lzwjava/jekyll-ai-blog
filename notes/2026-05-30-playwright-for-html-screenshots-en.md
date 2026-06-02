---
audio: false
generated: true
image: false
lang: en
layout: post
title: Playwright for HTML Screenshots
translated: false
type: note
---

**Question:** For the HTML→screenshot pipeline described, what Python library should be used for the headless browser step in [lzwjava/ww](https://github.com/lzwjava/ww)? Camoufox, raw CDP, or something else?

**Answer:**

For your use case — render local HTML → screenshot → crop — this is **not a scraping/anti-bot problem**, so the choice collapses to a simpler axis: **rendering fidelity vs. dependency weight vs. control level**. Here's the breakdown:

---

## The Stack Decision Tree

```
Need anti-bot fingerprint spoofing?
├── Yes → Camoufox (Firefox fork, overkill here)
└── No → Do you need pixel-perfect Chrome rendering?
    ├── Yes, local only → playwright (Chromium)
    └── Yes, with viewport/PDF control → playwright + CDP session
```

Your use case is **local HTML → screenshot**, no auth, no bot detection. The right answer is **Playwright (Python)**, and here's why:

---

## Option 1: Playwright — Recommended

Playwright is what Browserbase uses internally (it's their abstraction). You get it directly:

```python
# pip install playwright && python -m playwright install chromium
from playwright.sync_api import sync_playwright

def html_to_screenshot(html_path: str, output_path: str, width: int = 720):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": 800})
        page.goto(f"file://{html_path}")

        # Get exact content height
        height = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": width, "height": height})

        # Full-page screenshot, no ImageMagick crop needed
        page.screenshot(path=output_path, full_page=True)
        browser.close()
```

Key trick: **set viewport to content width before shooting** → eliminates the ImageMagick crop step entirely. `full_page=True` handles the vertical extent.

For PDF export (alternative to PNG/JPG):

```python
page.pdf(path="output.pdf", width="720px", print_background=True)
```

---

## Option 2: Raw CDP — When Playwright Isn't Enough

CDP is a set of APIs that exposes a running Chromium browser over a WebSocket connection, letting external tools open tabs, evaluate JavaScript, intercept network requests, and capture screenshots programmatically. Playwright and Puppeteer use CDP under the hood.

You'd use raw CDP directly via `pychrome` or `nodriver` when:
- You need to attach to an **already-running Chrome** (e.g., your daily browser session with logged-in state)
- You need low-level protocol access Playwright doesn't expose (e.g., `Page.captureScreenshot` with specific clip rects, or `Emulation.setDeviceMetricsOverride`)

```python
# pip install pychrome
import pychrome, base64

browser = pychrome.Browser(url="http://127.0.0.1:9222")  # Chrome --remote-debugging-port=9222
tab = browser.new_tab()
tab.start()
tab.Page.navigate(url=f"file:///path/to/file.html")
tab.wait(2)

# Capture at exact dimensions
result = tab.Page.captureScreenshot(
    format="png",
    clip={"x": 0, "y": 0, "width": 720, "height": 3008, "scale": 1}
)
with open("out.png", "wb") as f:
    f.write(base64.b64decode(result["data"]))
```

The CDP `clip` parameter is the **exact equivalent of your ImageMagick crop** — you can skip the post-process entirely.

---

## Option 3: Camoufox — Not the Right Tool Here

Camoufox is a Firefox fork engineered for AI agents. It is headless, undetectable, and optimized to run at scale. Its value is fingerprint spoofing for scraping protected sites. Running in headless mode may still be detectable in the future; it's recommended to use a virtual display buffer.

For your pipeline: local HTML files, no auth, no bot detection → Camoufox adds 0 value and costs you a Firefox binary download + Xvfb dependency. Skip it.

---

## Recommendation for `ww`

Use **Playwright** as the library, with this improved flow that kills the ImageMagick step:

```python
# In ww: render_html_screenshot(html_path, out_path, content_width=720)
from playwright.sync_api import sync_playwright
from pathlib import Path

def render(html_path: str, out_path: str, width: int = 720, fmt: str = "jpeg"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": 100})
        page.goto(f"file://{Path(html_path).resolve()}")
        page.wait_for_load_state("networkidle")  # wait for Google Fonts etc.
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

`wait_for_load_state("networkidle")` is critical — it waits for Google Fonts (Noto Sans SC) to fully load before shooting. Without it you get fallback fonts.

---

## Summary Table

| Library | Engine | Use case fit | Extra deps |
|---|---|---|---|
| **Playwright** | Chromium/Firefox/WebKit | ✅ Local HTML → PNG/JPG | minimal |
| **Raw CDP** | Chromium | ✅ Attach to running Chrome, exact clip | `pychrome` or `nodriver` |
| **Camoufox** | Firefox fork | ❌ Anti-bot scraping only | Firefox binary + Xvfb |
| **Selenium** | Any | ❌ Legacy, heavier | WebDriver binary |

Go with Playwright. It's what Browserbase abstracts anyway — cut the middleman and own the rendering directly in `ww`.

**References:**

- [Playwright Python docs](https://playwright.dev/python/docs/intro)
- [Chrome DevTools Protocol overview](https://chromedevtools.github.io/devtools-protocol/)
- [Camoufox GitHub](https://github.com/daijro/camoufox)
- [browser-use: Leaving Playwright for CDP](https://browser-use.com/posts/playwright-to-cdp)
