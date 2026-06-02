---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimal Parent Directory AI Start
translated: false
type: note
---

Question: When working across multiple projects, is it better to start Claude or Copilot in the parent directory so it can more easily reference files across the projects?

Answer:

Yes, starting Claude or Copilot from the **parent directory** is generally better when you need to work across multiple projects. Here's why:

1. **Wider context**:

   * Tools like Claude or Copilot can reference the folder structure and files from the starting directory.
   * If you start in a sub-project directory, the tool may only “see” files within that sub-project, making cross-project references harder.

2. **Easier code navigation**:

   * Starting from the parent directory allows you to open or edit files across multiple sub-projects without switching contexts.
   * Mentions, imports, or references between projects are easier because the tool can index all relevant files.

3. **Better suggestions for shared code**:

   * Many teams have shared libraries or modules in sibling directories.
   * Starting at the parent level helps Copilot or Claude suggest code completions that involve those shared modules naturally.

**Caveats:**

* Be careful if your parent directory is very large; it might slow down indexing or context loading.
* Some tools may have limits on the number of files they consider for context. In that case, a selective approach (e.g., symbolic links, monorepo setup) may help.

In short: if your work involves **cross-project references or shared code**, starting in the parent directory usually gives the tools the best awareness of all relevant files.
