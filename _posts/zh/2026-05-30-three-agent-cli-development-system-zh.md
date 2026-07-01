---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 三代理命令行界面开发系统
translated: true
type: note
---

好的，我已经对 `ww` 项目有了足够的了解。让我设计这三个 agent 系统。

**问题：** 为 `ww` CLI 项目设计一个三 agent 系统（编码 agent、测试 agent、文档 agent），要求职责清晰分离——每个 agent 操作不同的文件/值，避免冲突。

**答案：**

关键思路是**文件系统级别的分离**——每个 agent 拥有不同的文件类别，因此它们可以并行运行（或按顺序流水线运行）而不会产生合并冲突。以下是完整设计：

---

## `ww` 的 Agent 拓扑

```
               ┌─────────────────────────────────┐
               │         编排器 (Orchestrator)     │
               │    (你 / 一个顶层脚本)            │
               └────────┬────────┬────────┬───────┘
                        │        │        │
               ┌─────────┘  ┌────┘  ┌────┘
               ▼            ▼       ▼
         CodingAgent  TestingAgent  DocAgent
         拥有: src/   拥有: tests/  拥有: docs/ README
```

---

## 文件归属（无冲突）

| Agent | 读取 | 写入 | 从不触碰 |
| --- | --- | --- | --- |
| **CodingAgent** | `ww/**/*.py`, `pyproject.toml` | `ww/**/*.py`, 新模块 | `tests/`, `docs/`, `README.md` |
| **TestingAgent** | `ww/**/*.py` (只读), `tests/` | `tests/**/*.py`, `pytest.ini` | `ww/` 源码, `docs/` |
| **DocAgent** | `ww/**/*.py` (只读), `README.md` | `README.md`, `docs/**/*.md` | `ww/` 源码, `tests/` |

---

## 实现：`ww` 下的 `agents/` 目录

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
    owned_dirs: list[str]   # 该 agent 允许写入的目录
    read_dirs: list[str]    # 该 agent 允许读取的目录

    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)

    def read_file(self, path: str) -> str:
        return (self.repo_root / path).read_text()

    def write_file(self, path: str, content: str):
        target = self.repo_root / path
        # 强制执行所有权
        allowed = any(str(target).startswith(str(self.repo_root / d))
                      for d in self.owned_dirs)
        if not allowed:
            raise PermissionError(f"{self.name} 无法写入 {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        print(f"[{self.name}] 已写入 {path}")

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
    owned_dirs = ["ww"]          # 仅写入 ww/ 源码
    read_dirs = ["ww", "tests"]  # 可读取测试文件以获取上下文

    system_prompt = textwrap.dedent("""
        你是 `ww` 工具集的 Python CLI 编码 agent。
        你的工作：在 ww/**/*.py 中实现新命令或修复 bug。

        规则：
        - 仅输出有效的 Python 代码块，每个代码块前缀为：
          FILE: <relative/path/to/file.py>
          ```python
          <code>
          ```
        - 绝不要修改 tests/、docs/ 或 README.md。
        - 遵循现有的 ww 约定：Click 组、通过 openai/anthropic 客户端的 LLM 辅助函数。
        - 保持函数小巧，添加类型提示和文档字符串。
    """)

    def run(self, task: str) -> str:
        # 收集相关源码上下文
        src_files = list((self.repo_root / "ww").rglob("*.py"))
        context = ""
        for f in src_files[:10]:  # 限制上下文大小
            context += f"\n--- {f.relative_to(self.repo_root)} ---\n"
            context += f.read_text()[:500]  # 截断大文件

        prompt = f"""
当前代码库上下文：
{context}

任务：{task}

输出要创建/修改的文件。
"""
        response = self.call_llm(prompt)
        files_written = self._apply_response(response)
        return f"CodingAgent 已写入：{files_written}"

    def _apply_response(self, response: str) -> list[str]:
        """解析 FILE: 块并写入它们。"""
        import re
        written = []
        pattern = r"FILE:\s*(\S+)\s*```python\n(.*?)```"
        for match in re.finditer(pattern, response, re.DOTALL):
            path, code = match.group(1), match.group(2)
            # 写入前验证语法是否正确
            try:
                ast.parse(code)
            except SyntaxError as e:
                print(f"[CodingAgent] 跳过 {path} —— 语法错误：{e}")
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
    owned_dirs = ["tests"]       # 仅写入测试文件
    read_dirs = ["ww", "tests"]  # 读取源码以生成测试

    system_prompt = textwrap.dedent("""
        你是 `ww` CLI 工具集的 Python 测试 agent。
        你的工作：为 ww 命令编写 pytest 测试。

        规则：
        - 仅输出测试代码块，前缀为：
          FILE: tests/<test_file.py>
          ```python
          <code>
          ```
        - 使用 pytest、pytest-mock、Click 的 CliRunner 进行 CLI 测试。
        - 绝不要修改 ww/ 源码文件或 README。
        - 测试：快乐路径、边缘情况、错误处理。
        - 模拟外部调用（LLM、网络、文件系统写入）。
    """)

    def run(self, task: str) -> str:
        # 读取被测试的源文件
        src_context = ""
        for f in (self.repo_root / "ww").rglob("*.py"):
            src_context += f"\n--- {f.relative_to(self.repo_root)} ---\n"
            src_context += f.read_text()[:800]

        # 先运行现有测试，了解当前状态
        existing_results = self.run_shell("python -m pytest tests/ --tb=short -q 2>&1 | head -40")

        prompt = f"""
源代码：
{src_context}

现有测试结果：
{existing_results}

任务：{task}

编写 pytest 测试。仅输出 FILE: 块。
"""
        response = self.call_llm(prompt)
        written = self._apply_response(response)

        # 自动运行新测试
        run_result = self.run_shell(f"python -m pytest tests/ -v --tb=short 2>&1 | tail -30")
        return f"TestingAgent 已写入 {written}\n\n测试结果：\n{run_result}"

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
    owned_dirs = ["docs"]          # 写入 docs/
    read_dirs = ["ww", "docs"]     # 读取源码和现有文档
    # 特殊情况：README.md 在根目录，明确处理

    system_prompt = textwrap.dedent("""
        你是 `ww` CLI 工具集的文档 agent。
        你的工作：保持 README.md 和 docs/ 最新。

        规则：
        - 输出 Markdown 块，前缀为：
          FILE: README.md   （或 docs/something.md）
          ```markdown
          <content>
          ```
        - 绝不要修改 ww/ 源码或 tests/。
        - 从源码中的 Click 装饰器提取命令表。
        - 保持 README 的 Commands 部分按组字母顺序排序。
        - 文档风格：简洁，示例优先。
    """)

    def run(self, task: str) -> str:
        # 读取源码以进行命令内省
        src_context = self._extract_cli_commands()
        readme = (self.repo_root / "README.md").read_text()

        prompt = f"""
当前 README（前 2000 字符）：
{readme[:2000]}

从源码中提取的 CLI 命令：
{src_context}

任务：{task}

输出带有更新后 Markdown 的 FILE: 块。
"""
        response = self.call_llm(prompt)
        written = self._apply_response(response)
        return f"DocAgent 已更新：{written}"

    def _extract_cli_commands(self) -> str:
        """快速 grep 查找 Click @group.command() 装饰器。"""
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
                # 特殊情况：README 在根目录，不在 owned_dirs 中
                (self.repo_root / "README.md").write_text(content)
                written.append("README.md")
            else:
                self.write_file(path, content)
                written.append(path)
        return written
```

---

### `agents/orchestrator.py` —— 运行所有三个 agent

```python
#!/usr/bin/env python3
"""
ww 多 agent 编排器。

用法：
  python -m agents.orchestrator --task "添加 ww net ping-sweep 命令"
  python -m agents.orchestrator --agent coding --task "修复 ww git classify 中的 bug"
  python -m agents.orchestrator --agent testing --task "为 ww note obfuscate 添加边缘情况测试"
  python -m agents.orchestrator --agent doc --task "更新 README，包含本周新增的所有命令"
"""
import argparse
from .coding_agent import CodingAgent
from .testing_agent import TestingAgent
from .doc_agent import DocAgent

def run_pipeline(task: str, repo_root: str = "."):
    """
    顺序流水线：代码 → 测试 → 文档。
    每个 agent 都能看到前一个 agent 刚刚写入的文件。
    """
    print(f"\n{'='*50}")
    print(f"流水线任务：{task}")
    print('='*50)

    coding = CodingAgent(repo_root)
    testing = TestingAgent(repo_root)
    doc = DocAgent(repo_root)

    # 1. 编码 agent 实现
    print("\n[1/3] CodingAgent 运行中...")
    code_result = coding.run(task)
    print(code_result)

    # 2. 测试 agent 为刚刚实现的内容编写测试
    print("\n[2/3] TestingAgent 运行中...")
    test_result = testing.run(f"为以下内容编写测试：{task}\n\n刚刚实现的内容：\n{code_result}")
    print(test_result)

    # 3. 文档 agent 更新 README/docs
    print("\n[3/3] DocAgent 运行中...")
    doc_result = doc.run(f"更新以下内容的文档：{task}")
    print(doc_result)

    print("\n✅ 流水线完成。")

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

## 使用方法

```bash
# 为新功能运行完整流水线
python -m agents.orchestrator --task "添加 ww net ping-sweep，扫描一个 CIDR 范围"

# 运行单个 agent
python -m agents.orchestrator --agent coding --task "修复 ww git classify 以处理合并提交"
python -m agents.orchestrator --agent testing --task "为 ww note obfuscate 添加边缘情况测试"
python -m agents.orchestrator --agent doc --task "更新 README，包含本周新增的所有命令"
```

---

## 为什么这样可行（无冲突）

这种协作之所以干净，是因为严格的**写入域隔离**：

- `CodingAgent` → 仅修改 `ww/*.py`。它是生产者。
- `TestingAgent` → 仅修改 `tests/*.py`。它读取源码但从不写入。
- `DocAgent` → 仅修改 `README.md` 和 `docs/*.md`。它读取源码以内省 CLI 命令。

流水线也是**因果有序的**：先有代码 → 测试可以引用真实实现 → 文档反映最终状态。如果你想要并行，TestingAgent 和 DocAgent 可以在 CodingAgent 完成后同时运行（它们只读 `ww/`，不写入）。

下一步：添加 `--dry-run` 标志，使每个 agent 在写入前打印 diff，并将其接入 `ww agent` 子命令，这样你就可以直接从 CLI 调用 `ww agent run --task "..."`。
