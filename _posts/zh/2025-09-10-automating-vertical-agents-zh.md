---
audio: false
date: 2025-09-10
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 自动化垂直智能体的验证流程
translated: true
type: note
---

简短回答：你**基本正确**。可扩展的方式是构建**垂直的、编码化的智能体**来调用LLM API，并配合强大的**自动化验证**。你仍然需要"异常时人工介入"的循环，而非"完全无需人工"，因为现实情况包括API故障、模型漂移和边缘案例。但对于范围明确且具备良好检查机制的任务，你可以实现**全自动化运行**。

以下是可实施的实用蓝图。

# 实现"全自动化"的真正要素

* **确定性框架**：代码计划/模板只需生成一次，然后进行**参数化**；不要每次运行都"从头开始重新提示"
* **类型化、模式化的输入输出**：强制LLM返回JSON格式，并在使用前由代码进行验证
* **基础检查**：通过工具、编译器、单元测试、代码检查器、HTTP模拟、SQL模式等验证输出
* **风险门控**：仅在置信度和检查通过时自动应用更改；否则创建审查工单/PR
* **可观测性**：日志、追踪、成本/延迟监控、成功率、漂移/警报阈值
* **深度防御**：多模型交叉检查、自一致性投票、沙箱执行、差异大小限制、白名单/黑名单

# 参考架构（精简而可靠）

* **控制器**：从队列（Kafka/SQS/Redis/简单数据库）读取任务
* **规划器**（LLM）：将任务转化为具体计划和结构化步骤
* **执行器**（工具+必要时使用LLM）：代码编辑、API调用、文件操作
* **验证器**：模式/类型检查、静态分析、单元测试、黄金测试
* **策略引擎**：决定自动合并或"需要人工介入"
* **报告器**：创建PR、生成问题、发送Slack/邮件摘要

# 实际有效的验证模式

* JSON模式验证+重试直至有效
* AST解析+基础语义检查（确保类/方法存在）
* 运行**ruff/mypy/flake8**，**pytest**（含覆盖率阈值），**bandit**安全扫描
* 文本/数据：正则表达式不变量、参考答案、BLEU/ROUGE阈值或定制业务规则
* 调用外部系统：先进行模拟/桩测试；生产环境金丝雀部署采用**只读**或**影子**模式；然后逐步推广

---

# 入门：Python"垂直智能体"框架

该框架支持并行执行任务，强制JSON输出，进行验证，运行本地检查，并自动应用更改或创建PR。请将`call_llm()`桩函数替换为您的提供商/路由器。

```python
import asyncio, json, os, re, subprocess, time
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional, List, Tuple, Callable

# ---------- 任务规范 ----------
@dataclass
class Task:
    id: str
    kind: str            # 例如："refactor", "write_test", "doc_summarize"
    repo_path: str
    target: str          # 文件/路径/模块或URL
    spec: Dict[str, Any] # 自由格式详细信息

# ---------- LLM调用（在此替换为您的路由器） ----------
async def call_llm(system: str, user: str, schema_hint: str, max_retries=3) -> Dict[str, Any]:
    """
    返回结构化JSON。真实实现：Anthropic/OpenAI/Gemini/Mistral路由器配合
    工具强制/JSON模式/'respond_with_schema'等功能
    """
    last_err = None
    for _ in range(max_retries):
        # >>> 替换为实际的JSON模式API调用 <<<
        fake = {"plan": ["edit file", "run tests"], "edits":[{"path":"foo.py","patch":"print('ok')\n"}], "confidence": 0.92}
        try:
            # 提前验证基础字段
            if not isinstance(fake.get("edits"), list): raise ValueError("bad edits")
            return fake
        except Exception as e:
            last_err = e
    raise RuntimeError(f"LLM failed to produce valid JSON: {last_err}")

# ---------- 验证器 ----------
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
    # 替换为您的工具：ruff, mypy, eslint, mvn test, gradle等
    codes = []
    outputs = []

    # Python检查示例；如果工具缺失则跳过
    for cmd in [["python","-m","py_compile","."]]:
        rc, out = run_cmd(cmd, cwd=repo_path)
        codes.append(rc); outputs.append(out or "")
    ok = all(rc == 0 for rc in codes)
    return ok, "\n".join(outputs)

def unit_tests(repo_path: str) -> Tuple[bool, str]:
    # 根据需要替换为pytest/mvn/gradle/npm test
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

# ---------- 工作器 ----------
async def worker(task: Task, max_diff_lines=800) -> Dict[str, Any]:
    system_prompt = "You are a strict code agent. Output JSON only and follow the schema."
    user_prompt = json.dumps(asdict(task), ensure_ascii=False)
    schema_hint = '{"plan":[str], "edits":[{"path":str,"patch":str}], "confidence": float}'

    payload = await call_llm(system_prompt, user_prompt, schema_hint)
    ok, why = json_schema_validate(payload)
    if not ok:
        return {"task": task.id, "status":"FAILED", "reason": f"schema: {why}"}

    # 在沙箱分支中应用编辑
    run_cmd(["git","checkout","-B", f"agent/{task.id}"], cwd=task.repo_path)
    for e in payload["edits"]:
        apply_patch(task.repo_path, e["path"], e["patch"])
    run_cmd(["git","add","-A"], cwd=task.repo_path)
    run_cmd(["git","commit","-m", f"agent: {task.kind} {task.target}"], cwd=task.repo_path)

    # 验证
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
        # 合并到main；或通过CI规则推送和自动合并
        run_cmd(["git","checkout","main"], cwd=task.repo_path)
        run_cmd(["git","merge","--no-ff", f"agent/{task.id}"], cwd=task.repo_path)
        result["status"] = "APPLIED"
    else:
        # 通过CI机器人创建PR而非直接合并
        result["status"] = "REVIEW"
        result["note"] = "Opened PR or created issue for human-on-exception."
    return result

# ---------- 编排器 ----------
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

# 使用示例：
# asyncio.run(run_queue([Task(id="1", kind="refactor", repo_path="/path/to/repo", target="foo.py", spec={"goal":"extract fn"})]))
```

## 如何实现"无需对话，只需代码"

* **规划器**生成结构化编辑
* **验证器**确保正确性
* **策略引擎**自动应用安全差异，其余路由至审查
* 您无需与聊天机器人"对话"。只需提交任务（YAML/JSON或CLI），系统即会执行

---

# 您可能需要添加的升级功能

* **多模型路由器**，含回退机制和自一致性投票
* **JSON模式强制**，配合重新提示直至模式有效的工具
* **领域验证器**：数据库迁移试运行、API合约检查（OpenAPI）、负载测试
* **工件存储**：用于计划、差异、日志；Grafana仪表板用于SLI/SLO监控
* **密钥与数据治理**：范围化令牌、数据脱敏、仓库白名单

---

# 何时能真正实现"完全无人值守"

* 任务**范围明确**且可重复（例如文档同步、样板测试桩、常规重构）
* 具备**良好的预言测试**或强不变量
* **影子/金丝雀**测试已成功运行一段时间且实现零接触
* 影响范围有限（差异小、可逆、沙箱化）

对于其他情况，请保持**异常时人工介入**。这样您仍能获得80-95%的生产力提升，同时避免静默失败的风险。

如果需要，我可以根据您的具体技术栈（Python/Java Maven、Ruff/Mypy/PyTest，或Maven/Gradle + SpotBugs/Checkstyle/JUnit）调整此框架，并连接到您的路由器配置。
