---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: KMP算法高效字符串搜索
translated: true
type: note
---

### 理解 Knuth-Morris-Pratt (KMP) 算法

你的直觉很准确：KMP 的核心在于**不浪费字符串搜索过程中的部分匹配结果**。当你在长文本（如 "ababcabc"）中查找模式（如 "abc"）时，朴素方法每次遇到不匹配就从头开始重新比较，效率很低。KMP 巧妙地"记住"已经匹配了多少模式内容，然后跳过冗余比较直接前移。这使得算法非常快——达到线性时间复杂度 O(n + m)，其中 n 是文本长度，m 是模式长度。

我将通过一个简单示例逐步解析。我们在文本 `T = "ababababc"` 中搜索模式 `P = "abab"`（该模式出现在位置 0 和 2）。

#### 第一步：问题描述与朴素解法

- **目标**：找出 `P` 在 `T` 中完全匹配的所有起始位置。
- **朴素方法**：将 `P` 沿 `T` 滑动，逐字符比较。如果在 `P` 的位置 i 出现不匹配，则将 `P` 右移 1 位并从 `P` 开头重新开始。
  - 以我们的示例为例：
    - 从 T[0] 开始："a"=="a"（匹配），"b"=="b"（匹配），"a"=="a"（匹配），"b"=="b"（匹配）→ 在位置 0 找到匹配。
    - 移至 T[1]："b"=="a"？不匹配 → 从 `P` 开头重启。浪费！
    - T[2]："a"=="a"，"b"=="b"，"a"=="a"，"b"=="b" → 在位置 2 找到匹配。
    - T[3]："a"=="a"，"b"=="b"，"a"=="a"，"b"=="a"？不匹配 → 重启。
    - 依此类推。大量回溯到 `P` 的字符 0。

在最坏情况下（例如在 "aaaaa...a" 中搜索 "aaa...ab"），这种方法可能达到 O(n*m) 的时间复杂度。

#### 第二步：KMP 的核心思想——前缀表（或称"失效函数"）

KMP 预先为模式 `P` 计算一个表 `π`（pi）。该表告诉你，对于 `P` 中的每个位置 i，**`P[0..i]` 的最长真前缀（同时是后缀）的长度**。换句话说："如果在此处不匹配，我们可以通过跳转到这个重叠的前缀来复用多少部分匹配内容？"

- **真前缀/后缀**：指不是整个字符串的前缀/后缀（例如 "aba" 的前缀 "a" 与后缀 "a" 匹配）。
- 为什么这样做？它让你在不匹配时能够将模式滑动超过 1 位，复用重叠部分而不是重新开始。

对于 `P = "abab"`：

- 逐步构建 `π` 表（稍后我们将编写代码）。

| 位置 i | P[0..i] | 最长真前缀 = 后缀 | π[i] |
|--------|---------|-------------------|------|
| 0      | "a"     | 无（单字符）      | 0    |
| 1      | "ab"    | 无                | 0    |
| 2      | "aba"   | "a"（前缀 "a" == 后缀 "a"） | 1    |
| 3      | "abab"  | "ab"（前缀 "ab" == 后缀 "ab"） | 2  |

- π[2] = 1 表示：如果你已经匹配了 "aba" 但下一个字符不匹配，就假设你目前只匹配了前缀 "a"（长度为 1）。
- π[3] = 2 表示：对于完整的 "abab"，重叠部分是 "ab"。

#### 第三步：构建前缀表 (π)

这一步在 O(m) 时间内完成。它类似于用类似的逻辑让 `P` 与自身进行搜索。

伪代码：

```
def compute_prefix_function(P):
    m = len(P)
    pi = [0] * m
    k = 0  # 当前前缀-后缀匹配的长度
    for i in range(1, m):
        while k > 0 and P[k] != P[i]:
            k = pi[k-1]  # 跳转到前一个重叠（复用！）
        if P[k] == P[i]:
            k += 1
        pi[i] = k
    return pi
```

- 从 π[0] = 0 开始。
- 对于每个 i=1 到 m-1：
  - 尝试扩展当前匹配长度 k。
  - 如果不匹配，回退到 π[k-1]（不浪费——复用之前的重叠）。
  - 如果匹配，k++。

对于 "abab"：

- i=1：P[0]='a' != P[1]='b' → k=0，π[1]=0。
- i=2：P[0]='a' == P[2]='a' → k=1，π[2]=1。
- i=3：P[1]='b' == P[3]='b' → k=2，π[3]=2。

#### 第四步：使用前缀表进行搜索

现在使用 `P` 和 `π` 搜索 `T`：

- 维护一个变量 `q` = 当前状态（到目前为止匹配的前缀长度）。
- 对于 `T` 中的每个字符：
  - 当不匹配且 q>0 时，设置 q = π[q-1]（智能回跳）。
  - 如果匹配，q++。
  - 如果 q == m，找到匹配！然后 q = π[q-1] 以继续搜索重叠部分。

伪代码：

```
def kmp_search(T, P):
    n, m = len(T), len(P)
    if m == 0: return []
    pi = compute_prefix_function(P)
    q = 0
    matches = []
    for i in range(n):
        while q > 0 and P[q] != T[i]:
            q = pi[q-1]
        if P[q] == T[i]:
            q += 1
        if q == m:
            matches.append(i - m + 1)  # 起始位置
            q = pi[q-1]  # 为下一次搜索处理重叠
    return matches
```

对于 `T = "ababababc"`，`P = "abab"`：

- i=0：'a'=='a' → q=1
- i=1：'b'=='b' → q=2
- i=2：'a'=='a' → q=3
- i=3：'b'=='b' → q=4 == m → 在位置 0 找到匹配，q=π[3]=2
- i=4：现在 q=2，T[4]='a' == P[2]='a' → q=3
- i=5：'b'=='b' → q=4 == m → 在位置 2 找到匹配，q=2
- i=6：q=2，T[6]='a' == P[2]='a' → q=3
- i=7：q=3，T[7]='b' == P[3]='b' → q=4 == m → 在位置 4 找到匹配，q=2
- i=8：'c' 不匹配，循环结束。

看到了吗？在不匹配时（比如如果有不匹配发生），它会跳转到 q=π[q-1] 而不是 q=0。

#### 为什么它感觉如此神奇

- 在 `T` 中没有回溯——你只向前移动。
- 处理不匹配的 "while" 循环总摊还运行 O(1) 次，因为每次跳转都减少 q，而 q 最多增加 n 次。

#### 动手尝试：简单 Python 代码

```python
def compute_prefix_function(P):
    m = len(P)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and P[k] != P[i]:
            k = pi[k - 1]
        if P[k] == P[i]:
            k += 1
        pi[i] = k
    return pi

def kmp_search(T, P):
    n, m = len(T), len(P)
    if m == 0: return []
    pi = compute_prefix_function(P)
    q = 0
    matches = []
    for i in range(n):
        while q > 0 and P[q] != T[i]:
            q = pi[q - 1]
        if P[q] == T[i]:
            q += 1
        if q == m:
            matches.append(i - m + 1)
            q = pi[q - 1]
    return matches

# 测试
T = "ababababc"
P = "abab"
print(kmp_search(T, P))  # 输出: [0, 2, 4]
```

运行这段代码——调整 P/T 来观察跳转过程（可以添加打印语句输出 q 的值）。

#### 常见陷阱与技巧

- π[0] 总是 0。
- 对于没有自重叠的模式（例如 "abc"），π 全为 0——退化为朴素方法。
- 非常适用于 DNA 序列或代码自动补全场景。
- 如果还是觉得模糊，可以将 π 可视化为一个"状态机"：每个状态代表匹配长度，根据匹配/不匹配进行状态转移。

现在你应该明白了——它就是通过预计算的重叠来实现智能跳转。如果你有具体示例遇到困难，欢迎分享！

[GeeksforGeeks: KMP 算法](https://www.geeksforgeeks.org/dsa/kmp-algorithm-for-pattern-searching/)
[维基百科: Knuth–Morris–Pratt 算法](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
