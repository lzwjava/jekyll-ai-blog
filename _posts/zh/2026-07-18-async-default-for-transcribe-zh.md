---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 转录的异步默认
translated: true
type: note
---

已提交并推送：`c4371e3`。

现在 `ww gcp-speech transcribe` 默认使用**异步模式**——上传文件、提交任务、打印GCS输出路径和控制台链接，然后立即退出。无需等待。

```bash
# 异步（默认）——提交后稍后查看控制台
ww gcp-speech transcribe wh1_merged.mp3 --lang cmn-Hans-CN

# 等待模式——阻塞直到完成，下载并打印转录文本
ww gcp-speech transcribe wh1_merged.mp3 --lang cmn-Hans-CN --wait
```

控制台链接指向GCS存储桶文件夹，结果将出现在那里。完成后，您也可以使用 `gsutil cp` 手动获取结果，并使用 `ww transcript` 进行转换。