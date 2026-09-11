---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MODS和MATS旗帜参照
translated: true
type: note
---

首先直说：**MODS 是 NVIDIA 内部工具，从未公开文档化。** 不同 MODS 版本（367 / 400 / 455 构建）的确切标志列表不同，而流传的大多数“文档”来自 GPU 维修社区。因此，下面是维修工作中实际使用的标志的实用参考——以及如何从您手头的二进制文件中自行导出完整列表。

## 1. 从您自己的二进制文件中获取真实帮助（最可靠）

```bash
# From the shell (before mods loads):
./mods -h                # or --help / -help, varies by version
./mats -h

# After MODS loads (you get a "mods>" prompt):
help                     # lists available JS console commands
help -all                # more detail in some versions
./help.js                # some builds ship a help script
```

`-h` 输出由您正在运行的确切二进制文件生成——这是您版本权威的标志列表。如果您在自己的镜像上运行并将输出粘贴在这里，我可以翻译/解释每个标志。

## 2. 已知 MODS 启动标志

```bash
./mods [flags] script.js [script args]
```

| 标志 | 含义 |
| --- | --- |
| `-skip_rm_state_init` | 跳过完整的资源管理器初始化——在原始硬件级别访问 GPU（对于故障卡至关重要，如前所述） |
| `-notest` | 加载 MODS 并驻留，不运行任何测试脚本 |
| `-d N` | 调试/详细级别（数值越大日志越多，例如 `-d 5`） |
| `-verbose` | 详细输出（相当于提高调试级别） |
| `-gpuid N` / `-gpu N` | 当存在多个 GPU 时，定位特定 GPU |
| `-sysrm` | 使用系统驱动的 RM 而非 MODS 内部的 RM（维修中很少有用） |
| `-sim` | 仿真/模拟模式（芯片 bring-up 环境；在真实卡上无用） |
| `-noinit` / `-skip_dev_init` | 完全跳过设备初始化（某些构建） |
| `-trace` / `-tracefile x` | 导出内部跟踪以进行调试 |

⚠️ 并非所有标志在每个构建中都存在——较旧的 367 构建标志较少。

## 3. 已知的 `gputest.js` 参数（脚本参数，而非 mods 本身）

```bash
./mods gputest.js -skip_rm_state_init -notest
./mods gputest.js -skip_rm_state_init -mfg -notest        # 367 builds
./mods gputest.js -skip_rm_state_init -short -notest      # 400 builds
./mods gputest.js -skip_rm_state_init -oqa -test 118 -matsinfo
```

| 参数 | 含义 |
| --- | --- |
| `-mfg` | 运行“制造”测试流程——快速的工厂自检（367 时代构建） |
| `-short` | 简短测试套件——快速通过/失败屏幕而非完整套件（400 时代构建） |
| `-notest` | 不运行测试，仅设置环境 |
| `-oqa` | 输出/QA 模式——以 QA 格式报告结果 |
| `-test N` | 运行特定的测试编号（例如，**test 118 = matsinfo**，用于确认故障是内存还是核心的 VRAM/模块信息测试） |
| `-matsinfo` | 生成 MATS 风格的信息输出（与 `-test 118` 搭配使用） |

`-test N` 数字是最有趣的部分——不同的 N 值运行不同的子测试（内存、显示、PCIe、时钟域…）。测试 118 是手册用来区分核心故障和 VRAM 故障的测试。

## 4. 已知 MATS 标志

```bash
./mats -e 10          # single visible GPU
./mats -n 1 -e 10     # target 2nd GPU (dGPU when iGPU is #0)
./mats -3d_card -e 10 # force 3D-class device path
```

| 标志 | 含义 |
| --- | --- |
| `-e N` | **范围**——测试 N MB 帧缓冲。`-e 10` = 10MB 快速扫描；数字越大，测试越深越慢 |
| `-n N` | **设备索引**——测试哪个 GPU（0 = 第一个枚举的设备，通常是 iGPU） |
| `-3d_card` | 初始化为 3D/图形类设备而非计算设备——某些流程需要 |
| `-auto` | 自动运行，无需交互（某些构建） |
| `-maxerrors N` | 遇到 N 个错误后停止，而非扫描所有 |
| `-pattern X` | 强制特定的内存写入模式（某些构建） |
| `-help` | 导出此构建的实际标志列表 |

## 5. 在 `mods>` 提示符内——有用的控制台命令

一旦加载 MODS（即使使用 `-notest`），您就进入了交互式 JS shell。常用命令：

```
help                  # 列出命令
test 118              # 直接运行测试 118
run gputest.js        # 稍后加载一个脚本
dev.list()            # 列出检测到的 GPU        (名称因构建而异)
board                 # 显示板卡信息
exit / quit           # 退出 mods
```

（确切的方法名称因构建而异——`help` 是您的好帮手。）

## 6. 实用的维修工具包——4个关键命令

实际维修中，90% 的工作只需以下这些：

```bash
# ① 环境（必须看到 PASS，否则卡不可达）
./mods gputest.js -skip_rm_state_init -notest

# ② 在 dGPU 上测试 VRAM
./mats -n 1 -e 10
less report.txt

# ③ 区分核心 vs VRAM 故障
./mods gputest.js -oqa -test 118 -matsinfo

# ④ 关机/重启
reboot / poweroff
```

**我的建议：** 既然您的镜像已经在磁盘上，请运行以下两个命令并粘贴输出：

```bash
cd /home/400.281.2    # 或您版本的目录
./mods -h
./mats -h
```

这将为我们提供您构建的*确切*标志集——我上面表格中超出这些的内容都取决于版本，值得与输出结果进行核对。
