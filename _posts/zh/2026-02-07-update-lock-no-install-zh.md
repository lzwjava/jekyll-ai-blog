---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 无需安装即可更新锁定文件
translated: true
type: note
---

`npm install` 中的 `--package-lock-only` 标志告诉 npm **仅更新 `package-lock.json` 文件，而不实际安装任何 packages** 到你的 `node_modules` 文件夹中。

这在以下场景中非常有用：

1.  **在手动编辑 `package.json` 后更新 lock file** - 你可以重新生成 `package-lock.json` 以反映你的更改，而无需下载任何内容。

2.  **解决 lock file 冲突** - 如果你正在合并 branches 并且 `package-lock.json` 中存在冲突，你可以运行 `npm install --package-lock-only` 根据当前的 `package.json` 重新生成它。

3.  **检查将要安装的版本** - 你可以查看解析后的 dependency tree 的样子，而无需实际安装 packages。

4.  **在 CI/CD pipelines 中节省时间** - 如果你只需要为一次 commit 更新 lock file，则不会浪费时间下载 packages。

例如：
```bash
npm install --package-lock-only
```

这与 `--dry-run`（显示将要安装的内容但不修改任何内容）以及正常的 `npm install`（既更新 lock file 又安装 packages）有所不同。