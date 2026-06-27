---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC-EDGAR GPT Deployment
translated: false
type: note
---

Done. Deployed successfully: <https://sec-edgar-gpt.lzwjava.workers.dev>

---

Summary of all changes made this session:

1. **.gitignore** — Added LaTeX intermediate files (*.aux,*.log, *.out,*.toc, *.bbl,*.blg, *.fls,*.fdb_latexmk, *.synctex.gz,*.dvi)

2. **Git pull** — Pulled latest from origin (scripts/, server/, README updates)

3. **Paper (.tex)** — Added GitHub repo + HuggingFace model links as title footnote and new "Code and Model Availability" section

4. **Paper (.tex)** — Cleaned up Figure 2 caption: removed "Training loss curve" prefix, kept Hermes Agent mention

5. **Deleted** paper1.png

6. **PDF regenerated** (xelatex, 2 passes, 19 pages)

7. **Website** — Created `website/index.html` with project overview, key numbers, findings, citation, and links

8. **Cloudflare Worker** — Created `wrangler.toml` + `src/index.js` with inlined HTML (no deps needed). Fixed Worker Sites approach (env.ASSETS not available in Workers), switched to self-contained inline HTML

9. **HuggingFace link** — Changed text from "Model (HuggingFace)" to "HuggingFace"

10. **Deployed** to Cloudflare Workers at <https://sec-edgar-gpt.lzwjava.workers.dev>

All committed and pushed to GitHub.
