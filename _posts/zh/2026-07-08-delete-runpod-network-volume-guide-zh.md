---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 删除RunPod网络数据卷指南
translated: true
type: note
---

问题：当我尝试删除 RunPod 网络卷时，系统提示需要先从所有 pod 中移除该卷——我是否需要删除 pod？

回答：

是的——但“移除”并不总意味着完全删除，有一个常见的陷阱：**serverless 端点也算作附件，而不只是 pod。**

**步骤：**

1. **停止/终止任何使用该卷的 Pod。** 如果某个 pod 挂载了该网络卷，你需要：
   - 完全终止该 pod，或者
   - 编辑 pod 并分离该卷（如果 RunPod 的 UI 支持在不终止的情况下更换存储——对于 GPU pod，通常无法原地操作；你通常必须终止）。

   实际上，在 RunPod 上，网络卷在 pod 创建时绑定（你在数据中心锁定的配置中选择卷），因此**没有实时的“分离”按钮**——你必须终止 pod。

2. **同时检查 Serverless 端点。** 这是人们容易遗漏的部分（参见上面的社区讨论——“没有正在运行的 pod”但仍然被阻止）。如果任何 **Serverless 端点**（而不是 pod）在其模板/工作器配置中引用了该卷，它同样会阻止删除。前往 Serverless → 检查每个端点的模板中是否包含该卷，然后删除或编辑这些端点。

3. **然后删除该卷**，可以通过 UI 或 API：
```bash
curl --request DELETE \
  --url https://rest.runpod.io/v1/networkvolumes/{networkVolumeId} \
  --header 'Authorization: Bearer <API_KEY>'
```

**重试删除前的快速检查清单：**
- [ ] 所有使用该卷的 pod 都已终止（不仅仅是停止——停止的 pod 仍会持有卷引用）
- [ ] 所有引用该卷的 serverless 端点已被删除或重新配置
- [ ] 终止后等待约 30 秒——RunPod 的后端有时会延迟释放锁

如果你确认 pod 和 serverless 都已清理干净，但仍然被阻止，这是已知的 RunPod 后端 bug（参见 2025 年 3 月的讨论帖）——建议联系他们的 Discord/支持，因为 UI 状态可能会卡住。

参考资料：

- [Delete a network volume - Runpod API Docs](https://docs.runpod.io/api-reference/network-volumes/DELETE/networkvolumes/networkVolumeId)
- [Why can't I delete my storage - RunPod Community](https://www.answeroverflow.com/m/1351866718041145408)