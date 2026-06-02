---
audio: false
generated: true
image: false
lang: en
layout: post
title: Naming tmux sessions
translated: false
type: note
---

Question: How to create tmux sessions with a name?

Answer:

To create a tmux session with a custom name, use the `-s` flag with the `tmux new-session` command (or its shorthand `tmux new`).

### Basic Command

```bash
tmux new-session -s session_name
```

**Example:**

```bash
tmux new-session -s myproject
```

This creates a new tmux session named "myproject" and attaches to it immediately.

### Shorthand Version

```bash
tmux new -s myproject
```

### Additional Useful Options

- **Start detached** (create the session in the background without attaching):

  ```bash
  tmux new -s myproject -d
  ```

- **Specify a working directory**:

  ```bash
  tmux new -s myproject -c ~/projects/myapp -d
  ```

- **Run a command on session start**:

  ```bash
  tmux new -s myserver -c ~/projects -d "python run_server.py"
  ```

### Common Workflow Examples

1. **Create and attach**:

   ```bash
   tmux new -s dev
   ```

2. **Create detached** (useful in scripts or when you want to set up multiple sessions first):

   ```bash
   tmux new -s frontend -d
   tmux new -s backend -d
   tmux new -s database -d
   ```

3. **Attach to an existing named session**:

   ```bash
   tmux attach -t myproject
   ```

4. **List all sessions** (to see names):

   ```bash
   tmux list-sessions
   ```

   or the shorter:

   ```bash
   tmux ls
   ```

### Inside an Existing tmux Session

If you're already inside tmux and want to create a new named session:

- Press `Ctrl+b` (default prefix) then type `:new -s newname` and press Enter.

### Renaming an Existing Session

```bash
tmux rename-session -t oldname newname
```

or inside tmux: `Ctrl+b` then `:rename-session newname`

### Pro Tips

- Session names should be descriptive but short (e.g., `web`, `api`, `logs`, `project-v2`).
- You can use underscores `_` or hyphens `-` in names.
- To kill a session: `tmux kill-session -t session_name`

This method works on Linux, macOS, and any system with tmux installed.

References:

- [tmux man page](https://man7.org/linux/man-pages/man1/tmux.1.html)
