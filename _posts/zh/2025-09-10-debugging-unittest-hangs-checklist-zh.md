---
audio: false
date: 2025-09-10
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 调试单元测试卡死清单
translated: true
type: note
---

`unittest` 中的卡顿通常源于死锁（线程/异步）、I/O 阻塞、子进程/多进程问题，或测试在等待网络调用。以下是一份精要排查清单，用于*定位卡顿位置*并*解决问题*——适用于 Python 3.9–3.11。

### 1) 以详细模式运行 unittest（并确保正确执行）

```bash
# 若 xx.py 调用了 unittest.main()
python xx.py -v

# 或使用发现模式（推荐）
python -m unittest -v
python -m unittest discover -v -s tests -p "test_*.py"
```

> 注意：`python -v` 是**解释器导入详细模式**，而非测试详细模式。需使用 `-m unittest -v` 查看测试名称和进度。

### 2) 启用故障处理程序 + 开发模式（卡顿时输出堆栈转储，强化警告）

```bash
# 一次性执行
python -X faulthandler -X dev -u -m unittest -v
# 或通过环境变量
export PYTHONFAULTHANDLER=1
python -X dev -u -m unittest -v
```

* `-X faulthandler` 让 Python 在收到致命信号/超时时打印线程堆栈跟踪。
* `-X dev` 增强警告/错误提示强度。
* `-u` 解除标准输出/错误流的缓冲，实现*实时*输出显示。

### 3) 在疑似卡顿时强制获取跟踪信息

方案 A —— 在另一终端执行（Linux/macOS）：

```bash
kill -SIGUSR1 <进程号>  # 启用故障处理程序后，会输出所有线程堆栈
```

方案 B —— 在测试启动代码中添加（置于 `xx.py` 顶部）：

```python
import faulthandler, signal, sys
faulthandler.enable()
# 收到 SIGUSR1 信号时输出堆栈：
faulthandler.register(signal.SIGUSR1, all_threads=True)
# 若卡顿超过 120 秒自动输出：
faulthandler.dump_traceback_later(120, repeat=True)
```

### 4) 逐步跟踪执行过程（效果显著但资源密集）

```bash
python -m trace --trace xx.py
# 或
python -m trace --trace -m unittest discover -v
```

您将看到每行代码的执行过程；当输出“停滞”时即为卡顿位置。

### 5) 立即启用调试器

```bash
python -m pdb xx.py         # 若 xx.py 调用了 unittest.main()
# 在可疑行设置断点：
# (Pdb) b 模块名.py:行号
# (Pdb) c
```

对于发现模式运行，可在可疑位置添加 `import pdb; pdb.set_trace()`。

### 6) 常见原因与快速修复

* **macOS/Windows 多进程问题**：始终保护测试入口。

  ```python
  if __name__ == "__main__":
      import unittest
      unittest.main()
  ```

  若在 macOS 的测试中创建子进程：

  ```python
  import multiprocessing as mp
  if __name__ == "__main__":
      mp.set_start_method("fork")  # 相比默认 "spawn" 有时可避免卡顿
  ```

  （仅当确认代码兼容 fork 时使用。）

* **线程死锁**：检查无超时的 `join()`、未释放的锁，或后台线程等待主线程。将：

  ```python
  t.join()
  ```

  替换为：

  ```python
  t.join(timeout=5); assert not t.is_alive()
  ```

* **异步测试**：确保使用 `IsolatedAsyncioTestCase`（3.8+）或 `asyncio.run()`。重复事件循环或遗漏 `await` 常导致卡顿。

* **网络调用**：为所有操作添加**短超时**：

  ```python
  requests.get(网址, timeout=5)
  ```

* **标准输入等待**：移除 `input()` 或在测试中加以保护；CI/标准输入可能永久阻塞。

* **模拟异常**：被模拟的方法未解析 `Future`/承诺，或存根服务器未启动。

### 7) 增强可见性

* 若怀疑内存泄漏/循环，查看分配情况：

  ```bash
  python -X tracemalloc=25 -m unittest -v
  ```

* 显示导入详情（卡顿排查很少需要）：

  ```bash
  python -v -m unittest -v
  ```

### 8) 若仅在某 Python 版本卡顿

* 分别测试：

  ```bash
  pyenv local 3.11.9
  python -X faulthandler -X dev -m unittest -v

  pyenv local 3.9.19
  python -X faulthandler -X dev -m unittest -v
  ```

  差异通常出现在 `multiprocessing`、`asyncio` 或 C 扩展行为中。

---

若提供 `faulthandler` 的跟踪信息（或 `trace --trace` 的最后输出），我可帮您定位具体原因并提供针对性解决方案。
