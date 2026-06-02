---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Monitor Subprocess Output With Timeout
translated: false
type: note
---

```python
import subprocess
import threading
import queue
import time
import sys

def read_output(proc, output_queue):
    """Thread function to read stdout and stderr, put into queue."""
    try:
        for line in iter(proc.stdout.readline, b''):
            if not line:
                break
            output_queue.put(line.decode('utf-8', errors='ignore').rstrip())
        # Also check stderr if needed
        for line in iter(proc.stderr.readline, b''):
            if not line:
                break
            output_queue.put(line.decode('utf-8', errors='ignore').rstrip())
    except Exception as e:
        output_queue.put(f"Error reading output: {e}")

def main():
    # Command to run (e.g., 'mvn clean compile' on Windows)
    cmd = ['mvn', 'clean', 'compile']  # Adjust as needed, e.g., ['cmd', '/c', 'mvn build']
    timeout_seconds = 10

    # Start the subprocess
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,  # Line buffered
        universal_newlines=False,  # Handle bytes
        cwd=None  # Set working directory if needed
    )

    # Queue for output
    output_queue = queue.Queue()

    # Start thread to read output
    output_thread = threading.Thread(target=read_output, args=(proc, output_queue))
    output_thread.daemon = True
    output_thread.start()

    print("Started command. Monitoring for output every 10 seconds...")

    while proc.poll() is None:
        try:
            # Wait for output with timeout
            output = output_queue.get(timeout=timeout_seconds)
            print(f"Output: {output}")  # Optional: print or process output
        except queue.Empty:
            print(f"No output for {timeout_seconds} seconds. Terminating command and exiting.")
            proc.terminate()  # or proc.kill() for forceful kill
            try:
                proc.wait(timeout=5)  # Wait a bit for graceful shutdown
            except subprocess.TimeoutExpired:
                proc.kill()
            sys.exit(1)

    # Process has finished normally
    print("Command completed.")
    output_thread.join()  # Wait for output thread to finish

if __name__ == "__main__":
    main()
```

### Explanation

- **Subprocess**: Uses `subprocess.Popen` to run `mvn clean compile` (adjust the command as needed; for simple `mvn build`, it might be `['mvn', 'build']` or wrapped in `cmd /c` if needed). It's run asynchronously with pipes for stdout and stderr.
- **Queue Threading**: A separate thread reads from stdout and stderr line by line (to avoid reading entire output at once), decodes it, and puts lines into a `queue.Queue`. This allows non-blocking reads.
- **Timeout Monitoring**: In the main thread, check the queue for new output with `get(timeout=10)`. If no output arrives in 10 seconds, terminate the subprocess and exit.
- **Windows Compatibility**: `subprocess` works on Windows. If the command requires a shell (e.g., for `mvn` if not in PATH), you could set `shell=True` and pass the command as a string: `proc = subprocess.Popen("mvn clean compile", shell=True, ...)`.
- **Edge Cases**: If the process exits normally while waiting, the loop stops and we join the thread. The thread is daemonic to avoid hanging on exit.
- **Customization**: You can modify to process outputs differently (e.g., log to file instead of print). For stderr, it's combined into the same queue; you could separate if needed. If outputs are binary, adjust decoding.
