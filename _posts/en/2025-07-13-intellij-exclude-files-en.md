---
audio: false
generated: true
image: false
lang: en
layout: post
title: Excluding Files in IntelliJ IDEA
translated: false
type: note
---

In IntelliJ IDEA, you can exclude files or directories so they don’t appear in search, indexing, code completion, or builds. There are several ways to do it depending on your purpose:

---

### 1. Mark a Directory as *Excluded*

* In the **Project view**, right-click the folder you want to exclude.
* Choose **Mark Directory as → Excluded**.
* IDEA will stop indexing it, so it won’t show up in searches, navigation, or code analysis.

This is typically used for build output folders (`target/`, `out/`, `dist/`, etc.).

---

### 2. Exclude from Version Control (VCS Ignore)

If you don’t want IDEA (and Git) to track certain files:

* Create or edit a `.gitignore` file in your project.
* Add the directory or filename patterns there.
* IDEA will recognize `.gitignore` and hide them from VCS operations.

---

### 3. Exclude Files from Code Analysis / Inspections

* Go to **Settings → Editor → Inspections**.
* There you can configure **Scopes**, and assign inspections only to certain file sets while excluding others.

---

### 4. Exclude from Build (Gradle/Maven)

If you’re using Gradle or Maven, you can configure `build.gradle` or `pom.xml` to exclude certain directories (like generated code or resources). IDEA respects these build tool configurations.

---

### 5. Exclude Specific File Types

* Go to **Settings → Editor → File Types**.
* Add patterns (like `*.log`, `*.tmp`) to the "Ignore files and folders" list.

---

👉 Quick tip: If your goal is just to stop IDEA from wasting resources indexing large folders (like `node_modules/`), the **Mark Directory as Excluded** option is the fastest and most effective.

Do you want me to also show you how to exclude test directories (like `src/test/java`) from **code coverage** runs in IDEA?
