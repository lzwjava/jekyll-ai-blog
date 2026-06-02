---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 使用Psutil终止端口进程
translated: true
type: note
---

### 使用 psutil 检测并终止指定端口的进程（Windows）

Psutil 是一个跨平台的 Python 库，用于获取运行进程信息和系统利用率。你可以用它来查找监听特定端口的进程（例如，识别类似 npm 开发服务器是否正在该端口运行），然后终止该进程。该方法在 Windows 上有效，但请注意：

- **权限**：在 Windows 上终止进程通常需要管理员权限（以管理员身份运行 Python 脚本）。否则可能会引发 `AccessDenied` 异常。
- **端口检测**：我们将重点关注类型为 "inet" 的 TCP 连接（涵盖 IPv4 和 IPv6）。这对于由 `npm run dev` 或类似命令启动的 Web 服务器很常见。
- **假设**：我们假设你要检查的是监听（服务器）端口（例如，本地绑定的内容）。如果你指的是到某个端口的出站连接，方法会略有不同——如需澄清请告知。

#### 第 1 步：安装 psutil

如果尚未安装：

```bash
pip install psutil
```

#### 第 2 步：检测并终止的示例代码

这是一个完整的 Python 脚本。它定义了一个函数来查找监听给定端口的进程的 PID（使用你指定的 `kind='inet'`），然后终止它。在 Windows 上，`terminate()` 优于 `kill()`，因为它允许优雅关闭（相当于 Unix 上的 SIGTERM）。

```python
import psutil
import time  # 用于可选的延迟

def get_pid_listening_on_port(port, kind='inet'):
    """
    扫描网络连接以查找监听指定端口的进程。
    返回一个 PID 列表（通常是一个，但在极少数情况下可能是多个）。
    """
    pids = []
    for conn in psutil.net_connections(kind=kind):
        # 检查是否为监听连接 (status='LISTEN') 且本地地址端口匹配
        if conn.status == 'LISTEN' and conn.laddr and conn.laddr.port == port:
            if conn.pid:
                pids.append(conn.pid)
    return pids

def kill_process_on_port(port, kind='inet'):
    """
    查找并终止监听指定端口的进程。
    如果存在多个进程，则全部终止（并发出警告）。
    """
    pids = get_pid_listening_on_port(port, kind)
    if not pids:
        print(f"在端口 {port} 上未找到监听进程。")
        return

    for pid in pids:
        try:
            proc = psutil.Process(pid)
            print(f"正在终止端口 {port} 上的进程 {proc.name()} (PID {pid})...")
            # 使用 terminate() 进行优雅关闭；它发送类似 SIGTERM 的信号
            proc.terminate()
            # 可选：等待一段时间，如果未退出则强制杀死
            gone, still_alive = psutil.wait_procs([proc], timeout=3)
            if still_alive:
                print(f"正在强制杀死 PID {pid}...")
                still_alive[0].kill()
        except psutil.AccessDenied:
            print(f"访问被拒绝：无法终止 PID {pid}。请以管理员身份运行？")
        except psutil.NoSuchProcess:
            print(f"进程 {pid} 已不存在。")

# 示例用法：将 3000 替换为目标端口（例如，npm 开发服务器通常使用 3000）
if __name__ == "__main__":
    kill_process_on_port(3000)  # 如果需要，调整 kind（例如，'inet4' 仅用于 IPv4）
```

#### 关键说明

- **`psutil.net_connections(kind='inet')`**：这检索类型为 'inet' 的网络连接（包括 IPv4 和 IPv6）。每个连接都是一个具名元组，包含如下字段：
  - `laddr`：本地地址（例如，('0.0.0.0', 8080) – IP 和端口）。
  - `status`：对于等待连接的服务器为 'LISTEN'。
  - `pid`：所有者的进程 ID。
  - 我们过滤 `status == 'LISTEN'` 以查找服务器（如 npm 的开发端口），而不是客户端连接。
- **PID 检索**：脚本直接从连接元组获取 PID。如果只想检测而不杀死，使用 `get_pid_listening_on_port(port)`，它返回 PID（或多个 PID）。
- **终止进程**：
  - `psutil.Process(pid).terminate()`：发送终止信号。在 Windows 上，这类似于 CTRL+C。
  - 如果它不退出，我们可选地使用 `kill()` 强制杀死（相当于 SIGKILL）。
  - Psutil 的 `wait_procs()` 等待进程终止。
- **inet 类型特异性**：'inet' 包括 IPv4 和 IPv6。如果你知道它是 IPv4，更改为 `kind='inet4'`。THISNAME 直接解决了你对 "inet 类型" 的请求。
- **Windows 特定说明**：
  - Psutil 能很好地处理 Windows 内部机制，但在某些情况下，网络信息可能需要提升的权限。
  - 对于低于 1024 的端口（特权端口），只有系统服务可以绑定，但检测应该仍然有效。
- **错误处理**：添加了对无进程或访问问题的基本检查。
- **测试**：运行类似 `npm run dev` 的命令以占用端口 3000，然后运行此脚本。

如果这不完全符合你的需求（例如，如果 "npm run port" 意味着其他内容，或者你想检测非监听连接），请提供更多细节以便改进！出于安全考虑，请确保你只杀死目标进程。
