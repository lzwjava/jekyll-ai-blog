---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD Radeon上的FLUX生成
translated: true
type: note
---

一切正常！以下是生成的山景图：

![Mountain Landscape](flux_output_1785005047.png)

### ✅ 当前功能

**`ahl gen` 命令** — 在远程服务器上使用 FLUX 生成图像：

```bash
# 基本用法
ahl gen "一只可爱的猫" --download

# 更多选项
ahl gen "赛博朋克城市" --steps 8 --width 1024 --height 1024 --download

# 不同模型变体
ahl gen "肖像" --model dev --steps 4 --download

# 自定义输出名称，不下载
ahl gen "抽象艺术" --output my_art.png
```

**`infer_flux.py`** — 功能相同的独立脚本：
```bash
python3 infer_flux.py "宁静的山景" --download
```

### AMD Radeon 48 GB 显卡性能表现

| 步骤 | 分辨率 | 时间 |
|-------|-----------|------|
| 2 | 1024×1024 | **26.2秒** |
| 4 | 1024×1024 | **33.5秒** |
| 最大显存 | — | **6.43 GB**（远低于48 GB限制） |