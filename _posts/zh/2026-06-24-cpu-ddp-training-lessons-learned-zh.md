---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CPU DDP训练经验教训
translated: true
type: note
---

训练已停止。两台机器上的两个进程均死亡。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  关键经验总结 —— 双节点 CPU DDP 训练
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

运行内容
  模型: nanochat d8 (1.26亿参数)
  节点: 2个 (主节点 192.168.1.36 + 工作节点 192.168.1.28)
  后端: Gloo (纯 CPU DDP)
  持续时间: 26.4小时, 1329/5000步
  损失: 10.40 → 5.02

经验1: Gloo 需要双向网络连通性
  TCPStore 协调服务 (端口 29500) 仅需工作节点→主节点。
  但 Gloo 的数据传输也需要主节点→工作节点的临时端口。
  工作节点的防火墙阻止了这些连接。若不开放端口，训练会在协调阶段
  静默挂起——没有报错，只有卡死。
  解决方法: 为工作节点开放主节点 IP 的防火墙规则，或设置
  GLOO_PORT_RANGE 并开放指定端口范围。

经验2: 重启前务必清除残留进程
  残留的 torchrun/base_train 进程 (PPID=1) 会占用端口 29500 并
  干扰新启动的训练。启动前务必检查:
    ps aux | grep -E 'torchrun|base_train' | grep -v grep
    ss -tlnp | grep 29500
  清除命令: pkill -9 -f torchrun; fuser -k 29500/tcp

经验3: 全程使用 TMUX，绝不用后台 SSH
  后台 SSH (&) 会在会话断开时静默终止。tmux 能抵御断线。
  所有远程长时间运行进程都应使用 tmux。
  模式: tmux new-session -d -s name 'command; sleep 999999'
  sleep 命令确保命令结束后 tmux 会话仍保持存活。

经验4: CPU DDP 并行收益微乎其微
  两个节点各约 24 个 CPU 核心，总吞吐仅 57 tok/s。
  单节点 CPU 约为 60 tok/s。Gloo 在以太网 (~1 Gbps) 上的全规约
  速度极慢，几乎抵消了并行化的收益。
  CPU DDP 仅在需要合并内存容量时才有价值，而非追求速度。

经验5: 嵌套 SSH + TMUX = 引号噩梦
  通过 SSH 再 SSH 在工作节点上运行 tmux 会破坏引号解析。
  解决方案: 先将脚本文件写入工作节点，再用 tmux 执行:
    ssh master "ssh worker 'cat > /tmp/run.sh << EOF ... EOF'"
    ssh master "ssh worker 'tmux new -d -s x \"bash /tmp/run.sh\"'"

经验6: 日志捕获比想象中复杂
  tee 仅捕获标准输出，但 torchrun 将进度写入标准错误。
  script -q -c "cmd" log.txt 可同时捕获两者但存在严重缓冲。
  tmux capture-pane -p 是读取远程输出最可靠的方式。
  PYTHONUNBUFFERED=1 有助缓解但并非万能。

经验7: SSH 退出码 255 在嵌套 SSH 中属于正常现象
  执行 ssh host1 "ssh host2 cmd" 时，外层 SSH 的退出码 255
  并不意味着内部命令失败。应单独检查内部命令的实际输出。

经验8: 标注为 "80M" 的模型实际大小为 126M
  脚本声称 "约8000万参数"，但仅 value_embeds 一项就有 6700万。
  始终检查启动时打印的实际参数数量。
  126M 参数的 float32 模型约占用每进程 500MB。两台机器均能
  轻松放入内存。

经验9: 网络调试检查清单
  1. 工作节点能否访问主节点的 TCPStore 端口? (bash /dev/tcp 测试)
  2. 主节点能否访问工作节点的临时端口? (相同测试)
  3. Tailscale 是否造成干扰? (检查 tailscale status)
  4. nsswitch.conf 是否将主机名解析到回环地址? (grep myhostname)
  5. GLOO_SOCKET_IFNAME 是否设置为正确的网络接口?

经验10: CPU 训练受限于内存带宽，而非计算能力
  57 tok/s 的瓶颈来自 DDR 带宽 (~50-80 GB/s)，而非 CPU 算力。
  增加更多 CPU 核心或节点作用有限，因为数据总线已饱和。
  只有 GPU (504 GB/s GDDR6X) 或 HBM (1-3 TB/s) 才能突破此壁垒。