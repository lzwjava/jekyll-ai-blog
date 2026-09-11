---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MODS命令缺失测试模式
translated: true
type: note
---

问题：这个 MODS 命令有什么问题？

答案：截图显示的是**命令行参数错误**，而非 GPU 硬件故障。

你运行的命令是：

```bash
mods gpuTest.js --skip_rm_state_init --notest
```

关键错误信息如下：

```text
Invalid test mode 0: you must use one of: -mfg -slt -oqa
Error 0000000005: Global.DoCommonTestBookkeeping bad command line argument
```

你的 `--notest` **没有**选择任何 MODS 测试套件。MODS 需要以下测试模式之一：

```bash
# 制造/广泛压力测试
./mods gputest.js -skip_rm_state_init -mfg

# SLT 测试
./mods gputest.js -skip_rm_state_init -slt

# 出厂 QA，通常更轻量/更快
./mods gputest.js -skip_rm_state_init -oqa
```

这与 MODS 文档一致：常规 GPU 测试使用 `-mfg` 或 `-oqa`，而 `-slt` 是另一个已定义的测试规范。（[studylib.net][1]）

### 针对你的 GT730

我建议从以下命令开始：

```bash
cd /home/GT730

./mods gputest.js -skip_rm_state_init -mfg
```

如果你的目的是专门进行 **GPU 维修 / VRAM 诊断**，则可以尝试独立的 MATS：

```bash
./mats -h
```

然后根据该 GT730 是普通显示卡还是无头/矿卡类型，使用相应的 MATS 调用方式。MODS 文档将独立的 MATS 描述为帧缓冲/内存测试，并指出当 MODS 本身无法初始化 GPU 时，该测试尤其有用。（[studylib.net][1]）

因此，当前屏幕显示的本质是：

```text
MODS 本身正在运行
        ↓
gputest.js 已加载
        ↓
命令行参数已解析
        ↓
未选择任何测试套件
        ↓
退出并返回错误 5
```

**这并不意味着 GT730 已损坏。** 你实际上尚未开始 GPU 测试。

[1]: https://studylib.net/doc/28338650/toaz.info-modspdf-pr-d6c4fcd269959d8ff99a0a1323fbc5f6?utm_source=chatgpt.com "NVIDIA MODS Diagnostic Software Manual for 343.X"