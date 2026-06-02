---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Control-M Environment Variable Methods
translated: false
type: note
---

In BMC Control-M (both Control-M/Enterprise Manager and Control-M Automation API/Agent), there are several common and recommended ways to pass or make environment variables available to a job. Here are the most frequently used methods (from most recommended to older/legacy ones):

### 1. **Using Control-M Job Definition – “Environment Variables” section** (Recommended – Control-M 9.0.20+)

In Control-M Web (or Automation API JSON), you can directly define environment variables that will be set in the job’s process environment before execution.

**In Control-M Web GUI:**

- Open the job properties
- Go to the **Execution** tab → **Environment Variables**
- Add Name/Value pairs (e.g., MY_VAR = my_value)

**In Automation API (JSON):**

```json
{
  "MyJob": {
    "Type": "Job:OS",
    "Command": "echo $MY_VAR",
    "Environment Variables": [
      {"MY_VAR": "HelloFromControlM"},
      {"ANOTHER_VAR": "12345"}
    ]
  }
}
```

These variables are automatically exported in the job’s environment on both Windows and Unix/Linux agents.

### 2. **Using %%PARM syntax (AutoEdit variables)** – Very common in legacy environments

You define variables at folder or job level and they get resolved at order/run time.

**In job definition (cmm or JSON):**

```text
%%MY_VAR = some_value
```

or set it dynamically with:

```text
%%MY_VAR = %%$DATE
```

Then in the script/command you reference it with the agent’s native syntax:

- Unix/Linux: `$MY_VAR` or `${MY_VAR}`
- Windows: `%MY_VAR%`

You can also set them from shouting, cyclic jobs, or via Automation API.

### 3. **Set them explicitly in the script/command line**

```text
# Unix example
export MY_VAR=value && /path/to/script.sh

:: Windows example
set MY_VAR=value && script.bat
```

### 4. **Using Control-M Agent “agentenv” or profile scripts** (global for all jobs on the agent)

Not job-specific, but sometimes used:

- Unix: Edit `$HOME/.bashrc` or `$HOME/.profile` that Control-M sources
- Or use Control-M Agent utility `agt_profile` to add permanent environment settings

### 5. **Passing via “Parameters” (Local or SMART folder parameters) and then converting to env vars**

You can define folder parameters and reference them as %%PARAM_NAME, then in the job do:

```text
export MY_VAR=%%MY_PARAM
```

### 6. **Using Control-M Automation API “deploy” with variables or “run” with variables**

When you trigger a job via API, you can pass variables at run time:

```json
"variables": [
  {"MY_VAR": "runtime_value"},
  {"DEBUG": "true"}
]
```

These become available as %%MY_VAR inside the job and are automatically exported as environment variables if you use the modern “Environment Variables” feature.

### Summary – Best Practice (2024–2025)

- Control-M 9.0.21+: Use the native **Environment Variables** section in the job definition (GUI or JSON). It’s clean, visible, and works the same on Windows and Unix.
- Older versions or legacy definitions: Use %%AutoEdit variables + export/set in the script.

This way you keep everything visible inside Control-M without relying on external profile scripts or wrapper scripts.
