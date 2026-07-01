---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Draw.io：使用与程序化生成
translated: true
type: note
---

**问题：** 什么是 draw.io (diagrams.net)？如何高效使用它？

**答案：**

draw.io 是一款免费的开源图表绘制工具。你之所以关注它，是因为它拥有 VS Code 扩展、能导出干净的 SVG/XML，且 `.drawio` 格式本质就是 XML——这意味着你可以通过编程方式生成或对比图表。

**运行方式**

```bash
# VS Code 扩展（最适合你的工作流）
code --install-extension hediet.vscode-drawio

# 桌面应用
brew install --cask drawio

# 网页版（无需安装）
# https://app.diagrams.net
```

**核心概念**

- **文件格式**：`.drawio` 或 `.drawio.svg`——纯 XML，可 git diff，能在 GitHub 上的 markdown 中嵌入并直接渲染
- **模板库**：按图表类型加载形状（流程图、UML、网络图、AWS、k8s 等）
- **图层**：类似 Figma 图层——可按图层分组和锁定元素
- **连接器**：边缘路由自动完成但完全可覆盖；连接器会“粘合”到形状端口

**VS Code 工作流（你的配置）**

`hediet.vscode-drawio` 扩展允许你在 VS Code 内以可视方式编辑 `.drawio` 文件，或切换至 XML 模式（`Ctrl+Shift+P` → “Draw.io: Edit Diagram XML”）。这是强大之处——你可以直接编写/生成 XML。

**编程式图表生成**

由于 `.drawio` 是 XML，你可以通过代码生成图表：

```python
def make_flowchart(nodes: list[dict], edges: list[tuple]) -> str:
    cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']

    for i, node in enumerate(nodes):
        nid = i + 2
        cells.append(
            f'<mxCell id="{nid}" value="{node["label"]}" '
            f'style="rounded=1;" vertex="1" parent="1">'
            f'<mxGeometry x="{node.get("x", 100)}" y="{node.get("y", i*80)}" '
            f'width="120" height="40" as="geometry"/></mxCell>'
        )

    for i, (src, dst) in enumerate(edges):
        eid = len(nodes) + 2 + i
        cells.append(
            f'<mxCell id="{eid}" edge="1" source="{src+2}" target="{dst+2}" parent="1">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    inner = "\n".join(cells)
    return f'''<mxGraphModel><root>{inner}</root></mxGraphModel>'''

xml = make_flowchart(
    nodes=[{"label": "Input"}, {"label": "Process"}, {"label": "Output"}],
    edges=[(0,1), (1,2)]
)
with open("diagram.drawio", "w") as f:
    f.write(xml)
```

**导出选项**

```bash
# CLI 导出（需要桌面应用或 drawio-cli）
drawio --export --format svg --output out.svg diagram.drawio
drawio --export --format png --scale 2 --output out.png diagram.drawio
```

**Mermaid vs draw.io —— 何时使用哪种**

| | Mermaid | draw.io |
| --- | --- | --- |
| 版本控制 | ✅ 文本差异 | ✅ XML 差异 |
| GitHub 渲染 | ✅ 在 .md 中原生支持 | ✅ 使用 .drawio.svg |
| 布局控制 | ❌ 仅自动 | ✅ 全手动 |
| 编程式生成 | ✅ 简单字符串拼接 | ✅ XML 生成 |
| 复杂图表 | ❌ 变得混乱 | ✅ |
| 嵌入文档 | ✅ | ✅ |

**针对你的用例** —— 生成 AI 系统架构图、智能体管道或模型训练流程 —— 上述编程式 XML 生成方法扩展性很好。你可以编写一个 Python 脚本，接收系统拓扑并生成 `.drawio` 文件，然后在 VS Code 中完美渲染，或导出为 SVG 用于你的博客。
