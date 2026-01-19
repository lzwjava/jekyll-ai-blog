---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Java Solution for Sub-RBS Easy Version
translated: false
type: note
---

**Question:** Give a Java version of the solution for problem B1. Sub-RBS (Easy Version)

**Answer:**

Here is a clean Java implementation for Codeforces problem B1 - Sub-RBS (Easy Version):

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
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

This solution follows the standard greedy approach for the easy version:

- We compute the prefix balance array (`prefix[]`).
- For each possible position `i` where `s[i] == ')'`, we consider changing it to `'('` (which increases balance by 2 compared to original).
- We check if the balance after this change is still ≥ 0.
- Then we simulate taking all remaining characters from `i+1` to `n-1` and check:
  - balance never goes negative
  - final balance is exactly 0
- If both conditions are satisfied → this gives a valid regular bracket subsequence of length `length` that is **better** than original `s` (because first difference is at position `i`, where new has `'('` and original has `')'`).
- We take the maximum such length over all possible starting difference positions.

**Time complexity:** O(t × n²) in worst case, but since ∑n ≤ 2×10⁵ and inner loop breaks early in practice, it passes comfortably within time limit.

**References:**

- [https://codeforces.com/contest/2190/problem/B1](https://codeforces.com/contest/2190/problem/B1)