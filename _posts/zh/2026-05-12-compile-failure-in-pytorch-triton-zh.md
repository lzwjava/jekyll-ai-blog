---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PyTorch Triton编译失败
translated: true
type: note
---

这是 `torch.compile` 失败的情况——Triton 试图调用 `gcc` 来构建一个 CUDA 辅助模块，而 gcc 返回了非零状态。烟雾测试从未遇到这个问题，因为我们强制设置了 `--compile=False`。

**最快的修复：直接禁用编译。** 你会损失 20–30% 的吞吐量（因此对于 19073 次迭代，时间从 ~42h 变为 ~59h），但训练过程完全一致，模型质量也相同。

```bash
cd /mnt/data/nanoGPT
tmux new -s nano    # 或：tmux attach -t nano
source venv/bin/activate

PYTORCH_ALLOC_CONF=expandable_segments:True \
python -u train.py config/train_fineweb_gpt3.py --compile=False 2>&1 \
  | tee -a out-fineweb-gpt3/train.log
```

### 有一个地方看起来不对劲

回溯路径是 `/home/lzw/.local/lib/python3.11/...`——这是**系统 Python 3.11**，而不是 nanoGPT 的虚拟环境（之前我用的 Python 3.14 位于 `/mnt/data/nanoGPT/venv/bin/python`）。你是在 tmux 会话中忘记执行 `source venv/bin/activate` 了吗？这并非导致当前错误的原因（gcc 失败在任何环境下都会发生），但为了长期运行，你需要保持环境的一致性。

检查：
```bash
which python && python -c "import sys; print(sys.executable, sys.version)"
```

### 可选：真正修复编译（如果你想要加速）

gcc 编译失败——要查看*原因*，可以根据回溯中的参数手动运行 gcc。Ubuntu 上的常见原因：

```bash
# 快速检查
gcc --version
ls /usr/local/cuda/lib64/libcuda.so* /usr/lib/x86_64-linux-gnu/libcuda.so*
ls /usr/local/cuda/include/cuda.h
echo $CUDA_HOME
```

典型修复方法：
- `sudo apt install nvidia-cuda-toolkit`（获取 Triton 所需的头文件）
- 在运行前设置 `export CUDA_HOME=/usr/local/cuda` 和 `export PATH=$CUDA_HOME/bin:$PATH`
- 或者：重新运行烟雾命令——有时 Triton 的陈旧缓存 `~/.triton/cache` 会导致虚假失败；`rm -rf ~/.triton/cache` 可以清除它

**我的建议：** 现在先用 `--compile=False` 启动长时间训练（你已经在失败的启动上浪费了时间）。在第一天并行诊断编译问题——如果你能解决，就终止训练，然后使用 `--init_from=resume` 和 `compile=True` 恢复。不会有数据浪费。