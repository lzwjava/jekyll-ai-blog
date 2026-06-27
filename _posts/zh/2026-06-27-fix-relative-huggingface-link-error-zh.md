---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复相对HuggingFace链接错误
translated: true
type: note
---

我需要看到实际代码才能判断问题所在。404错误来自你的 Cloudflare Worker，而不是 HuggingFace，所以问题出在 HuggingFace 按钮的链接/路由构建或处理方式上。

让我检查一下实际线上内容。按钮本身指向 `https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf`——这个链接没问题，是外部链接。404 不是来自按钮的 `href`，而是因为 **那个仓库不存在**（或者设为私有/名称错误）导致 HuggingFace 返回了 404。让我确认。HuggingFace 仓库存在且能正常访问（返回 200，完整的模型卡片）。所以 404 并不是目标地址的问题——而是链接在你页面上渲染/点击的方式有问题。

最可能的原因：你的 Worker HTML 中的 HuggingFace 链接是 **相对路径，而不是绝对路径**。在获取的 markdown 中，链接渲染为 `[HuggingFace]` 且没有可见的协议，而你的 Worker 从根域名提供所有内容。如果 `href` 写成 `huggingface.co/lzwjava/...`（缺少 `https://`），浏览器会将其视为 **相对路径**，解析为：

```
https://sec-edgar-gpt.lzwjava.workers.dev/huggingface.co/lzwjava/sec-edgar-gpt-124m-hf
```

——你的 Worker 没有该路由 → 显示它自己的 404 页面（就是你看到的 “Sorry, we can't find the page”）。

修复方法：将 href 改为绝对路径。检查你的源文件（HTML 或 markdown）：

```bash
# 找到有问题的链接
grep -rn "huggingface" .

# 查找缺少协议前缀的 href
grep -rn 'href="huggingface' .
grep -rn '](huggingface' .   # markdown 格式
```

错误模式和修复方式如下：

```html
<!-- 错误：相对路径 → 解析到你的 worker 域名下 → 404 -->
<a href="huggingface.co/lzwjava/sec-edgar-gpt-124m-hf">HuggingFace</a>

<!-- 正确 -->
<a href="https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf">HuggingFace</a>
```

对应的 Markdown 格式：

```markdown
<!-- 错误 -->  [HuggingFace](huggingface.co/lzwjava/sec-edgar-gpt-124m-hf)
<!-- 正确 --> [HuggingFace](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf)
```

注意你的 GitHub 和 Paper 按钮应该能正常工作，因为它们写成了 `https://` 开头，只有 HuggingFace 那个是裸写的。要一次性确认诊断，打开页面并检查解析后的 URL：

```bash
curl -s https://sec-edgar-gpt.lzwjava.workers.dev/ | grep -i huggingface
```

如果输出的 `href` 没有 `https://`，那就是这个问题。添加协议前缀后重新部署（`wrangler deploy`）。
