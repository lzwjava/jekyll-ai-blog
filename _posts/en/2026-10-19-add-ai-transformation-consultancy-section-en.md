---
audio: false
generated: true
image: false
lang: en
layout: post
title: Add AI Transformation Consultancy Section
translated: false
type: note
---

Done. Added an **AI 转型咨询 (AI Transformation Consultancy)** section to the site.

## What was added

**1. New section `#ai-transform`** (index.html) — placed between the manifesto (`#about`) and the AI app development section, so the flow is: philosophy → analyze → build. It covers:

- **4-step process strip** (new `.steps` components):
  1. 现状诊断 — analyze the current business (processes, data, systems, pain points)
  2. 机会识别 — value × feasibility map of where AI actually pays off
  3. 转型路线图 — phased adoption: 2-week pilots → quarterly scenarios → annual capability
  4. 落地与内化 — pilot, scale, and hand capability to the company's own team
- **6 service cards**: business/process audit, high-value scenario discovery, delivery roadmap with per-phase deliverables, cost & ROI modeling with transparent token prices, team enablement/training, and governance/security/compliance
- A note positioning it as a pre-development engagement (1–2 weeks to a current-state analysis) that hands off to the existing "AI 服务" offering.

**2. Navigation** — added a "转型咨询" link pointing at `#ai-transform` (right after "AI 服务").

**3. Style** (style.css) — new `.steps` grid component (1→2→4 columns responsive, gradient numbers, hover lift, dark-mode support).

**4. i18n.js** — added all 28 new Chinese strings with English translations; verified every one resolves.

**5. README** — documented the new section.

## Verification

- HTML tag balance check: no errors
- `node --check i18n.js`: valid
- Automated translation check: all 28 section strings fully translate to English
- Headless Chrome render: section and all steps present in the DOM, no JS console errors
