---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 远程 Firefox 登录，实现无缝访问
translated: true
type: note
---

💡 **这是完美的协作方式！** 💡

由于我正在你的第二台电脑上运行，你可以通过打开一个**可见的 browser session** 来登录我，然后我就可以“接管”它。

**这是帮助我的确切方法：**

1. **Physical Access**：前往你的第二台电脑。
2. **Open Firefox**：启动一个新的 Firefox 窗口。
3. **Use MY Managed Profile**：在那台第二台电脑的终端中运行此命令，使用我正在使用的确切 profile 打开 Firefox：

```bash
firefox --profile /home/lzw/.openclaw/browser-profiles/openclaw --no-remote
```

4. **Login**：在该窗口中访问 `github.com` 并以 `lzwjava` 身份登录。
5. **Close Firefox**：完全关闭浏览器窗口。

**Result**：
你的 session cookies 现在将保存在那个文件夹中（`~/.openclaw/browser-profiles/openclaw`）。下次我启动我的 **headless** browser 时，它会找到那些 cookies，并且**我会自动以你的身份登录！**

完成这些后，我就能在不打扰你的情况下授权 Copilot 代码了。🐙✨💂‍♂️🚀🛋️

（我随时待命——告诉我何时完成登录！）
