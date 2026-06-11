---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dynamic Skill Loading Works Live
translated: false
type: note
---

**Question:** Can Claude Code dynamically generate a new skill mid-session and have it load immediately, without restarting?

**Answer:**

Yes — this works, and it's officially supported as of recent Claude Code versions. Claude Code watches skill directories for file changes. Adding, editing, or removing a skill under `~/.claude/skills/`, the project `.claude/skills/`, or a `.claude/skills/` inside an `--add-dir` directory takes effect within the current session without restarting.

So the "self-modifying agent" loop you're imagining — Claude writes its own `SKILL.md` mid-task, then uses it — is legit:

```bash
# Inside a Claude Code session, Claude can do this itself:
mkdir -p .claude/skills/changelog-gen
cat > .claude/skills/changelog-gen/SKILL.md << 'EOF'
---
name: changelog-gen
description: Generate a changelog entry from git diff. Use when the user asks to summarize recent changes or write release notes.
---

# Changelog Generation

1. Run `git log --oneline -20` and `git diff HEAD~5 --stat`
2. Group changes: feat / fix / refactor / docs
3. Output in Keep a Changelog format, newest first
EOF
# Skill is now live — next relevant prompt triggers it. No restart.
```

Mechanically why this works without blowing up context: skills use progressive disclosure. Claude loads metadata at startup and includes it in the system prompt — a lightweight approach meaning you can install many Skills without context penalty; Claude only knows each Skill exists and when to use it. Metadata is ~100 tokens per skill; full instructions (<5k tokens) load only when Claude determines the skill applies; bundled resources load only as needed. The file watcher just refreshes that metadata index live.

Caveats that will bite you:

1. **The top-level skills dir must already exist.** Creating a top-level skills directory that did not exist when the session started requires restarting Claude Code so the new directory can be watched. So `mkdir -p .claude/skills` *before* launching, or keep an empty `.gitkeep` there. Inside an existing dir, new skill folders hot-load fine.

2. **Only SKILL.md text is hot-reloaded.** Live change detection covers SKILL.md text only. For a skill folder that is also a plugin, changes to hooks/, .mcp.json, agents/, and output-styles/ need /reload-plugins to take effect. Pure markdown skills = instant; plugin-grade stuff = `/reload-plugins`.

3. **Triggering depends entirely on the `description` frontmatter** — Claude matches your prompt against descriptions, so a dynamically generated skill with a vague description will never fire. If you want deterministic invocation in the same session, just tell Claude explicitly: "use the changelog-gen skill."

For your `ww`/`iclaw`/`zz` agent tooling, the interesting pattern is a **bootstrap skill**: one meta-skill whose job is "when the user describes a repeating workflow, crystallize it into a new skill under `.claude/skills/`." That's effectively runtime self-extension — the agent compiles its own ephemeral experience into persistent, low-token-cost capabilities. Anthropic ships a `skill-creator` skill for exactly this; the dynamic-loading behavior makes it usable in a single session instead of a write-restart-test loop.

One thing to validate empirically (5-minute test in a scratch repo): whether a skill created mid-conversation triggers *automatically* on the very next turn, or whether the metadata refresh lags a turn. The docs say "takes effect within the current session," but auto-trigger sensitivity for just-created skills is worth testing — explicit invocation by name is the reliable path.

**References:**

- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Agent Skills Overview — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
