---
audio: false
generated: true
image: false
lang: zh
layout: post
title: muda 0.9.0 已推送，只需一条命令
translated: true
type: note
---

已推送 **`muda 0.9.0`**（`62fe80b`）。

## 关于 “do it”——这个阻碍无法绕开

在继续之前我重新检查了：`sudo` 需要交互式密码，而我没有 TTY，并且 `/sys/.../driver/unbind` 对用户不可写。因此我**无法**自行执行 nvidia↔nouveau 切换。只有你能运行那一条命令。其他一切我都能做。

## 作为替代，我做了这些（可测试、可衡量）

**更快的 SGEMM** —— 添加了第二个 register-blocked kernel，并按 size 选择：

- `m,n < 1024`: `sgemm_rb` (64×64, 4×4/thread, 70 regs)
- `m,n ≥ 1024`: `sgemm_rb128` (128×64, 8×4/thread, ~90 regs, better FMA:load ratio)

```
    size  naive GFLOP/s  tuned GFLOP/s   speedup
     256          275.8          603.4     2.19x
     512          320.4         1291.4     4.03x
    1024          286.2         1577.7     5.51x
    2048          318.6         1785.2     5.60x
```

这相比 1024 / 2048 时的 ~1.17 / ~1.43 TFLOP/s 有所提升。Python binding 现在在 2048³ 下显示 **~1.73 TFLOP/s**。在这个过程中发现并修复了一个真实 bug（tile x/y 被互换了，导致静默地产生错误结果——在 benchmark 的 CPU cross-check 中可见）。

完整测试套件依然全绿：**77 项检查 + 4 个 mudac 程序**。

## 我需要你运行的那一条命令

请停止任何使用 M40 的程序，然后：

```sh
cd ~/projects/muda
sudo tools/muda-gpu-mode.sh nouveau      # switch to the open driver
MUDA_DRIVER=nouveau ./build/mudainfo     # test the native backend
MUDA_DRIVER=nouveau ./build/test_memory
```

请粘贴那份输出。要撤销：`sudo tools/muda-gpu-mode.sh nvidia`，或者直接重启（nouveau 仍会留在黑名单中）。

一旦 nouveau 被绑定，我就能作为普通用户打开它的 render node，这样我就能和你**真正地开发和测试** native 路径——先进行 GEM allocation，然后是 compute channel。如果你的 `mudainfo` 输出显示你的 kernel 上的 `GETPARAM`/GEM 常量不同，我会根据输出修复它们。
