---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 静默模块防护故障修复
translated: true
type: note
---

已保存到内存。反思摘要：

根本原因：`ww/main.py` 缺少 `if __name__ == "__main__": main()`。Hermes `/note` 插件通过子进程调用 `python -m ww.main note`——Python 导入了模块但从未执行任何操作。静默无操作，退出码为 0。

为何难以察觉：插件有一个安全检查，如果 `ww note watch` 未运行则会发出警告。由于 watcher 确实在运行，因此没有出现警告。插件打印了“Queued.”，用户以为已生效。典型的静默失败——无错误、无输出、无队列条目。

已应用两项修复：

1. `ww/main.py` — 末尾添加了 `if __name__ == "__main__": main()`
2. 插件 — 从 `sys.executable -m ww.main` 切换为 `shutil.which("ww")` CLI 调用

教训：任何可能通过 `python -m` 调用的 Python 模块都需要 `__main__` 守卫。值得检查整个代码库中其他入口点是否存在同样的问题。
