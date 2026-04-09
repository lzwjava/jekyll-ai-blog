---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 平衡实验与生产代码库
translated: true
type: note
---

问题：对于仓库 https://github.com/lzwjava/blog-source 和 https://github.com/lzwjava/ww，如果从一开始就正确分离（将大型脚本分离到独立仓库），你还会有后来的迁移需求吗？如何平衡游乐场/实验性项目与面向公众使用的外部开源项目？

回答：

是的，你说得完全正确。如果你从一开始就通过恰当关注点分离来合理组织代码，那么后来就不需要进行迁移了。这是软件开发中的常见挑战：关于代码组织的初始决策能够显著节省后续重构的工作量。

## 为何初始合理分离很重要

良好的项目组织能将返工需求降至最低并减少项目延误。当你以清晰的架构开始时，就能避免因混杂不同类型代码而产生的技术债务。建议从一开始就建立标准并采用良好实践，以减少代码编写与实现方式的不一致性。

此处的核心原则在于提前考虑可扩展性。你应始终将可扩展性作为设计文件夹结构时的考量前提，可以采用分层结构、命名空间和基于功能分区的实践方法。

## 平衡游乐场项目与生产项目

这是真正的挑战所在。以下是几种策略性方法：

**基于意图从第一天起进行分离**

开发、测试和生产环境应当相互隔离，这样既能将实验和变更控制在安全空间，又能将生产环境视为特殊且受保护的区域。对代码仓库也应采用相同原则：

- **游乐场仓库**：用于实验性探索、学习和快速迭代，无需担心破坏性变更
- **生产仓库**：用于存放稳定、文档完善、经过充分测试且面向公众使用的代码

**考虑变更频率**

最需要问的问题是：组件需要多频繁地协同变更？如果组件真正独立且通过稳定版本化API进行交互，那么多仓库模式就能良好运作。

就你的情况而言，如果`ww`中的脚本是与博客内容独立演进的实用工具，它们从一开始就应该放在独立仓库中。

**建立清晰边界和文档**

你应该建立一组预期规范，明确项目各部分存放位置及各部分的衔接顺序。秉持你的工作将被他人共享和复现的心态进行处理。

对于游乐场项目，应在README中明确标注其为实验性项目。对于生产项目，则需保持全面文档、版本管理和稳定性保证。

## 实用策略

以下是一种平衡方法：

1. **始于明确意图**：提前决定某事物是实验性还是面向公众使用
2. **采用仓库命名规范**：为非生产仓库考虑添加`playground-*`或`experimental-*`前缀
3. **早期模块化**：将代码分解为模块和函数，使其逻辑保持独立性，让代码更可重用、有条理且易于管理
4. **规划升级路径**：制定明确的路径，在实验代码成熟时将其迁移至生产仓库
5. **避免早期过度设计**：对于真正的实验性工作，可以初始阶段保持简洁，但要明确在公开前需要进行重构

你从`blog-source`到`ww`的迁移本可通过这种前瞻性思考来避免。不过，这是许多开发者都会经历的学习过程。现在投入学习代码组织的时间将有助于优化未来项目，并在各项目间建立一致性。

参考文献：

- https://kodus.io/en/monorepo-vs-multi-repo-strategy/
- https://www.thoughtworks.com/insights/blog/agile-engineering-practices/monorepo-vs-multirepo
- https://www.iteratorshq.com/blog/a-comprehensive-guide-on-project-folder-organization/
- https://www.c-sharpcorner.com/article/common-software-engineering-practices-for-production-code/
- https://mitcommlab.mit.edu/broad/commkit/file-structure/
- https://iseoblue.com/iso-27001/annex-a/control-8-31/