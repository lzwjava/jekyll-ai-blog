---
audio: false
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Diagram Tools Beyond Graphviz and NetworkX
translated: false
type: note
---

Great options beyond Graphviz and NetworkX, grouped by how you like to work.

Text/DSL “diagrams as code”
- PlantUML: Full UML (sequence, class, component, deployment), C4 model, activity; huge ecosystem.
- Mermaid: Lightweight Markdown-like syntax; great for flowcharts, sequence, class, ER, state; renders natively on GitHub/GitLab.
- D2 (by Terrastruct): Clean, general-purpose diagram DSL with good auto-layout; supports layers and big diagrams.
- Structurizr (C4): Model-first (C4) with a DSL; exports to PlantUML/Mermaid; good for architecture docs.
- C4-PlantUML: C4 model templates on top of PlantUML.
- nomnoml: Minimal syntax, quick class/relationship sketches.
- Kroki: Server that renders many DSLs (PlantUML, Mermaid, Graphviz) for docs pipelines.

Code-first (generate diagrams from code/IaC)
- diagrams (mingrammer, Python): Programmatic cloud architecture diagrams (AWS/Azure/GCP/K8s).
- Terraform helpers: Inframap (draw from state), Blast Radius (interactive graphs from Terraform).
- AWS CDK: cdk-dia for architecture diagrams from CDK apps.
- Go/TS libs: GoDiagrams (Go), ts-graphviz (TypeScript) for code-based generation.

Web visualization libraries (interactive graphs)
- Cytoscape.js: Large graph visualization, layout algorithms, good performance.
- D3.js: Powerful but lower-level for custom graph/diagram visuals.
- vis-network (vis.js): Easy network graphs with physics.
- Sigma.js: Fast rendering for big graphs.
- ECharts: General charts with graph module; quick results.
- pyvis (Python): Simple interactive network graphs via Vis.js.

GUI diagramming tools (drag-and-drop)
- diagrams.net (draw.io): Free, easy, large stencils (UML, cloud icons).
- yEd/yFiles: Great auto-layout; yFiles is commercial SDK, yEd is free desktop.
- Lucidchart/Miro: Collaborative web tools; good for teams.
- OmniGraffle (macOS), Visual Paradigm, StarUML, Enterprise Architect: UML/architecture tooling.

Architecture-specific and domain tools
- C4 model: Structurizr, C4-PlantUML, Mermaid C4 extensions.
- Cloud architecture SaaS: Cloudcraft (AWS), Hava, Lucidscale, CloudSkew; import from cloud/IaC.
- BPMN/Process: Camunda Modeler, bpmn.io.
- Sequence/timing: WebSequenceDiagrams, WaveDrom (timing diagrams).
- ER/DB diagrams: dbdiagram.io, SchemaSpy.

Quick picks by scenario
- Docs-as-code in Markdown/READMEs: Mermaid.
- Full UML + C4 with templates: PlantUML or Structurizr.
- Cloud architecture from code/IaC: diagrams (Python), Inframap/Blast Radius (Terraform), cdk-dia (AWS CDK).
- Interactive web app graphs: Cytoscape.js or vis-network; for custom viz, D3.js.
- Fast GUI drawing: diagrams.net (draw.io); for auto-layout, yEd.

If you share your preferences (text vs GUI, static images vs interactive, languages you use, and diagram types like sequence/C4/cloud/ER), I can recommend a short list and starter templates.
