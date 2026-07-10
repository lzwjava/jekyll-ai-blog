---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 长提示代码生成分析
translated: true
type: note
---

结果保存在 `/mnt/data/zz/codeparrot/eval_long/results/long_prompt_results.log` 中。以下是详细分析：

**样本 1 — BinarySearchTree**  
生成了 `insert`、`search`、`delete`、`__str__`、`__repr__`、`__len__`、`__iter__`、`__getitem__`——覆盖了令人印象深刻的魔术方法。`insert()` 方法有误（同时插入左右子节点），但模型知道创建 `TreeNode(val)` 并检查 `self.root is None`。整体结构正确，逻辑有误。

**样本 2 — longest_common_subsequence**  
识别出动态规划方法，创建了二维表。但递推公式 `dp[i][j] = max(dp[i][j], dp[i][j + 1])` 错误——没有字符比较。随后退化为重复同一函数但使用更长的名称。

**样本 3 — timer_decorator — ✓ 正确**  

```
def wrapper(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    print("Execution time: %.2f seconds" % (end - start))
    return result
return wrapper
```

随后以轻微名称变化重复自身 5 次以上。

**样本 4 — load_json_data — ✓ 基本正确**  
正确处理了 `try/except` 中的 `FileNotFoundError` 和 `json.decoder.JSONDecodeError`。后转变为 `load_csv_data`、`load_csv_data_from_json` 等。

**样本 5 — is_prime — ✓ 正确**，`prime_factors` — ✗ 错误

**样本 6 — APIClient — ✓ 最佳样本**  
生成了 `get`、`post`、`put`、`delete` 方法，且均采用一致的错误处理模式。方法体几乎相同（复制粘贴模式）。识别到 `requests.Session()`、请求头、`response.json()`。

**样本 7 — clean_and_transform**  
开始良好：`drop_duplicates()`、数值列选择。随后退化为对数值列应用 `apply(lambda x: x.lower().strip())` ——不合理。

**样本 8 — fetch_url — ✓ 正确**  
`async with session.get(url)`、`await response.json()`。随后退化为 `fetch_json_async_async_async_async...`。

**全部 8 个样本的总结模式：**

- 延续的前 **50-100 个 token** 通常合理或正确
- 随后出现 **退化**——以轻微变化重复第一个成功的模式
- 模型学习了良好的 **代码结构**（缩进、导入、类/方法模式、try/except、装饰器、异步）
- 但随着长度增加，**语义正确性**迅速下降——286M 参数存在容量瓶颈
- 贪婪采样（temperature=0.3）加剧了退化——确定性模式放大了重复循环
