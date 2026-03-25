---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模块化软件代码仓库的优势
translated: true
type: note
---

Question: 是否有必要将 software projects 组织成独立的 repositories 或模块化结构（类似于 microservices），而不是全部保存在一个 monolithic repository 中？

Answer:

是的，将 software 组织成独立的 repositories 或模块化组件（类似于 microservices 方法）非常重要，原因如下：

1. **Maintainability**：更小、更专注的 repositories 更易于维护。当代码是模块化的，你可以更新或修复一部分，而不会冒着对无关部分产生副作用的风险。

2. **Reusability**：分离通用脚本或 modules 允许你在不同项目中复用它们，而无需复制大量无关代码。

3. **Collaboration**：当多名 developers 协作时，更小的 repositories 可以减少 merge conflicts，并使 code reviews 更易于管理。Monolithic repositories 可能会成为瓶颈。

4. **Distribution**：如果你想共享或开源特定的功能，模块化的 repository 使提供简洁的 interface 变得更加简单，而不会暴露个人脚本或无关文件。

5. **Automated Workflows**：通过模块化项目，CI/CD pipelines、GitHub Actions 或自动化 workflows 可以针对单个 modules，从而提高 build times、test coverage 和 deployment 效率。

6. **Scalability**：随着项目增长，monolithic repositories 变得难以扩展。Microservices 或模块化结构允许团队独立扩展，每个 module 按照自己的节奏演进。

7. **Focus and Clarity**：用户或贡献者可以快速理解一个小 repository 的用途，而一个大型混合 repository 则难以导航。

在你的例子中，将 `blog-source` 脚本（个人与通用分离）并为 translation、PDF generation 或 audio output (`ww`) 等功能使用专用 repo 是完全正确的方法。这反映了良好的 software engineering 实践：清晰的边界、模块化和可维护的 workflows。

从本质上讲，无论是 software programming、个人项目还是服务，**模块化和组织性都能节省时间、减少错误，并使未来的扩展或共享变得更加容易**。

References:

* [Microservices vs Monolithic Architecture](https://martinfowler.com/articles/microservices.html)
* [GitHub Monorepo vs Multi-repo Strategies](https://docs.github.com/en/repositories/organizing-your-repository/managing-large-projects-with-multiple-repositories)
* [Software Modularity and Maintainability](https://stackify.com/software-modularity-best-practices/)