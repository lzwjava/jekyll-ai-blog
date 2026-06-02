---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Git 行尾控制指南
translated: true
type: note
---

`git config core.autocrlf` 控制 Git 在检出仓库文件及提交回仓库时如何处理行尾符。这个问题很重要，因为 Windows 使用 **CRLF** (`\r\n`) 作为行尾符，而 Linux 和 macOS 使用 **LF** (`\n`)。若不加以处理，文件格式可能会因编辑者不同而不断变化，导致出现“不干净”的差异对比和不必要的更改。

---

### 工作原理

* **检出（读取）** 文件时，Git 可能会转换行尾符以匹配您操作系统的惯例（这样在编辑器中看起来更自然）。
* **提交（写入）** 文件时，Git 可能会将行尾符转换回 LF（代码仓库中的跨平台标准）。

---

### 设置选项

通过以下命令进行设置：

```bash
git config --global core.autocrlf <value>
```

常用取值：

* `true`
  检出时将 **LF → CRLF**，提交时将 **CRLF → LF**。
  最适合使用 Windows 编辑器编写代码的 **Windows 开发者**。

* `input`
  检出时**不**修改文件，但提交时将 **CRLF → LF**。
  最适合 **Linux/macOS 开发者**，可确保仓库中仅包含 LF 行尾符。

* `false`
  完全不进行转换。Git 按原样存储和检出文件。
  最适合团队/编辑器能一致处理行尾符的情况。

---

### 典型建议

* **Windows**：

  ```bash
  git config --global core.autocrlf true
  ```
* **Linux/macOS**：

  ```bash
  git config --global core.autocrlf input
  ```

对于混合团队，建议在仓库中添加 `.gitattributes` 文件来强制保持行尾符一致性，例如：

```
* text=auto
```

---

需要我为您展示一个适用于跨平台团队的推荐 **`.gitattributes` 配置**吗（这样就不必仅依赖 `core.autocrlf`）？
