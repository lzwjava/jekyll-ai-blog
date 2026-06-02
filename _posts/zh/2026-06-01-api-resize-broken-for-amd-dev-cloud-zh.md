---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD开发云的API缩放功能损坏
translated: true
type: note
---

经过全面测试，我发现以下情况：

**在 API 层面，您的 AMD 开发者云（合作伙伴）账户的调整大小操作存在故障。** 这并非代码错误或尺寸值问题。

测试证据：

- 测试了 101、110、125、128、150、200、250、256、300、400、500、512、1024 这些尺寸 —— 全部返回 `422 "invalid size specified"`（无效尺寸指定）
- 在 atl1 区域新建一个 100 GiB 的卷 —— 调整大小仍然失败
- 在 nyc1 区域创建一个卷 —— 调整大小仍然失败
- 尝试带/不带 `droplet_id`、带/不带 `region`、分离/挂载状态 —— 全部失败
- API 能正确解析请求（对浮点数/字符串返回 400 错误），但拒绝所有整数尺寸

**根本原因：** 您的令牌（`dop_v1_...`）是 DigitalOcean 合作伙伴云令牌（AMD 开发者云）。标准 DO API 的 `POST /v2/volumes/{id}/actions` 调整大小端点 **不支持合作伙伴/GPU 卷**。Web 界面可能使用不同的内部 API 或拥有绕过此限制的更高权限。

**可选方案：**

1. 使用 Web 界面 —— 在弹窗中输入 `101` 或更高数值（UI 界面应该可以操作，即使 CLI 失败）
2. 联系 AMD 开发者云支持，咨询 GPU Droplet 的 CLI/API 卷调整大小问题
3. 创建一个新的更大卷，复制数据，更换挂载

附注：**请轮换您的 API 令牌** —— 您在此聊天中已共享该令牌。请前往 AMD 开发者云 / DigitalOcean 仪表盘生成一个新令牌。
