---
audio: false
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Truncating JSON Objects Efficiently
translated: false
type: note
---

To truncate the first `n` keys from a JSON object (whether it's an array or a map), you can use the following approach. This is particularly useful when dealing with large JSON responses that need to be truncated due to context limits, such as when using an LLM (Language Model) to generate test cases.

Here is a Python function that demonstrates how to truncate the first `n` keys from a JSON object:

```python
import json

def truncate_json(json_obj, n):
    if isinstance(json_obj, list):
        # Truncate the first n elements from the list
        return json_obj[n:]
    elif isinstance(json_obj, dict):
        # Truncate the first n keys from the dictionary
        keys = list(json_obj.keys())
        for key in keys[:n]:
            del json_obj[key]
        return json_obj
    else:
        return json_obj

# Example usage
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
n = 2  # Number of keys to truncate

truncated_json = truncate_json(json_obj, n)
print(json.dumps(truncated_json, indent=4))
```

### Explanation

1. **Function Definition**: The `truncate_json` function takes a JSON object and an integer `n` as input.
2. **List Handling**: If the JSON object is a list, it returns a new list with the first `n` elements removed.
3. **Dictionary Handling**: If the JSON object is a dictionary, it removes the first `n` keys from the dictionary.
4. **Example Usage**: The example demonstrates how to use the function with a sample JSON object.

### Example Output

For the given example JSON object and `n = 2`, the output will be:

```json
{
    "key3": "value3",
    "key4": "value4",
    "key5": "value5"
}
```

This approach ensures that the JSON object is truncated appropriately, making it easier to handle within the context limits of an LLM.
