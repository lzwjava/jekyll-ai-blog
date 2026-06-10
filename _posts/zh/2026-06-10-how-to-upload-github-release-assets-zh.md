---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何上传GitHub发布资源
translated: true
type: note
---

**问题：** 在 GitHub 上起草 Release 时，为什么看不到专门的“Assets”设置区域——在哪里附加资产文件？

**回答：**

草稿表单中没有独立的“Assets”设置面板——上传区域就是你看到的那个拖放框：

> *"Attach binaries by dropping them here or selecting them."*

该框直接位于**Release 描述文本框下方**，*就是*资产上传区域。将文件拖入或点击它即可打开文件选择器。熟悉的 **“Assets”部分**（可折叠列表，显示你的二进制文件以及自动生成的`Source code (zip/tar.gz)`）只有在你**保存草稿或发布后**才会出现——在编辑草稿时，它仅仅是那个拖放区域。

常见的原因导致它看起来缺失或无法工作：

- **尚未选择标签**——某些控件在创建/选择标签之前保持无效状态。
- **移动浏览器**——拖放区域在移动设备上不可靠；请使用桌面端或 CLI。
- **文件过大**——每个资产必须 ≤ 2 GiB；超大文件会静默失败。
- **广告拦截器/网络**——上传请求发往 `uploads.github.com`，有时会被代理拦截。

既然你习惯终端优先操作，可以直接用 `gh` 绕过 UI：

```bash
# 一次性创建 Release 并附加资产
gh release create v0.3.0 ./dist/ww-darwin-arm64 ./dist/ww-linux-amd64 \
  --title "v0.3.0" \
  --generate-notes

# 向现有 Release/草稿添加资产
gh release upload v0.3.0 ./dist/ww-darwin-arm64 --clobber

# 仅创建草稿（暂不发布）
gh release create v0.3.0 ./dist/* --draft --generate-notes
```

对于 CI，可通过 GitHub Actions 实现相同效果：

```yaml
- uses: softprops/action-gh-release@v2
  with:
    files: dist/*
  if: startsWith(github.ref, 'refs/tags/')
```

对于 `ww`，最干净的长远方案是设置一个标签触发的工作流，自动为每个平台构建二进制文件并上传——从此无需手动拖放。

**参考资料：**

- [Managing releases in a repository — GitHub Docs](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [gh release create — GitHub CLI manual](https://cli.github.com/manual/gh_release_create)
