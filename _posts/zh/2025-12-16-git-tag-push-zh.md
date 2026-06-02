---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Git 标签使用与推送
translated: true
type: note
---

问题：如何使用 `git tag` 以及如何使用 `git push` 推送标签？

答案：

Git 标签用于标记仓库历史中的特定提交，通常用于发布版本（例如 `v1.0.0`）。

### 标签类型

- **轻量级标签 (Lightweight tags)**：指向提交的简单指针（像书签）。没有额外的元数据。
- **附注标签 (Annotated tags)**（推荐用于发布）：完整的 Git 对象，包括标签创建者姓名、电子邮件、日期、消息，以及可选的 GPG 签名。

### 创建标签

- 列出现有标签：

  ```
  git tag
  ```

- 创建一个**轻量级标签**（在当前 HEAD 上）：

  ```
  git tag <tagname>
  ```

  示例：`git tag v1.0`

- 创建一个**附注标签**（推荐）：

  ```
  git tag -a <tagname> -m "Your message"
  ```

  示例：`git tag -a v1.0 -m "Stable release version 1.0"`

- 标记一个旧的提交（指定提交哈希）：

  ```
  git tag -a v0.9 <commit-hash> -m "Previous release"
  ```

- 查看标签详情：

  ```
  git show <tagname>
  ```

  （附注标签显示元数据；轻量级标签只显示提交。）

### 推送标签到远程仓库

标签**不会**随 `git push` **自动推送**。您必须显式地推送它们。

- 推送单个标签：

  ```
  git push origin <tagname>
  ```

  示例：`git push origin v1.0`

- 推送所有本地标签：

  ```
  git push origin --tags
  ```

- 自动推送可从已推送提交中触及的附注标签（Git 2.4+ 开始）：
  配置：

  ```
  git config --global push.followTags true
  ```

  然后 `git push` 将会包含它们。

### 删除标签

- 本地：

  ```
  git tag -d <tagname>
  ```

- 远程：

  ```
  git push origin :refs/tags/<tagname>
  ```

  或（较新版本的 Git）：`git push origin --delete <tagname>`

最佳实践：对公开发布使用附注标签以保留元数据。

参考资料：

- [Git - Tagging (官方文档)](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
- [git-tag Documentation](https://git-scm.com/docs/git-tag)
