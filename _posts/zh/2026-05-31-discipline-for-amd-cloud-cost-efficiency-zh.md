---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD云成本效率规范
translated: true
type: note
---

**问题：** 如何通过消除干扰（停止 Warp/agent 会话、并行任务，只专注训练）来节省 AMD Dev Cloud（1.99 美元/小时）的费用？

**答案：**

是的，完全正确。AMD MI300X 是计算资源，而非开发环境。你支付的每一分钟都应用来让 GPU 工作，而不是让终端在 Warp 会话中闲置。

以下是纪律：

## 启动实例之前

1. **先在本地准备好所有内容** —— 训练脚本定稿、配置调优、数据集就绪、依赖列表明确
2. **不要在付费实例上调试** —— 先在 MacBook 或工作站上完成调试
3. **编写一个启动脚本** —— 一个命令即可启动完整的训练运行

## 在实例上：最小化空闲时间

```bash
# 不要使用交互式 Warp 会话 —— 使用 tmux 并立即分离
tmux new -s train
python train.py --config config.yaml
# Ctrl+B, D  ← 分离，实例继续运行，你无需盯着看

# 或者直接用 nohup 运行并完全断开连接
nohup python train.py > train.log 2>&1 &
echo $! > train.pid
```

## 杀死所有非训练进程

```bash
# 检查运行内容
ps aux | grep python

# 杀死任何残留的 agent/工具会话
pkill -f "warp"
pkill -f "claude"
pkill -f "cursor"

# 最小化环境 —— 无编辑器、无 agent、无多余终端
```

## 完成后自动关机（最重要）

```bash
# 附加到训练脚本末尾，或在训练后运行
python train.py && sudo shutdown -h now

# 或包含错误处理
python train.py; EXIT_CODE=$?; sudo shutdown -h now; exit $EXIT_CODE
```

这样训练一结束实例就会关闭，即使你正在睡觉也没问题。

## 积极保存检查点

```bash
# 每 N 步保存一次，避免崩溃浪费整个运行
# 在训练循环中：
if step % 500 == 0:
    torch.save(model.state_dict(), f"ckpt_{step}.pt")
```

## 成本计算

按 1.99 美元/小时计算，闲置 1 小时 ≈ 浪费 2 美元。一次 10 小时的运行因为忘记关闭而多跑 2 小时 = 损失 4 美元。自动关机立即回本。

**纪律总结：**
- 本地：在 CPU/小批量上编写、调试、测试
- AMD：启动训练、分离、自动关机
- 不要在付费实例上运行 agent、Warp 会话或并行探索