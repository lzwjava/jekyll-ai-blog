---
audio: false
generated: false
image: true
lang: zh
layout: post
title: 网站深色模式实现
translated: true
type: post
---

在我的 Jekyll 博客中实现深色模式。

## 切换

```html
<script>
  const rootElement = document.documentElement;
  const themeToggleBtn = document.getElementById('themeToggle');
  const sunIcon = document.getElementById('sunIcon');
  const moonIcon = document.getElementById('moonIcon');
  const avatarImg = document.getElementById('avatarImg'); // 引用 <img>

  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    rootElement.classList.add('dark-mode');
  }

  function updateIconsAndAvatar() {
    const isDark = rootElement.classList.contains('dark-mode');
    sunIcon.style.display = isDark ? 'inline-block' : 'none';
    moonIcon.style.display = isDark ? 'none' : 'inline-block';
    avatarImg.src = isDark
      ? '/assets/images/avatar_dark.png'
      : '/assets/images/avatar.jpg';
  }

  updateIconsAndAvatar();

  themeToggleBtn.addEventListener('click', function () {
    rootElement.classList.toggle('dark-mode');
    if (rootElement.classList.contains('dark-mode')) {
      localStorage.setItem('theme', 'dark');
    } else {
      localStorage.setItem('theme', 'light');
    }
    updateIconsAndAvatar();
  });
</script>
```

## CSS

```scss
.dark-mode {
  // 覆盖主背景颜色
  body {
    background-color: $dark-main-bg-color;
    color: white;
  }

  .main-content {
    background-color: $dark-main-bg-color;

    h6,
    blockquote {
      color: $dark-section-headings-color;
    }

    a {
      color: white !important;
    }
  }

  .page-header {
    // 如果需要更深的背景
    background-image: linear-gradient(120deg, $dark-main-bg-color, #222);
    background-color: #2f2f2f !important;
    // 或选择不同的深色，例如 #1f1f1f, #3a3a3a 等。
  }

  // Pre/code 块背景颜色（原来是 #e0d9cf）
  pre {
    background-color: #3a3a3a !important;
    // 或 #2f2f2f 等。
  }

  // 日期颜色覆盖（原来是 darkgray）
  .date {
    color: #aaa !important;
    // 或 #ccc, #bbb 等。
  }

  .main-content h1,
  .main-content h2,
  .main-content h3,
  .main-content h4,
  .main-content h5,
  .main-content h6 {
    color: $dark-section-link-color;
  }

  // 等等 - 根据需要覆盖
}
```

## Markdown 语法

```scss
@import "syntax";
@import "syntax-dark";
```

```scss
.dark-mode {
  .highlight {
    table {
      td {
        padding: 5px;
      }

      pre {
        margin: 0;
      }
    }

    color: $color_1;
    background-color: $background-color_1;

    .w {
      color: $color_1;
      background-color: $background-color_1;
    }
  }
}
```

## Markdown 图片

```scss
.magnet-image {
  width: 300px;
  /* 小屏幕上全宽 */
  min-height: 300px;
  /* 根据需要调整 */
  background-image: url('/assets/images/magnet/magnet.jpg');
  background-size: cover;
}

.dark-mode .magnet-image {
  background-image: url('/assets/images/magnet/magnet_dark.jpg');
}
```

```html
<picture>
  <source srcset="/assets/images/magnet/magnet_dark.jpg" media="(prefers-color-scheme: dark)">
  <img src="/assets/images/magnet/magnet.jpg" alt="Magnet Image">
</picture>
```
