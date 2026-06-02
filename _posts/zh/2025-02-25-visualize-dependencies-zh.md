---
audio: false
generated: true
lang: zh
layout: post
title: 可视化依赖关系
translated: true
type: note
---

要可视化由提供的 Python 脚本生成的 Maven 依赖关系图，您可以使用 **Graphviz**，这是一个广泛使用且简单的图形工具，可以渲染以 DOT 语言描述的图。该脚本以 DOT 格式输出依赖关系图，将 Maven 项目中模块间的依赖关系表示为有向图，其中节点由 `artifactId` 标记，边显示依赖关系。以下是使用 Graphviz 绘制和可视化此图的步骤，如果您偏好其他选项，也会提及替代工具如 Polyglot 或其他工具。

---

### 使用 Graphviz（推荐方法）

Graphviz 在这里很理想，因为脚本直接生成 DOT 格式输出，而 Graphviz 原生支持此格式。请按照以下步骤操作：

1. **运行脚本**
   执行 Python 脚本，提供 Maven 项目的根目录作为参数。这将生成依赖关系图的 DOT 输出。

   ```bash
   python script.py /path/to/maven/project
   ```

2. **将 DOT 输出保存到文件**
   将脚本的输出重定向到一个文件，例如 `dependencies.dot`。该文件将包含 DOT 格式的图描述。

   ```bash
   python script.py /path/to/maven/project > dependencies.dot
   ```

3. **安装 Graphviz（如果尚未安装）**
   Graphviz 可用于 Windows、macOS 和 Linux。使用您的包管理器安装它：
   - **Ubuntu/Debian**：

     ```bash
     sudo apt-get install graphviz
     ```

   - **macOS（使用 Homebrew）**：

     ```bash
     brew install graphviz
     ```

   - **Windows**：从 [Graphviz 网站](https://graphviz.org/download/) 下载并安装。

4. **生成可视化图像**
   使用 Graphviz 的 `dot` 命令将 DOT 文件转换为图像。例如，要创建 PNG 文件：

   ```bash
   dot -Tpng dependencies.dot -o dependencies.png
   ```

   - 您可以根据偏好将 `-Tpng` 替换为其他格式，如用于 SVG 的 `-Tsvg` 或用于 PDF 的 `-Tpdf`。

5. **查看图**
   使用任何图像查看器打开生成的 `dependencies.png` 文件，查看依赖关系图。每个节点将代表一个模块的 `artifactId`，箭头将指示模块间的依赖关系。

---

### 替代工具

如果您不想使用 Graphviz 或想探索其他常见的图形工具，以下是一些选项：

#### Polyglot Notebooks（例如，使用 Jupyter）

Polyglot Notebooks 不直接可视化 DOT 文件，但您可以在 Jupyter notebook 环境中集成 Graphviz：

- **步骤**：
  1. 安装 Graphviz 和 `graphviz` Python 包：

     ```bash
     pip install graphviz
     sudo apt-get install graphviz  # 对于 Ubuntu，请根据您的操作系统调整
     ```

  2. 修改脚本以使用 Python 的 `graphviz` 库而不是打印原始 DOT。在脚本末尾添加以下内容：

     ```python
     from graphviz import Digraph

     dot = Digraph()
     for from_module, to_module in sorted(dependencies):
         dot.edge(from_module, to_module)
     dot.render('dependencies', format='png', view=True)
     ```

  3. 运行修改后的脚本，直接生成并显示 `dependencies.png`。
- **注意**：这仍然依赖于底层的 Graphviz，因此不是一个完全独立的工具。

#### Gephi

Gephi 是一个开源的网络可视化工具，可以导入 DOT 文件：

- **步骤**：
  1. 从 [gephi.org](https://gephi.org/) 下载并安装 Gephi。
  2. 运行脚本并将 DOT 输出保存到 `dependencies.dot`。
  3. 打开 Gephi，转到 `文件 > 导入 > 图文件`，然后选择 `dependencies.dot`。
  4. 调整布局（例如 ForceAtlas 2）并进行交互式可视化。
- **优点**：适用于具有高级布局选项的大型图。
- **缺点**：需要手动导入和设置。

#### 在线 Graphviz 工具

对于快速、无需安装的选项：

- **步骤**：
  1. 运行脚本并复制 DOT 输出（从 `digraph G {` 到 `}`）。
  2. 访问在线工具，如 [GraphvizOnline](https://dreampuf.github.io/GraphvizOnline/)。
  3. 粘贴 DOT 内容并点击渲染图。
- **优点**：无需安装。
- **缺点**：需要互联网访问；对输出格式的控制较少。

#### yEd

yEd 是一个免费的图编辑器，但它不原生支持 DOT：

- **步骤**：
  1. 使用诸如 `dot` 之类的工具将 DOT 文件转换为 GraphML 或其他支持的格式（例如，`dot -Tgraphml dependencies.dot -o dependencies.graphml`）。
  2. 打开 yEd，导入 GraphML 文件，并调整布局。
- **缺点**：需要额外的转换步骤。

---

### 为什么 Graphviz 在这里是最佳选择

脚本的输出专为 DOT 定制，使得 Graphviz 成为最直接和高效的选择。它轻量级、命令行驱动且广泛支持。生成的图将大致如下所示（概念上）：

- 节点：每个模块的 `artifactId`（例如 `"module-a"`、`"module-b"`）。
- 边：箭头如 `"module-a" -> "module-b"`，显示 `module-a` 依赖于 `module-b`。

如果您的图很大，您可以使用 Graphviz 选项调整布局（例如，使用 `dot -Kneato` 进行不同的排列），但上述基本步骤应该足够。

---

### 最终建议

要可视化脚本中的 Maven 依赖关系图：

1. 运行：`python script.py /path/to/maven/project > dependencies.dot`
2. 如果需要，安装 Graphviz。
3. 转换为图像：`dot -Tpng dependencies.dot -o dependencies.png`
4. 打开 `dependencies.png` 查看您的图。

这种方法简单，使用常见工具（Graphviz），并且与脚本的输出完美对齐。如果您需要交互性或替代格式，请尝试 Gephi 或在线工具。
