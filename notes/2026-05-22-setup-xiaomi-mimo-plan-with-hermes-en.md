---
audio: false
generated: true
image: false
lang: en
layout: post
title: Setup Xiaomi Mimo Plan with Hermes
translated: false
type: note
---

Question: How to set up a Xiaomi Mimo token plan using the Hermes agent with the API at `https://token-plan-cn.xiaomimimo.com/v1`?

Answer:

To set up or configure a Xiaomi Mimo token plan via their API, you typically need to follow these steps:

---

### 1. **Obtain API Access**

* Make sure you have a Xiaomi account with permissions to access Mimo services.
* Get an **API token** or **authorization key** for the Xiaomi Mimo token plan API.

---

### 2. **Understand the API Endpoint**

The base endpoint is:

```
https://token-plan-cn.xiaomimimo.com/v1
```

Key endpoints may include:

* **GET `/plans`** → List available token plans.
* **POST `/subscribe`** → Subscribe to a specific plan.
* **GET `/usage`** → Check current usage or balance.
* **POST `/update`** → Change plan or update subscription info.

You will need the exact API documentation or Swagger spec for all available endpoints, parameters, and headers.

---

### 3. **Prepare Authentication**

Most Xiaomi APIs use **Bearer token** authentication. Example in headers:

```http
Authorization: Bearer <your_api_token>
Content-Type: application/json
```

---

### 4. **Subscribe to a Plan**

Example `POST` request to subscribe:

```bash
curl -X POST "https://token-plan-cn.xiaomimimo.com/v1/subscribe" \
-H "Authorization: Bearer <your_api_token>" \
-H "Content-Type: application/json" \
-d '{
  "planId": "pro_monthly",
  "autoRenew": true
}'
```

Parameters:

* `planId` → the ID of the plan you want (e.g., monthly, yearly, Pro).
* `autoRenew` → whether the subscription automatically renews.

---

### 5. **Check Usage**

After subscribing, check your usage:

```bash
curl -X GET "https://token-plan-cn.xiaomimimo.com/v1/usage" \
-H "Authorization: Bearer <your_api_token>"
```

This returns current token usage, expiry, and remaining balance.

---

### 6. **Integrating with Hermes Agent**

If you are using Hermes for automation:

1. Use **Hermes’s HTTP request tool** (or `requests` in Python) to call the Xiaomi API.
2. Include **headers** with your token.
3. Handle JSON responses for plan selection, usage, and subscription updates.
4. Optionally, store the token securely in Hermes for repeated calls.

Example Python snippet inside Hermes:

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

### ⚠️ Notes

* Xiaomi Mimo API may have region restrictions; make sure your account is in **China region**.
* Tokens and subscriptions are **per-account**, not per-device.
* Keep your API token secure—do not hardcode in shared scripts.

---

References:

* [Xiaomi Mimo Token Plan (official Chinese API)](https://token-plan-cn.xiaomimimo.com/v1)
* [Example usage with Hermes agent](https://github.com/your-automation-docs/hermes-agent)

---

I can also provide a **ready-to-use Hermes agent script** to automatically subscribe and check Xiaomi Mimo token plans if you want. Do you want me to prepare that?