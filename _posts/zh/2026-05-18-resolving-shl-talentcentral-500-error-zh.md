---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决SHL TalentCentral 500错误
translated: true
type: note
---

问题：在 `tcplus` 自动登录集成过程中，如何修复 SHL TalentCentral 500 错误？

答案：

详细错误信息显示，问题出现在 **SHL TalentCentral 的自动登录 API** 中，具体如下：

```
POST /epl/api/v1/auth/auto-login
message: "Unable to apply response reuse for candidate on amcat"
status: 500
```

这意味着 **服务器未能处理您候选账户的自动登录请求**（可能由于 AMCAT 集成或会话处理问题）。由于这是 **服务器端问题**，您这边的控制能力有限，但有以下变通方法：

---

### 1. **绕过自动登录**

* 不依赖自动登录，直接打开 TalentCentral 登录页面：
  [https://talentcentral-experience.shlglobal.cn](https://talentcentral-experience.shlglobal.cn)
* 使用收到的凭据或邮件链接手动登录。
* 这样可以避免出错的 `tcplus` 集成流程。

---

### 2. **清理浏览器**

* **清除 SHL 域名的 Cookie 和缓存**。
* 尝试 **无痕/隐私模式**。
* 禁用广告拦截或脚本拦截等扩展程序。

---

### 3. **网络考虑**

* 避免使用可能干扰 API 请求的企业 VPN 或代理。
* 使用稳定的家庭网络。

---

### 4. **等待并重试**

* 500 错误可能是 SHL 侧的临时服务器问题或部署问题。
* 等待几分钟或几小时后，有时会自动解决。

---

### 5. **联系 SHL 支持**

如果手动登录或重试失败：

* 通过电子邮件或电话联系 SHL 支持，并提供：

  * 精确的错误消息和时间戳
  * 您的候选 ID（来自邀请邮件）
  * 控制台日志的截图
* 请他们 **重置您的会话** 或生成 **新的直接登录链接**。

---

### 6. **技术说明**

* `Unable to apply response reuse for candidate on amcat` 表示 **会话令牌重用失败**。这是 SHL 内部针对关联 AMCAT 测试的候选人的逻辑。如果服务器持续失败，只有 SHL 才能修复。

---

**结论：** 最快的变通方法是 **通过主门户手动登录** 或请 HR 提供 **新的登录链接**。如果问题在不同浏览器和网络中持续存在，则 **100% 需要 SHL 进行服务器端修复**。

---

参考资料：

* [SHL 支持](https://www.shl.com/en/support/)
* [HTTP 500 错误说明](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500)

---

如果您愿意，我可以提供 **逐步操作指南，安全绕过自动登录 API 错误并立即访问门户**。您需要我这样做吗？