---
audio: false
generated: true
image: false
lang: en
layout: post
title: Browser Choices for M2 MacBooks
translated: false
type: note
---

**Question:** What browser should I use on macOS (MacBook Air M2)?

**Answer:**

On M2 Mac, the engine choice matters more because of Apple Silicon optimization.

## Safari — Actually the Best Default Here

Even though it's closed source, on M2 Mac, **Safari is genuinely the right choice** for most browsing:

- **Battery life**: Safari uses ~30-50% less energy than Chrome/Brave on Apple Silicon. WebKit is deeply integrated with the M2's efficiency cores and GPU.
- **JavaScriptCore is ARM-native**: JSC has been tuned for Apple Silicon — benchmark scores are competitive with V8.
- **WebKit is open source**: So you're not on a fully black-box engine. You can read the rendering code, file bugs, even contribute.
- **Memory**: Safari uses significantly less RAM than Chromium-based browsers — relevant since your Air only has 16 GB.

## Brave — Best Open Source Daily Driver

If you want fully open source and Chromium compat (important for web dev work, since most corporate internal tools target Chrome):

```bash
brew install --cask brave-browser
```

Brave on M2 is compiled natively for Apple Silicon, so performance is good. Still burns more battery than Safari.

## Firefox — Worth Having for Engine Diversity

```bash
brew install --cask firefox
```

Gecko on M2 is decent. Firefox is the only way to test non-WebKit, non-Blink rendering — important if you're doing any frontend work.

## My Recommended Setup for Your Workflow

| Browser | Use Case |
|---|---|
| **Safari** | Default browsing, reading, battery life |
| **Brave** | Web dev, testing, sites that need Chrome compat |
| **Firefox** | Cross-browser QA, DevTools for CSS debugging |

## For Automation / AI Work

Since you build CLI agents and scrapers — on macOS, Playwright handles M2 well:

```bash
pip install playwright
playwright install chromium  # or webkit, firefox
```

WebKit via Playwright is the lightest option on M2 and uses Safari's engine — good for testing iOS-equivalent behavior without an emulator.

**Bottom line:** Use Safari as your main browser on M2 — the battery and memory wins are real and compound over a workday. Keep Brave for dev work. The "open source browser" question matters less on Mac because the most important component (WebKit/JSC) is already open source and it's what Safari runs on.
