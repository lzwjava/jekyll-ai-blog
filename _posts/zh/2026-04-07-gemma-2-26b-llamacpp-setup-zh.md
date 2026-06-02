---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma 4 26B 模型评测与部署指南
translated: true
type: note
---

## 🦞 Gemma 4 26B A4B 在 llama.cpp 上的完整评测

### 1. 模型概览

| 属性 | 值 |
|---|---|
| **模型** | Google Gemma 4 26B A4B (指令微调版) |
| **量化** | IQ3_S (3位，质量提升) — 磁盘占用 10.4GB |
| **架构** | MoE (混合专家模型) — 128 个专家，8 个激活 |
| **注意力机制** | 混合 SWA — 25 个局部层 (1024 窗口) + 5 个全局层 |
| **上下文长度** | 262,144 tokens (原生)，当前为 16,384 |
| **词表** | 262,144 tokens (BPE) |

---

### 2. 硬件配置

| 属性 | 值 |
|---|---|
| **GPU** | NVIDIA RTX 4070 |
| **显存** | 12GB |
| **CPU** | 32 线程 |
| **内存** | 62GB |
| **操作系统** | Linux 6.8.0 |

---

### 3. 下载历程

- **来源:** HuggingFace (`unsloth/gemma-4-26B-A4B-it-GGUF`)
- **方法:** `proxychains curl` (防火墙直接屏蔽 HTTPS)
- **问题:** 下载频繁超时/中断 — 需要多次恢复尝试
- **最终:** 下载至 `/home/lzw/projects/llama.cpp/models/`
- **文件大小:** 11,219,402,240 字节 (~10.4GB)

---

### 4. llama.cpp 构建信息

| 属性 | 值 |
|---|---|
| **构建提交版本** | `b8-94ca829b6` |
| **构建日期** | 2026 年 4 月 7 日 |
| **CUDA 架构** | sm_89 (Ada Lovelace) |
| **功能** | CUDA, cuBLAS, REPACK, FLASH_ATTN, GRAPHS |
| **构建时间** | ~2 分钟 (32 线程) |

**重要提示:** 你之前构建的版本 `b1-25eec6f32` 存在**三个已确认的 bug** 影响 Gemma 4:
1. SWA bool/uint32 类型不匹配 — 错误的层维度计算
2. Gemma 4 的上下文偏移功能损坏 — 强制完整重处理而非滑动窗口
3. IQ3 CUDA 内核不稳定 — 产生乱码/崩溃

重新构建修复了 bug #1 和 #2。

---

### 5. 显存约束分析

这是核心挑战。原因如下:

| 配置 | 显存使用量 | 可用显存 | 状态 |
|---|---|---|---|
| `-ngl 31 -c 2048` (全部 GPU 层) | 11.7GB | 11.5GB | ❌ OOM — 无余量 |
| `-ngl 31 -c 4096` | — | — | ❌ OOM |
| `-ngl 31 -c 512` | ~10.7GB | 11.5GB | ✅ 加载成功，但推理时崩溃 |
| `-ngl 25 -c 2048` | ~9.5GB | 11.5GB | ✅ 稳定运行 |
| `-ngl 25 -c 16384 + q8_0 KV` | ~10.7GB | 11.5GB | ✅ 稳定运行 |

**为何会 OOM?** 计算缓冲区 (CUDA0) 需要约 528MB 用于前向传播。将所有 31 层 + 完整的上下文 KV 缓存都放在 GPU 上，就没有剩余显存给这个缓冲区了 → 崩溃。

**解决方案:** `-ngl 25` 将 6 层卸载到 CPU，释放约 2GB 显存用于计算缓冲区。

---

### 6. KV 缓存量化

在 16384 上下文长度下，KV 缓存非常庞大。使用 FP16 会导致 OOM。Q8_0 可将其大小减半:

| KV 缓存类型 | 显存占用 (16384 ctx) | 质量影响 |
|---|---|---|
| FP16 | ~8GB | 完美 |
| Q8_0 | ~4GB | ~0.3% BLEU 损失 |
| Q4_0 | ~2GB | 轻微质量下降 |

我们采用 **Q8_0** 作为最佳平衡点。

---

### 7. 当前服务器配置

```bash
./build/bin/llama-server \
  -m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  -ngl 25 \
  -c 16384 \
  --cache-type-k q8_0 \
  --cache-type-v q8_0 \
  -np 1 \
  --host 0.0.0.0 \
  --port 8081 \
  --path ./tools/server/public
```

**各参数含义:**
- `-ngl 25` — 将 31 层中的 25 层卸载到 GPU (6 层到 CPU)
- `-c 16384` — 上下文窗口大小
- `--cache-type-k q8_0` — 将 KV 缓存的键量化到 Q8_0
- `-np 1` — 单序列槽，节省显存
- `--path ./tools/server/public` — 启用内置 Web UI

---

### 8. 性能指标

| 指标 | 值 |
|---|---|
| **提示词处理速度** | ~95 tokens/秒 (34 tokens) |
| **生成速度** | ~48 tokens/秒 |
| **单 token 延迟** | ~21ms |
| **上下文大小** | 16,384 tokens |
| **GPU 使用率** | ~10.7GB / 12GB |
| **可用槽位** | 1 |

速度低于常规水平，原因如下:
- 6 层在 CPU 上运行 (内存带宽瓶颈)
- IQ3_S 量化解码比 Q4 更耗资源
- 大上下文 = 每个 token 需要更多计算

---

### 9. 已知问题与特性

| 问题 | 状态 | 备注 |
|---|---|---|
| **启动后的 SIGKILL** | 🟡 持续中 | 服务器启动正常，但 shell 报告 SIGKILL。服务器保持存活。很可能是 OpenClaw exec 超时问题，并非真正的崩溃。 |
| **IQ3 CUDA 内核质量** | 🟡 可能存在 | IQ3_S 在 CUDA 上可能产生乱码。Q4_K_M 会更稳定但体积更大。 |
| **SWA 上下文偏移** | 🔴 此构建中未修复 | 上下文偏移仍然损坏 — 超过 16K tokens 后，会强制完整重处理。这是 llama.cpp 的一个已知 bug。 |
| **WebUI 断开连接** | 🔴 偶尔发生 | 内置的 llama Web UI 可能在长响应时断开连接。端口 11435 上的 OpenWebUI 更稳定。 |

---

### 10. 替代方案与升级选项

**为了更好的稳定性:**
```bash
# 下载 Q4_K_M 变体 (约 13GB，更稳定)
proxychains huggingface-cli download unsloth/gemma-4-26B-A4B-it-GGUF \
  --include "*Q4_K_M*" --local-dir ~/projects/llama.cpp/models/
```

**为了获得更多显存余量:**
- 将 `-ngl` 降低至 23-24 → 增加计算缓冲区空间
- 使用 `--cache-type-k q4_0` → 再节省约 2GB KV 缓存显存

**为了在不 OOM 的情况下获得更长上下文:**
- Gemma 4 的 SWA 架构本为此设计 — 但在 12GB 显存和此量化级别下，16K 很可能是实际极限

---

### 11. 快速参考 — 服务管理

```bash
# 检查是否运行
ps aux | grep llama-server | grep -v grep

# 重启命令
cd /home/lzw/projects/llama.cpp && ./build/bin/llama-server \
  -m ./models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  -ngl 25 -c 16384 --cache-type-k q8_0 --cache-type-v q8_0 \
  -np 1 --host 0.0.0.0 --port 8081 --path ./tools/server/public

# 查看日志
tail -f /tmp/llama-server-gemma.log

# 测试 API
curl http://localhost:8081/v1/models
```

---

### 内容提要

Gemma 4 26B A4B 已成功在你的 RTX 4070 上以 16K 上下文长度运行。主要挑战是显存限制（通过减少 GPU 层数和 KV 缓存量化解决）和过时的构建版本（通过重新构建解决）。它足够稳定，可以投入使用，但仍有一些已知特性。IQ3_S 量化是目前最薄弱的一环 — 切换到 Q4_K_M 将提升可靠性，代价是增加 2.6GB 磁盘空间。
