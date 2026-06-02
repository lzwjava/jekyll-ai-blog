---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 优化Clash代理选择性能
translated: true
type: note
---

### 优化总结：Clash 代理选择脚本

我对 Clash 代理选择脚本进行了优化，避免测试不会被选中的代理，通过减少不必要的速度测试显著提升了性能。

#### 优化内容

原始代码采用以下低效工作流程：
1. 测试所有可用代理的速度
2. 然后筛选仅保留 SG/TW（或 HK）代理
3. 这导致大量时间浪费在测试最终会被丢弃的代理上

#### 解决方案

修改了 `speed.py` 中的 `get_top_proxies()` 函数，使其接受 `name_filter` 参数并在速度测试前进行过滤：

```python
def get_top_proxies(num_results=5, name_filter=None):
    """
    并发测试 Clash 代理速度并返回前 N 个最快的独立代理。

    参数：
        num_results (int): 返回的顶级代理数量（默认：5）
        name_filter (list): 用于过滤代理名称的字符串列表。仅测试名称中包含
                           任意这些字符串的代理。
    """
```

#### 性能优势

- **减少网络请求**：仅测试实际打算使用的代理
- **更快执行速度**：消除在无关代理上花费的不必要时间
- **更清晰的日志**：明确显示被过滤的代理数量，提高透明度

#### 简化配置

移除了 `--hk` 标志。脚本现在默认始终仅测试 SG 和 TW 代理，以实现最大专注度和简洁性。

#### 成果

优化大幅减少了执行时间，因为大多数代理名称中不包含 "SG" 或 "TW"。这使得速度测试阶段效率显著提高，在不影响功能的前提下更快地提供结果。
