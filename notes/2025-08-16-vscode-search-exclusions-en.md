---
audio: false
generated: true
image: false
lang: en
layout: post
title: Customize Search Exclusions in VS Code
translated: false
type: note
---

In VS Code, the global file search respects the **search exclusions** you configure. You can tell it to ignore certain files or folders so they don’t appear in search results.

Here are the main ways:

---

### 1. Use `search.exclude` in **settings.json**

Open your settings (`⌘,` / `Ctrl+,` → top right “Open Settings (JSON)”) and add:

```json
"search.exclude": {
  "**/node_modules": true,
  "**/dist": true,
  "**/*.log": true
}
```

* The keys are [glob patterns](https://code.visualstudio.com/docs/editor/codebasics#_advanced-search-options).
* `true` means “exclude from search”.
* Examples:

  * `**/node_modules` → all node\_modules folders
  * `**/*.log` → all `.log` files anywhere
  * `**/build/**` → everything inside build folders

---

### 2. Use `.gitignore`

If your project has a `.gitignore`, you can tell VS Code to respect it during search:

```json
"search.useIgnoreFiles": true
```

That way, anything ignored by Git won’t show in search results.

---

### 3. Use `.ignore`

You can also create a `.ignore` file in your project root (same format as `.gitignore`) specifically for editor tooling. VS Code will respect it if `search.useIgnoreFiles` is enabled.

---

### 4. Quick Exclude in Search UI

When you search, hover over a file/folder in the results and click **“Exclude”**. This temporarily adds that path to `search.exclude` in settings.

---

👉 So the most common setup is:

* Add general project-wide ignores in `.gitignore`.
* Add editor-specific ignores (like `dist`, `.vscode`) in `search.exclude`.

---

Do you want me to show you how to **exclude only during search** but still keep those files in Explorer, or also hide them from the Explorer side panel?
