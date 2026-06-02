---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 监控带超时的子进程输出
translated: true
type: note
---

```python
import subprocess
import threading
import queue
import time
import sys

def read_output(proc, output_queue):
    """线程函数：读取stdout和stderr，放入队列"""
    try:
        for line in iter(proc.stdout.readline, b''):
            if not line:
                break
            output_queue.put(line.decode('utf-8', errors='ignore').rstrip())
        # 同时检查stderr（如需要）
        for line in iter(proc.stderr.readline, b''):
            if not line:
                break
            output_queue.put(line.decode('utf-8', errors='ignore').rstrip())
    except Exception as e:
        output_queue.put(f"读取输出时出错: {e}")

def main():
    # 要运行的命令（例如在Windows上执行'mvn clean compile'）
    cmd = ['mvn', 'clean', 'compile']  # 根据需要调整，例如['cmd', '/c', 'mvn build']
    timeout_seconds = 10

    # 启动子进程
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,  # 行缓冲
        universal_newlines=False,  # 处理字节
        cwd=None  # 如需设置工作目录
    )

    # 输出队列
    output_queue = queue.Queue()

    # 启动输出读取线程
    output_thread = threading.Thread(target=read_output, args=(proc, output_queue))
    output_thread.daemon = True
    output_thread.start()

    print("已启动命令。每10秒监控输出...")

    while proc.poll() is None:
        try:
            # 带超时等待输出
            output = output_queue.get(timeout=timeout_seconds)
            print(f"输出: {output}")  # 可选：打印或处理输出
        except queue.Empty:
            print(f"{timeout_seconds}秒内无输出。终止命令并退出。")
            proc.terminate()  # 或使用proc.kill()强制终止
            try:
                proc.wait(timeout=5)  # 稍等片刻实现优雅关闭
            except subprocess.TimeoutExpired:
                proc.kill()
            sys.exit(1)

    # 进程正常结束
    print("命令执行完成。")
    output_thread.join()  # 等待输出线程结束

if __name__ == "__main__":
    main()
```

### 说明

- **子进程**：使用`subprocess.Popen`运行`mvn clean compile`（根据需要调整命令；对于简单的`mvn build`，可能是`['mvn', 'build']`，如果需要可封装在`cmd /c`中）。通过管道异步运行stdout和stderr。
- **队列线程**：单独线程逐行读取stdout和stderr（避免一次性读取全部输出），解码后将行数据放入`queue.Queue`，实现非阻塞读取。
- **超时监控**：在主线程中使用`get(timeout=10)`检查队列中的新输出。如果10秒内没有输出到达，则终止子进程并退出。
- **Windows兼容性**：`subprocess`在Windows上可用。如果命令需要shell（例如当`mvn`不在PATH中时），可设置`shell=True`并将命令作为字符串传递：`proc = subprocess.Popen("mvn clean compile", shell=True, ...)`。
- **边界情况**：如果进程在等待时正常退出，循环停止并合并线程。线程设置为守护模式以避免退出时挂起。
- **自定义**：可修改以不同方式处理输出（例如记录到文件而非打印）。对于stderr，已合并到同一队列；如需分离可另行处理。如果输出是二进制数据，需调整解码方式。
