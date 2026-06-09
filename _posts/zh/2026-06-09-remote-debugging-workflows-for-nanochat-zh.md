---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nanoChat的远程调试工作流程
translated: true
type: note
---

**可以远程调试。** 一种误解认为 PyCharm 不支持远程调试——实际上 PyCharm *专业版* 完全支持通过 SSH 进行远程调试，具备完整的断点/检查功能。但考虑到你崇尚终端优先的工作哲学，你可能更想要更轻量的方案。

## 三种实用工作流：

### 1. **命令行优先：通过 SSH 使用 `debugpy`**（我推荐你的方案）

这是终端原生方案，速度快，兼容性好。在工作站上安装 `debugpy`，用它启动训练脚本，然后从 Mac 通过 VSCode 的调试器连接（轻量，无图形界面开销）。

```bash
# 在工作站上 (192.168.1.36)
pip install debugpy

# 启动脚本并开启调试监听
python -m debugpy.adapter --listen 0.0.0.0:5678 your_training_script.py
# 或内联方式：
python -c "
import debugpy; debugpy.listen(('0.0.0.0', 5678))
debugpy.wait_for_client()
exec(open('train.py').read())
"
```

然后在 Mac 上的 VSCode 中创建 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "远程附加 (工作站)",
      "type": "python",
      "request": "attach",
      "connect": {
        "host": "192.168.1.36",
        "port": 5678
      },
      "pathMapping": {
        "/home/lzw/nanoGPT": "/Users/zhiwei/nanoGPT"  // 本地路径映射
      }
    }
  ]
}
```

按下 F5，设置断点，检查变量——全部在 Mac 上完成。无需远程 IDE 开销。

### 2. **VSCode/Zed 远程 SSH 开发**（更干净的体验，启动稍慢）

两者都能挂载远程文件系统，并直接在工作站上运行调试器：

**VSCode：**
```bash
# 安装 Remote - SSH 扩展
# 在 VSCode 中：Cmd+Shift+P → "Remote-SSH: Connect to Host"
# 输入：ssh lzw@192.168.1.36

# 然后打开文件夹，终端直接在工作站上
# 调试器原生运行在那里
```

**Zed：**
```bash
# 较新版本的 Zed 支持 SSH（0.140+ 版本）
# File → Open Remote → SSH
# zed --new-window /home/lzw/nanoGPT
```

优点：IDE 体验如同本地。缺点：WiFi 弱时网络延迟，且 Zed 的远程功能仍在完善中。

### 3. **PyCharm 专业版远程调试**（对你的工作流来说过于复杂）

确实可用：
- Settings → Project → Python Interpreter → Add → SSH Interpreter
- 配置连接到 192.168.1.36
- 设置断点，直接调试

但图形界面繁重，对于快速迭代比 `debugpy` + VSCode 慢。

## 针对你的配置我的真实建议：

既然你**终端优先**且使用 nanoGPT 进行 GPU 训练，推荐使用 **`debugpy` + VSCode** 或 **VSCode SSH 远程**。原因：

- **debugpy** 让你保持在代码/终端环境中，快速附加/分离，开销极小。非常适合长时间运行的训练任务，偶尔检查状态。
- **VSCode SSH 远程** 适合活跃开发场景（编辑配置、修改损失计算）——文件同步无缝，集成终端。
- **Zed 远程** 适合长期使用（Zed 在处理大型代码库时比 VSCode 更流畅，且为原生应用）。

对于训练过程中的实际调试（检查张量、梯度、激活值），你可能还是倾向于在终端中使用 **pdb/pdbpp**：

```python
# 在你的训练循环中
import pdb

if step % 100 == 0:
    print(f"Loss: {loss}, hidden shape: {h.shape}")
    pdb.set_trace()  # 进入 REPL，检查 h、梯度等
```

通过 SSH 配合 Warp：
```bash
ssh lzw@192.168.1.36
cd ~/nanoGPT && python train.py
# 命中断点，进入 pdb shell
# 检查变量，计算表达式
# `c` 继续执行
```

**无需 PyCharm。无需远程 IDE。只需 SSH + pdb + Warp。**

---

**对于 AMD MI300X 云端工作负载：** 方法相同。在云实例上开启 `debugpy` 监听，从 Mac 连接。或者干脆加大日志输出（print → wandb/tensorboard），因为云环境无状态，你通常是在迭代批次配置，而不是逐行调试代码。