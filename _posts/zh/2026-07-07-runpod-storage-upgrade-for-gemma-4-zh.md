---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma 4 的 RunPod 存储升级
translated: true
type: note
---

问题：如何升级 RunPod 存储配额，以便 Gemma 4 26B A4B AWQ 模型能够容纳？

回答：

您的 `/workspace` 很可能是一个大小较小（约 10GB）的 **RunPod Network Volume**。您需要增加 **Network Volume 的大小**，而不是 Pod 的 GPU/容器磁盘。RunPod 支持后续增加网络卷大小，但**之后无法减小**。（[Runpod 文档][1]）

## 方案 A — RunPod Web UI（推荐）

1. 打开 RunPod 控制面板：

   * 前往 **Storage**
   * 找到您的 Network Volume

2. 编辑该卷：

   * 将大小从：

     ```
     10 GB
     ```

     增加到类似：

     ```
     50 GB
     ```

3. 重启/重新连接您的 Pod。

RunPod 的文档指出网络卷大小之后可以增加，但不能减小。（[Runpod 文档][1]）

对于您的情况，我会选择：

```
Gemma 4 26B A4B AWQ
约20GB 模型

+ tokenizer
+ SGLang 缓存
+ LibreChat
+ 日志

最低：
40 GB

舒适：
50 GB
```

---

## 方案 B — API

RunPod 提供了一个更新端点：

```bash
curl --request POST \
  --url https://rest.runpod.io/v1/networkvolumes/<NETWORK_VOLUME_ID>/update \
  --header "Authorization: Bearer <RUNPOD_API_KEY>" \
  --header "Content-Type: application/json" \
  --data '
{
  "size": 50
}
'
```

新大小必须大于当前大小。（[Runpod 文档][2]）

---

## 检查当前卷

在 Pod 内：

```bash
df -h /workspace
```

您可能会看到类似：

```
Filesystem      Size Used Avail
moosefs         10G  10G     0
```

调整大小后：

```
Filesystem      Size Used Avail
moosefs          50G  10G    40G
```

---

## 重要：不要混淆这三种存储

RunPod 提供：

```
容器磁盘
    |
    | 临时
    | Pod 移除时删除


卷磁盘
    |
    | Pod 本地


网络卷 (/workspace)
    |
    | 持久化
    | 模型存储
```

对于 LLM 服务，您需要 Network Volume。（[Runpod 文档][1]）

---

## 我对您配置的建议

鉴于您正在构建：

```
SGLang
   |
   |
LibreChat
   |
   |
本地 LLM API
```

我会一次性升级：

```
10GB  ❌
50GB  ✅
100GB ⭐
```

50GB 足够容纳：

```
Gemma4-26B-A4B-AWQ     20GB
Qwen2.5-14B-AWQ         8GB
embeddings              1-2GB
LibreChat               2GB
缓存                    5GB
```

这样您就可以随时更换模型，而不必每次都纠结于存储空间。（[Runpod 文档][1]）

参考：

* RunPod Network Volumes 文档（[Runpod 文档][1]）
* RunPod Network Volume 更新 API（[Runpod 文档][2]）

[1]: https://docs.runpod.io/storage/network-volumes?utm_source=chatgpt.com "Network volumes - Runpod Documentation"
[2]: https://docs.runpod.io/api-reference/network-volumes/POST/networkvolumes/networkVolumeId/update?utm_source=chatgpt.com "Update a network volume - Runpod Documentation"
