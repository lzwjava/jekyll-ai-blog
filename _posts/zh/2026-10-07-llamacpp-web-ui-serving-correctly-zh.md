---
audio: false
generated: true
image: false
lang: zh
layout: post
title: llama.cpp Web UI服务正常运行
translated: true
type: note
---

🎉 **已修复！Web UI 现在可以正常提供服务。**（415 错误只是因为 curl 没有发送 `Accept-Encoding: gzip` —— 真实浏览器总是会发送的，你之前看到的 JSON 错误已被 UI 取代。）

`GET /` → **200** ✅ · 静态资源 → **200** ✅

## 在浏览器中打开

```
http://192.168.1.137:8080/
```

你将看到 llama.cpp 的聊天 UI（它会自动连接到 M40 上的 Qwen2.5-14B 模型）。

## 最终状态 — 所有操作完成 ✅

| Item | Status |
| --- | --- |
| Tesla M40 24GB 正常运行（BIOS "Above 4G"，驱动 550.163.01） | ✅ |
| llama.cpp 为 Maxwell 编译（CUDA sm_52 + MMQ） | ✅ |
| Qwen2.5-14B-Instruct Q5_K_M（10.5GB）完全在 GPU 上 | ✅ |
| llama-server 运行在 :8080（API + **web UI**） | ✅ 运行中 |
| Web UI 已嵌入并 gzipped | ✅ |
| 自动挂起已禁用（systemd + GNOME） | ✅ — 全天候保持运行 |
| 速度 | **~38 t/s 提示处理, ~13.6 t/s 生成** |

## 快速参考

```bash
# 终端聊天
~/projects/run-chat.sh

# 必要时重启服务器
~/projects/run-server.sh        # web UI + OpenAI API 在 :8080

# OpenAI 兼容 API
http://192.168.1.137:8080/v1   (model = .gguf 路径)
```

⚠️ 提醒：未设置 API 密钥——请将端口 8080 仅保留在局域网内使用。

是否还需要我配置 **systemd 服务**（每次启动时自动启动 llama-server）？否则此方案已完全可用——尽情享受吧！🚀
