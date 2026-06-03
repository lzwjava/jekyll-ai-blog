---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choosing Between CLI and HTML GUI Tools
translated: false
type: note
---

Question: Should I build a CLI tool as a self-contained HTML GUI instead, especially for non-engineer users? When does the GUI tradeoff make sense?

Answer:

**Short take:** CLI is your native habitat and ships faster. HTML GUI unlocks a different market (non-engineers), but only build it if that market is actually worth serving. Don't optimize for "everyone" — optimize for your core user first.

**When CLI is the right call:**
- You (engineer) use it daily
- Your users are engineers/terminal-native
- Iteration speed matters more than polish
- Integration with other tools (pipes, scripts, containers) is a feature

You ship faster, maintain less surface area, and stay in flow.

**When HTML GUI makes sense:**
- Non-engineers need to use it (accountants, ops, PMs)
- The tool solves a business problem with repeating users
- You have adoption goals beyond yourself
- The domain naturally maps to visual interaction (data exploration, dashboards)

Examples: duckdb *could* have an HTML GUI for SQL exploration, but engineers prefer `duckdb file.db` in the terminal. Excel handling in Python benefits from a GUI because end-users aren't running Python.

**The practical hybrid:**

Don't build CLI *then* GUI. Build the **library/daemon** first, then wrap it:

```python
# Core logic as a library
# mylib/processor.py
class DataProcessor:
    def process(self, data, config):
        # actual work
        return result
```

**Then:** Two thin layers on top:

1. **CLI wrapper** (20 lines of Click/Typer):
```bash
myapp process --input data.csv --output result.json
```

2. **HTML GUI** (self-contained, ~300-500 lines of HTML/JS):
```html
<!-- index.html -->
<input type="file" id="upload">
<button onclick="processLocal()">Process</button>
<script>
async function processLocal() {
  // Call WASM or fetch to local Python server
  // Display results in table
}
</script>
```

**For "sheer-excel" style spreadsheet handling:**

If you want non-engineers to manipulate tabular data visually, use **[SheetJS](https://sheetjs.com/)** (or libre office.js) + a simple HTML wrapper:

```html
<input type="file" id="excel" accept=".xlsx">
<table id="grid"></table>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.min.js"></script>
<script>
document.getElementById('excel').onchange = (e) => {
  const file = e.target.files[0];
  const workbook = XLSX.read(file, {type: 'array'});
  const data = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]]);
  // Render to table, allow editing, export back
};
</script>
```

This is **self-contained** (one .html file + SheetJS CDN), works offline-ish, and non-engineers can use it.

**Your actual decision:**

- **If you're the user and your collaborators are engineers:** CLI all day. Ship in days, not weeks.
- **If you want to sell/distribute widely:** HTML GUI for onboarding, CLI for power users. Build library first, both wrappers second.
- **If you want to stay AI-native:** Build the core as a Python library that LLM agents can call directly, then wrap UI later if revenue demands it.

Given your profile (ship fast, deeply technical, terminal-first), I'd bet you get more compounding value out of 10 polished CLI tools than 1 overengineered GUI. Ship the CLI, use it in your own workflows, and add the GUI only if non-engineers actually show up.

What's the tool, and who are the actual users?
