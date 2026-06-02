---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 轻松将Markdown转换为幻灯片
translated: true
type: note
---

Marp CLI 能够将 Markdown 文件转换为幻灯片（HTML、PDF、PPTX）。如果你想用纯 Markdown 编写演示文稿并尽量减少格式调整，这个工具特别实用。

以下是详细操作指南：

---

### 1. 安装 Marp CLI

需要先安装 Node.js。

```bash
npm install -g @marp-team/marp-cli
```

验证安装：

```bash
marp --version
```

---

### 2. 编写 Markdown 演示文稿

创建文件，例如 `slides.md`。

```markdown
---
marp: true
theme: default
paginate: true
---

# 你好，Marp！

---

## 第二页幻灯片

- 项目符号 1
- 项目符号 2
```

关键要点：

* `---`（YAML 前置元数据）用于启用 Marp 和配置
* `---`（内容之间的分隔符）用于划分幻灯片

---

### 3. 在浏览器中预览

启动带自动重载的本地服务器：

```bash
marp -p slides.md
```

在浏览器中打开 [http://localhost:8080](http://localhost:8080)。

---

### 4. 导出幻灯片

生成不同格式：

* HTML（独立文件）：

  ```bash
  marp slides.md -o slides.html
  ```

* PDF：

  ```bash
  marp slides.md -o slides.pdf
  ```

* PowerPoint（PPTX）：

  ```bash
  marp slides.md -o slides.pptx
  ```

---

### 5. 实用选项

* **监听文件变更**（自动重建）：

  ```bash
  marp -w slides.md
  ```

* **设置主题**（default、gaia、uncover 或自定义 CSS）：

  ```bash
  marp --theme-set ./my-theme.css slides.md -o slides.html
  ```

* **添加演讲者注释**：

  ```markdown
  ---
  marp: true
  ---

  # 标题

  <!--
  这是演讲者注释
  -->
  ```

---

### 6. 编辑器集成

* VSCode 提供 [Marp 扩展](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
* 可在编辑 Markdown 时实时预览幻灯片

---

👉 通过以上配置，你可以在几分钟内从纯 `.md` 文件生成精美的演示文稿。

需要我为你提供**可直接使用的 Markdown 模板文件**（包含标题页、议程页、内容页和结束页）吗？这样你就能立即开始创作。
