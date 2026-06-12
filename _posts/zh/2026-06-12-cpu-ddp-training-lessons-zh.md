---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CPU DDP训练课程
translated: true
type: note
---

训练已停止。两台机器上的两个进程均已死。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  关键经验总结 — 2 节点 CPU DDP 训练
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

运行内容
  模型：nanochat d8（1.26 亿参数）
  节点数：2（主节点 192.168.1.36 + 工作节点 192.168.1.28）
  后端：Gloo（纯 CPU DDP）
  时长：26.4 小时，1329/5000 步
  损失：10.40 → 5.02

经验 1：Gloo 需要双向连接
  TCPStore 集合点（端口 29500）仅需工作节点→主节点。
  但 Gloo 的数据传输也需要主节点→工作节点上的临时端口。
  工作节点的防火墙阻止了这些端口。如果不开放，训练会在集合阶段
  静默挂起——没有错误，只是卡住。
  解决方法：在工作节点上开放主节点 IP 的防火墙，或使用
  GLOO_PORT_RANGE 并开放该特定范围。

经验 2：重新启动前杀死残留进程
  孤立的 torchrun/base_train 进程（PPID=1）会占用端口 29500 并
  干扰新启动的进程。启动前务必检查：
    ps aux | grep -E 'torchrun|base_train' | grep -v grep
    ss -tlnp | grep 29500
  使用以下命令杀死：pkill -9 -f torchrun; fuser -k 29500/tcp

经验 3：全程使用 tmux，绝不在后台运行 SSH
  后台 SSH（&）会在会话断开时静默死亡。tmux 能抵抗断连。
  所有长时间运行的远程进程都应使用 tmux。
  模式：tmux new-session -d -s name 'command; sleep 999999'
  命令退出后，sleep 会保持 tmux 会话存活。

经验 4：CPU DDP 并行带来的速度提升微乎其微
  2 个节点，每个约 24 个 CPU 核心，总速度 57 tok/s。
  单节点 CPU 约为 60 tok/s。通过以太网（~1 Gbps）进行的 Gloo all-reduce
  非常慢，几乎抵消了并行带来的好处。
  仅当需要合并内存时才值得使用 CPU DDP，而不是为了速度。

经验 5：嵌套 SSH + tmux = 引号地狱
  通过 SSH 再 SSH 在工作节点上运行 tmux 会破坏引号。
  解决方法：先将脚本文件写入工作节点，然后用 tmux 运行：
    ssh master "ssh worker 'cat > /tmp/run.sh << EOF ... EOF'"
    ssh master "ssh worker 'tmux new -d -s x \"bash /tmp/run.sh\"'"

经验 6：日志捕获比想象的更棘手
  tee 捕获 stdout，但 torchrun 将进度写入 stderr。
  script -q -c "cmd" log.txt 能同时捕获两者，但缓冲严重。
  tmux capture-pane -p 是读取远程输出最可靠的方式。
  PYTHONUNBUFFERED=1 有帮助，但不能解决所有问题。

经验 7：嵌套 SSH 中退出码 255 是正常的
  执行 ssh host1 "ssh host2 cmd" 时，外层 SSH 返回退出码 255
  并不意味着内部命令失败。请单独检查内部命令的实际输出。

经验 8：标称为“80M”的模型实际为 126M
  脚本上写着“~80M 参数”，但仅 value_embeds 就有 67M。
  始终检查启动时打印的实际参数数量。
  126M 模型在 float32 下 = 每个 rank 约 500MB。两台机器
  的 RAM 都能轻松容纳。

经验 9：网络调试检查清单

  1. 工作节点能否访问主节点的 TCPStore 端口？（bash /dev/tcp 测试）
  2. 主节点能否访问工作节点的临时端口？（相同测试）
  3. Tailscale 是否有干扰？（检查 tailscale status）
  4. nsswitch.conf 是否将主机名解析到回环地址？（grep myhostname）
  5. GLOO_SOCKET_IFNAME 是否设置为正确的接口？

经验 10：CPU 训练是内存受限，而非计算受限
  57 tok/s 的瓶颈在于 DDR 带宽（~50-80 GB/s），而非 CPU
  算力。增加更多 CPU 核心或节点帮助不大，因为
  数据总线已经饱和。只有 GPU（504 GB/s GDDR6X）或 HBM
  （1-3 TB/s）才能打破这一壁垒。
