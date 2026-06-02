---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Kill Process on Port with Psutil
translated: false
type: note
---

### Using psutil to Detect and Kill a Process on a Specific Port (Windows)

Psutil is a cross-platform Python library for retrieving information on running processes and system utilization. You can use it to find processes listening on a specific port (e.g., identifying if something like an npm dev server is running on that port) and then terminate the process. This works on Windows, but keep in mind:

- **Permissions**: On Windows, terminating processes often requires administrative privileges (run your Python script as an administrator). Failing to do so may raise an `AccessDenied` exception.
- **Port Detection**: We'll focus on TCP connections with "inet" kind (which covers IPv4 and IPv6). This is common for web servers like those started by `npm run dev` or similar.
- **Assumptions**: We're assuming you want to check for a listening (server) port (e.g., something bound locally). If you mean outbound connections to a port, the approach differs slightly—let me know for clarification.

#### Step 1: Install psutil
If you haven't already:
```bash
pip install psutil
```

#### Step 2: Sample Code to Detect and Kill
Here's a complete Python script. It defines a function to find the PID of the process listening on a given port (using `kind='inet'` as you specified), then terminates it. On Windows, `terminate()` is preferred over `kill()` as it allows graceful shutdown (equivalent to SIGTERM on Unix).

```python
import psutil
import time  # For optional delay

def get_pid_listening_on_port(port, kind='inet'):
    """
    Scans network connections for processes listening on the specified port.
    Returns a list of PIDs (usually one, but could be multiple if rare).
    """
    pids = []
    for conn in psutil.net_connections(kind=kind):
        # Check if it's a listening connection (status='LISTEN') and the local address port matches
        if conn.status == 'LISTEN' and conn.laddr and conn.laddr.port == port:
            if conn.pid:
                pids.append(conn.pid)
    return pids

def kill_process_on_port(port, kind='inet'):
    """
    Finds and terminates the process listening on the specified port.
    If multiple processes, kills all (with a warning).
    """
    pids = get_pid_listening_on_port(port, kind)
    if not pids:
        print(f"No process found listening on port {port}.")
        return

    for pid in pids:
        try:
            proc = psutil.Process(pid)
            print(f"Terminating process {proc.name()} (PID {pid}) on port {port}...")
            # Use terminate() for graceful shutdown; it sends a SIGTERM-like signal
            proc.terminate()
            # Optional: Wait a bit and force kill if it doesn't exit
            gone, still_alive = psutil.wait_procs([proc], timeout=3)
            if still_alive:
                print(f"Force killing PID {pid}...")
                still_alive[0].kill()
        except psutil.AccessDenied:
            print(f"Access denied: Cannot terminate PID {pid}. Run as administrator?")
        except psutil.NoSuchProcess:
            print(f"Process {pid} no longer exists.")

# Example usage: Replace 3000 with your target port (e.g., npm dev servers often use 3000)
if __name__ == "__main__":
    kill_process_on_port(3000)  # Adjust kind if needed (e.g., 'inet4' for IPv4 only)
```

#### Key Explanations
- **`psutil.net_connections(kind='inet')`**: This retrieves network connections of kind 'inet' (encompassing IPv4 and IPv6). Each connection is a namedtuple with fields like:
  - `laddr`: Local address (e.g., ('0.0.0.0', 8080) – IP and port).
  - `status`: 'LISTEN' for servers awaiting connections.
  - `pid`: Process ID of the owner.
  - We filter for `status == 'LISTEN'` to find servers (like npm's dev port), not client connections.
- **PID Retrieval**: The script directly gets the PID from the connection tuple. If you only want to detect without killing, use `get_pid_listening_on_port(port)` which returns the PID(s).
- **Killing the Process**:
  - `psutil.Process(pid).terminate()`: Sends a termination signal. On Windows, this is like CTRL+C.
  - If it doesn't exit, we optionally force-kill with `kill()` (equivalent to SIGKILL).
  - Psutil's `wait_procs()` waits for the process to die.
- **inet Kind Specificity**: 'inet' includes both IPv4 and IPv6. If you know it's IPv4, change to `kind='inet4'`. THISNAME addresses your "inet kind" request directly.
- **Windows-Specific Notes**:
  - Psutil handles Windows internals well, but network info may require elevated privileges in some cases.
  - For ports below 1024 (privileged), only system services can bind, but detection should still work.
- **Error Handling**: Added basic checks for no process or access issues.
- **Testing**: Run something like `npm run dev` to occupy port 3000, then run this script.

If this doesn't match your exact need (e.g., if "npm run port" means something else or you want to detect non-listening connections), provide more details for refinement! For security/tsafety, ensure you're only killing intended processes.
