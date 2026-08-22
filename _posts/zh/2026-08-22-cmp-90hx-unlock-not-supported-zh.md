---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CMP 90HX 解锁不支持
translated: true
type: note
---

问题：`amoghmunikote/cmpunlocker` 能否用于解锁 NVIDIA CMP 90HX？

答案：

不行，**原始的 `amoghmunikote/cmpunlocker` 无法直接解锁 CMP 90HX**。该项目专门针对 **CMP 170HX（GA100）** 编写，其目标 PCI ID 为 `10de:20c2` / `10de:2082`（CMP 170HX 变体），解锁逻辑适用于 GA100 HBM2e 几何结构及 SM 解锁。（[GitHub][1]）

CMP 90HX 是另一款不同的 GPU：

* CMP 170HX → **GA100**（A100 芯片）
* CMP 90HX → **GA102**（RTX 3080 级别芯片）（[GitHub][2]）

由于 Falcon/GSP 固件不同，利用路径也有所区别。原始的 ROP payload 和寄存器偏移量并不通用。（[GitHub][2]）

对于 CMP 90HX，你需要一个 **针对 90HX 的专用分支/工具**。社区已有以下移植版本：

* `WildFlash1st/cmp90hx-unlock` — 针对 CMP 90HX 的研究移植版。该版本增加了 GA102 支持（`PCI ID 10de:220d`），但完整解锁仍处于实验阶段；自述文件指出利用链可激活，但 PLM 解锁仍需完善 ROP 工具。（[GitHub][2]）
* `pearlfortune/cmpunlocker` — 更新版分支，新增 CMP 90HX 支持，并提供 `compute90hx-v67` 路径。其中列出了经测试的 CMP 90HX 环境及命令示例，例如：

```bash
sudo ./cmpunlocker-rs compute90hx-v67 run \
  --all-cmp90hx \
  --acknowledge I-ACCEPT-90HX-V67-COMPUTE-UNLOCK

sudo ./cmpunlocker-rs compute90hx-v67 verify \
  --all-cmp90hx \
  --expect full
```

（[GitHub][3]）

对于 AI 工作站而言，CMP 90HX 之所以值得关注，是因为它本质上是一款功能受限的 GA102 显卡：

* 10GB GDDR6X
* 320-bit 显存位宽
* 约 760 GB/s 带宽
* RTX 3080 级别芯片（[VideoCardz.com][4]）

但其价值定位与 CMP 170HX 不同：

* CMP 170HX 解锁 → 可达 40/64GB 显存，对大型语言模型提升巨大
* CMP 90HX 解锁 → 主要解锁计算/功能，**显存仍为 10GB**（[GitHub][2]）

针对你的 AI 应用场景（Qwen/DeepSeek 推理、LoRA、训练实验），CMP 90HX 仍受限于 10GB 显存。一块便宜的 3090 24GB、RTX A5000 24GB 或已解锁的 CMP 170HX 会更具吸引力。

参考来源：

* amoghmunikote/cmpunlocker（CMP 170HX）（[GitHub][1]）
* WildFlash1st/cmp90hx-unlock（CMP 90HX 研究）（[GitHub][2]）
* pearlfortune/cmpunlocker（CMP 90HX 支持）（[GitHub][3]）

[1]: https://github.com/amoghmunikote/cmpunlocker?utm_source=chatgpt.com "GitHub - amoghmunikote/cmpunlocker: 一款用于解除 NVIDIA 显卡限制的工具！"
[2]: https://github.com/WildFlash1st/cmp90hx-unlock?utm_source=chatgpt.com "GitHub - WildFlash1st/cmp90hx-unlock: 解锁 NVIDIA CMP 90HX (GA102)：内核 6.12 移植版 + Falcon ROP 利用研究。欢迎贡献者加入！"
[3]: https://github.com/pearlfortune/cmpunlocker/blob/main/README.en.md?utm_source=chatgpt.com "cmpunlocker/README.en.md at main · pearlfortune/cmpunlocker"
[4]: https://videocardz.com/newz/nvidia-crypto-mining-processor-90hx-card-is-based-on-ampere-ga102-100-gpu?utm_source=chatgpt.com "NVIDIA Crypto Mining Processor 90HX 显卡基于 Ampere GA102-100 GPU - VideoCardz.com"