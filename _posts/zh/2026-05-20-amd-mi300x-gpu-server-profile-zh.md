---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD MI300X GPU服务器规格
translated: true
type: note
---

这里是 **165.245.137.138** 端到端的完整概况：

---

## 系统概览

| 项目 | 详情 |
|---|---|
| **操作系统** | Ubuntu 24.04，内核 6.8.0-106-generic |
| **CPU** | Intel Xeon Platinum 8568Y+（20 核） |
| **内存** | 235 GB（241,610 MiB 总计） |
| **磁盘** | 697 GB（611 GB 空闲） |

---

## GPU — AMD Instinct MI300X VF

| 属性 | 值 |
|---|---|
| PCIe | 5.0 x16 @ 32 GT/s |
| HBM3 | 256 GB 物理 / **196,288 MiB 可见**（约 192 GB 可用） |
| GFX 架构 | gfx942 |
| ROCm | **7.2.0**，位于 `/opt/rocm-7.2.0` |
| 驱动 | amdgpu 内核内建 v6.16.13 |
| `rocm-smi` | 已检测到，RAS 全部启用 |

加载 Qwen3.5-122B（37 GB GGUF）后的 VRAM 余量：**约 190 GB 空闲**——你可以同时运行多个模型或一个更大的模型。

---

## 构建产物（`/root/llama.cpp/`）

### llama-cli（`build/bin/llama-cli`）
用于一次性终端推理。已用 Qwen2.5-0.5B 冒烟测试通过。

### llama-server（`build/bin/llama-server`）
**当前正在运行**，端口 8080，PID 292080。

| 详情 | 值 |
|---|---|
| 已加载模型 | `models/Qwen3.5-122B-A10B-UD-IQ1_M.gguf`（37 GB） |
| 文件重命名 | 已移除 `?download=true` 后缀 |
| 上下文 | 32,768 个 token × 4 个槽位 |
| 提示缓存 | 8192 MiB RAM 缓存已启用 |
| API | 兼容 OpenAI 的聊天补全 |
| 预热 | 启动时已完成 |
| 聊天模板 | Qwen3.5，支持思考/推理 |

### 性能确认

| 场景 | 吞吐量 |
|---|---|
| Qwen2.5-0.5B（冒烟测试） | 提示：748 t/s，生成：484 t/s |
| **Qwen3.5-122B-A10B-IQ1_M（生产）** | **提示：77 t/s，生成：91 t/s** |

在 122B 参数模型上达到 91 t/s。表现强劲——MoE 稀疏激活（每 token 仅约 10B 活跃）保证了速度。

---

## 你现在可以做什么

**1. 从任何地方调用 API：**
```bash
curl http://165.245.137.138:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "Qwen3.5-122B-A10B-UD-IQ1_M",
    "messages": [{"role": "user", "content": "你的问题"}],
    "max_tokens": 500
  }'
```

**2. 直接在服务器上运行推理**（无 HTTP 开销）：
```bash
cd /root/llama.cpp
export ROCM_PATH=/opt/rocm-7.2.0
export HIP_PATH=$ROCM_PATH
export PATH=$ROCM_PATH/bin:$PATH
./build/bin/llama-cli -m models/Qwen3.5-122B-A10B-UD-IQ1_M.gguf \
  -ngl 99 -p "你的问题" -n 500
```

**3. VRAM 还能装下什么？** 约有 190 GB 空闲，你可以运行：

| 模型 | 量化 | 预估 VRAM | 是否可行 |
|---|---|---|---|
| DeepSeek-V2 236B | IQ2_XXS | ~90 GB | 轻松 |
| DeepSeek-V3 671B | IQ1_S | ~140 GB | 可以 |
| Llama 3.1 405B | Q2_K | ~120 GB | 可以 |
| Qwen 3.5 235B | IQ2_XXS | ~95 GB | 轻松 |

**4. 服务器生命周期**
- 重启：`ssh root@165.245.137.138 "bash /root/run_server.sh"`
- 日志：`ssh root@165.245.137.138 "tail -f /tmp/llama-server.log"`
- 停止：`ssh root@165.245.137.138 "kill 292080"`
- 脚本位于服务器上的 `/root/run_server.sh`

---

需要我下载并加载一个更大的模型，还是帮你将这个 API 端点集成到你本地机器的某个应用中？
