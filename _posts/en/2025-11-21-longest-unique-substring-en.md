---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Longest Unique Character Substring Length
translated: false
type: note
---

**Problem**: Find the length of the longest substring without repeating characters.

**Solution**: Sliding Window + HashMap (or array since lowercase letters)

We use two pointers (`left` and `right`) to maintain a window `[left, right]`.
As we move `right`, we check if `s[right]` already appeared in the current window:
- If yes, move `left` forward until the duplicate is removed.
- Track the position where each character was last seen to jump `left` directly.

This runs in **O(n)** time and **O(1)** space (at most 26 or 128 characters).

```python
def lengthOfLongestSubstring(s: str) -> int:
    if not s:
        return 0

    # char -> last seen index
    last_seen = {}
    max_len = 0
    left = 0

    for right in range(len(s)):
        ch = s[right]

        # If character is already in current window, shrink from left
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        else:
            # Update max length when window is valid
            max_len = max(max_len, right - left + 1)

        # Record the latest position of this character
        last_seen[ch] = right

    return max_len
```

### Test cases

```python
print(lengthOfLongestSubstring("abacabcbb"))  # 3 ("abc" or "bac")
print(lengthOfLongestSubstring("bbbbb"))      # 1 ("b")
print(lengthOfLongestSubstring("pwwkew"))     # 3 ("wke")
```

**Explanation of examples**:
- "abacabcbb" → "abc" or "bac" length = 3
- "bbbbb" → only "b" length = 1
- "pwwkew" → "wke" length = 3 (note: "pwke" is also valid, but "ww" breaks it earlier)

You can also use a list of size 128 instead of a dict for slightly faster constant time if you know the character set is ASCII.
