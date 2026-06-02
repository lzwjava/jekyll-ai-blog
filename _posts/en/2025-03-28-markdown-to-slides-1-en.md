---
audio: false
generated: true
image: false
lang: en
layout: post
title: Markdown to Slides Made Easy
translated: false
type: note
---

Marp CLI lets you turn Markdown files into slides (HTML, PDF, PPTX). It’s especially useful if you want to write presentations in plain Markdown with minimal formatting effort.

Here’s a step-by-step guide:

---

### 1. Install Marp CLI

You need Node.js first.

```bash
npm install -g @marp-team/marp-cli
```

Check installation:

```bash
marp --version
```

---

### 2. Write a Markdown Presentation

Create a file, for example `slides.md`.

```markdown
---
marp: true
theme: default
paginate: true
---

# Hello, Marp!

---

## Slide 2

- Bullet 1
- Bullet 2
```

Key points:

* `---` (YAML frontmatter) enables Marp and config.
* `---` (between content) separates slides.

---

### 3. Preview in Browser

Run a local server with auto-reload:

```bash
marp -p slides.md
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

---

### 4. Export Slides

Generate different formats:

* HTML (self-contained):

  ```bash
  marp slides.md -o slides.html
  ```

* PDF:

  ```bash
  marp slides.md -o slides.pdf
  ```

* PowerPoint (PPTX):

  ```bash
  marp slides.md -o slides.pptx
  ```

---

### 5. Useful Options

* **Watch for changes** (auto rebuild):

  ```bash
  marp -w slides.md
  ```

* **Set theme** (default, gaia, uncover, or your custom CSS):

  ```bash
  marp --theme-set ./my-theme.css slides.md -o slides.html
  ```

* **Include speaker notes**:

  ```markdown
  ---
  marp: true
  ---

  # Title

  <!--
  These are speaker notes
  -->
  ```

---

### 6. Editor Integration

* VSCode has a [Marp extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode).
* It shows live previews while editing Markdown.

---

👉 With this setup, you can go from a plain `.md` file to a polished presentation in minutes.

Do you want me to give you a **ready-to-use template Markdown file** (with title slide, agenda, content, and closing slide) so you can start right away?
