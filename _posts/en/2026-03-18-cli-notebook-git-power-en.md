---
audio: false
generated: true
image: false
lang: en
layout: post
title: CLI Notebook With Git Power
translated: false
type: note
---

**Question:** Provide a comprehensive introduction to https://github.com/xwmx/nb?tab=readme-ov-file#-revision-history

**Answer:**

`nb` (short for "notebook") is a powerful, portable **command-line tool** (and local web interface) for plain-text note-taking, bookmarking, archiving, and building a personal knowledge base. Developed by xwmx, it is written as a single Bash script and stores everything in ordinary plain-text files (primarily Markdown) inside Git repositories. This design makes it lightweight, future-proof, fully searchable, versioned, syncable, and independent of proprietary formats or cloud services.

### Core Philosophy
- Data in plain text files using standard formats (Markdown, Org, etc.)
- Git handles versioning and synchronization automatically and transparently
- No database — just normal directories and files you can manage with any tool
- Works offline, locally-first, with optional remote Git sync (GitHub, GitLab, private servers, etc.)
- Very close digital equivalent to a physical Zettelkasten system

### Key Features
- **Notes** — Create, edit, view, delete Markdown files with titles, tags, and content
- **Bookmarks** — Save URLs with full cached content, quotes, comments, tags; full-text searchable
- **Todos & Tasks** — Dedicated `.todo.md` files with checkboxes, due dates, subtasks, and status tracking (`do` / `undo`)
- **Tagging** — `#hashtags` (including nested `#parent/child`), powerful filtering
- **Linking** — Wiki-style `[[notebook:folder/id\|custom text]]` internal links for Zettelkasten-style knowledge graphs
- **Pinning** — Pin important items to appear at the top of lists
- **Folders & Notebooks** — Organize hierarchically; support multiple global/local notebooks
- **Search** — Full-text search (with regex, AND/OR/NOT, tag/type filters) using `git grep`, `ripgrep`, or similar
- **Revision History** — Every change is a Git commit; view with `nb history` (prefers `tig` if installed)
- **Git Sync** — Automatic commits + push/pull to remotes; handles conflicts reasonably
- **Encryption** — Per-item password protection via OpenSSL AES-256 or GPG
- **Browsing** — `nb browse` starts a local web server to navigate notes interactively (works in terminal browsers like w3m or GUI browsers)
- **Import / Export** — Pandoc-powered conversion to/from many formats (HTML, DOCX, EPUB, PDF, etc.)
- **Images** — Inline image support, import, terminal viewing
- **Plugins & Themes** — Extensible with custom subcommands and color themes
- **Interactive Shell** — `nb shell` for REPL-style usage

### How Revision History Works
The section **#-revision-history** in the README explains Git-based versioning:

- Every add, edit, move, delete, or other modification automatically creates a Git commit in the background.
- Use `nb history` (or `nb history <selector>`) to view changes:
  - `nb history` — current notebook
  - `nb history 42` — specific item by ID
  - `nb history example:7` — item 7 in notebook "example"
  - `nb history "My Note Title"` — by title
- Displays commit log (date, message, author); uses `tig` for interactive view when available
- Author name/email comes from global Git config or can be overridden per-notebook with `nb notebooks author`
- Because each notebook is its own Git repository, history is isolated per notebook

This gives every note, bookmark, and todo immutable version control similar to a lightweight personal wiki with full change tracking.

### Installation (as of 2026)
- **Homebrew** (macOS/Linux): `brew install xwmx/taps/nb`
- **npm**: `npm install -g nb.sh`
- **Manual** (most portable):
  ```bash
  sudo wget https://raw.githubusercontent.com/xwmx/nb/master/nb -O /usr/local/bin/nb
  sudo chmod +x /usr/local/bin/nb
  nb completions install
  ```
- **Update**: `nb update` (when not installed via package manager)
- **Required**: Bash + Git
- **Optional (highly recommended)**: pandoc, ripgrep/rga, bat, tig, w3m/lynx, socat/ncat (for browse)

### Quick Start Examples
```bash
# Create a note
nb add "Meeting notes 2026-03" --tags projectX meeting

# Add a bookmark
nb https://example.com/article --quote "Important insight" --tags research

# Create a todo
nb todo add "Finish report" --due 2026-04-01 --task "Write summary" --task "Proofread"

# Search
nb q "quantum" --tag physics --type note

# View history of a note
nb history 15

# Browse in browser
nb browse

# Sync everything
nb sync --all
```

### Strengths & Trade-offs
**Pros**:
- Extremely portable and long-term sustainable (plain text + Git)
- Powerful linking and search for knowledge work
- Zero vendor lock-in
- Active development (recent commits in March 2026, version ~7.25.x)

**Cons / Considerations**:
- Requires comfort with terminal and basic Git
- Conflict resolution during sync is manual (Git-style)
- Advanced rendering (images, complex tables) depends on optional tools

Overall, `nb` is one of the most mature, feature-rich CLI-first plain-text notebook systems available, especially for users who value Git, plain text, and Zettelkasten principles.

**References:**

- [https://github.com/xwmx/nb](https://github.com/xwmx/nb)
- [https://xwmx.github.io/nb/](https://xwmx.github.io/nb/) (demo / extended docs)
