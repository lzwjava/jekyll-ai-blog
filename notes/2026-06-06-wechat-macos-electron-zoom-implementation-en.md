---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat macOS Electron Zoom Implementation
translated: false
type: note
---

Question: How does WeChat on macOS implement font scaling with Command+Plus/Minus shortcuts? Is it Electron-based?

Answer:

Yes, WeChat macOS is Electron. The Command+Plus/Minus zoom is Electron's built-in **webview zoom** mechanism.

Here's what's happening:

## The Tech

Electron wraps Chromium's BrowserWindow. When you press Command+Plus, it's triggering the **zoom level** API, not actual font resizing:

```javascript
// In the main process (Electron)
const { app, BrowserWindow, Menu } = require('electron');
const mainWindow = new BrowserWindow({...});

// Built-in zoom shortcuts (Command+Plus, Command+Minus, Command+0)
// are captured automatically by Electron's default menu OR
// you explicitly handle them:

app.whenReady().then(() => {
  const mainWindow = createWindow();

  // Set zoom level (1 = 100%, 0.1 increment = ~10%)
  mainWindow.webContents.setZoomLevel(1.2);

  // Get current zoom
  const currentZoom = mainWindow.webContents.getZoomLevel(); // returns factor
});

// Programmatically:
mainWindow.webContents.setZoomLevel(mainWindow.webContents.getZoomLevel() + 0.1);
```

The zoom level is **not per-element font resizing** — it's a uniform **scale transform** applied to the entire rendered content:

- `zoomLevel = 1.0` → 100%
- `zoomLevel = 1.2` → 120%
- `zoomLevel = 0.9` → 90%

Under the hood, Chromium applies a CSS transform or DPI-scale to all rendered pixels.

## How WeChat Likely Implements It

WeChat's macOS app probably:

1. **Captures Command+Plus/Minus** in the main Electron process
2. **Calls `setZoomLevel()`** on the renderer's webContents
3. **Persists the zoom** to local storage so it survives restarts:

```javascript
// Renderer process (in WeChat's UI layer)
const savedZoom = localStorage.getItem('wechat_zoom') || 1.0;
window.api.setZoomLevel(parseFloat(savedZoom));

document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === '+') {
    const newZoom = currentZoom + 0.1;
    window.api.setZoomLevel(newZoom);
    localStorage.setItem('wechat_zoom', newZoom);
  }
  if ((e.metaKey || e.ctrlKey) && e.key === '-') {
    const newZoom = Math.max(0.5, currentZoom - 0.1);
    window.api.setZoomLevel(newZoom);
    localStorage.setItem('wechat_zoom', newZoom);
  }
});
```

## Why Electron Uses Zoom Level (Not Font Scaling)

- **Simple**: One API call scales everything uniformly
- **Fast**: Hardware-accelerated transform, not re-layout
- **Consistent**: Works for images, text, UI controls, everything
- **Stateless**: No CSS mutations needed

Alternative (CSS font-size scaling) would require traversing the DOM and mutating every element — slower and fragile.

## Practical Limit

Electron's zoom typically clamps to `[0.25, 5.0]` to prevent weird rendering artifacts.

References:

- [Electron BrowserWindow.webContents.setZoomLevel()](https://www.electronjs.org/docs/latest/api/web-contents#contentsetzoomlevel-level)
- [Chromium zoom implementation](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/exported/web_view.cc)
