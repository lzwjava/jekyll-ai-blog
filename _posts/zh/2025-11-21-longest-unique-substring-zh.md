---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 最长无重复字符子串长度
translated: true
type: note
---

**问题**：找出最长无重复字符子串的长度。

**解决方案**：滑动窗口 + 哈希表（由于是小写字母，也可使用数组）

我们使用两个指针（`left` 和 `right`）来维护窗口 `[left, right]`。
当移动 `right` 时，检查 `s[right]` 是否已在当前窗口中出现：

- 若存在，则将 `left` 前移至重复字符被移除的位置。
- 通过记录每个字符最后出现的位置，可直接跳跃移动 `left`。

该方法时间复杂度为 **O(n)**，空间复杂度为 **O(1)**（最多26或128个字符）。

```python
def lengthOfLongestSubstring(s: str) -> int:
    if not s:
        return 0

    # 字符 -> 最后出现的位置
    last_seen = {}
    max_len = 0
    left = 0

    for right in range(len(s)):
        ch = s[right]

        # 若字符已在当前窗口中出现，从左侧收缩窗口
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        else:
            # 窗口有效时更新最大长度
            max_len = max(max_len, right - left + 1)

        # 记录该字符的最新位置
        last_seen[ch] = right

    return max_len
```

### 测试用例

```python
print(lengthOfLongestSubstring("abacabcbb"))  # 3 ("abc" 或 "bac")
print(lengthOfLongestSubstring("bbbbb"))      # 1 ("b")
print(lengthOfLongestSubstring("pwwkew"))     # 3 ("wke")
```

**示例解析**：

- "abacabcbb" → "abc" 或 "bac" 长度 = 3
- "bbbbb" → 仅 "b" 长度 = 1
- "pwwkew" → "wke" 长度 = 3（注意："pwke" 虽有效，但 "ww" 会提前终止窗口）

若已知字符集为ASCII，也可使用长度为128的数组替代字典以获得更快的常数时间性能。
