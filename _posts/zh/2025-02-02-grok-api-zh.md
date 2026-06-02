---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 测试Grok API
translated: true
type: post
---

- 可以使用中国签发的Visa卡。

- [https://console.x.ai](https://console.x.ai)

- `grok-2-latest` 模型: 输入每百万个标记需要2美元，输出每百万个标记需要10美元。

代码：

```python
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.environ.get("GROK_API_KEY")
if not GROK_API_KEY:
    raise ValueError("GROK_API_KEY环境变量未设置")

url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GROK_API_KEY}"
}
data = {
    "model": "grok-2-latest",
    "messages": [
        {
            "role": "user",
            "content": "解释AI的工作原理"
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    json_response = response.json()
    if 'choices' in json_response and json_response['choices']:
        first_choice = json_response['choices'][0]
        if 'message' in first_choice and 'content' in first_choice['message']:
            print(first_choice['message']['content'])
        else:
            print("意外的响应格式：消息或内容缺失")
    else:
        print("响应中未找到选择")
except requests.exceptions.RequestException as e:
    print(f"API请求期间出错: {e}")
    if e.response:
        print(f"响应状态代码: {e.response.status_code}")
        print(f"响应内容: {e.response.text}")
except json.JSONDecodeError as e:
    print(f"解码JSON响应期间出错: {e}")
```
