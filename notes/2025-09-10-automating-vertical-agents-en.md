---
audio: false
date: 2025-09-10
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Automating Vertical Agents with Validation
translated: false
type: note
---

Short answer: you’re **mostly right**. The scalable way is to build **vertical, coded agents** that call LLM APIs, plus strong **automatic validation**. You still want a “human-on-exception” loop, not “human-never,” because reality includes API hiccups, drift, and edge cases. But on well-scoped tasks with good checks, you can run **fully automated**.

Below is a practical blueprint you can implement.

# What “fully automated” really takes

* **Deterministic scaffolding**: code plans/templates generated once, then **parameterized**; don’t “re-prompt from scratch” every run.
* **Typed, schema’d I/O**: force the LLM to return JSON that your code validates before use.
* **Grounded checks**: validate outputs against tools, compilers, unit tests, linters, HTTP mocks, SQL schemas, etc.
* **Risk gating**: only auto-apply changes when confidence + checks pass; otherwise raise a ticket/PR for review.
* **Observability**: logs, traces, cost/latency meters, success rates, drift/alarm thresholds.
* **Defense in depth**: multi-model cross-checks, self-consistency votes, sandbox exec, diff size limits, allowlists/denylists.

# Reference architecture (minimal but solid)

* **Controller**: reads tasks from a queue (Kafka/SQS/Redis/simple DB).
* **Planner** (LLM): turns task into a concrete plan and structured steps.
* **Executors** (tools + LLM where needed): code edits, API calls, file ops.
* **Validators**: schema/type checks, static analysis, unit tests, golden tests.
* **Policy Engine**: decides auto-merge vs. “needs human.”
* **Reporter**: opens PRs, creates issues, posts Slack/Email summaries.

# Validation patterns that actually work

* JSON schema + retries until valid.
* AST parse + basic semantics (e.g., ensure class/method exists).
* Run **ruff/mypy/flake8**, **pytest** with coverage threshold, **bandit** for sec.
* For text/data: regex invariants, reference answers, BLEU/ROUGE thresholds, or bespoke business rules.
* For calling external systems: mock/stub first; canary in prod with **read-only** or **shadow** mode; then progressive rollout.

---

# Starter: Python “vertical agent” skeleton

This runs tasks in parallel, forces JSON output, validates, runs local checks, and either auto-applies or opens a PR. Swap the `call_llm()` stub with your provider/router.

```python
import asyncio, json, os, re, subprocess, time
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, List, Tuple, Callable

# ---------- Task spec ----------
@dataclass
class Task:
    id: str
    kind: str            # e.g., "refactor", "write_test", "doc_summarize"
    repo_path: str
    target: str          # file/path/module or URL
    spec: Dict[str, Any] # free-form details

# ---------- LLM call (stub your router here) ----------
async def call_llm(system: str, user: str, schema_hint: str, max_retries=3) -> Dict[str, Any]:
    """
    Return structured JSON. Your real impl: Anthropic/OpenAI/Gemini/Mistral router with
    tool forcing / JSON mode / 'respond_with_schema' etc.
    """
    last_err = None
    for _ in range(max_retries):
        # >>> replace with real API call in JSON mode <<<
        fake = {"plan": ["edit file", "run tests"], "edits":[{"path":"foo.py","patch":"print('ok')\n"}], "confidence": 0.92}
        try:
            # Validate basic fields early
            if not isinstance(fake.get("edits"), list): raise ValueError("bad edits")
            return fake
        except Exception as e:
            last_err = e
    raise RuntimeError(f"LLM failed to produce valid JSON: {last_err}")

# ---------- Validators ----------
def json_schema_validate(payload: Dict[str, Any]) -> Tuple[bool, str]:
    if "edits" not in payload: return False, "missing edits"
    for e in payload["edits"]:
        if "path" not in e or "patch" not in e:
            return False, f"bad edit item: {e}"
    return True, "ok"

def apply_patch(repo_path: str, path: str, patch: str) -> None:
    abs_path = os.path.join(repo_path, path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "a", encoding="utf-8") as f:
        f.write("\n" + patch)

def run_cmd(cmd: List[str], cwd: Optional[str]=None, timeout: int=300) -> Tuple[int, str]:
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        out, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        return 124, "timeout"
    return proc.returncode, out

def static_checks(repo_path: str) -> Tuple[bool, str]:
    # Swap in your tools: ruff, mypy, eslint, mvn test, gradle, etc.
    codes = []
    outputs = []

    # Example Python checks; guard if tools missing.
    for cmd in [["python","-m","py_compile","."]]:
        rc, out = run_cmd(cmd, cwd=repo_path)
        codes.append(rc); outputs.append(out or "")
    ok = all(rc == 0 for rc in codes)
    return ok, "\n".join(outputs)

def unit_tests(repo_path: str) -> Tuple[bool, str]:
    # Replace with pytest/mvn/gradle/npm test as needed
    if not os.path.exists(os.path.join(repo_path, "tests")):
        return True, "no tests dir, skipping"
    rc, out = run_cmd(["pytest","-q"], cwd=repo_path)
    return rc == 0, out

def policy_decision(confidence: float, static_ok: bool, tests_ok: bool, max_diff_lines: int, diff_lines: int) -> str:
    if confidence >= 0.9 and static_ok and tests_ok and diff_lines <= max_diff_lines:
        return "AUTO_APPLY"
    return "REVIEW"

def compute_diff_size(repo_path: str) -> int:
    rc, out = run_cmd(["git","-c","color.ui=never","diff"], cwd=repo_path)
    if rc != 0: return 10**9
    return len(out.splitlines())

# ---------- Worker ----------
async def worker(task: Task, max_diff_lines=800) -> Dict[str, Any]:
    system_prompt = "You are a strict code agent. Output JSON only and follow the schema."
    user_prompt = json.dumps(asdict(task), ensure_ascii=False)
    schema_hint = '{"plan":[str], "edits":[{"path":str,"patch":str}], "confidence": float}'

    payload = await call_llm(system_prompt, user_prompt, schema_hint)
    ok, why = json_schema_validate(payload)
    if not ok:
        return {"task": task.id, "status":"FAILED", "reason": f"schema: {why}"}

    # Apply edits in sandbox branch
    run_cmd(["git","checkout","-B", f"agent/{task.id}"], cwd=task.repo_path)
    for e in payload["edits"]:
        apply_patch(task.repo_path, e["path"], e["patch"])
    run_cmd(["git","add","-A"], cwd=task.repo_path)
    run_cmd(["git","commit","-m", f"agent: {task.kind} {task.target}"], cwd=task.repo_path)

    # Validate
    static_ok, static_out = static_checks(task.repo_path)
    tests_ok, tests_out = unit_tests(task.repo_path)
    diff_lines = compute_diff_size(task.repo_path)
    decision = policy_decision(payload.get("confidence",0.0), static_ok, tests_ok, max_diff_lines, diff_lines)

    result = {
        "task": task.id,
        "decision": decision,
        "confidence": payload.get("confidence"),
        "static_ok": static_ok,
        "tests_ok": tests_ok,
        "diff_lines": diff_lines,
    }

    if decision == "AUTO_APPLY":
        # merge to main; or push & auto-merge via CI rules
        run_cmd(["git","checkout","main"], cwd=task.repo_path)
        run_cmd(["git","merge","--no-ff", f"agent/{task.id}"], cwd=task.repo_path)
        result["status"] = "APPLIED"
    else:
        # open PR via your CI bot instead of merging directly
        result["status"] = "REVIEW"
        result["note"] = "Opened PR or created issue for human-on-exception."
    return result

# ---------- Orchestrator ----------
async def run_queue(tasks: List[Task], concurrency: int = 4) -> List[Dict[str, Any]]:
    sem = asyncio.Semaphore(concurrency)
    results = []
    async def run_one(t: Task):
        async with sem:
            try:
                res = await worker(t)
            except Exception as e:
                res = {"task": t.id, "status":"FAILED", "reason": repr(e)}
            results.append(res)
    await asyncio.gather(*(run_one(t) for t in tasks))
    return results

# Example usage:
# asyncio.run(run_queue([Task(id="1", kind="refactor", repo_path="/path/to/repo", target="foo.py", spec={"goal":"extract fn"})]))
```

## How this gets you “no chat, just code”

* The **planner** produces structured edits.
* The **validators** gate correctness.
* The **policy engine** auto-applies safe diffs, routes the rest to review.
* You don’t “talk” to a chatbot. You submit tasks (YAML/JSON or CLI), and the system executes.

---

# Upgrades you’ll likely add

* **Multi-model router** with fallbacks and self-consistency voting.
* **JSON-mode enforcement** with a tool that re-prompts until schema-valid.
* **Domain validators**: DB migrations dry-run, API contract checks (OpenAPI), load tests.
* **Artifact store** for plans, diffs, logs; Grafana dashboards for SLIs/SLOs.
* **Secrets & data governance**: scoped tokens, redaction, allowlisted repos.

---

# When you can truly go “fully unattended”

* The task is **narrow** and repeatable (e.g., doc sync, boilerplate test stubs, routine refactors).
* You have **good oracle tests** or strong invariants.
* You’ve run **shadow/canary** successfully with zero-touch for a while.
* Blast radius is limited (small diffs, reversible, sandboxed).

For everything else, keep **human-on-exception**. You’ll still get 80–95% of the productivity wins without risking silent failures.

If you want, I can adapt the skeleton to your exact stack (Python/Java Maven, Ruff/Mypy/PyTest, or Maven/Gradle + SpotBugs/Checkstyle/JUnit) and wire it to your router config.
