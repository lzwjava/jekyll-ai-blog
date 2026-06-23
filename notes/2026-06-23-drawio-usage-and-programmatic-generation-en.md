---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Draw.io: Usage and Programmatic Generation"
translated: false
type: note
---

**Question:** What is draw.io (diagrams.net) and how do I use it effectively?

**Answer:**

draw.io is a free, open-source diagramming tool. You care about it because it has a VS Code extension, exports to clean SVG/XML, and the `.drawio` format is just XML — meaning you can generate or diff diagrams programmatically.

**Ways to run it**

```bash
# VS Code extension (best for your workflow)
code --install-extension hediet.vscode-drawio

# Desktop app
brew install --cask drawio

# Web (no install)
# https://app.diagrams.net
```

**Core concepts**

- **File format**: `.drawio` or `.drawio.svg` — pure XML, git-diffable, can be embedded in markdown on GitHub and renders inline
- **Stencil libraries**: shapes are loaded per-diagram-type (flowchart, UML, network, AWS, k8s, etc.)
- **Layers**: like Figma layers — group and lock elements per layer
- **Connectors**: edge routing is automatic but fully overridable; connectors "glue" to shape ports

**VS Code workflow (your setup)**

The `hediet.vscode-drawio` extension lets you edit `.drawio` files visually inside VS Code, or switch to XML mode (`Ctrl+Shift+P` → "Draw.io: Edit Diagram XML"). This is the power move — you can write/generate the XML directly.

**Programmatic diagram generation**

Since `.drawio` is XML, you can generate diagrams from code:

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

**Export options**

```bash
# CLI export (requires desktop app or drawio-cli)
drawio --export --format svg --output out.svg diagram.drawio
drawio --export --format png --scale 2 --output out.png diagram.drawio
```

**Mermaid vs draw.io — when to use which**

| | Mermaid | draw.io |
|---|---|---|
| Version control | ✅ text diff | ✅ XML diff |
| GitHub render | ✅ native in .md | ✅ with .drawio.svg |
| Layout control | ❌ auto only | ✅ full manual |
| Programmatic gen | ✅ easy string concat | ✅ XML gen |
| Complex diagrams | ❌ gets messy | ✅ |
| Embed in docs | ✅ | ✅ |

**For your use case** — generating architecture diagrams for AI systems, agent pipelines, or model training flows — the programmatic XML generation approach above scales well. You can write a Python script that takes your system topology and emits a `.drawio` file, which then renders perfectly in VS Code or exports to SVG for your blog.
