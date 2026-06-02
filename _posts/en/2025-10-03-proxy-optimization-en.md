---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Optimizing Clash Proxy Selection Performance
translated: false
type: note
---

### Summary of Optimization: Clash Proxy Selection Scripts

I optimized the Clash proxy selection scripts to avoid testing proxies that won't be selected, significantly boosting performance by minimizing unnecessary speed tests.

#### What Was Optimized

The original code followed this inefficient workflow:
1. Test all available proxies for speed.
2. Then filter to select only SG/TW (or HK) proxies.
3. This resulted in wasted time testing proxies that would be discarded.

#### The Fix

Modified the `get_top_proxies()` function in `speed.py` to accept a `name_filter` parameter and apply filtering before speed testing:

```python
def get_top_proxies(num_results=5, name_filter=None):
    """
    Tests Clash proxy speeds concurrently and returns the top N fastest individual proxies.

    Args:
        num_results (int): Number of top proxies to return (default: 5)
        name_filter (list): List of strings to filter proxy names. Only proxies containing
                           any of these strings in their name will be tested.
    """
```

#### Performance Benefits

- **Reduced network requests**: Only tests proxies you actually intend to use.
- **Faster execution**: Eliminates unnecessary time spent on irrelevant proxies.
- **Clearer logging**: Displays exactly how many proxies were filtered, improving transparency.

#### Simplified Configuration

Removed the `--hk` flag. The script now always tests only SG and TW proxies by default for maximum focus and simplicity.

#### Results

The optimization drastically reduced execution time, as most proxies do not contain "SG" or "TW" in their names. This makes the speed-testing phase far more efficient, delivering results faster without compromising functionality.
