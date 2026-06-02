---
audio: false
generated: true
image: false
lang: en
layout: post
title: PyCharm Rename Files Safely and Smartly
translated: false
type: note
---

Yes — if you use **PyCharm’s refactoring feature** (right-click the file → Refactor → Rename, or press `Shift+F6` on the file name), it will not just rename the file on disk but also update **all references and import statements** that point to it, as long as they are resolvable inside the project.

A few important details to keep in mind:

* **Scope of refactor**: PyCharm analyzes your whole project, so imports in other Python files within the project will be updated automatically.
* **Unresolved / dynamic imports**: If some imports are built dynamically (for example using `__import__`, `importlib`, or string-based module paths), PyCharm won’t detect those, so they won’t be updated.
* **Multiple roots / external scripts**: If other scripts are outside the PyCharm project or aren’t indexed (e.g., not in your project source roots), PyCharm won’t catch them either.
* **Tests and relative imports**: If you use relative imports (`from . import something`) and the folder structure changes, you may need to check that separately.

So, for normal `import mymodule.something` cases inside your project, renaming with PyCharm refactor will keep everything consistent.

Do you want me to also explain **how to safely test after renaming** so you’re sure nothing broke?
