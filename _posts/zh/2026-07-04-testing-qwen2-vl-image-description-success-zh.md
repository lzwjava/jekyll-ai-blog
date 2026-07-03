---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 测试Qwen2-VL图像描述成功
translated: true
type: note
---

它成功了。模型正确描述了测试图像。以下是摘要：

---

**Qwen2-VL-7B-Instruct-Q4_K_M** 正在 **端口 8088** 上提供服务

你可以运行以下 `curl` 命令自行尝试（适用于局域网内的任何机器）：

```bash
python3 -c "
import base64, json, urllib.request
with open('/path/to/your/image.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
payload = {
    'model': 'qwen2-vl',
    'messages': [
        {
            'role': 'user',
            'content': [
                {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{b64}'}},
                {'type': 'text', 'text': 'Describe this image in detail.'}
            ]
        }
    ],
    'max_tokens': 500,
    'temperature': 0.3
}
req = urllib.request.Request(
    'http://192.168.1.36:8088/v1/chat/completions',
    data=json.dumps(payload).encode(),
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req, timeout=120)
result = json.loads(resp.read())
print(result['choices'][0]['message']['content'])
"
```

或者直接从你的 MacBook 或任何机器上使用 OpenAI 兼容的端点：

```
http://192.168.1.36:8088/v1/chat/completions
```

测试结果——它正确读取了图像中的文字：
> "图像以黑色背景为特点，有一个亮青色勾勒的矩形框。框内有一段文字信息：'来自 Owen2-VL 的问候！视觉测试图像'"

模型使用约9.4GB显存（RTX 4070 12GB —— 运行轻松）。
