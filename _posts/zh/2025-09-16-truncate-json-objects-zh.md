---
audio: false
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 高效截断JSON对象
translated: true
type: note
---

要从JSON对象（无论是数组还是映射）中截断前`n`个键，可以采用以下方法。这在处理需要因上下文限制（例如使用LLM生成测试用例时）而被截断的大型JSON响应时特别有用。

以下是一个Python函数，演示如何截断JSON对象的前`n`个键：

```python
import json

def truncate_json(json_obj, n):
    if isinstance(json_obj, list):
        # 截断列表中的前n个元素
        return json_obj[n:]
    elif isinstance(json_obj, dict):
        # 截断字典中的前n个键
        keys = list(json_obj.keys())
        for key in keys[:n]:
            del json_obj[key]
        return json_obj
    else:
        return json_obj

# 使用示例
json_str = '''
{
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
    "key4": "value4",
    "key5": "value5"
}
'''

json_obj = json.loads(json_str)
n = 2  # 需要截断的键数量

truncated_json = truncate_json(json_obj, n)
print(json.dumps(truncated_json, indent=4))
```

### 功能说明

1. **函数定义**：`truncate_json`函数接收一个JSON对象和整数`n`作为输入
2. **列表处理**：若JSON对象为列表，则返回移除前`n`个元素后的新列表
3. **字典处理**：若JSON对象为字典，则从字典中移除前`n`个键
4. **使用示例**：示例展示了如何使用该函数处理示例JSON对象

### 示例输出

对于给定的示例JSON对象和`n = 2`，输出结果将为：

```json
{
    "key3": "value3",
    "key4": "value4",
    "key5": "value5"
}
```

这种方法能确保JSON对象被适当截断，使其更容易在LLM的上下文限制范围内进行处理。
