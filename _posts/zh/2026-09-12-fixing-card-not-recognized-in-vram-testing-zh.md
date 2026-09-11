---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复VRAM测试中的卡未识别错误
translated: true
type: note
---

我完整读了一遍手册（《显存测试软件使用手册》— VRAM Testing Software Manual，25页，涵盖MODS+MATS的HDD/USB版本）。先纠正几个关于它工作原理的问题，然后解释为什么你会遇到“启动时不识别显卡”的情况。

## 首先，理解MODS和MATS的关系

两者都是NVIDIA内部工具，泄露到维修社区，它们配合工作：

| Tool | 作用 | 类比 |
| --- | --- | --- |
| **MODS** | 加载底层驱动，初始化GPU，运行JS测试脚本（`gputest.js`）——这是“搭建环境”的步骤 | 一个绕过操作系统的迷你驱动+测试框架 |
| **MATS** | Memory Access Test System——逐位读写VRAM，生成`report.txt`，按FBPA/channel报告错误 | 依赖于MODS首先初始化GPU |

所以正确的流程是两步，**而且顺序不能颠倒**：

```bash
cd /home/400.250                      # 选择与你的显卡匹配的版本
./mods gputest.js -skip_rm_state_init -notest   # ① 搭建环境——必须看到PASS
./mats -n 1 -e 10                     # ② 实际测试VRAM（-n 1 = 第二张GPU，也就是独显）
less report.txt                       # ③ 读取结果：FBI0A0后面的数字 = 坏显存芯片
```

当显卡能自己显示时，`./mats -e 10`会自动运行。但**当你用核显（iGPU）测试一张坏掉的独显（dGPU）时，必须先执行第①步**。否则你得到的就是你描述的情况——“无法识别”/“GPU register invalid”错误（就是手册第17步显示的错误）。

## “启动时无法识别”的常见原因（按可能性排序）

1. **在搭建环境之前运行mats**——在“核显宿主独显”的设置中，跳过`./mods gputest.js -skip_rm_state_init -notest`直接运行`./mats -e 10`，总会报“GPU register invalid”错误。
2. **MODS版本与GPU不匹配**——三个版本对应不同的显卡代际（大致：367 → GTX9xx及更低，400 → 10xx/16xx/20xx，455 → RTX 30系列）。版本不对 = GPU无法被枚举。
3. **显卡太新**——这个2021年的镜像只支持到RTX 3090。RTX 40系列、Intel GPU、以及矿卡变体（P106等）**不在支持范围内**——再怎么测也无法识别。
4. **启动模式错误**——菜单项1仅支持Legacy；只有2/3项支持UEFI。在UEFI下你只能测试NVIDIA显卡。选错模式会导致无法启动或什么都检测不到。
5. **显卡核心/供电已损坏**——如果连`./mods gputest.js -skip_rm_state_init -notest`都不显示PASS，说明显卡的供电或核心有故障。**MODS根本初始化不了这种卡；没有软件修复办法。**先检查外部供电（6/8-pin）、PCIe金手指、以及BIOS中的Primary Display设置。
6. **双GPU设置缺少步骤**——必须在BIOS中启用Multi-GPU，并加上`-n 1`来指定独显（否则默认测试核显，当然“什么都显示不出来”）。
7. **内存不足**——手册要求系统内存 ≥ 显存（8GB显卡需要8GB以上内存），否则测试无法运行。

## 手册本身的陷阱（不要照抄它的格式）

- 文本中的`./MATS`、`. /mats`和`–e`（长破折号）都是笔误。真正的命令是**小写的`mats` + ASCII连字符**：`./mats -e 10`，每个空格都很重要。
- 版本目录名：应该是`cd /home/400.281.2`——手册里的“cd /home/ 400.281.2”多了一个空格。
- AMD显卡使用不同的流程：RX580及以下使用`./model`测试，`./modelg`查看结果；RX5700及以上使用`./tserver -boardtest=memfa`，结果在`memfa.log`中。

## 建议的下一步

你说测试还没成功——为了帮你定位问题，请告诉我：

1. 你在什么环境下运行？（这个镜像的哪个菜单项？还是自己搭建的？）
2. 具体是哪张卡？（具体型号，是不是矿卡？）
3. 具体失败在哪一步：**根本进不了启动菜单** / **在目录下运行mods时报错** / **mods从未显示PASS** / **mats报告invalid register**？

每个失败点都指向完全不同的原因。如果是在菜单里运行命令后立刻报错，请粘贴屏幕上的确切错误文本——我通常一眼就能判断是版本选错还是显卡本身无法初始化。
