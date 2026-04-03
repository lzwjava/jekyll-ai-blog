---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Jenkins构建中清理node_modules目录
translated: true
type: note
---

**问题：** 在同一 Jenkins 构建节点上，如果 npm 包的 `node_modules` 在多次构建之间持续存在，我们需要清理它们吗？保留它们可能会导致不同构建之间的依赖冲突，从而引发错误——这种说法正确吗？

**回答：**

## 是的——但这比简单的“总要清理”更为微妙

您的担忧**在原则上是有效且正确的**。同一 Jenkins 构建节点上共享的、残留的 `node_modules` 绝对可能导致跨构建污染。但是，是否*必须*删除它们取决于您的 npm 版本和工作流程。以下是完整的分析：

---

## 为什么残留的 `node_modules` 可能导致问题

1. **过时/孤立的包** — 如果之前的构建安装了某些包，而这些包已不在 `package.json` 中，它们会静默地保留在 `node_modules` 里。新的构建可能会意外地使用它们。
2. **分支之间的版本冲突** — 分支 A 可能使用 `lodash@4.x`，分支 B 使用 `lodash@3.x`。如果同一个工作空间/节点在没有清理的情况下被重复使用，错误的版本可能会残留。
3. **损坏的安装** — 如果之前的构建在安装过程中崩溃，`node_modules` 可能处于损坏/不完整的状态。
4. **不可复现的构建** — 构建依赖于隐藏的本地状态，而不是 `package.json` 中声明的依赖，这使得调试极其困难。

---

## npm 的自动处理机制（现代 npm ≥ v3）

从 npm 3 开始，npm 会在 `package-lock.json` 中跟踪已解析的依赖项，确保无论 `node_modules` 的先前状态如何，都使用相同的依赖版本。此外，`npm install` 会删除不在 `package.json` / `package-lock.json` 中的包，因此不再需要的先前构建的包会被自动移除。

这意味着**现代 `npm install` 能处理许多情况**——但它不能防止：
- 手动篡改 `node_modules`
- 损坏的构建中间状态
- 平台特定的二进制文件过时（例如，原生插件）
- 多个不同项目共享相同的工作目录

---

## 推荐策略

### ✅ 选项 1：每次构建前完全清理（最安全，最慢）
在每次构建前完全删除 `node_modules`，以确保可复现性：

```bash
rm -rf node_modules
npm install
```

在 Jenkinsfile 中：
```groovy
stage('Install') {
    steps {
        sh 'rm -rf node_modules'
        sh 'npm install'
    }
}
```

### ✅ 选项 2：使用 `npm ci` 替代 `npm install`（CI 最佳实践）
`npm ci` 专为 CI 环境设计 — 它**总是会删除 `node_modules` 并根据 `package-lock.json` 重新安装**：

```bash
npm ci
```

这是**推荐的 CI 方法**，因为它：
- 确保每次都是全新安装
- 在许多情况下比 `rm -rf node_modules && npm install` 更快
- 严格遵循 `package-lock.json`

### ✅ 选项 3：使用 `npm prune`（更轻量的清理）
如果您需要速度并且只需要移除孤立的包：

```bash
npm prune
npm install
```

`npm prune` 会移除多余的包 — 即那些存在于 `node_modules` 但未列为任何包的依赖的包。当使用 `--production` 标志时，它也可以移除 `devDependencies`。

### ✅ 选项 4：Jenkins 工作空间清理插件
您可以使用 Jenkins 工作空间清理插件在构建前后清理工作空间。例如，您可以清理所有内容但排除 `node_modules`，如果您想为未来的构建缓存它；或者包含它以确保干净的状态。

在构建前清理的 Jenkinsfile 示例：
```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                cleanWs()       // 清空工作空间
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'npm ci'     // 始终全新安装
                sh 'npm run build'
            }
        }
    }
    post {
        always {
            cleanWs(deleteDirs: true, notFailBuild: true)
        }
    }
}
```

---

## 总结表格

| 策略 | 清理程度？ | 速度 | 安全性 |
|---|---|---|---|
| `npm install`（复用 node_modules） | 否 | 快 | 中等（npm 3+ 处理大部分情况） |
| `npm prune` + `npm install` | 部分 | 中等 | 良好 |
| `rm -rf node_modules` + `npm install` | 完全 | 慢 | 最佳 |
| `npm ci` | 完全（自动） | 中等-快 | CI 最佳 |
| Jenkins `cleanWs()` | 整个工作空间 | 最慢 | 最佳 |

**TL;DR：** 在 Jenkins 流水线中使用 **`npm ci`** — 它正是为此用例设计的，并能消除您所描述的跨构建污染问题，而无需您手动管理 `node_modules` 的清理。

---

**参考资料：**

- [Jenkins 工作空间清理插件](https://plugins.jenkins.io/ws-cleanup/)
- [自动清理 Jenkins 工作空间](https://computingpost.medium.com/automatically-clean-up-jenkins-workspace-after-builds-complete-d3f29f230a5f)
- [在构建服务器的构建之前是否有必要删除 node_modules？](https://software.codidact.com/posts/280097)
- [如何清理 node_modules](https://medium.com/@mariokandut/how-to-clean-up-node-modules-41a5)