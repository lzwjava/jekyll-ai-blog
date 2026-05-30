---
audio: false
generated: true
image: false
lang: en
layout: post
title: Three-Agent CLI Development System
translated: false
type: note
---

Good, I have enough context on the ww project. Let me design the three-agent system.

**Question:** Design a three-agent system (coding agent, testing agent, documentation agent) for the `ww` CLI project with clean separation of concerns — each agent touches different files/values so they don't conflict.

**Answer:**

The key insight here is **file-system-level separation** — each agent owns distinct file categories, so they can run in parallel (or sequentially in a pipeline) without merge conflicts. Here's the full design:

---

## Agent Topology for `ww`

```
               ┌─────────────────────────────────┐
               │         Orchestrator             │
               │   (you / a top-level script)     │
               └────────┬────────┬────────┬───────┘
                        │        │        │
               ┌─────────┘  ┌────┘  ┌────┘
               ▼            ▼       ▼
         CodingAgent  TestingAgent  DocAgent
         owns: src/   owns: tests/  owns: docs/ README
```

---

## File Ownership (No Conflicts)

| Agent | Reads | Writes | Never touches |
|---|---|---|---|
| **CodingAgent** | `ww/**/*.py`, `pyproject.toml` | `ww/**/*.py`, new modules | `tests/`, `docs/`, `README.md` |
| **TestingAgent** | `ww/**/*.py` (read-only), `tests/` | `tests/**/*.py`, `pytest.ini` | `ww/` source, `docs/` |
| **DocAgent** | `ww/**/*.py` (read-only), `README.md` | `README.md`, `docs/**/*.md` | `ww/` source, `tests/` |

---

## Implementation: `agents/` directory in `ww`

### `agents/base_agent.py`

```python
import anthropic
import subprocess
from pathlib import Path
from abc import ABC, abstractmethod

client = anthropic.Anthropic()

class BaseAgent(ABC):
    name: str
    system_prompt: str
    owned_dirs: list[str]   # dirs this agent is allowed to write
    read_dirs: list[str]    # dirs this agent may read

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)

    def read_file(self, path: str) -> str:
        return (self.repo_root / path).read_text()

    def write_file(self, path: str, content: str):
        target = self.repo_root / path
        # Enforce ownership
        allowed = any(str(target).startswith(str(self.repo_root / d))
                      for d in self.owned_dirs)
        if not allowed:
            raise PermissionError(f"{self.name} cannot write to {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        print(f"[{self.name}] wrote {path}")

    def run_shell(self, cmd: str) -> str:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True,
                                cwd=self.repo_root)
        return result.stdout + result.stderr

    def call_llm(self, user_msg: str) -> str:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_msg}]
        )
        return response.content[0].text

    @abstractmethod
    def run(self, task: str) -> str:
        ...
```

---

### `agents/coding_agent.py`

```python
from .base_agent import BaseAgent
import ast, textwrap

class CodingAgent(BaseAgent):
    name = "CodingAgent"
    owned_dirs = ["ww"]          # writes only to ww/ source
    read_dirs = ["ww", "tests"]  # can read tests for context

    system_prompt = textwrap.dedent("""
        You are a Python CLI coding agent for the `ww` toolkit.
        Your job: implement new commands or fix bugs in ww/**/*.py.
        
        Rules:
        - Output ONLY valid Python code blocks, each prefixed with:
          FILE: <relative/path/to/file.py>
          ```python
          <code>
          ```
        - Never modify tests/ or docs/ or README.md.
        - Follow existing ww conventions: Click groups, LLM helpers via openai/anthropic clients.
        - Keep functions small, add type hints, docstrings.
    """)

    def run(self, task: str) -> str:
        # Collect relevant source context
        src_files = list((self.repo_root / "ww").rglob("*.py"))
        context = ""
        for f in src_files[:10]:  # limit context
            context += f"\n--- {f.relative_to(self.repo_root)} ---\n"
            context += f.read_text()[:500]  # truncate large files

        prompt = f"""
Current codebase context:
{context}

Task: {task}

Output the files to create/modify.
"""
        response = self.call_llm(prompt)
        files_written = self._apply_response(response)
        return f"CodingAgent wrote: {files_written}"

    def _apply_response(self, response: str) -> list[str]:
        """Parse FILE: blocks and write them."""
        import re
        written = []
        pattern = r"FILE:\s*(\S+)\s*```python\n(.*?)```"
        for match in re.finditer(pattern, response, re.DOTALL):
            path, code = match.group(1), match.group(2)
            # Validate it's syntactically correct before writing
            try:
                ast.parse(code)
            except SyntaxError as e:
                print(f"[CodingAgent] Skipping {path} — syntax error: {e}")
                continue
            self.write_file(path, code)
            written.append(path)
        return written
```

---

### `agents/testing_agent.py`

```python
from .base_agent import BaseAgent
import textwrap, re

class TestingAgent(BaseAgent):
    name = "TestingAgent"
    owned_dirs = ["tests"]       # writes only test files
    read_dirs = ["ww", "tests"]  # reads source to generate tests

    system_prompt = textwrap.dedent("""
        You are a Python testing agent for the `ww` CLI toolkit.
        Your job: write pytest tests for ww commands.
        
        Rules:
        - Output ONLY test code blocks prefixed with:
          FILE: tests/<test_file.py>
          ```python
          <code>
          ```
        - Use pytest, pytest-mock, Click's CliRunner for CLI tests.
        - Never modify ww/ source files or README.
        - Test: happy path, edge cases, error handling.
        - Mock external calls (LLM, network, filesystem writes).
    """)

    def run(self, task: str) -> str:
        # Read the source file being tested
        src_context = ""
        for f in (self.repo_root / "ww").rglob("*.py"):
            src_context += f"\n--- {f.relative_to(self.repo_root)} ---\n"
            src_context += f.read_text()[:800]

        # Run existing tests first to understand current state
        existing_results = self.run_shell("python -m pytest tests/ --tb=short -q 2>&1 | head -40")

        prompt = f"""
Source code:
{src_context}

Existing test results:
{existing_results}

Task: {task}

Write pytest tests. Output FILE: blocks only.
"""
        response = self.call_llm(prompt)
        written = self._apply_response(response)

        # Auto-run the new tests
        run_result = self.run_shell(f"python -m pytest tests/ -v --tb=short 2>&1 | tail -30")
        return f"TestingAgent wrote {written}\n\nTest results:\n{run_result}"

    def _apply_response(self, response: str) -> list[str]:
        written = []
        pattern = r"FILE:\s*(tests/\S+)\s*```python\n(.*?)```"
        for match in re.finditer(pattern, response, re.DOTALL):
            path, code = match.group(1), match.group(2)
            self.write_file(path, code)
            written.append(path)
        return written
```

---

### `agents/doc_agent.py`

```python
from .base_agent import BaseAgent
import textwrap, re

class DocAgent(BaseAgent):
    name = "DocAgent"
    owned_dirs = ["docs"]          # writes docs/
    read_dirs = ["ww", "docs"]     # reads source and existing docs
    # Special case: README.md is in root, handled explicitly

    system_prompt = textwrap.dedent("""
        You are a documentation agent for the `ww` CLI toolkit.
        Your job: keep README.md and docs/ up-to-date.
        
        Rules:
        - Output Markdown blocks prefixed with:
          FILE: README.md   (or docs/something.md)
          ```markdown
          <content>
          ```
        - Never modify ww/ source or tests/.
        - Extract command tables from source Click decorators.
        - Keep the README Commands section alphabetically sorted by group.
        - Docs tone: concise, example-first.
    """)

    def run(self, task: str) -> str:
        # Read source for command introspection
        src_context = self._extract_cli_commands()
        readme = (self.repo_root / "README.md").read_text()

        prompt = f"""
Current README (first 2000 chars):
{readme[:2000]}

Extracted CLI commands from source:
{src_context}

Task: {task}

Output FILE: blocks with updated markdown.
"""
        response = self.call_llm(prompt)
        written = self._apply_response(response)
        return f"DocAgent updated: {written}"

    def _extract_cli_commands(self) -> str:
        """Quick grep for Click @group.command() decorators."""
        result = self.run_shell(
            "grep -rn '@.*command\\|@click.group\\|help=' ww/ --include='*.py' | head -60"
        )
        return result

    def _apply_response(self, response: str) -> list[str]:
        written = []
        pattern = r"FILE:\s*(\S+\.md)\s*```(?:markdown)?\n(.*?)```"
        for match in re.finditer(pattern, response, re.DOTALL):
            path, content = match.group(1), match.group(2)
            if path == "README.md":
                # Special: README is at root, not in owned_dirs
                (self.repo_root / "README.md").write_text(content)
                written.append("README.md")
            else:
                self.write_file(path, content)
                written.append(path)
        return written
```

---

### `agents/orchestrator.py` — run all three

```python
#!/usr/bin/env python3
"""
ww multi-agent orchestrator.

Usage:
  python -m agents.orchestrator --task "add ww net ping-sweep command"
  python -m agents.orchestrator --agent coding --task "fix git classify bug"
"""
import argparse
from .coding_agent import CodingAgent
from .testing_agent import TestingAgent
from .doc_agent import DocAgent

def run_pipeline(task: str, repo_root: str = "."):
    """
    Sequential pipeline: code → test → doc.
    Each agent sees the freshly written files from the previous.
    """
    print(f"\n{'='*50}")
    print(f"Pipeline task: {task}")
    print('='*50)

    coding = CodingAgent(repo_root)
    testing = TestingAgent(repo_root)
    doc = DocAgent(repo_root)

    # 1. Coding agent implements
    print("\n[1/3] CodingAgent running...")
    code_result = coding.run(task)
    print(code_result)

    # 2. Testing agent writes tests for what was just implemented
    print("\n[2/3] TestingAgent running...")
    test_result = testing.run(f"Write tests for: {task}\n\nWhat was just implemented:\n{code_result}")
    print(test_result)

    # 3. Doc agent updates README/docs
    print("\n[3/3] DocAgent running...")
    doc_result = doc.run(f"Update docs for: {task}")
    print(doc_result)

    print("\n✅ Pipeline complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--agent", choices=["coding", "testing", "doc", "all"], default="all")
    parser.add_argument("--repo", default=".")
    args = parser.parse_args()

    if args.agent == "all":
        run_pipeline(args.task, args.repo)
    elif args.agent == "coding":
        CodingAgent(args.repo).run(args.task)
    elif args.agent == "testing":
        TestingAgent(args.repo).run(args.task)
    elif args.agent == "doc":
        DocAgent(args.repo).run(args.task)
```

---

## Usage

```bash
# Run full pipeline for a new feature
python -m agents.orchestrator --task "add ww net ping-sweep that scans a CIDR range"

# Run individual agents
python -m agents.orchestrator --agent coding --task "fix ww git classify to handle merge commits"
python -m agents.orchestrator --agent testing --task "add edge case tests for ww note obfuscate"
python -m agents.orchestrator --agent doc --task "update README with all new commands added this week"
```

---

## Why This Works (No Collision)

The collaboration is clean because of strict **write-domain isolation**:

- `CodingAgent` → only mutates `ww/*.py`. It's the producer.
- `TestingAgent` → only mutates `tests/*.py`. It reads source but never writes it.
- `DocAgent` → only mutates `README.md` and `docs/*.md`. It reads source to introspect CLI commands.

The pipeline is also **causally ordered**: code first → tests can reference real implementations → docs reflect final state. If you want parallelism, TestingAgent and DocAgent can run concurrently after CodingAgent finishes (they only read `ww/`, don't write it).

Next step: add a `--dry-run` flag so each agent prints diffs before writing, and wire it into a `ww agent` subcommand so you can call `ww agent run --task "..."` directly from the CLI.