---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote Debugging Workflows for nanoChat
translated: false
type: note
---

Question: Can you debug nanoGPT/nanoChat on your home workstation (Ubuntu/LAN) remotely, or do you need to physically sit at the machine? How do PyCharm, VSCode, and Zed compare for this workflow?

Answer:

**You can absolutely remote debug.** The misconception is that PyCharm remote debugging isn't available — PyCharm *Professional* supports remote debugging via SSH with full breakpoint/inspection capability. But given your terminal-first philosophy, you probably want something faster anyway.

## Three practical workflows:

### 1. **CLI-first: `debugpy` over SSH** (my recommendation for you)

This is terminal-native, fast, and works anywhere. Install `debugpy` on your workstation, start your training script with it, and attach from your Mac via VSCode's debugger (lightweight, no GUI overhead).

```bash
# On workstation (192.168.1.36)
pip install debugpy

# Launch script with debugger listening
python -m debugpy.adapter --listen 0.0.0.0:5678 your_training_script.py
# or inline:
python -c "
import debugpy; debugpy.listen(('0.0.0.0', 5678))
debugpy.wait_for_client()
exec(open('train.py').read())
"
```

Then in VSCode on your Mac, create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Remote Attach (Workstation)",
      "type": "python",
      "request": "attach",
      "connect": {
        "host": "192.168.1.36",
        "port": 5678
      },
      "pathMapping": {
        "/home/lzw/nanoGPT": "/Users/zhiwei/nanoGPT"  // local path mapping
      }
    }
  ]
}
```

Hit F5, breakpoint, inspect — all from your Mac. No remote IDE overhead.

### 2. **VSCode/Zed remote SSH development** (cleaner UX, slower startup)

Both can mount your remote filesystem and run the debugger directly on the workstation:

**VSCode:**
```bash
# Install Remote - SSH extension
# In VSCode: Cmd+Shift+P → "Remote-SSH: Connect to Host"
# Enter: ssh lzw@192.168.1.36

# Then open folder, terminal is directly on workstation
# Debugger runs there natively
```

**Zed:**
```bash
# Newer Zed has SSH support (version 0.140+)
# File → Open Remote → SSH
# zed --new-window /home/lzw/nanoGPT
```

Pro: IDE feels native. Con: Network latency if your WiFi is weak, and Zed's remote is still evolving.

### 3. **PyCharm Professional remote debugging** (overkill for your workflow)

Yes, it works:
- Settings → Project → Python Interpreter → Add → SSH Interpreter
- Configure SSH to 192.168.1.36
- Set breakpoints, debug directly

But it's GUI-heavy and slower than `debugpy` + VSCode for quick iterations.

## My honest take for your setup:

Since you're **terminal-first** and doing GPU training with nanoGPT, use **`debugpy` + VSCode** or **VSCode SSH remote**. Why:

- **debugpy** keeps you in code/terminal, fast attach/detach, minimal overhead. Perfect for long-running training jobs where you inspect state occasionally.
- **VSCode SSH remote** if you're doing active development (editing config, modifying loss calculations) — seamless file sync, integrated terminal.
- **Zed remote** if you want to live there long-term (Zed is snappier than VSCode for large codebases, native).

For actual debugging during training (inspecting tensors, gradients, activations), you probably want **pdb/pdbpp in the terminal** anyway:

```python
# In your training loop
import pdb

if step % 100 == 0:
    print(f"Loss: {loss}, hidden shape: {h.shape}")
    pdb.set_trace()  # Drop into REPL, inspect h, grads, etc.
```

Over SSH with Warp:
```bash
ssh lzw@192.168.1.36
cd ~/nanoGPT && python train.py
# Hits breakpoint, you're in pdb shell
# Inspect variables, evaluate code
# `c` to continue
```

**No PyCharm needed. No remote IDE. Just SSH + pdb + Warp.**

---

**For AMD MI300X cloud workloads:** Same approach. `debugpy` listening on the cloud instance, attach from your Mac. Or just log aggressively (print → wandb/tensorboard) since cloud boxes are stateless and you're usually iterating batch configs, not stepping through code.
