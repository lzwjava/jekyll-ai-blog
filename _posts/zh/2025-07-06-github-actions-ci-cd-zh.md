---
audio: false
generated: true
lang: zh
layout: post
title: GitHub Actions：持续集成与交付的演进
translated: true
type: note
---

GitHub Actions 是一个强大的**持续集成和持续交付（CI/CD）平台**，直接集成在 GitHub 中。它允许开发者自动化软件开发工作流的各个阶段，从构建和测试代码到部署应用程序。

### 发展历程与发布时间

GitHub 本身成立于 **2007 年**，其网站于 **2008 年 4 月**上线。GitHub 平台的开发始于 **2005 年 10 月**，由 Tom Preston-Werner、Chris Wanstrath、P. J. Hyett 和 Scott Chacon 正式推出。

作为特定的 CI/CD 平台，GitHub Actions 于 **2018 年 10 月**首次发布，并于 **2019 年 11 月**正式全面推出。它源自 GitHub 的核心使命，即为开发者提供简化协作和自动化的工具。

### 用户规模

虽然很难获得 GitHub Actions 具体用户的精确实时数据，但值得注意的是，截至 2023 年初，**GitHub 本身拥有超过 1 亿开发者**。鉴于 GitHub Actions 的深度集成以及市场对 CI/CD 日益增长的需求，其中相当大比例的用户都在其项目中运用了这一平台。从初创公司到大型企业，众多行业的开发团队都在使用它。

### 哪些代码库广泛使用 Actions？

GitHub Actions 在单个代码库中定义，通常位于 `.github/workflows` 目录。广泛使用 GitHub Actions 的代码库通常包括：

* **官方 GitHub Actions 代码库：** GitHub 上的 `github/actions` 组织包含许多核心和常用操作，例如 `actions/checkout`、`actions/setup-python`、`actions/setup-node`、`actions/upload-artifact` 和 `actions/download-artifact`。这些是许多工作流的基础。
* **大型开源项目：** 跨多种编程语言（例如 Python、JavaScript、Go、C++）的主要开源项目大量使用 GitHub Actions 来执行构建、测试和发布流程。这类项目通常来自谷歌、微软等科技巨头，以及流行的框架和库。
* **专注于自动化和 DevOps 的项目：** 展示 DevOps 实践、自动化基础设施、测试或部署各个方面的代码库，自然会包含丰富的 GitHub Actions 工作流。
* **热门代码库：** 如今 GitHub 上的许多热门代码库（可在 GitHub 趋势页面找到）通常展示了 GitHub Actions 的创新应用，例如生成内容、运行安全扫描或自动化发布。

本质上，任何受益于自动化流程以提升代码质量、测试、部署或常规代码库管理的项目，都可能拥有完善的 GitHub Actions 工作流集。
