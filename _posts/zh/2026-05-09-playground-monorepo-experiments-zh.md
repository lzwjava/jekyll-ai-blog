---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用游乐场单仓库进行实验
translated: true
type: note
---

问题：我有很多废弃的GitHub仓库，每个仓库的提交数都少于100次。我是否应该使用一个单一的“playground”单体仓库进行实验，然后把成功的项目提升到独立的仓库？

答案：

是的——你的直觉完全正确，这是许多开发者广泛认可的模式。以下是详细解析：

---

## 你描述的问题

你正经历着**“仓库蔓延”**——那些曾经感觉很重要但半途而废的项目墓地。每个项目都有自己的仓库，你在几次提交后失去了动力，现在你的GitHub个人资料里充满了幽灵项目。这非常普遍。

---

## 解决方案：一个`playground`单体仓库

### 这是什么

一个单一的GitHub仓库（例如`yourname/playground`），你将所有实验、技术探索和探索性代码都扔进去——按文件夹组织。这是一个用于所有实验和小项目的单体仓库，也是一个尝试你不曾在大型项目中使用过的新工具的机会。

### 文件夹结构示例

```
playground/
├── experiments/
│   ├── rust-wasm-try/
│   ├── openai-agent-poc/
│   └── svelte-dashboard/
├── snippets/
│   └── useful-utils.ts
└── README.md
```

---

## 升级工作流

这是关键模式——将playground视为一个**孵化器**：

```
playground/feature-folder  →  (被证明有价值？)  →  独立仓库
```

| 阶段 | 位置 | 升级标准 |
| --- | --- | --- |
| 构思/技术验证 | `playground/` 文件夹 | — |
| 增长势头 | 仍在playground中 | 50+次提交，明确的目的 |
| 真正的项目 | 新的独立仓库 | 有用户、文档、CI/CD需求 |

当你准备升级时，可以使用`git subtree split`或`git filter-repo`干净地将一个文件夹的完整历史提取到一个新仓库中。

---

## 为什么这比单独的仓库更好

**特别是对于探索性项目：**

- **更低的摩擦**——无需为了尝试一个想法而建立新仓库、README、许可证、CI。只需创建一个文件夹并编码。
- **一个地方找到所有实验**——而不是40个无人访问的仓库，一个拥有组织良好的文件夹的仓库。
- **共享工具**——所有项目共享一个`.editorconfig`、`prettier`、`eslint`配置。
- 当项目存在于自己的仓库中时，其代码主要被维护者看到。当维护者离开后，代码通常被闲置并开始腐烂，落后于最佳实践和依赖更新。

---

## 何时不使用单体仓库

单体仓库最适合你的项目共享大量代码、需要跨服务原子提交，或者你想要强制使用一致的工具。对于小的、不相关的项目或需要严格访问控制的团队，它可能不太合适。

对于**个人playground**，“不相关项目”的担忧并不重要——重点在于探索，而非生产架构。

---

## Playground仓库的实用技巧

1. **使用清晰的文件夹命名规范**——例如`YYYY-topic`，如`2025-rust-http-server`
2. **每个实验写一行README**——哪怕只是`# 这是什么：尝试用X解决Y`
3. **使用GitHub Topics**——给仓库打上`playground`、`experiments`、`learning`标签
4. **设定升级门槛**——定义你的个人规则，例如：*“如果我回来访问这个项目3次以上，或者有人觉得它有用，就把它变成一个真正的仓库。”*
5. **不要过度设计单体仓库本身**——对于个人探索，你不需要Turborepo或Nx。一个简单的文件夹结构就足够了。

---

## 提取到独立仓库（升级时）

```bash
# 提取子文件夹并保留完整git历史
git filter-repo --subdirectory-filter experiments/my-cool-project
```

这将保留该文件夹的所有提交历史到新仓库——干净且专业。

---

## 总结

你的想法很扎实并且经过了实战检验。Playground仓库充当了一个**低承诺的沙盒**，而升级过程让你的公开仓库保持有意义。停止为想法创建仓库——先创建文件夹，之后再赚取仓库。

参考资料：

- [GitHub Well-Architected: 单体仓库](https://wellarchitected.github.com/library/scenarios/monorepos/)
- [Atlassian: Git中的单体仓库](https://www.atlassian.com/git/tutorials/monorepos)
- [island-is 手册: 单体仓库原理](https://github.com/island-is/handbook/blob/master/monorepo.md)
- [示例: playground单体仓库](https://github.com/Ashishamar99/playground)
