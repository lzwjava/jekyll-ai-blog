---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Flash-Attn CUDA版本修复
translated: true
type: note
---

## ✅ 完成！`flash-attn==2.8.3` 安装成功

### 发生了什么

真正的问题并非卡住或编译，而是 **CUDA 版本不匹配**：

| 组件 | 预期版本 | 实际版本 |
|-----------|----------|---------|
| **PyTorch CUDA** | 13.0（编译时使用的） | `torch 2.11.0+cu130` |
| **系统 CUDA 12.8** | ❌ | 版本检查失败 |
| **系统 CUDA 13.2** | ❌ | `13.2 != 13.0` |
| **预编译 wheel cu13torch2.10** | ✅ | 使用了该版本 |

### 我做了什么

1. **终止**了 `/mnt/data/` 下无意义的 sm_80 编译过程
2. **发现**你的 PyTorch 需要 CUDA 13.0，而非 12.8
3. **找到**了一个预编译的 wheel，位于：
   ```
   flash_attn-2.8.3+cu13torch2.10cxx11abiTRUE-cp312-cp312-linux_x86_64.whl
   ```
4. **安装**了它——无需编译，瞬间完成安装

### 验证

- `flash-attn` 2.8.3 ✓
- `PyTorch` 2.11.0+cu130 ✓
- `CUDA` 13.0 ✓
- `设备` RTX 4070 ✓
- `flash_attn_func` 导入成功 ✓

**注意：** PyPI 上不存在 `2.8.4` 版本——`2.8.3` 和 `2.8.3.post1` 是最新的。已安装的 `2.8.3` 在功能上与之等效。