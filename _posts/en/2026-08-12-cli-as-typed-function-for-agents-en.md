---
audio: false
generated: true
image: false
lang: en
layout: post
title: CLI as Typed Function for Agents
translated: false
type: note
---

Question: Is a CLI essentially a function call, and what matters when designing CLIs for humans and agents?

Answer:

Yes. In the agent era, a CLI is very close to a **typed function interface**. The difference is that the caller is a process (shell, human, or agent) and the return channel is stdout/stderr + exit code + files/state changes.

A good mental model:

```python
result = deploy(
    app="my-api",
    env="prod",
    replicas=3
)
```

is equivalent to:

```bash
mycli deploy \
  --app my-api \
  --env prod \
  --replicas 3
```

The CLI is basically a serialization layer:

```
human / agent
      |
      v
  CLI parser
      |
      v
 typed function
      |
      v
 business logic
      |
      v
 structured result
```

For AI agents, the design principles change.

## 1. Streaming progress is critical

Traditional CLI:

```
$ deploy

(wait 5 minutes)

done
```

Bad for agents because the model has no observation.

Better:

```
$ deploy

[1/5] validating config...
[2/5] building image...
[3/5] pushing registry...
[4/5] rolling deployment...
[5/5] health check...

status=success
duration=312s
```

Agents operate through the loop:

```
observe -> reason -> act -> observe
```

No observation means the agent is blind.

This is why tools like:

* `git`
* `kubectl`
* `docker`
* cloud CLIs

are powerful: they expose intermediate states.

---

## 2. Logs are not just for humans anymore

Traditional thinking:

```
logs -> developer debugging
```

Agent-native thinking:

```
logs -> agent perception input
```

Example:

Bad:

```
Error: failed
```

Good:

```json
{
  "status": "failed",
  "step": "database_migration",
  "error_type": "connection_timeout",
  "database": "postgres",
  "retryable": true,
  "suggestion": "check network policy"
}
```

An agent cannot reliably infer hidden state.

Give it:

* current step
* inputs
* outputs
* errors
* possible recovery actions

---

## 3. Human CLI and Agent CLI should differ

Humans like:

```bash
git rm file.txt
```

Short.

Agents prefer:

```bash
git remove-file \
  --path=file.txt \
  --confirm=true \
  --reason="cleanup unused file"
```

Because language models are not typing shortcuts. They are generating structured actions.

For agents:

clarity > brevity.

---

## 4. Exit codes are underrated

Many CLIs only return:

```
0 success
1 error
```

Agent-friendly:

```
0  success

10 invalid_argument
20 permission_denied
30 network_failure
40 resource_missing
50 retryable_failure
```

Then an agent can decide:

```python
if exit_code == 30:
    retry()

if exit_code == 40:
    ask_user()

if exit_code == 50:
    exponential_backoff()
```

---

## 5. Make output machine-readable

A modern CLI should have:

```bash
mycli deploy --json
```

Output:

```json
{
  "deployment_id": "abc123",
  "status": "running",
  "progress": 0.7
}
```

Human:

```bash
mycli deploy
```

Output:

```
Deploying api-server...
70% complete
```

Same engine, different renderer.

---

## 6. Design CLI like an API

Good architecture:

```
              REST API
                 |
Human CLI ---- Core Engine ---- Agent Tool
                 |
              Python SDK
```

The CLI should not contain business logic.

Example:

```
cli.py
   |
   v
services/deploy.py
   |
   v
cloud provider
```

Then later:

```python
agent.call(
    "deploy",
    {
      "app": "api",
      "environment": "prod"
    }
)
```

works naturally.

---

This is why MCP/tool calling feels similar to CLI design. MCP tools are basically:

```
CLI command
      +
JSON schema
      +
structured output
```

The future pattern is probably:

```
old:
human -> CLI -> program

new:
human -> CLI -> program
agent -> tool -> program
agent -> CLI -> program
```

The best CLI today is not only a command interface. It is a **human-readable, machine-callable API with observable execution**.