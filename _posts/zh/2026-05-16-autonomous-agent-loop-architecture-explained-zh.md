---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自主代理循环架构解析
translated: true
type: note
---

以下是自主编码智能体（如 Copilot Agent）核心架构和循环逻辑的底层解释。

## 1. 基础智能体循环

最简单的智能体是一个在“思考”和“行动”之间交替的 while 循环：

```python
def agent_loop(task: str, max_iterations: int = 50):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task}
    ]

    for i in range(max_iterations):
        # THINK: 询问 LLM 下一步做什么
        response = llm.chat(messages=messages, tools=TOOL_SCHEMAS)

        # DONE: 没有工具调用意味着智能体认为任务已完成
        if not response.tool_calls:
            return response.content

        # ACT: 执行每个工具调用并将结果反馈回去
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call.name, tool_call.arguments)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # 助手消息（包含 tool_calls）也加入历史
        messages.append(response.message)

    return "Max iterations reached"
```

就这些。整个 Copilot Agent、Claude Code、Codex 等都是这个循环的扩展。神奇之处**不在于**循环本身——而在于三件事：系统提示词、工具定义以及如何处理错误。

## 2. 关键洞察：它如何“退后一步”

智能体并非在哲学意义上真正“反思”。它在机械层面上的运作方式如下：

```
迭代 1:  LLM 读取代码 → 提出修复方案 → 工具写入文件
迭代 2:  LLM 运行测试 → 看到失败 → 错误消息被放回上下文
迭代 3:  LLM 读取错误 → 意识到方法错误 → 尝试不同的修复
```

“退后一步”其实就是：**上一次迭代的错误输出成为下一次迭代的输入**。LLM 在对话历史中看到自己失败的尝试，自然就会尝试不同的方法。这源于：

- 保留完整的对话历史
- 错误消息足够具体，能揭示问题所在
- LLM 有足够的上下文来理解*为什么*第一种方法会失败

下面是具体模式：

```python
# 智能体尝试修复 A，测试失败：
messages = [
    system_prompt,
    user_task,
    assistant("我将修改认证中间件..."),  # 尝试 1
    tool_result("文件已写入：middleware.py"),
    assistant("让我运行测试"),
    tool_result("FAIL: AttributeError: 'NoneType' object has no attribute 'token'"),
    # ^^^ 这就是机械层面“退后一步”发生的地方
    assistant("我明白了——session 可能是 None。让我先添加一个空值检查..."),  # 尝试 2
]
```

## 3. 真正的架构：错误恢复策略

玩具级智能体与 Copilot Agent 的区别在于它如何**处理失败**。有几种策略：

### 策略 A：逐字错误注入（基础）

```python
# 直接将错误塞入下一轮 LLM
messages.append({
    "role": "tool",
    "content": f"ERROR: {stderr_output}\nExit code: {exit_code}"
})
```

LLM 读取错误并决定下一步怎么做。这是大多数智能体的做法。

### 策略 B：错误分类（高级）

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

# 注入分类后的上下文
error_msg = f"""
ERROR TYPE: {classify_error(stderr)}
EXIT CODE: {process.returncode}
STDERR:
{stderr[:2000]}
STDOUT:
{stdout[:500]}
"""
```

这有助于 LLM 更快地匹配已知的失败模式。

### 策略 C：每个子任务的迭代预算（Copilot 风格）

```python
class IterationBudget:
    def __init__(self, total: int = 50, per_subtask: int = 5):
        self.total = total
        self.per_subtask = per_subtask
        self.current_subtask_iterations = 0

    def should_try_different_approach(self) -> bool:
        """如果长时间卡在同一个子任务上，提示切换方向。"""
        return self.current_subtask_iterations >= self.per_subtask
```

当子任务的预算耗尽时，注入一条消息：

```python
if budget.should_try_different_approach():
    messages.append({
        "role": "user",
        "content": "你已经尝试这种方法几次都没有成功。"
                    "考虑一个完全不同的策略。"
    })
```

### 策略 D：基于差异的验证（Copilot 实际的做法）

```python
def execute_with_rollback(tool_call):
    """每次更改前保存状态，更改后验证。"""
    snapshot = git_create_stash()  # 或文件系统快照

    result = execute_tool(tool_call)

    # 写入后自动验证
    if tool_call.name == "write_file" or tool_call.name == "edit_file":
        verify_result = run_linter_and_tests()
        if verify_result.failed:
            # 回滚并告知 LLM 发生了什么
            git_restore_stash(snapshot)
            return f"更改导致测试失败：\n{verify_result.stderr}\n\n更改已被回滚。"

    return result
```

这就是“自我修复”行为：智能体做出更改，验证它，如果出现问题，在告知 LLM 之前自动回滚。LLM 永远不会累积错误。

## 4. 完整的智能体框架

下面是一个更完整的实现，展示了所有组件：

```python
import subprocess, json, os
from dataclasses import dataclass, field
from pathlib import Path

# ── 工具定义 ──────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取文件内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "将内容写入文件（创建或覆盖）",
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
            "description": "运行 shell 命令并返回输出",
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
            "description": "在文件中搜索模式（类似 grep）",
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

# ── 工具执行 ──────────────────────────────────────────────────

def execute_tool(name: str, args: dict) -> str:
    if name == "read_file":
        try:
            return Path(args["path"]).read_text()[:50000]
        except FileNotFoundError:
            return f"ERROR: 文件未找到：{args['path']}"

    elif name == "write_file":
        try:
            Path(args["path"]).parent.mkdir(parents=True, exist_ok=True)
            Path(args["path"]).write_text(args["content"])
            return f"成功写入 {len(args['content'])} 字符到 {args['path']}"
        except Exception as e:
            return f"ERROR 写入文件：{e}"

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
            return f"ERROR: 命令超时，限制时间 {args.get('timeout', 30)}s"

    elif name == "search_files":
        try:
            result = subprocess.run(
                f"grep -rn {args['pattern']} {args.get('path', '.')}",
                shell=True, capture_output=True, text=True, timeout=10
            )
            return result.stdout[:5000] or "未找到匹配"
        except Exception as e:
            return f"ERROR: {e}"

    return f"未知工具：{name}"

# ── 智能体框架 ───────────────────────────────────────────────

@dataclass
class AgentConfig:
    max_iterations: int = 50
    max_subtask_attempts: int = 3      # 每个子任务在切换方向前的尝试次数
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
            # ── LLM 决定下一步行动 ──
            response = self._call_llm(messages)

            # ── 没有工具调用 = 完成 ──
            if not response.tool_calls:
                return response.content

            # ── 执行每个工具调用 ──
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

        return "Agent 用尽了迭代预算"

    def _execute_with_recovery(self, tool_call, messages) -> str:
        """执行工具调用并自动进行错误恢复。"""
        result = execute_tool(tool_call.name, json.loads(tool_call.arguments))

        # ── 文件写入后自动验证 ──
        if self.config.auto_verify_after_write and tool_call.name in ("write_file", "edit_file"):
            verify_output = self._run_verification()

            if "FAIL" in verify_output or "ERROR" in verify_output:
                self.consecutive_failures += 1

                # ── 模式检测：同一错误重复出现？ ──
                current_error = self._extract_error_signature(verify_output)
                if current_error == self.last_error_pattern:
                    self.consecutive_failures += 2  # 重复时加重惩罚

                self.last_error_pattern = current_error

                # ── 如果配置了回滚 ──
                if self.config.auto_rollback_on_failure:
                    self._rollback_last_change(tool_call)
                    result += f"\n\n⚠️  验证失败（尝试 {self.consecutive_failures} 次）：\n{verify_output}\n更改已回滚。"

                # ── 切换方向提示：告诉 LLM 尝试其他方法 ──
                if self.consecutive_failures >= self.config.max_subtask_attempts:
                    result += (
                        "\n\n🔴 你在这个子任务上多次使用相同方法失败。"
                        "强烈建议：(1) 采用完全不同的解决方案策略，"
                        "(2) 阅读更多代码以理解根本原因，"
                        "(3) 简化你的方法。"
                    )
                    self.consecutive_failures = 0  # 注入切换提示后重置
            else:
                # 成功 — 重置计数器
                self.consecutive_failures = 0
                self.last_error_pattern = None
                result += f"\n\n✅ 验证通过。"

        return result

    def _run_verification(self) -> str:
        try:
            r = subprocess.run(
                self.config.verify_command, shell=True,
                capture_output=True, text=True, timeout=60
            )
            return r.stdout + r.stderr
        except subprocess.TimeoutExpired:
            return "ERROR: 验证超时"

    def _rollback_last_change(self, tool_call):
        """使用 git 或备份撤销最后一次文件写入。"""
        path = json.loads(tool_call.arguments).get("path", "")
        if path and Path(path).exists():
            subprocess.run(f"git checkout -- {path}", shell=True,
                         capture_output=True, timeout=10)

    def _extract_error_signature(self, output: str) -> str:
        """提取核心错误模式（去除行号）用于去重。"""
        import re
        # 移除行号和地址以标准化错误
        normalized = re.sub(r'line \d+', 'line N', output)
        normalized = re.sub(r'0x[0-9a-f]+', '0xADDR', normalized)
        return normalized[:200]

    def _call_llm(self, messages):
        """调用 LLM API — 替换为你的供应商。"""
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
        return """你是一个自主编码智能体。你可以读取文件、
写入文件、运行命令和搜索代码。

工作流程：
1. 首先，读取相关文件以理解代码库
2. 形成关于需要更改什么的假设
3. 进行最小、有针对性的更改
4. 通过运行测试/linter 验证你的更改
5. 如果验证失败，在再次尝试之前仔细阅读错误

关键规则：
- 如果一种更改首次失败，永远不要重复相同的更改
- 如果测试失败，在尝试修复之前阅读实际错误消息
- 当卡住时，阅读更多代码而不是猜测
- 更倾向于小的增量更改，而不是大规模重写
- 写入文件后始终进行验证

当你遇到同一问题的重复失败时：
- 退一步重新阅读相关代码
- 检查是否缺失了依赖或导入
- 考虑你对代码的心智模型可能是错误的
"""

# ── 使用示例 ──────────────────────────────────────────────────

if __name__ == "__main__":
    harness = AgentHarness()
    result = harness.run("修复 src/auth.py 中的登录错误——令牌过期的用户得到 500 而不是 401")
    print(result)
```

## 5. Copilot Agent 在此基础上添加了什么

上面的基本循环大约 200 行。Copilot Agent 增加了：

| 层 | 功能 | 为什么重要 |
| ------- | -------------- | ---------------- |
| **子智能体生成** | 将任务分解为子任务，并行运行 | 速度——多个文件同时编辑 |
| **上下文管理** | 滑动窗口 + 旧轮次的摘要 | 使长任务适合上下文限制 |
| **先计划后执行** | 第一次 LLM 调用生成计划，后续调用执行步骤 | 更好的任务分解 |
| **语义搜索** | 嵌入代码库，按查询检索相关片段 | 智能体无需读取每个文件就能找到代码 |
| **安全执行** | 沙盒文件系统，网络限制 | 不会删除你的仓库 |
| **检查点** | 每次成功验证步骤后 git 提交 | 轻松回滚到任何已知良好的状态 |
| **人工参与** | 在破坏性操作上暂停等待批准 | 安全网 |

## 6. 实践中的“自我修复”循环

以下是智能体遇到并修复问题时实际对话的样子：

```
第 1 轮  [LLM]: 我将修复认证错误。让我读取文件。
         [TOOL] read_file("src/auth.py")
         [RESULT] ... 代码显示 `user.token.verify()` 没有空值检查 ...

第 2 轮  [LLM]: 问题很明确——`user.token` 可能为 None。我将添加一个检查。
         [TOOL] write_file("src/auth.py", content_with_fix)
         [RESULT] ✅ 文件已写入

第 3 轮  [LLM]: 让我用测试验证一下。
         [TOOL] run_command("pytest tests/test_auth.py")
         [RESULT] FAIL: ImportError: cannot import name 'TokenValidator' from 'auth.utils'

第 4 轮  [LLM]: 测试导入有问题。让我检查实际导出的内容。
         [TOOL] read_file("src/auth/utils.py")
         [RESULT] ... 类实际上叫 `TokenCheck` 而不是 `TokenValidator` ...

第 5 轮  [LLM]: 我明白了——类被重命名了。让我修复测试导入。
         [TOOL] write_file("tests/test_auth.py", fixed_imports)
         [RESULT] ✅ 文件已写入

第 6 轮  [LLM]: 再次运行测试。
         [TOOL] run_command("pytest tests/test_auth.py")
         [RESULT] 全部 12 个测试通过。

第 7 轮  [LLM]: 错误已修复。问题在于 `user.token` 缺少空值检查...
```

注意第 3→4 轮：智能体遇到了一个*不同于*预期的错误，并自然转向去调查。它不需要特殊的代码——工具结果中的错误消息足以让 LLM 改变策略。

## TL;DR

核心循环非常简单——while 循环、LLM 调用、工具执行、将结果反馈回去。让它起作用的是：

1. **上下文中完整的错误输出**——LLM 看到自己的错误并自我纠正
2. **每次更改后验证**——立即捕获错误，不累积它们
3. **回滚 + 切换方向提示**——当陷入循环时，机械地注入“尝试不同方法”
4. **错误模式去重**——检测到同一错误重复时提升提示强度
5. **良好的系统提示词**——告诉智能体工作流程：读取 → 假设 → 编辑 → 验证 → 重复

“智能” 90% 来自 LLM 本身。框架只是防止它原地打转的脚手架。
