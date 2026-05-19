---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 避免Jekyll的CSS缓存破坏
translated: true
type: note
---

你所看到的是 Jekyll（通过主题或 `jekyll-assets`/`jekyll-feed`/`minima` 管道）自动在样式表 URL 后附加**指纹（哈希值）**以实现缓存更新。这就是为什么同一个 CSS 文件在重新构建后会带有不同 `?v=...` 查询参数的原因。

若你不想让 Jekyll 在每次构建时更改该查询参数，可以禁用或覆盖“缓存更新”/“摘要”行为：

### 方案 1：使用固定链接

不使用 Jekyll 的辅助标签（例如 `{{ "/assets/css/style.css" | relative_url }}` 或 `{{ "/assets/css/style.css" | asset_path }}`），而是直接硬编码：

```html
<link rel="stylesheet" href="/assets/css/style.css">
```

这样就不会注入指纹。

### 方案 2：禁用资源摘要

如果你正在使用 **jekyll-assets** 或会对文件添加指纹的主题，可以在 `_config.yml` 中禁用摘要功能：

```yml
assets:
  digest: false
```

### 方案 3：使用不带摘要的 `relative_url`

如果你的主题使用了类似这样的代码：

{% raw %}
```liquid
<link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">
```
{% endraw %}

请确保你没有通过启用了摘要功能的 `asset_path` 或 `absolute_url` 进行管道传输。直接使用 `relative_url` 即可。

---

👉 简而言之：

* 如果你希望链接**永不改变**，请硬编码路径。
* 如果你想通过配置来控制，请设置 `assets.digest: false`。
* 如果你仍需要版本控制但保持稳定，则需要手动管理自己的 `?v=...` 参数。

你是希望链接**完全静态**（永不改变），还是仅仅希望阻止 Jekyll**每次构建都生成新哈希值**？