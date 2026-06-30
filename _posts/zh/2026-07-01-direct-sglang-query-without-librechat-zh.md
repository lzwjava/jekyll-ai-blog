---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 直接SGLang查询（无LibreChat）
translated: true
type: note
---

问题：我已经在我的GPU机器上运行了SGLang。我是否需要LibreChat来提供/与之对话，还是可以直接查询它？

回答：

不需要，你不需要LibreChat。SGLang本身*就是*服务器。`python -m sglang.launch_server` 在 `:30000` 端口暴露了一个兼容OpenAI的HTTP端点——这就是完整的服务层。LibreChat只是一个可选的聊天UI前端；它是客户端，不是必需品。

所以从你的MacBook Air上，通过隧道直接访问它：

```bash
ssh -L 30000:localhost:30000 gpu
```

**原始curl请求**（兼容OpenAI的 `/v1` 接口）：

```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "default",
    "messages": [{"role":"user","content":"用一句话解释KV cache"}],
    "temperature": 0.7
  }'
```

**Python——只需将OpenAI SDK指向SGLang：**

```python
from openai import OpenAI
c = OpenAI(base_url="http://localhost:30000/v1", api_key="none")  # 密钥被忽略
r = c.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "用一句话解释KV cache"}],
)
print(r.choices[0].message.content)
```

**SGLang原生端点**（相比 `/v1` 对采样有更多控制）：

```bash
curl http://localhost:30000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "法国的首都是", "sampling_params": {"temperature": 0, "max_new_tokens": 16}}'
```

**检查已加载的内容：**

```bash
curl http://localhost:30000/get_model_info
curl http://localhost:30000/v1/models
```

---

什么时候你*确实*需要添加像LibreChat / Open WebUI这样的UI：仅当你想要一个带有历史记录、多用户、系统提示预设、对话分支等功能的浏览器聊天界面时——即类似ChatGPT的前端。它通过相同的 `base_url: http://gpu:30000/v1` 连接到SGLang。对于你的工作流（命令行、REPL、智能体、脚本），这纯粹是额外开销——curl和OpenAI SDK是更精简的路径。

如果你想在局域网中暴露它而不使用隧道：用 `--host 0.0.0.0` 启动SGLang，这样其他机器可以直接访问 `http://192.168.x.x:30000/v1`。默认只绑定到localhost，这就是为什么你需要SSH转发。

如果你仍然想要一个轻量级的本地聊天UI，Open WebUI只需一次 `docker run` 并指向相同的端点——需要的话告诉我，我给你精确的命令。
