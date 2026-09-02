---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MATS TServer 2in1 pmfx诊断镜像
translated: true
type: note
---

## 问题

`Mats-4090_Tserver-6900_2in1.pmfx` —— 这是较新的 **MATS/TServer GPU VRAM 诊断工具**吗？其中的 `.pmfx` 文件扩展名代表什么？

## 回答

是的。该文件名强烈表明它是一个**同时包含 NVIDIA MATS 和 AMD TServer 的可启动/测试镜像**，专门针对较新 GPU 设计：

```text
Mats-4090_Tserver-6900_2in1.pmfx
│         │          │
│         │          └── 二合一镜像
│         └───────────── 用于 AMD / 6900 系列显卡的 TServer
└────────────────────── 用于 NVIDIA / RTX 4090 的 MATS
```

关键区别如下：

### 1. MATS = NVIDIA VRAM 诊断

MATS 是一种底层 NVIDIA 内存测试工具。它通过 GPU 的帧缓冲内存接口写入/读取特定模式，并按照 **FBIO 子分区/通道** 报告错误，例如：

```text
FBIOA0   0   0   0
FBIOA1   0   0   0
FBIOB0   0   0   0
FBIOB1   0 560   0   <-- 错误
FBIOC0   0   0   0
...
```

这对 GPU 维修极为有用，因为像 `FBIOB1` 这样的错误可以帮助你定位**需要检查的 VRAM 芯片/通道**。([Бытовая техника для дома -][1])

但重要的是：

> **MATS 报告 VRAM 通道错误，并不自动意味着 VRAM 芯片本身损坏。**

故障也可能来自：

```text
VRAM 芯片
   ↓
PCB 走线 / 焊点
   ↓
供电 / 信号
   ↓
GPU 内存控制器
```

一个维修参考资料明确警告，MATS 错误可能源于 GPU 内存控制器或内存缺少信号/电压。([ААНТ КОНТАКТ][2])

### 2. TServer = AMD 等效工具

TServer 用于 AMD 显卡。常见的内存诊断命令是：

```bash
./tserver -boardtest=memfa
```

并生成内存故障分析日志。([PPT Online][3])

因此，一个标记为：

```text
MATS + TServer
```

的软件包，本质上就是**同时支持 NVIDIA 和 AMD 的 GPU 维修技师诊断环境**。

### 3. 为什么是 `4090` 和 `6900`？

这个软件包很可能围绕以下支持构建：

```text
NVIDIA:
RTX 4090
       ↓
     MATS

AMD:
RX 6900 XT / 6900 系列
       ↓
    TServer
```

具体支持的 GPU 列表在很大程度上取决于 **MATS/MODS 的构建版本及 GPU 架构**。你不应该因为文件名写着 `4090`，就假设所有 Ada 显卡或所有 40 系列 GPU 都能被正确支持。

这一点非常重要：使用不合适的 MATS/MODS 版本可能会产生错误的结果。([ААНТ КОНТАКТ][2])

### 4. `.pmfx` 是什么？

这是最有趣的部分。

`.pmfx` **并不是普通的 MATS 可执行文件本身**。它似乎是这些预构建 GPU 诊断 USB 环境所使用的打包/启动镜像格式。

可以将其理解为：

```text
Mats-4090_Tserver-6900_2in1.pmfx
                 │
                 ▼
        可启动诊断镜像
                 │
        ┌────────┴────────┐
        ▼                 ▼
      NVIDIA             AMD
       MATS             TServer
        │                 │
        ▼                 ▼
      VRAM 测试         VRAM 测试
```

这就是为什么你会看到人们分发巨大的“MATS/MODS/TServer”USB 镜像，而不是仅仅一个 `mats` 二进制文件。已知存在包含 NVIDIA MATS/MODS 和 AMD TServer 环境的多分区可启动镜像。([RMPrepUSB][4])

---

### 针对你的 GPU 维修实验

这正是**你需要的工具类型**。

例如，对于疑似 RTX 4090 VRAM 问题，你的工作流程可能变成：

```text
RTX 4090
   │
   ├── 目视检查
   │
   ├── 对地电阻测量
   │
   ├── 电源轨
   │
   ├── PCIe 初始化
   │
   ├── MATS
   │      │
   │      └── FBIO? 错误
   │
   ├── 将 FBIO 通道映射到物理 VRAM 芯片
   │
   ├── 检查 VRAM 供电 / CLK / CMD / DQ
   │
   └── 判断：
          VRAM 芯片损坏？
          焊点/BGA 问题？
          PCB 问题？
          GPU 内存控制器问题？
```

这远比仅仅运行 FurMark/3DMark 更接近**实际的板级诊断**。

一个有用的细节：MATS 可以配置为测试指定数量的 VRAM，例如 `-e 20`，或使用 `-c` 测试百分比；某些环境先使用少量内存进行快速测试，然后增加数量进行深度测试。([PC1][5])

如果你**手头有实际的 `Mats-4090_Tserver-6900_2in1.pmfx` 文件**，可以在此上传，我可以检查其结构，并告诉你**它里面有什么、如何启动、包含哪个 MATS 版本、是否真正支持 4090，以及如何逐步使用它诊断一块损坏的 4090**。

### 参考

* [MATS/MODS GPU 内存测试说明](https://xn----9sbnsmbfcfrsidc.xn--p1ai/forum/viewtopic.php?p=7216&sid=43dfddeafc5ecabe5df3f628751b0a85&utm_source=chatgpt.com)
* [MATS/TServer 诊断命令和示例](https://rmprepusb.blogspot.com/2022/06/run-nvidia-graphics-memory-tests-from.html?utm_source=chatgpt.com)
* [NVIDIA MATS 内存测试演示](https://en.ppt-online.org/632320?utm_source=chatgpt.com)

[1]: https://instrukciya.top/2023/06/27/proverka-pamyati-videokarty-nvidia-na-oshibki-mats/?utm_source=chatgpt.com "Проверка памяти видеокарты nvidia на ошибки mats - Ремонт и установка крупной бытовой техники"
[2]: https://xn----9sbnsmbfcfrsidc.xn--p1ai/forum/viewtopic.php?p=7216&sid=43dfddeafc5ecabe5df3f628751b0a85&utm_source=chatgpt.com "Скачать MATS MODS: Диагностика видеокарт NVIDIA. Тест видеопамяти Nvidia. Пошаговая инструкция для теста vram - Форум по ремонту ноутбуков, моноблоков, мобильной электроники"
[3]: https://en.ppt-online.org/632320?utm_source=chatgpt.com "VGA Test 2019 - online presentation"
[4]: https://rmprepusb.blogspot.com/2022/06/run-nvidia-graphics-memory-tests-from.html?utm_source=chatgpt.com "RMPrepUSB, Easy2Boot and USB booting: Run nVidia/AMD GPU graphics memory tests from an Easy2Boot drive"
[5]: https://pc1.pp.ua/infa/test-pamyati-videokarty-programmoj-mats?utm_source=chatgpt.com "Мастер Ломастер - Тест памяти видеокарты программой MATS"