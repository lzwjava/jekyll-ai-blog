---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exclude Ignored Files in VS Code
translated: false
type: note
---

You can make “Go to File” (Quick Open, Ctrl + P) include files that live in your `.gitignore` by tweaking three settings in your `settings.json`:

1. **Tell search to ignore your `.gitignore` rules**

   ```jsonc
   "search.useIgnoreFiles": false,      // don’t respect .gitignore
   "search.useGlobalIgnoreFiles": false // don’t respect your global gitignore
   ```
2. **Ensure your exclusion globs don’t hide those files**
   By default VS Code inherits all the patterns from `files.exclude` into `search.exclude`.  If you’ve manually excluded `.gitignore`-dirs there, re-enable them:

   ```jsonc
   "search.exclude": {
     "**/.git": false,          // do index .git (if you want)
     "**/.gitignore": false     // definitely don’t hide your .gitignore file itself
     // …any other patterns you’d like to override
   }
   ```
3. **Reload the window**
   After saving your user or workspace settings, run **Developer: Reload Window** (⇧ ⌘ P → “Reload Window”) so the file-indexer picks up the change.

Now when you hit Ctrl + P you’ll see *all* files by name—ignored or not. ([stackoverflow.com][1])

[1]: https://stackoverflow.com/questions/62855190/how-do-you-include-git-ignored-files-in-vscode-quick-search?utm_source=chatgpt.com "How do you include git ignored files in VSCode quick search"
