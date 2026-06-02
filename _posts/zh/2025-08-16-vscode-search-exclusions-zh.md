---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在VS Code中自定义搜索排除项
translated: true
type: note
---

在 VS Code 中，全局文件搜索会遵循您配置的**搜索排除**规则。您可以设置忽略某些文件或文件夹，使其不会出现在搜索结果中。

以下是主要方法：

---

### 1. 在 **settings.json** 中使用 `search.exclude`

打开设置（`⌘,` / `Ctrl+,` → 右上角“打开设置(JSON)”）并添加：

```json
"search.exclude": {
  "**/node_modules": true,
  "**/dist": true,
  "**/*.log": true
}
```

* 键名采用 [glob 模式](https://code.visualstudio.com/docs/editor/codebasics#_advanced-search-options)
* `true` 表示“从搜索中排除”
* 示例：

  * `**/node_modules` → 所有 node_modules 文件夹
  * `**/*.log` → 任意位置的 .log 文件
  * `**/build/**` → build 文件夹内的所有内容

---

### 2. 使用 `.gitignore`

如果项目包含 `.gitignore` 文件，可设置 VS Code 在搜索时遵循该规则：

```json
"search.useIgnoreFiles": true
```

这样被 Git 忽略的内容就不会出现在搜索结果中。

---

### 3. 使用 `.ignore`

您还可以在项目根目录创建 `.ignore` 文件（格式与 `.gitignore` 相同），专门用于编辑器工具。当启用 `search.useIgnoreFiles` 时，VS Code 会遵循此文件规则。

---

### 4. 在搜索界面快速排除

进行搜索时，将鼠标悬停在结果中的文件/文件夹上，点击**“排除”**按钮。这会临时将该路径添加到设置的 `search.exclude` 中。

---

👉 最常用的配置方案是：

* 在 `.gitignore` 中添加项目全局忽略规则
* 在 `search.exclude` 中添加编辑器特定忽略规则（如 `dist`, `.vscode`）

---

需要我为您演示如何**仅在搜索时排除**文件，同时让这些文件仍显示在资源管理器中？还是需要同时从侧边面板中隐藏这些文件？
