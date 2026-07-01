---
audio: false
generated: true
image: false
lang: en
layout: post
title: Switch Homebrew Claude Code to npm
translated: false
type: note
---

**Question:** How do I remove the Homebrew-installed Claude Code and switch to the npm-installed version?

**Answer:**

## Remove Homebrew Claude Code & Switch to npm Version

### Step 1: Uninstall Claude Code via Homebrew

```bash
brew uninstall claude
```

If it was installed as a cask:

```bash
brew uninstall --cask claude
```

---

### Step 2: Verify It's Gone

```bash
which claude
```

It should return **nothing** (or `claude not found`). If it still shows `/opt/homebrew/bin/claude`, force-remove the binary:

```bash
rm /opt/homebrew/bin/claude
```

---

### Step 3: Install Claude Code via npm (Specific Version)

```bash
npm install -g @anthropic-ai/claude-code@2.1.77
```

---

### Step 4: Verify npm Version is Active

```bash
which claude
claude --version
```

You should now see something like:

```
/Users/yourname/.npm-global/bin/claude   # or ~/.nvm/versions/node/.../bin/claude
2.1.77 (Claude Code)
```

---

### Troubleshooting: PATH Priority

If `which claude` still points to Homebrew after installing via npm, your `PATH` is prioritizing `/opt/homebrew/bin` over npm's bin directory.

Check your `~/.zshrc` or `~/.bash_profile` and make sure npm's bin path comes **before** Homebrew:

```bash
# In ~/.zshrc — npm global BEFORE homebrew
export PATH="$HOME/.npm-global/bin:$PATH"
# or if using nvm:
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

Then reload:

```bash
source ~/.zshrc
```

---

### Quick Summary

| Step | Command |
| --- | --- |
| Remove Homebrew version | `brew uninstall claude` |
| Install npm version | `npm install -g @anthropic-ai/claude-code@2.1.77` |
| Verify | `which claude && claude --version` |
