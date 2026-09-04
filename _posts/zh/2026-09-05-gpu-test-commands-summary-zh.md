---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU测试命令摘要
translated: true
type: note
---

## 6. 常用命令汇总

### NVIDIA（N卡）测试流程

| 步骤 | 描述 | 命令/操作 |
|------|------|-----------|
| 1 | 开机，按 **F8** 选择 **Legacy/Traditional mode** 启动 | — |
| 2 | 根据显卡型号选择对应程序：**1/2/3** = 主要用于N卡，**4/5/6** = 主要用于A卡 | — |
| 3 | 程序自动运行（通过或失败——暂时忽略），然后输入 | `LS` |
| 4 | 查看主目录中的测试程序（例如 GT610 ~ GTX980i） | — |
| 5 | 进入测试版本目录，例如 400.250 | `CD 400.250` |
| 6 | 运行测试命令 | `./MATS –e 10` |
| 7 | 如果运行成功，说明GPU供电正常；否则检查GPU状态或尝试其他版本 | — |
| 8 | 查看测试结果（FBI0A0 = VRAM；无数字表示正常，有数字表示故障） | `nano report.txt` |
| 9 | 退出编辑器 | `Ctrl+X` 或 `Ctrl+Z` |
| 9' | 返回主目录 | `CD ..` |
| 10 | 重启 / 关机 | `reboot` / `poweroff` |

### GPU无显示时——使用iGPU测试dGPU（步骤11–30）

1. **步骤11–14**：将外接显示器插入主板。按 **Del** 进入BIOS（以ASUS H170 PRO为例）→ 按 **F7** 进入高级模式 → **Advanced** → **System Agent (SA) Configuration** → **Graphics Configuration** → 将 **Primary Display** 设置为 **CPU Graphics**（iGPU）或 **PCIE**（dGPU）→ **F10** 保存并退出。
2. **步骤16**：进入版本400.250，运行 `./mats –e 10`
3. **步骤18**：**先设置环境**（使用iGPU测试dGPU时必须执行）：
   ```
   ./mods gputest.js -skip_rm_state_init -notest
   ```
4. **步骤19**：必须看到 **PASS** 画面才能继续，否则GPU存在硬件故障（供电或核心）。
5. **步骤20**：在后台运行测试：
   ```
   ./mats -n 1 -e 5
   ```
6. **步骤21**：查看结果：
   ```
   less report.txt
   ```
   （FBI0A0后全为零 = PASS；有数字 = FAIL）
7. **步骤27 —— N卡显存布局**：
   - 双面卡：A面 = 高字节 32–63，B面 = 低字节 0–31
   - 单面卡：左（下）侧 = 高字节 32–63，右（上）侧 = 低字节 0–31
8. **步骤29 —— 二次验证**（确认核心或显存故障）：
   ```
   ./mods gputest.js -oqa -test 118 -matsinfo
   ```

### AMD（A卡）测试关键命令

- RX580及以下选择 **选项4**。针对240：`./240` → 查看结果 `./240g`；通道 `ChC/ChD/ChA/ChB/ChE/ChF/ChG` 无数字表示正常。
- 针对RX580：`./rx580a6` → 查看结果 `./rx580a6g`；`ChB1/ChA0/ChA1/ChC0/ChC1` 显示 `55555555` 表示通道故障。
- 针对RX5700：`CD rx57009` → `./tserver –boardtest=memfa` → 查看结果 `Pico memfa.log`。
- **A卡显存布局**：低字节在左（下）侧 0–31，高字节在右（上）侧 32–63。

> 注：原手册中步骤3和9各出现两次（重复的"9"实际上是第二次出现，与步骤8的布局内容重叠）。