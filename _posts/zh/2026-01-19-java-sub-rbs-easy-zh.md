---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Java 解题方案：子级 RBS 简单版
translated: true
type: note
---

**Question:** 请提供 Codeforces 题目 B1. Sub-RBS (Easy Version) 的 Java 版本解决方案。

**Answer:**

这里是 Codeforces 题目 B1 - Sub-RBS (Easy Version) 的一个简洁的 Java 实现：

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.util.in);
        int t = sc.nextInt();
        
        for (int test = 0; test < t; test++) {
            int n = sc.nextInt();
            String s = sc.next();
            
            // prefix[i] = balance after first i characters (0-based)
            int[] prefix = new int[n + 1];
            for (int i = 0; i < n; i++) {
                prefix[i + 1] = prefix[i] + (s.charAt(i) == '(' ? 1 : -1);
            }
            
            int ans = -1;
            
            // Try each possible first differing position i (0-based)
            // where s[i] == ')' and we pretend it is '(' instead
            for (int i = 0; i < n; i++) {
                if (s.charAt(i) != ')') continue;
                
                // balance just before i
                int balBefore = prefix[i];
                
                // if we put '(' instead of ')' at position i
                int balAfterChange = balBefore + 1;
                
                // prefix must stay non-negative
                if (balAfterChange < 0) continue;
                
                // now try to take as many characters as possible from i+1 onwards
                int current = balAfterChange;
                int length = i + 1;  // 0..i inclusive
                
                boolean canContinue = true;
                for (int j = i + 1; j < n; j++) {
                    current += (s.charAt(j) == '(' ? 1 : -1);
                    if (current < 0) {
                        canContinue = false;
                        break;
                    }
                    length++;
                }
                
                // must end at balance 0
                if (canContinue && current == 0) {
                    ans = Math.max(ans, length);
                }
            }
            
            System.out.println(ans);
        }
        
        sc.close();
    }
}
```

### Explanation

该解决方案采用了针对 Easy Version 的标准 Greedy 方法：

- 我们计算前缀 balance 数组 (`prefix[]`)。
- 对于每个可能的、`s[i] == ')'` 的位置 `i`，我们考虑将其改为 `'('`（这与原字符串相比，该位置的 balance 增加了 2）。
- 我们检查在该变化后，balance 是否仍然保持 ≥ 0。
- 然后我们模拟选取从 `i+1` 到 `n-1` 的所有剩余字符，并检查：
  - balance 始终不为负数
  - 最终 balance 恰好为 0
- 如果两个条件都满足，则会得到一个长度为 `length` 的有效 Regular Bracket Subsequence，且该序列优于原始的 `s`（因为第一个差异点在位置 `i`，新序列为 `'('` 而原始序列为 `')'`）。
- 我们在所有可能的起始差异位置中取最大长度。

**Time complexity:** 最坏情况下为 O(t × n²)，但由于 ∑n ≤ 2×10⁵ 且内层循环在实践中会提前 break，因此可以顺利在时间限制内通过。

**References:**

- [https://codeforces.com/contest/2190/problem/B1](https://codeforces.com/contest/2190/problem/B1)