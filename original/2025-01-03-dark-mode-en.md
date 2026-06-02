---
audio: true
generated: false
image: true
lang: en
layout: post
title: Website Dark Mode Implementation
type: post
---

Dark Mode implementation in my Jekyll blog.

## Toggle

```html
<script>
  const rootElement = document.documentElement;
  const themeToggleBtn = document.getElementById('themeToggle');
  const sunIcon = document.getElementById('sunIcon');
  const moonIcon = document.getElementById('moonIcon');
  const avatarImg = document.getElementById('avatarImg'); // reference to the <img>

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
  // Override your main background color
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
    // If you need a darker background
    background-image: linear-gradient(120deg, $dark-main-bg-color, #222);
    background-color: #2f2f2f !important;
    // Or pick a different dark color, e.g., #1f1f1f, #3a3a3a, etc.
  }

  // Pre/code block background color (was #e0d9cf)
  pre {
    background-color: #3a3a3a !important;
    // or #2f2f2f, etc.
  }

  // Date color override (was darkgray)
  .date {
    color: #aaa !important;
    // or #ccc, #bbb, etc.
  }

  .main-content h1,
  .main-content h2,
  .main-content h3,
  .main-content h4,
  .main-content h5,
  .main-content h6 {
    color: $dark-section-link-color;
  }

  // etc. - override as needed
}
```

## Markdown Syntax

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

## Markdown Image

```scss
.magnet-image {
  width: 300px;
  /* Full width on small screens */
  min-height: 300px;
  /* Adjust as needed */
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
