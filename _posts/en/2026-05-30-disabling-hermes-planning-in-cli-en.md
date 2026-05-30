---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disabling Hermes Planning in CLI
translated: false
type: note
---

**Question:** How do I disable the Hermes agent's planning/delegation feature in my CLI agent setup? It's too slow.

**Answer:**

That output is from your custom `mimo` / `Hermes` agent framework — the orchestrator loop with `delegate_task`. To disable planning, the approach depends on how Hermes is implemented. Based on the pattern shown (self-improvement review → spec review → code quality review → delegate), here's how to track it down and disable it:

## 1. Find the planning/delegation config

```bash
# Search for the orchestration entrypoint
grep -r "hermes\|delegate_task\|plan\|spec.*review\|code.*quality" ~/your-agent-repo --include="*.py" -l

# Or if it's in a config file
find . -name "*.yaml" -o -name "*.toml" -o -name "*.json" | xargs grep -l "hermes\|delegate\|plan"
```

## 2. Common patterns to disable

**If it's a flag in a config file:**
```yaml
# agent config
planning: false
delegate: false
review_steps: []
```

**If it's a CLI flag:**
```bash
mimo --no-plan
mimo --disable-hermes
mimo --mode direct   # skip orchestration layer
```

**If it's code — find the orchestration loop:**
```python
# Look for something like this and short-circuit it
class Hermes:
    def run(self, task):
        if self.config.get("planning", True):  # <-- set to False
            plan = self.make_plan(task)
            for step in plan:
                self.delegate_task(step)
        else:
            self.execute_direct(task)  # what you want
```

## 3. Quick env var override (common pattern)

```bash
HERMES_PLAN=false mimo "do the task"
DISABLE_PLANNING=1 mimo "do the task"
```

## 4. If this is a third-party agent framework

Based on the UI (`⚕ Hermes`, `mimo-v2.5-pro`, token counter), this looks like it could be **Hermes by Nous Research** or a custom wrapper. Share the repo/tool name and I can give exact steps. Or:

```bash
mimo --help | grep -i "plan\|delegate\|review\|mode"
```

What's the actual tool/repo behind `mimo` and `Hermes`? That'll let me give you the exact flag.