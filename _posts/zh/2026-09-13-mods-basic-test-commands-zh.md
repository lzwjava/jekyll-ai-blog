---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MODS基本测试命令
translated: true
type: note
---

根据 MODS 诊断文档，以下是运行基本测试的方法：

## 基本 MODS 测试命令

### 1. 运行标准制造测试套件

```bash
mods gputest.js -mfg
```

这将在所有检测到的 GPU 上运行完整的制造测试套件。

### 2. 通过 ID 运行特定测试

```bash
mods gputest.js -mfg -test <test_number>
```

例如，测试 58 = Random2D，测试 61 = GpuDmaTest，测试 2 和 79 对应 GLStress/TurboCipher 等。

### 3. 跳过特定测试

```bash
mods gputest.js -mfg -skip <test_number>
```

### 4. 针对特定 GPU 设备

```bash
mods gputest.js -mfg -dev <device_id>
```

例如，`-dev 0` 对应第一个 GPU，`-dev 1` 对应第二个，以此类推。

### 5. 在所有 GPU 上并发运行测试

```bash
mods gputest.js -mfg -concurrent_devices
```

### 6. 每个 GPU 运行不同的测试

```bash
mods gputest.js -mfg -concurrent_devices -test 58 -dev 0 -test 61 -dev 1 -test 2 -test 79 -concurrent
```

这将在 GPU 0 上运行 Random2D，同时在 GPU 1 上并发运行 GLStress 和 TurboCipher。

### 7. 保存/加载自定义测试规格

```bash
# 将当前规格保存到文件
mods gputest.js -mfg -savespec my_spec.txt

# 使用保存的规格运行
mods gputest.js -readspec my_spec.txt
```

### 8. 在主测试运行时运行后台测试

```bash
mods gputest.js -mfg -threadid -dev 1 -bgtest_flags 16 disp,roe -dev 0 -skip 24 -skip 17
```

这将在设备 1 上以后台线程运行测试 16（开启显示和出错继续运行），同时在设备 0 上运行完整套件（跳过测试 24 和 17）。

### 9. 启用线程日志

```bash
mods gputest.js -mfg -threadid
```

在每个日志行前添加线程 ID 信息，用于调试。

---

**关键标志总结：**

| 标志 | 用途 |
| --- | --- |
| `-mfg` | 制造测试规格 |
| `-slt` | 系统级测试规格 |
| `-test N` | 运行指定测试编号 N |
| `-skip N` | 跳过测试编号 N |
| `-dev N` | 针对 GPU 设备 N |
| `-concurrent_devices` | 在所有 GPU 上同时运行 |
| `-bgtest N` | 将测试 N 作为后台线程运行 |
| `-threadid` | 在日志中显示线程 ID |
| `-concurrent` | 在同一 GPU 上并发运行测试 |

MODS 工具由 JavaScript 驱动，因此你也可以使用 MODS 的 JavaScript API 编写自定义测试脚本（例如 `g.Thermal.SetFanSpeed()`、`this.SignalSetupCompleteAndWait()` 等）。
