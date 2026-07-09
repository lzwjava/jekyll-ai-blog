---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI50二手AI设置指南
translated: true
type: note
---

问题：我在闲鱼上刚淘到一张二手的AMD Instinct MI50 16GB显卡，需要了解哪些信息，以及如何真正让它跑起AI训练/推理？

答案：

## 硬件实情

MI50基于**Vega 20 (gfx906)** 核心，台积电7nm工艺，2018年11月发布。你的16GB版本（PCB编号可能为`100-506143`）规格：26.5 TFLOPS FP16、13.3 TFLOPS FP32、6.6 TFLOPS FP64（HPC工作负载），16GB HBM2显存带ECC，带宽约1024 GB/s。这个带宽数字才是2026年你还值得买这张卡的原因——差不多和RTX 3090一个水平，比之后发布的大多数消费级显卡都强。计算能力（FP16 TFLOPS）按现在标准看比较一般；你买的是带宽。

这是一张无风扇的服务器显卡——专为强制风冷机箱设计。如果你的卡裸放在桌面上，需要配一个涡轮散热罩或3D打印的风扇支架，否则会因过热降频。在裸卡/无散热条件下进行10分钟压力测试后达到90°C属于临界但不算危险——配个像样的风扇后，持续负载下目标温度应在82°C或以下。

## 真正的问题：ROCm支持时间线

这部分比硬件本身更重要。gfx906在2023年第三季度进入维护模式（与ROCm 5.7对齐），2024年第二季度结束维护——ROCm 5.7之后不再有新功能/性能优化。截至ROCm 7.0，AMD的Compute Profiler完全移除了MI50/MI60专用数据（不过这看起来像是意外的范围蔓延，并非有意——AMD的AI软件副总裁表示会考虑撤销）。

实际影响（已有人用MI50微调Gemma 2B/9B证实）：ROCm 6.x官方不支持GCN5.1/gfx906，非官方尝试会导致加载模型时段错误。降级到ROCm 5.7.3即可解决一切问题。这带来连锁反应：PyTorch 2.4+需要ROCm 6.x，所以你只能使用PyTorch 2.3.1；Python 3.12在Dynamo下会破坏PEFT的初始化，所以请用Python 3.11。

**训练/微调**可用的技术栈：

```bash
# 强烈推荐Ubuntu 22.04 LTS而非24.04，以保证驱动稳定性
# ROCm 5.7.3是gfx906最后一个官方支持的版本
wget https://repo.radeon.com/amdgpu-install/5.7.3/ubuntu/jammy/amdgpu-install_5.7.50703-1_all.deb
sudo apt install ./amdgpu-install_5.7.50703-1_all.deb
sudo amdgpu-install --usecase=rocm --no-dkms

# 必须固定以下精确版本——这是强制性的
pyenv install 3.11.9
pyenv local 3.11.9
pip install torch==2.3.1+rocm5.7 --index-url https://download.pytorch.org/whl/rocm5.7
```

在执行其他操作之前，先验证显卡是否被正确识别：

```bash
rocminfo | grep -A2 "Marketing Name"
rocm-smi --showproductname --showmeminfo vram --showtemp
```

确认`rocminfo`中显示`gfx906`，且16GB显存正确报告，ECC已启用（`rocm-smi --showmemuse` / 检查`EDC`/`ECC`字段）。这是你在二手卡上真正的验收测试——卖家声称"ECC正常，无维修"应该在此处可验证，而非仅凭信任。

## 用于推理：绕过所有麻烦

llama.cpp + gguf可以在ROCm 5.7上无需修改即可稳定运行，有人在这张卡上对Llama-3-70B-Q4_K_M实现了100–110 tokens/sec。考虑到你对MoE/DeepSeek的兴趣，这比与PyTorch训练兼容性死磕更有用。如果你的实际目标是廉价服务量化后的30B+模型，这张卡在llama.cpp/vLLM模式下才能真正发挥作用——用它训练只是好奇探索，不是生产路径。

```bash
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
HIPCXX=$(hipconfig -l)/clang HIP_PATH=$(hipconfig -R) \
cmake -S . -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx906 -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j$(nproc)
```

## 融入你的技术栈

鉴于你已经拥有RTX 4070工作站和按需使用的MI300X来处理真正的MoE/DeepSeek v4工作，MI50的角色应该很明确：充当廉价常开的16GB HBM2本地推理服务、生成embedding，或者进行ROCm内核开发/测试——避免消耗AMD Dev Cloud的按小时费用。不要用它来跑正经的微调任务——ROCm 5.7的天花板意味着没有flash-attention-2、没有现代量化内核、部分算子不支持bf16。它是一台带宽便宜的推理机，而不是训练机，不管闲鱼上的描述如何暗示"适合AI训练"。

还有一件事值得检查（毕竟是二手）：避开早期PCB版本"100-506142"——它缺乏稳定的VBIOS选项；如果你的卡在PCIe上能被干净枚举，并通过`rocminfo`正确报告16GB+ECC，那无论版本号如何，你得到的都是能正常工作的卡。

参考链接：

- [ROCm System Requirements (Linux)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html)
- [GPU Hardware Specifications — ROCm Documentation](https://rocm.docs.amd.com/en/develop/reference/gpu-arch-specs.html)
- [Fine-Tuning Large Language Models on AMD Instinct MI50 — Medium](https://medium.com/@nejc.fosnaric/fine-tuning-large-language-models-on-amd-instinct-mi50-54118824fcd1)
- [How to Choose the AMD Radeon Instinct MI50 for Local AI](https://electronics.alibaba.com/buyingguides/mi50-32gb-guide-is-it-worth-it-for-local-llms)
- [AMD Hardware Would Ideally Be Supported By ROCm For ~10 Years — Phoronix](https://www.phoronix.com/news/AMD-ROCm-Hardware-Length)
- [Support your GPUs for 8+ years — ROCm/ROCm Discussion #3893](https://github.com/ROCm/ROCm/discussions/3893)
- [AMD Radeon Instinct MI50 16GB — Exxact](https://www.exxactcorp.com/AMD-100-506077-E195930514)
