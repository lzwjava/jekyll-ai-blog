---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用prompt_async的异步REPL转换
translated: true
type: note
---

以下是提交 `f148313` 的完整说明：

**标题：** refactor: 将 REPL 循环转换为 async 并使用 prompt_async

**改动内容及原因：**

iclaw REPL 原先使用了 prompt_toolkit 的 `session.prompt()`（同步方式）。这种方式会在等待用户输入时阻塞线程，对于简单的 CLI 来说没问题，但限制了未来的扩展性——例如运行后台任务、处理异步工具回调、或与异步原生库集成。

**iclaw/main.py（2 处改动）：**

1. 在顶部添加了 `import asyncio`。
2. 将 `main()` 拆分为两个函数：
   - `main()` —— 薄封装，调用 `asyncio.run(_main())`
   - `async _main()` —— 实际的 REPL 逻辑，现在为异步
3. 将 `session.prompt("> ")` 改为 `await session.prompt_async("> ")`

REPL 的其余逻辑（工具调用循环、token 刷新、命令处理）在异步函数内部仍为同步——目前只在 prompt 调用上用了 `await`。这是一个过渡步骤：异步外壳已搭建好，后续可以逐步将各个操作迁移为 `await`。

**tests/test_main.py（2 处改动）：**

1. `_mock_session()` —— 更新为模拟 `prompt_async` 而非 `prompt`。添加了一个 `async def _async_side_effect()`，按顺序返回输入（对错误输入抛出异常）。保留 `.prompt()` 作为安全的空操作回退。

2. `test_token_refresh` —— 这个比较棘手。`asyncio.run()` 内部会调用 `time.monotonic()` 进行关闭/生成器清理，这会导致从 `side_effect=[0, 99999, ...]` 列表中不可预测地消费条目。将静态的 side_effect 列表替换为可调用对象 `_monotonic()`，它跟踪调用计数：前 2 次调用（asyncio 内部 + 启动）返回 `0`，然后返回 `99999` 以触发 token 刷新检查。这使得测试不受 asyncio 内部调用 monotonic 的次数影响，变得确定。

**Pre-commit：**
- 第一次提交尝试失败——ruff 修复了测试文件中未使用的 `import asyncio`（它被添加了，但 `asyncio` 没有在模块作用域内直接调用；async def 隐式使用了它）。
- 第二次尝试通过了 ruff 和 ruff-format。

**净效果：** 2 个文件增加 41 行，删除 3 行。对用户无行为变化——REPL 的工作方式完全相同，只是现在在异步事件循环下运行。