---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Hermes设置小米Mimo Plan
translated: true
type: note
---

问题：如何使用 Hermes 代理通过 API `https://token-plan-cn.xiaomimimo.com/v1` 设置小米 Mimo 令牌计划？

答案：

要通过小米 Mimo API 设置或配置令牌计划，通常需要执行以下步骤：

---

### 1. **获取 API 访问权限**

* 确保你拥有一个具有 Mimo 服务访问权限的小米账户。
* 获取小米 Mimo 令牌计划 API 的 **API 令牌** 或 **授权密钥**。

---

### 2. **了解 API 端点**

基础端点为：

```
https://token-plan-cn.xiaomimimo.com/v1
```

关键端点可能包括：

* **GET `/plans`** → 列出可用的令牌计划。
* **POST `/subscribe`** → 订阅特定计划。
* **GET `/usage`** → 查看当前使用量或余额。
* **POST `/update`** → 更改计划或更新订阅信息。

你需要获取准确的 API 文档或 Swagger 规范，以了解所有可用的端点、参数和请求头。

---

### 3. **准备身份验证**

大多数小米 API 使用 **Bearer 令牌** 进行身份验证。请求头示例：

```http
Authorization: Bearer <你的API令牌>
Content-Type: application/json
```

---

### 4. **订阅计划**

订阅的 `POST` 请求示例：

```bash
curl -X POST "https://token-plan-cn.xiaomimimo.com/v1/subscribe" \
-H "Authorization: Bearer <你的API令牌>" \
-H "Content-Type: application/json" \
-d '{
  "planId": "pro_monthly",
  "autoRenew": true
}'
```

参数说明：

* `planId` → 所需计划的 ID（例如月度、年度、Pro 版）。
* `autoRenew` → 订阅是否自动续费。

---

### 5. **查看使用量**

订阅后检查使用量：

```bash
curl -X GET "https://token-plan-cn.xiaomimimo.com/v1/usage" \
-H "Authorization: Bearer <你的API令牌>"
```

这将返回当前令牌使用量、到期时间和剩余余额。

---

### 6. **与 Hermes 代理集成**

如果你使用 Hermes 进行自动化：

1. 使用 **Hermes 的 HTTP 请求工具**（或 Python 中的 `requests`）调用小米 API。
2. 在 **请求头** 中包含你的令牌。
3. 处理 JSON 响应，用于计划选择、使用量和订阅更新。
4. 可选：将令牌安全地存储在 Hermes 中，以便重复调用。

Hermes 内部的 Python 代码示例：

```python
import requests

url = "https://token-plan-cn.xiaomimimo.com/v1/subscribe"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "planId": "pro_monthly",
    "autoRenew": True
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

---

### ⚠️ 注意事项

* 小米 Mimo API 可能有区域限制；请确保你的账户位于 **中国区域**。
* 令牌和订阅是 **按账户** 而非按设备管理的。
* 妥善保管你的 API 令牌——不要将其硬编码在共享脚本中。

---

参考文档：

* [小米 Mimo 令牌计划（官方中文 API）](https://token-plan-cn.xiaomimimo.com/v1)
* [Hermes 代理使用示例](https://github.com/your-automation-docs/hermes-agent)

---

如果你需要，我还可以提供一个 **可直接使用的 Hermes 代理脚本**，用于自动订阅和查看小米 Mimo 令牌计划。需要我准备吗？