---
audio: false
generated: true
image: false
lang: en
layout: post
title: From Prompt Chaos to Skill Engineering
translated: false
type: note
---

Question: If we settle agent code/skills in Hermes, is writing scripts first better than repeatedly prompting agents?

Answer:

Yes. This is actually one of the key transitions from **"using agents" → "engineering agents"**.

For a project like your `ww` agent framework, the better loop is:

```
human intent
    ↓
write deterministic workflow/script
    ↓
run it many times
    ↓
observe failures
    ↓
improve tools / skills / prompts / evals
    ↓
agent becomes better
```

not:

```
every task
    ↓
new prompt
    ↓
agent guesses
    ↓
hope it works
```

The second approach has a hidden problem: **you cannot accumulate learning**.

Example:

Today:

> "Agent, deploy my service"

Agent uses:

* ssh
* docker
* kubectl
* cloud API

Tomorrow:

> "Agent, deploy my service"

Maybe a different reasoning path happens.

You cannot easily know:

* which step failed
* which tool call was bad
* which assumption was wrong
* which context was missing

But if you convert it into:

```bash
ww deploy production
```

with something like:

```python
def deploy():
    check_git_status()
    run_tests()
    build_image()
    push_registry()
    rollout_k8s()
    verify_health()
```

then every failure becomes data.

You can improve:

### 1. Skills become versioned code

Instead of:

```
skill:
"know how to deploy"
```

you get:

```
skills/
  deploy/
    README.md
    deploy.py
    tests/
    examples/
```

Now you can diff:

```
git diff skill/deploy
```

and understand improvement.

---

### 2. Prompts become smaller

Bad:

```
You are a senior DevOps engineer.
Please deploy my app...
Remember all these rules...
```

Good:

```
Use skill: deploy.production.v3
Input:
 app=my-service
 env=prod
```

The intelligence moves from prompt → system.

---

### 3. Agent becomes planner, not executor

The ideal architecture:

```
             user
              |
              v
          LLM planner
              |
              |
        decide workflow
              |
              v
       Hermes skills
              |
     -----------------
     |       |       |
  deploy   test   monitor
```

The LLM is good at:

* understanding intent
* choosing tools
* adapting

The code is good at:

* repeatability
* safety
* correctness

---

This is similar to software engineering evolution:

Before:

```
copy/paste code
```

Then:

```
functions
```

Then:

```
libraries
```

Then:

```
frameworks
```

Agents are currently moving from:

```
prompt engineering
```

towards:

```
skill engineering
```

---

The interesting part: your `ww` direction is closer to how future agent systems will likely work.

The winning agent may not have the longest prompt.

It may have:

```
1000 reliable skills
+
good planner
+
memory
+
evaluation loop
```

Similar to humans:

A junior engineer asks ChatGPT every time.

A senior engineer has:

* scripts
* aliases
* internal libraries
* debugging habits
* mental models

The agent needs the same transition.

References:

* Your repository: `lzwjava/ww` (GitHub metadata accessed)
