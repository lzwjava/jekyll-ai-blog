---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 理解HTML视口
translated: true
type: note
---

以下是对 **viewport** 在 HTML/CSS 中清晰实用的理解方式，特别是你在手机和桌面浏览器（如 macOS 上的 Safari）之间注意到的差异。

### 1. 什么是 Viewport？
Viewport 是网页在浏览器窗口（或屏幕）内**当前对用户可见的区域**。

它**不是**整个网页——它只是任何给定时刻可见的部分。

### 2. 你看到的两种不同的 Viewport

| 情况                          | "viewport" 的含义                                   | 在手机上的典型尺寸          | 在桌面上的典型尺寸               |
|-------------------------------|-----------------------------------------------------|----------------------------|----------------------------------|
| **手机浏览器** (iPhone Safari, Android Chrome 等) | **布局 viewport** (CSS 看到的那个)                  | 通常是 980px、375px 或浏览器设置的某个固定值（不是物理屏幕宽度） | 在桌面上几乎不会发生             |
| **桌面浏览器** (macOS/Windows 上的 Safari/Chrome/Firefox) | **视觉 viewport** = 实际的浏览器窗口大小            | –                          | 恰好是浏览器窗口的内部宽度/高度 |

### 3. 为什么手机行为不同（这是关键困惑点）

默认情况下，手机浏览器会对你的 CSS 说谎。

- iPhone 16 Pro 的物理屏幕：1290 × 2796 像素
- 但如果你打开开发者工具并运行 `document.documentElement.clientWidth`，你很可能得到 **390** 或 **430** CSS 像素。
- 许多旧网站是为约 980px 宽度设计的，所以手机浏览器假装 viewport 约 980px 宽（或者在带有正确 meta 标签的现代 iPhone 上是 375px）。这被称为**布局 viewport**。

如果在 `<head>` 中没有这行代码，移动版 Safari 会假定你想要旧的桌面行为：

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

使用此 meta 标签 → 布局 viewport ≈ 以 CSS 像素为单位的物理设备宽度
不使用它 → 布局 viewport = 980px（或类似值），即使在小小的手机上也是如此

这就是为什么在手机上，如果你忘记添加 meta 标签，100vw 看起来会很大的原因。

### 4. 你提到的单位：vw 和 vh

- 1vw = **布局 viewport 宽度**的 1%
- 1vh = **布局 viewport 高度**的 1%

所以：

| 设备 / 情况                               | 100vw 等于…                                        |
|------------------------------------------|----------------------------------------------------|
| 桌面 Safari、Chrome 等                   | 当前浏览器窗口宽度（调整窗口大小时会改变）         |
| 带有正确 `<meta name="viewport">` 的手机 | 大致是 CSS 像素中的屏幕宽度（例如，许多 iPhone 上是 393px） |
| 没有 meta 标签的手机                     | 通常是 980px 或浏览器默认的任何值                  |

### 5. 总结 – 针对你具体问题的答案

- 在手机上，除非你有 meta viewport 标签，否则 viewport **不会**自动意味着整个物理屏幕。
- 在 macOS 的 Safari（或任何桌面浏览器）上，是的——viewport 恰好是浏览器窗口的大小，并且当你调整窗口大小时 vw/vh 会立即改变。
- Viewport **从来不是完全固定的**——它总是在以下情况下改变：
  - 你调整浏览器窗口大小（桌面）
  - 你旋转手机（手机）
  - 屏幕键盘出现/消失（手机）
  - 你进行缩放（尽管在手机上缩放通常不会改变布局 viewport）

### 6. 你现在就可以尝试的快速测试

将以下代码粘贴到任何 HTML 文件中，并在手机和 Mac 上打开它：

```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { margin:0; font-family:sans-serif; }
    .box {
      width: 100vw;
      height: 100vh;
      background: #f06d06;
      color: white;
      display: grid;
      place-items: center;
      font-size: 2rem;
    }
  </style>
</head>
<body>
  <div class="box">
    100vw × 100vh<br>
    宽度: <span id="w"></span>px<br>
    高度: <span id="h"></span>px
  </div>

<script>
  function update() {
    document.getElementById('w').textContent = window.innerWidth;
    document.getElementById('h').textContent = window.innerHeight;
  }
  update();
  window.addEventListener('resize', update);
</script>
</body>
</html>
```

- 在 macOS Safari 上 → 橙色框会随着浏览器窗口大小调整而精确调整。
- 在 iPhone Safari 上 → 橙色框几乎填满整个屏幕（减去 Safari 的 UI 部分），并且数字与你设备的 CSS 像素宽度匹配（例如，许多 iPhone 上是 393px）。

这就是 viewport 的实际作用！
