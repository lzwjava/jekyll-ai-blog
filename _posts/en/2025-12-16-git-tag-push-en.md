---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Git Tag Usage and Pushing
translated: false
type: note
---

Question: How to use `git tag` and how to push tags with `git push`?

Answer:

Git tags mark specific commits in your repository history, often used for releases (e.g., `v1.0.0`).

### Types of Tags
- **Lightweight tags**: Simple pointers to a commit (like a bookmark). No extra metadata.
- **Annotated tags** (recommended for releases): Full Git objects including tagger name, email, date, message, and optional GPG signing.

### Creating Tags
- List existing tags:
  ```
  git tag
  ```
- Create a **lightweight tag** (on current HEAD):
  ```
  git tag <tagname>
  ```
  Example: `git tag v1.0`

- Create an **annotated tag** (recommended):
  ```
  git tag -a <tagname> -m "Your message"
  ```
  Example: `git tag -a v1.0 -m "Stable release version 1.0"`

- Tag an older commit (specify commit hash):
  ```
  git tag -a v0.9 <commit-hash> -m "Previous release"
  ```

- View tag details:
  ```
  git show <tagname>
  ```
  (Shows metadata for annotated tags; just the commit for lightweight.)

### Pushing Tags to Remote
Tags are **not pushed automatically** with `git push`. You must push them explicitly.

- Push a single tag:
  ```
  git push origin <tagname>
  ```
  Example: `git push origin v1.0`

- Push all local tags:
  ```
  git push origin --tags
  ```

- To automatically push annotated tags reachable from pushed commits (since Git 2.4+):
  Configure with:
  ```
  git config --global push.followTags true
  ```
  Then `git push` will include them.

### Deleting Tags
- Local:
  ```
  git tag -d <tagname>
  ```
- Remote:
  ```
  git push origin :refs/tags/<tagname>
  ```
  Or (newer Git): `git push origin --delete <tagname>`

Best practice: Use annotated tags for public releases to preserve metadata.

References:

- [Git - Tagging (official documentation)](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
- [git-tag Documentation](https://git-scm.com/docs/git-tag)
