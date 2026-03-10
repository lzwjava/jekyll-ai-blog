---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在本地分叉并修改 NPM 包
translated: true
type: note
---

我会搜索关于 forking 和修改 npm 包的最佳实践。现在让我搜索更多关于 npm link 和 path overrides 的具体信息。---

**问题：** 如何 fork 一个像 form-data 这样的 NPM 包，手动编辑其代码以调试、添加功能或修复 bug？可以使用 path overrides 来实现吗？

**回答：**

有几种方法可以在本地 fork 和修改 NPM 包。以下是主要方法：

## 方法 1：使用 npm link（符号链接方法）

npm link 命令会在你的本地包和依赖它的项目之间创建符号链接。这是开发过程中测试更改的最快方式。

**步骤：**

1. **克隆仓库**：首先 fork 你想要修改的包的仓库，然后克隆该 fork。

   ```bash
   git clone https://github.com/your-username/form-data.git
   cd form-data
   ```

2. **安装依赖并构建**：
   ```bash
   npm install
   npm run build  # 检查 package.json 中的 build 脚本
   ```

3. **在包目录中创建全局链接**：
   ```bash
   npm link
   ```

4. **链接到你的项目**：在你的主项目目录中：
   ```bash
   npm link form-data
   ```

5. **进行更改**：编辑 fork 包中的代码并立即测试。

6. **完成后清理**：
   ```bash
   npm unlink form-data      # 在你的主项目中
   npm unlink                 # 在包目录中
   ```

## 方法 2：在 package.json 中直接使用路径覆盖

你可以使用相对路径直接指向本地文件夹：

```json
{
  "dependencies": {
    "form-data": "file:../path-to-local-form-data"
  }
}
```

然后运行：
```bash
npm install
```

这会在 node_modules 中创建到实际文件夹的链接，并节省每次更改后打包和安装的额外步骤。

## 方法 3：带有分支指针的 GitHub URL

不要使用库 fork 的 github URL，而是包含你正在处理的分支，例如：yarn upgrade form-data@https://github.com/yourname/form-data.git#your-branch-name。

在 package.json 中：
```json
{
  "dependencies": {
    "form-data": "yourname/form-data#feature-branch"
  }
}
```

## 方法 4：GitHub Tarball URL

你可以使用带有特定 commit hash 的 tarball 链接，将 package.json 指向 GitHub 上你的 fork 的下载 URL：

```json
{
  "dependencies": {
    "form-data": "https://github.com/yourname/form-data/tarball/abc123def456"
  }
}
```

## 方法 5：npm pack（最适合发布前测试）

你可以使用 npm pack 作为 symlinks 的替代方案，它会创建一个 .tgz 文件，并提供测试本地组件的绝佳方法，因为它模拟了实际发布到 npm 的过程。

```bash
cd form-data
npm run build
npm pack
cd ../your-project
npm install ../form-data/form-data-1.0.0.tgz
```

## 方法 6：在 Git 中构建文件

为了确保包正常工作，fork 仓库中的所有构建文件在构建后不得从源控制中隐藏。通常运行 npm run build 命令就足够了，你需要从 .gitignore 中移除构建输出目录。

## 重要注意事项

- 确保检查你想要修改的库的许可，并通过查看 readme 或 package.json 脚本熟悉构建库的过程。

- 当你链接一个包时，它不会自动链接其依赖。如果你的包依赖于项目中未安装的内容，你可能需要在链接的包目录中运行 npm install。

- 在运行 npm link 命令时，会考虑当前使用的 node 版本。如果你想在不同的 node 环境中测试库，需要为每个 node 版本重复该过程。

---

**参考资料：**

- https://schalkneethling.com/posts/using-npm-link-for-local-package-development/
- https://medium.com/@ruben.alapont/npm-link-developing-and-testing-local-npm-packages-b50a32b50c4a
- https://teambrookvale.com.au/articles/modifying-npm-packages-the-right-way
- https://www.pluralsight.com/resources/blog/guides/how-to-use-forked-npm-dependencies
- https://medium.com/@chrisdmasters/how-to-fork-a-dependency-and-use-it-locally-in-a-project-707c80d3449c
- https://dev.to/one-beyond/different-approaches-to-testing-your-own-packages-locally-npm-link-4hoj
- https://maecapozzi.com/blog/how-to-locally-test-an-npm-package
- https://dev.to/azophy/how-to-edit-replace-npm-package-dependency-1b5e
- https://nickconfrey.medium.com/how-to-edit-a-node-module-locally-1cb8d3530d78
- http://debuggable.com/posts/how-to-fork-patch-npm-modules:4e2eb9f3-e584-44be-b1a9-3db7cbdd56cb