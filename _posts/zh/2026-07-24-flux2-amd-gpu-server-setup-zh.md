---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX.2 AMD GPU服务器设置
translated: true
type: note
---

## ✅ 全面总结

### 服务器设置

| 步骤 | 状态 |
| ------ | ------ |
| SSH连接测试 | ✅ 已连接 |
| GPU检测 (ROCm) | ✅ AMD Radeon GPU, 48GB显存 |
| tmux已安装 | ✅ |
| Python虚拟环境已创建 (`/root/flux_env`) | ✅ |

### GPU规格

- **GPU**: AMD RDNA 3 (gfx1100) — 48GB显存 (三星)
- **ROCm**: v7.2.1, HIP 7.2.53211
- **CPU**: AMD EPYC 9334, 128线程
- **内存**: 503 GB
- **磁盘**: 3.5TB (2.9TB空闲)

### 已安装软件

| 包 | 版本 | 备注 |
| --------- | --------- | ------- |
| PyTorch | 2.13.0+rocm7.2 | 兼容ROCm 7.2 |
| diffusers | 0.39.0 | 最新 |
| transformers | 4.57.6 | 从5.x降级以兼容 |
| accelerate | 1.14.0 | 用于CPU卸载 |
| sentencepiece | 0.2.2 | 分词器 |
| huggingface-hub | 已使用token登录 | 已配置HF镜像 |

### 遇到的问题及修复

1. **无法连接到huggingface.co** → 使用`HF_ENDPOINT=https://hf-mirror.com` (清华镜像)

2. **Transformers 5.x与diffusers不兼容** → 降级到`transformers==4.57.6`

3. **错误的pipeline类** → FLUX.2-dev使用`Flux2Pipeline`（而非`FluxPipeline`）

4. **在`pipe.to("cuda")`时出现OOM** → 模型在bf16下约35GB，尝试一次性加载到48GB显存中 → 通过`pipe.enable_model_cpu_offload()`修复（一次仅在GPU上保留一个组件）

### 最终脚本 (`/root/run_flux.py`)

- 使用CPU卸载加载FLUX.2-dev
- 生成一张1024×1024的图片，内容为“一只可爱的猫举着一块写着hello world的牌子”
- 28步推理
- 结果保存到`test_flux.png`

### 运行方式

```bash
ssh -p 31145 root@36.150.116.206
tmux new -s flux
source /root/flux_env/bin/activate
python3 /root/run_flux.py
```

使用`Ctrl+B, D`分离 · 使用`tmux attach -t flux`重新连接
