---
audio: false
generated: true
image: false
lang: en
layout: post
title: Microsoft Visio Quick Start Guide
translated: false
type: note
---

**Question:** How do I use Microsoft Visio?

**Answer:**

Visio is a diagramming tool for flowcharts, network diagrams, org charts, UML, etc. Here's the practical rundown:

**Getting started**

- Open Visio → choose a template (flowchart, network, UML, etc.) or blank canvas
- Templates pre-load relevant shape stencils on the left panel

**Core workflow**

1. **Drag shapes** from the left stencil panel onto the canvas
2. **Connect shapes** — hover over a shape edge until you see a blue arrow/dot, then drag to another shape to create a connector
3. **Label shapes/connectors** — double-click any shape or line to type
4. **Format** via right-click → Format Shape, or the ribbon (fill, line color, font)

**Key panels**

- **Shapes panel (left)** — stencil library; search for shapes with the search box
- **Page tabs (bottom)** — multi-page diagrams
- **View → Connection Points** — toggle to see where connectors snap

**Useful shortcuts**

| Action | Shortcut |
|---|---|
| Pan | Hold Ctrl + drag |
| Zoom | Ctrl + scroll |
| Select all | Ctrl + A |
| Duplicate shape | Ctrl + D |
| Auto-connect | Hover shape edge → blue arrow |
| Align/distribute | Home tab → Arrange |

**Import/Export**

- Export: File → Export → PDF, PNG, SVG, or VSDX
- You can also paste Visio diagrams directly into PowerPoint/Word

**Honest take for your workflow:** Given you're terminal-first and building AI tooling, you'd likely get more mileage from **draw.io (diagrams.net)** (free, VS Code extension exists), **Mermaid** (text-to-diagram, embeds in markdown/GitHub), or **D2** (declarative diagramming language). Visio is mainly useful if you're in a corporate environment where `.vsdx` files are the standard exchange format.

If you're stuck with Visio for work, the main thing to know is connectors behave better when you use **glue points** (blue Xs on shapes) rather than floating connections — that's the #1 source of diagrams breaking when you move shapes around.
