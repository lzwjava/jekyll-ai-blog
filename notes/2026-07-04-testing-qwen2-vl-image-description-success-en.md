---
audio: false
generated: true
image: false
lang: en
layout: post
title: Testing Qwen2-VL Image Description Success
translated: false
type: note
---

It works. The model correctly describes the test image. Here's a summary:

---

**Qwen2-VL-7B-Instruct-Q4_K_M** is serving on **port 8088**

`curl` command you can run to try it yourself (works from any machine on the LAN):

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

Or use the OpenAI-compatible endpoint directly from your MacBook or any machine:

```
http://192.168.1.36:8088/v1/chat/completions
```

Test result — it read the text in the image correctly:
> "The image features a dark background with a rectangular frame outlined in a bright cyan color. Inside the frame, there is a text message that reads: 'Hello from Owen2-VL! Test Image for Vision'"

Model uses ~9.4GB VRAM (RTX 4070 12GB — fits comfortably).