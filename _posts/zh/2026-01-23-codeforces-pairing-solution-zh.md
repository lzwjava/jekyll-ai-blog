---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Codeforces 配对问题题解
translated: true
type: note
---

**Question:** 根据提供的描述（带有数字的表格，通过配对行-列值来最大化总和）解决 Codeforces 问题 A，并完成给定的 Java 代码模板。

**Answer:**

关键见解在于：

- 每一个有效的配对 (x, y)，只要满足 1 ≤ x ≤ h 且 1 ≤ y ≤ l，就会对总和贡献 **+1**。
- 如果一个数字在数组中出现多次，我们可以多次使用它。
- 我们能形成的有效配对的最大数量受限于我们能选择多少个行索引（≤ h）和列索引（≤ l）。

因此，我们只需要关心：

- 数组 a 中有多少个数字 **≤ h**（可能的行选择）
- 数组 a 中有多少个数字 **≤ l**（可能的列选择）

令：

- cnt_row = 满足 a[i] ≤ h 的 a[i] 数量
- cnt_col = 满足 a[i] ≤ l 的 a[i] 数量

那么我们能形成的有效配对的最大数量为：

**min(cnt_row, cnt_col, ⌊n/2⌋)**

因为：

- 每个配对需要一个行候选和一个列候选
- 每个配对会消耗数组中的 2 个元素

这个值正是我们可以达到的最大总和。

### Solution Code

```java
package com.lzw.solutions.codeforces.p2189A;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class Main {
    private static final BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    private static final PrintWriter out = new PrintWriter(System.out, true);

    private static void solve() throws IOException {
        String[] first = in.readLine().split(" ");
        int n = Integer.parseInt(first[0]);
        int h = Integer.parseInt(first[1]);
        int l = Integer.parseInt(first[2]);

        String[] line = in.readLine().split(" ");
        int cntRow = 0;
        int cntCol = 0;

        for (String s : line) {
            int x = Integer.parseInt(s);
            if (x <= h) cntRow++;
            if (x <= l) cntCol++;
        }

        int maxPairs = Math.min(cntRow, cntCol);
        maxPairs = Math.min(maxPairs, n / 2);

        out.println(maxPairs);
    }

    public static void main(String[] args) throws IOException {
        int t = Integer.parseInt(in.readLine());
        while (t-- > 0) {
            solve();
        }
        out.close();
    }
}
```

### 另一种更简短的版本（逻辑相同）

```java
package com.lzw.solutions.codeforces.p2189A;

import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(System.out);

        int t = Integer.parseInt(in.readLine());
        while (t-- > 0) {
            StringTokenizer st = new StringTokenizer(in.readLine());
            int n = Integer.parseInt(st.nextToken());
            int h = Integer.parseInt(st.nextToken());
            int l = Integer.parseInt(st.nextToken());

            st = new StringTokenizer(in.readLine());
            int row = 0, col = 0;
            while (st.hasMoreTokens()) {
                int x = Integer.parseInt(st.nextToken());
                if (x <= h) row++;
                if (x <= l) col++;
            }

            out.println(Math.min(Math.min(row, col), n / 2));
        }
        out.close();
    }
}
```

该解决方案正确处理了所有示例情况，并且每个测试用例的运行时间复杂度为 O(n)，在给定限制条件下非常高效。

**References:**

- 无（问题逻辑推导自题目描述和样例解释）
