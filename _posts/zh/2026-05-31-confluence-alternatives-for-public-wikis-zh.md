---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 公开维基的 Confluence 替代方案
translated: true
type: note
---

**问题：** Confluence 是否有像 GitHub 那样公开/世界可访问的版本？最接近的替代方案是什么——Substack、Medium、Quora？

**回答：**

## Confluence：没有公开的“世界”版本

Confluence **纯粹是企业级**——Atlassian 从未推出过面向公众、由社区托管的变体。GitHub 有 github.com，任何人都可以创建免费仓库。Confluence 没有类似的版本。你的选择包括：

- **Confluence Cloud** (atlassian.net)——企业级 SaaS，位于认证墙之后
- **Confluence Data Center**——自托管，默认仍为私有
- 不存在像 "public.confluence.com" 这样的等价物

## Confluence 实际是什么（功能上）

结构化、层级化的 **wiki + 知识库**，包含：

- 空间 → 页面 → 子页面
- 丰富的嵌入（Jira 工单、图表、代码块）
- 团队协作、评论、页面历史
- 按空间/页面的权限控制

## 最接近的公开替代方案（按使用场景排名）

| 工具 | 最适合 | 与 Confluence 的重叠度 |
| ------ | -------- | ------------------------ |
| **Notion** (notion.so) | Wiki + 文档，可创建公开页面 | 最高——空间、数据库、层级结构 |
| **GitBook** | 技术文档，默认公开 | 高——开发团队将其用作公开版 Confluence |
| **GitHub Wiki** | 每个仓库的文档 | 中等——仅支持 Markdown，无丰富结构 |
| **GitHub Pages / Jekyll** | 发布静态文档/博客 | 中等——你正在 lzwjava.github.io 上做的 |
| **Obsidian Publish** | 个人知识库，公开 | 中等——完全符合你的笔记用途 |
| **BookStack** | 自托管 Wiki | 结构匹配度高 |
| **Wiki.js** | 自托管，面向公开 | 高 |

## Substack / Medium / Quora —— 并非真正替代品

这些是 **内容发布平台**，而非知识库：

- **Substack** → 通讯优先，线性文章，无层级
- **Medium** → 文章，无结构化 wiki 概念
- **Quora** → 问答，众包，非你自己的知识

它们与 Confluence 的“页面”概念仅表面重叠。没有空间，没有嵌套层级，没有版本控制的结构化文档。

## 针对你的具体用例

你已经在做正确的事——**lzwjava.github.io**（Jekyll/GitHub Pages）实际上就是你的公开版 Confluence 替代方案。它具有：

- 版本控制（Git）
- 层级结构（分类、标签）
- 可被公开索引
- 免费且完全自主

如果你想要更丰富的结构，**GitBook**（免费版，公开空间）或 **Obsidian Publish**（$8/月）是最接近的升级选择。特别是 GitBook，大多数开源项目在需要“Confluence 但公开”时都会使用它。
