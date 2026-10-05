---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ComfyUI已在M40上安装并验证
translated: true
type: note
---

完成。ComfyUI 已安装并在 Tesla M40 上验证运行。

## 结果

**位置：** `~/projects/ComfyUI`（总计 6.6 GB）

**工作栈：**

| 组件 | 版本 | 原因 |
|---|---|---|
| Python | 3.12.15 (uv venv) | torch 2.7 wheels 需要 ≤3.13 |
| PyTorch | **2.7.0+cu126** | 最后支持 Maxwell `sm_50`/`sm_52` 内核的版本，**并且** `comfy_kitchen==0.2.37` 所需的 `list[int]` 感知模式推断 |
| CUDA runtime | 12.6 (bundled) | 与你的驱动程序 580 兼容 |

**已验证：**
- `torch.cuda.is_available() == True`，设备 `Tesla M40 (5, 2)`
- `compiled arch list: ['sm_50', 'sm_60', 'sm_70', 'sm_75', 'sm_80', 'sm_86', 'sm_90']` → Maxwell 内核存在
- 真实 GPU 矩阵乘法成功
- ComfyUI **0.38.0** 启动，绑定到 CUDA，并提供 `GET / → 200` + `/system_stats`

## 如何运行
```bash
cd ~/projects/ComfyUI
./run.sh                 # 或：./run.sh --port 8188
# 然后打开 http://127.0.0.1:8188
```
`run.sh` 内置了 `--disable-cuda-malloc`（M40 早于 `cudaMallocAsync`；ComfyUI 本身会对此发出警告）。

## 两个值得注意的陷阱
1. **`comfy_kitchen` 在 torch 2.6 上失效** — 它在 `torch.library.custom_op` 签名中使用了 `list[int]`，而 2.6 的 `infer_schema` 拒绝接受。这正是我升级到 2.7+cu126 而不是停留在 2.6 的原因。
2. **Maxwell 的 FP16 较弱。** 如果遇到半精度错误，请运行 `./run.sh --fp32`（较慢，但安全）。你的 11.5 GB 显存足以在 fp32 下运行 SDXL。

## 下一步
尚无模型。将检查点文件放入 `~/projects/ComfyUI/models/checkpoints/`（例如 SD 1.5 或 SDXL 的 `.safetensors` 文件），然后刷新浏览器。

需要我下载一个入门级 SDXL/SD1.5 检查点并运行一次完整的端到端生成以确认 M40 上的速度吗？