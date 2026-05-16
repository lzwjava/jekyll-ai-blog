---
audio: false
generated: true
image: false
lang: en
layout: post
title: Autonomous Agent Loop Architecture Explained
translated: false
type: note
---

Here's the core architecture and loop logic behind autonomous coding agents like Copilot Agent, explained from the ground up.

## 1. The Fundamental Agent Loop

The simplest agent is a while loop that alternates between "think" and "act":

```python
def agent_loop(task: str, max_iterations: int = 50):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task}
    ]
    
    for i in range(max_iterations):
        # THINK: ask the LLM what to do next
        response = llm.chat(messages=messages, tools=TOOL_SCHEMAS)
        
        # DONE: no tool calls means agent thinks it's finished
        if not response.tool_calls:
            return response.content
        
        # ACT: execute each tool call and feed results back
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call.name, tool_call.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        # The assistant message (with tool_calls) also goes into history
        messages.append(response.message)
    
    return "Max iterations reached"
```

That's it. The entire Copilot Agent, Claude Code, Codex, etc. are elaborations of this loop. The magic is NOT in the loop — it's in three things: the system prompt, the tool definitions, and how you handle errors.

## 2. The Key Insight: How It "Takes a Step Back"

The agent doesn't genuinely "reflect" in a philosophical sense. What happens mechanically:

```
Iteration 1:  LLM reads code → proposes fix → tool writes file
Iteration 2:  LLM runs tests → sees FAILURE → the error message goes back into context
Iteration 3:  LLM reads the error → realizes approach was wrong → tries different fix
```

The "taking a step back" is just: **the error output from the previous iteration becomes input for the next iteration**. The LLM sees its own failed attempt in the conversation history and naturally tries something different. This is emergent from:

- Full conversation history being preserved
- Error messages being specific enough to reveal what went wrong
- The LLM having enough context to understand *why* the first approach failed

Here's the concrete pattern:

```python
# The agent tries Fix A, tests fail:
messages = [
    system_prompt,
    user_task,
    assistant("I'll change the auth middleware to..."),  # attempt 1
    tool_result("File written: middleware.py"),
    assistant("Let me run the tests"),
    tool_result("FAIL: AttributeError: 'NoneType' object has no attribute 'token'"),
    # ^^^ This is where "taking a step back" happens mechanically
    assistant("I see — the session can be None. Let me add a null check first..."),  # attempt 2
]
```

## 3. The Real Architecture: Error Recovery Strategies

What separates a toy agent from Copilot Agent is HOW it handles failures. There are several strategies:

### Strategy A: Verbatim Error Injection (basic)

```python
# Just stuff the error into the next LLM turn
messages.append({
    "role": "tool",
    "content": f"ERROR: {stderr_output}\nExit code: {exit_code}"
})
```

The LLM reads the error and decides what to do. This is what most agents do.

### Strategy B: Error Classification (advanced)

```python
def classify_error(stderr: str) -> str:
    if "ModuleNotFoundError" in stderr:
        return "missing_dependency"
    elif "SyntaxError" in stderr:
        return "syntax_error"  
    elif "AssertionError" in stderr:
        return "logic_error"
    elif "PermissionError" in stderr:
        return "permission_issue"
    else:
        return "unknown"

# Inject classified context
error_msg = f"""
ERROR TYPE: {classify_error(stderr)}
EXIT CODE: {process.returncode}
STDERR:
{stderr[:2000]}
STDOUT:
{stdout[:500]}
"""
```

This helps the LLM pattern-match faster against known failure modes.

### Strategy C: Iteration Budget per Subtask (Copilot-style)

```python
class IterationBudget:
    def __init__(self, total: int = 50, per_subtask: int = 5):
        self.total = total
        self.per_subtask = per_subtask
        self.current_subtask_iterations = 0
    
    def should_try_different_approach(self) -> bool:
        """If stuck on same subtask for too long, signal a pivot."""
        return self.current_subtask_iterations >= self.per_subtask
```

When the budget for a subtask is exhausted, you inject a message:

```python
if budget.should_try_different_approach():
    messages.append({
        "role": "user", 
        "content": "You've tried this approach several times without success. "
                    "Consider a completely different strategy."
    })
```

### Strategy D: Diff-based Verification (what Copilot actually does)

```python
def execute_with_rollback(tool_call):
    """Save state before each change, verify after."""
    snapshot = git_create_stash()  # or filesystem snapshot
    
    result = execute_tool(tool_call)
    
    # Auto-verify after writes
    if tool_call.name == "write_file" or tool_call.name == "edit_file":
        verify_result = run_linter_and_tests()
        if verify_result.failed:
            # Rollback and tell the LLM what happened
            git_restore_stash(snapshot)
            return f"Change caused test failure:\n{verify_result.stderr}\n\nChange was reverted."
    
    return result
```

This is the "self-healing" behavior: the agent makes a change, verifies it, and if it breaks things, automatically rolls back before telling the LLM. The LLM never gets to compound errors.

## 4. The Complete Agent Harness

Here's a more complete implementation showing all the pieces:

```python
import subprocess, json, os
from dataclasses import dataclass, field
from pathlib import Path

# ── Tool Definitions ──────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "write_file",
            "description": "Write content to a file (creates or overwrites)",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return output",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "timeout": {"type": "integer", "default": 30}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for patterns in files (like grep)",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "path": {"type": "string", "default": "."}
                },
                "required": ["pattern"]
            }
        }
    }
]

# ── Tool Execution ────────────────────────────────────────────────

def execute_tool(name: str, args: dict) -> str:
    if name == "read_file":
        try:
            return Path(args["path"]).read_text()[:50000]
        except FileNotFoundError:
            return f"ERROR: File not found: {args['path']}"
    
    elif name == "write_file":
        try:
            Path(args["path"]).parent.mkdir(parents=True, exist_ok=True)
            Path(args["path"]).write_text(args["content"])
            return f"Successfully wrote {len(args['content'])} chars to {args['path']}"
        except Exception as e:
            return f"ERROR writing file: {e}"
    
    elif name == "run_command":
        try:
            result = subprocess.run(
                args["command"], shell=True,
                capture_output=True, text=True,
                timeout=args.get("timeout", 30),
                cwd=os.getcwd()
            )
            output = ""
            if result.stdout:
                output += f"STDOUT:\n{result.stdout[:3000]}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr[:3000]}\n"
            output += f"EXIT CODE: {result.returncode}"
            return output
        except subprocess.TimeoutExpired:
            return f"ERROR: Command timed out after {args.get('timeout', 30)}s"
    
    elif name == "search_files":
        try:
            result = subprocess.run(
                f"grep -rn {args['pattern']} {args.get('path', '.')}",
                shell=True, capture_output=True, text=True, timeout=10
            )
            return result.stdout[:5000] or "No matches found"
        except Exception as e:
            return f"ERROR: {e}"
    
    return f"Unknown tool: {name}"

# ── The Agent Harness ─────────────────────────────────────────────

@dataclass
class AgentConfig:
    max_iterations: int = 50
    max_subtask_attempts: int = 3      # tries per subtask before pivoting
    auto_verify_after_write: bool = True
    auto_rollback_on_failure: bool = True
    verify_command: str = "cd /tmp/agent_work && python -m pytest -x -q 2>&1 | tail -30"

class AgentHarness:
    def __init__(self, config: AgentConfig = AgentConfig()):
        self.config = config
        self.consecutive_failures = 0
        self.last_error_pattern = None
    
    def run(self, task: str) -> str:
        messages = self._build_initial_messages(task)
        
        for iteration in range(self.config.max_iterations):
            # ── LLM decides next action ──
            response = self._call_llm(messages)
            
            # ── No tool calls = done ──
            if not response.tool_calls:
                return response.content
            
            # ── Execute each tool call ──
            assistant_msg = {
                "role": "assistant",
                "content": response.content or None,
                "tool_calls": [
                    {"id": tc.id, "type": "function", 
                     "function": {"name": tc.name, "arguments": tc.arguments}}
                    for tc in response.tool_calls
                ]
            }
            messages.append(assistant_msg)
            
            for tc in response.tool_calls:
                result = self._execute_with_recovery(tc, messages)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })
        
        return "Agent exhausted iteration budget"
    
    def _execute_with_recovery(self, tool_call, messages) -> str:
        """Execute a tool call with automatic error recovery."""
        result = execute_tool(tool_call.name, json.loads(tool_call.arguments))
        
        # ── Auto-verify after file writes ──
        if self.config.auto_verify_after_write and tool_call.name in ("write_file", "edit_file"):
            verify_output = self._run_verification()
            
            if "FAIL" in verify_output or "ERROR" in verify_output:
                self.consecutive_failures += 1
                
                # ── Pattern detection: same error repeatedly? ──
                current_error = self._extract_error_signature(verify_output)
                if current_error == self.last_error_pattern:
                    self.consecutive_failures += 2  # penalty for repeating
                
                self.last_error_pattern = current_error
                
                # ── Rollback if configured ──
                if self.config.auto_rollback_on_failure:
                    self._rollback_last_change(tool_call)
                    result += f"\n\n⚠️  VERIFICATION FAILED (attempt {self.consecutive_failures}):\n{verify_output}\nChange was rolled back."
                
                # ── Pivot hint: tell the LLM to try something else ──
                if self.consecutive_failures >= self.config.max_subtask_attempts:
                    result += (
                        "\n\n🔴 You've failed this subtask multiple times with the same approach. "
                        "STRONGLY consider: (1) a completely different solution strategy, "
                        "(2) reading more code to understand the root cause, "
                        "(3) simplifying your approach."
                    )
                    self.consecutive_failures = 0  # reset after injecting pivot hint
            else:
                # Success — reset counters
                self.consecutive_failures = 0
                self.last_error_pattern = None
                result += f"\n\n✅ Verification passed."
        
        return result
    
    def _run_verification(self) -> str:
        try:
            r = subprocess.run(
                self.config.verify_command, shell=True,
                capture_output=True, text=True, timeout=60
            )
            return r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return "ERROR: Verification timed out"
    
    def _rollback_last_change(self, tool_call):
        """Undo the last file write using git or backup."""
        path = json.loads(tool_call.arguments).get("path", "")
        if path and Path(path).exists():
            subprocess.run(f"git checkout -- {path}", shell=True, 
                         capture_output=True, timeout=10)
    
    def _extract_error_signature(self, output: str) -> str:
        """Extract the core error pattern (line number stripped) for dedup."""
        import re
        # Remove line numbers and addresses to normalize errors
        normalized = re.sub(r'line \d+', 'line N', output)
        normalized = re.sub(r'0x[0-9a-f]+', '0xADDR', normalized)
        return normalized[:200]
    
    def _call_llm(self, messages):
        """Call the LLM API — swap with your provider."""
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1",
                       api_key=os.environ["OPENROUTER_API_KEY"])
        return client.chat.completions.create(
            model="anthropic/claude-sonnet-4",
            messages=messages,
            tools=TOOLS,
            max_tokens=4096
        )
    
    def _build_initial_messages(self, task: str) -> list:
        return [
            {"role": "system", "content": self._system_prompt()},
            {"role": "user", "content": task}
        ]
    
    @staticmethod
    def _system_prompt() -> str:
        return """You are an autonomous coding agent. You can read files, 
write files, run commands, and search code.

WORKFLOW:
1. First, READ relevant files to understand the codebase
2. Form a hypothesis about what needs to change
3. Make minimal, targeted changes
4. VERIFY your changes by running tests/linter
5. If verification fails, READ the error carefully before trying again

CRITICAL RULES:
- Never make the same change twice if it failed the first time
- If tests fail, read the ACTUAL error message before attempting a fix
- When stuck, read MORE code rather than guessing
- Prefer small, incremental changes over large rewrites
- Always verify after writing files

When you encounter repeated failures on the same issue:
- Step back and re-read the relevant code
- Check if there's a dependency or import you're missing
- Consider that your mental model of the code might be wrong
"""

# ── Usage ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    harness = AgentHarness()
    result = harness.run("Fix the login bug in src/auth.py — users with expired tokens get a 500 instead of 401")
    print(result)
```

## 5. What Copilot Agent Adds on Top

The basic loop above is ~200 lines. Copilot Agent adds:

| Layer | What it does | Why it matters |
|-------|--------------|----------------|
| **Subagent spawning** | Breaks task into subtasks, runs them in parallel | Speed — multiple files edited simultaneously |
| **Context management** | Sliding window + summarization of old turns | Fits long tasks into context limits |
| **Plan-then-execute** | First LLM call generates a plan, subsequent calls execute steps | Better task decomposition |
| **Semantic search** | Embed codebase, retrieve relevant chunks per query | Agent finds code without reading every file |
| **Safe execution** | Sandboxed filesystem, network restrictions | Doesn't delete your repo |
| **Checkpointing** | Git commit after each successful verification step | Easy rollback to any known-good state |
| **Human-in-the-loop** | Pauses for approval on destructive operations | Safety net |

## 6. The "Self-Healing" Loop in Practice

Here's what the actual conversation looks like inside the agent when it encounters and fixes an issue:

```
Turn 1  [LLM]: I'll fix the auth bug. Let me read the file.
        [TOOL] read_file("src/auth.py")
        [RESULT] ... code showing `user.token.verify()` with no null check ...

Turn 2  [LLM]: The issue is clear — `user.token` can be None. I'll add a check.
        [TOOL] write_file("src/auth.py", content_with_fix)
        [RESULT] ✅ File written

Turn 3  [LLM]: Let me verify with tests.
        [TOOL] run_command("pytest tests/test_auth.py")
        [RESULT] FAIL: ImportError: cannot import name 'TokenValidator' from 'auth.utils'

Turn 4  [LLM]: The test imports are broken. Let me check the actual exports.
        [TOOL] read_file("src/auth/utils.py")  
        [RESULT] ... the class is actually called `TokenCheck` not `TokenValidator` ...

Turn 5  [LLM]: I see — the class was renamed. Let me fix the test import.
        [TOOL] write_file("tests/test_auth.py", fixed_imports)
        [RESULT] ✅ File written

Turn 6  [LLM]: Running tests again.
        [TOOL] run_command("pytest tests/test_auth.py")
        [RESULT] All 12 tests passed.

Turn 7  [LLM]: The bug is fixed. The issue was a missing null check on user.token...
```

Notice Turn 3→4: the agent encountered a *different* error than expected, and naturally pivoted to investigate. It didn't need special code for this — the error message in the tool result was sufficient for the LLM to change strategy.

## TL;DR

The core loop is trivially simple — while loop, LLM call, tool execution, feed results back. What makes it work is:

1. **Full error output in context** — the LLM sees its own mistakes and self-corrects
2. **Verification after every change** — catch errors immediately, don't compound them  
3. **Rollback + pivot hints** — when stuck in a loop, mechanically inject "try something different"
4. **Error pattern dedup** — detect when the same error repeats and escalate the hint
5. **Good system prompt** — tells the agent the workflow: read → hypothesize → edit → verify → repeat

The "intelligence" is 90% the LLM itself. The harness is just the scaffolding that keeps it from going in circles.