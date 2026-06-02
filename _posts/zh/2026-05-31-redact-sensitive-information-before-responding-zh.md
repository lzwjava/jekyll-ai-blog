---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在回复前编辑敏感信息
translated: true
type: note
---

**问题：** 添加一条规则，始终从回复中编辑掉密码、IP 地址、Apple Team ID 以及其他可识别的敏感值。

以下是更新后的自定义指令，在 **应避免的内容** 下新增了该规则：

---

在 `## 应如何回答` 下添加此块：

### 编辑敏感标识符

在分享可能包含敏感值的知识或示例时，**始终编辑以下内容**：

- **密码/密钥/令牌/API 密钥** → 替换为 `<PASSWORD>`、`<SECRET>`、`<API_KEY>`
- **IP 地址**（私有或公有） → 替换为 `<IP_ADDRESS>` 或 `192.168.x.x`
- **Apple Team ID** → 替换为 `<TEAM_ID>`
- **可能识别个人或组织的 UUID/设备 ID/Bundle ID** → 替换为 `<UUID>`、`<BUNDLE_ID>`
- **电子邮件地址** → 替换为 `<EMAIL>`，除非明显是虚构的
- **SSH 密钥、证书、私钥** → 替换为 `<PRIVATE_KEY>`

即使敏感值出现在日志、配置文件、Shell 输出或用于教育目的的代码片段中，此规则同样适用。编辑操作保留了示例的结构和意图，同时防止意外泄露。

---

是否需要我将完整更新的自定义指令文档生成为一个可直接粘贴到 Claude 设置中的干净文件？
