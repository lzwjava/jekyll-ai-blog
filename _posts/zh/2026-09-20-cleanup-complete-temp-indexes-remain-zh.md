---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理完成，临时索引保留
translated: true
type: note
---

已终止——进程已消失，GPU 空闲（桌面使用 1.2 GB），且 `rag_index/` 为空（尚未写入任何内容，因为写入仅在所有嵌入完成后才会进行）。

剩余内容：

- `rag/` 脚本 + `README.md` + `requirements.txt` + 可用的 `.venv`
- 在 `/tmp/rag_smoke`（e5-small，423 个块）和 `/tmp/rag_m3`（bge-m3，652 个块）处的冒烟测试索引
- `rag/logs/build_bge_m3.log`（部分运行，约 20k/186k 个块）

如果需要我再次运行（完整版，或快速的 `--model intfloat/multilingual-e5-small` 变体）或清理临时索引，请说一声。
