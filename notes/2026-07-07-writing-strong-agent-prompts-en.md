---
audio: false
generated: true
image: false
lang: en
layout: post
title: Writing Strong Agent Prompts
translated: false
type: note
---

Your prompt is understandable, but for an agent like Hermes (especially an autonomous coding/ops agent), it is too conversational and missing some important constraints. Agents perform better when you define:

1. **Goal**
2. **Environment**
3. **Steps**
4. **Rules**
5. **Expected output**

Your current prompt:

> remember you need to document all code or script down and then execute it, in runpod directory here, ssh ..., now go to here, to check librechat and sglang setup, use 8888 port, so I can have chatbot

Problems:

* "here" is ambiguous.
* "check setup" does not define what success means.
* "document all code or script" is good, but should specify location.
* SSH command contains infrastructure details; better tell the agent to use it, but avoid repeating secrets/tokens.
* It does not tell the agent not to destroy existing setup.
* It does not ask for a final status report.

A stronger agent prompt:

```
Task: Set up and verify LibreChat + SGLang chatbot service on the RunPod instance.

Environment:
- SSH into the RunPod machine:
  root@<RUNPOD_HOST> -p <PORT> -i ~/.ssh/id_ed25519
- Work inside the RunPod project directory.

Requirements:
1. Before running any command, create/update a documentation file explaining:
   - what the command does
   - why it is needed
   - expected output
2. Save all scripts/configuration files in the project directory.
3. Do not put passwords, API keys, SSH keys, or secrets into files that may be uploaded to GitHub.
4. First inspect the existing LibreChat and SGLang installation.
5. Reuse existing setup if possible. Do not reinstall or delete things without checking.
6. Verify:
   - SGLang model server is running
   - LibreChat can connect to SGLang
   - Port 8888 is exposed and accessible
7. Start/fix the services so I can open the chatbot through port 8888.

After completion, report:
- Files created/modified
- Commands executed
- Current service status
- URL/port to access chatbot
- Any remaining issues
```

For autonomous agents, the phrase:

> "document first, then execute"

is actually a very good constraint. It forces the agent to create reproducible operations instead of doing random shell exploration.

One more improvement: ask it to create a **single entrypoint script**:

```
Create run.sh or setup.sh so the entire environment can be reproduced later.
```

That fits your workflow better because the next time you spin up a RunPod instance, the agent can run the script instead of rediscovering everything.
