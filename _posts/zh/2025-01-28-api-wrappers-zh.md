---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 原生 HTTP 请求与包装器
translated: true
type: post
---

```python
import requests
import json
import time

def translate_text(text, target_language, special=False):
    if not text or not text.strip():
        return ""
    if target_language == 'en':
        print(f"  Skipping translation for English: {text[:50]}...")
        return text
    print(f"  Translating text: {text[:50]}...")

    retries = 3
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": create_translation_prompt(target_language, special)},
                    {"role": "user", "content": text}
                ],
                stream=False
            )
            if not response or not response.choices or not response.choices[0].message.content:
                print(f"  Error: Translation response is empty or invalid: {response}")
            if response and response.choices:
                translated_text = response.choices[0].message.content
                return translated_text
            else:
                print(f"  Translation failed on attempt {attempt + 1}.")
                if attempt == retries - 1:
                    return None
        except Exception as e:
            print(f"  Translation failed with error on attempt {attempt + 1}: {e}")
            if attempt == retries - 1:
                return None
            time.sleep(1)  # Wait before retrying
    return None
```

错误：

```bash
Translation failed with error on attempt 1: Expecting value: line 5 column 1 (char 4)
```

这个错误表明DeepSeek API返回的响应不是有效的JSON，可能是HTML或其他格式。这是意外的，因为API预期返回JSON。问题可能是API临时问题、速率限制或提示问题。重要的是优雅地处理错误，记录错误并可能重试。
