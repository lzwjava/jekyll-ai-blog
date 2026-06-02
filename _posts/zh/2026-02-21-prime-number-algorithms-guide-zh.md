---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 高效素数算法指南
translated: true
type: note
---

很高兴听到你在思考高效的质数算法——这是竞赛编程（CP）中的经典且重要的话题！以下是最常见任务及高效方法的分解，并附有 Python 示例。

---

## **1. 判断一个数是否为质数**

### **快速方法：试除法（至 √n）**

- **思路：** 如果一个数 `n` 不能被 2 到 √n 之间的任何数整除，则 `n` 是质数。
- **优化：**
  - 检查 2 后跳过所有偶数。
  - 只检查到 √n。

```python
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True
```

---

## **2. 生成小于等于 `s` 的所有质数（埃拉托斯特尼筛法）**

### **快速方法：埃拉托斯特尼筛法**

- **思路：** 从 2 开始，标记每个质数的所有倍数为非质数。
- **优化：**
  - 从 `i*i` 开始标记（较小的倍数已被更小的质数标记）。
  - 使用布尔数组实现 O(1) 查找。

```python
def sieve(s: int) -> list[int]:
    if s < 2:
        return []
    sieve = [True] * (s + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(s**0.5) + 1):
        if sieve[i]:
            sieve[i*i : s+1 : i] = [False] * len(sieve[i*i : s+1 : i])
    return [i for i, is_prime in enumerate(sieve) if is_prime]
```

---

## **3. 竞赛编程中常见的质数相关任务**

### **常见问题：**

- **质因数分解**（如用于 GCD、LCM 或模运算）。
- **计算区间内的质数数量**（如用于数论问题）。
- **哥德巴赫猜想**（将偶数表示为两个质数之和）。
- **欧拉函数**（计算与 `n` 互质的数）。
- **模指数运算**（如用于加密或哈希）。

---

## **4. 进一步优化**

- **分段筛法：** 对于非常大的范围（如 1e12），使用分段筛法减少内存使用。
- **Miller-Rabin 质数检测：** 用于概率性质数检测（适用于非常大的数）。
- **预计算质数：** 在 CP 中，提前计算好质数（如 1e6 以内），并在程序中重复使用。

---

## **示例：质因数分解**

```python
def prime_factors(n: int) -> list[int]:
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 2:
        factors.append(n)
    return factors
```

---

## **总结表**

| 任务                     | 方法                     | 时间复杂度       |
|--------------------------|--------------------------|------------------|
| 判断 `n` 是否为质数      | 试除法（√n）             | O(√n)            |
| 生成小于等于 `s` 的质数  | 埃拉托斯特尼筛法       | O(n log log n)   |
| 质因数分解               | 试除法                   | O(√n)            |

---

### **你的想法？**

你提到使用已有质数的倍数排除非质数——这正是埃拉托斯特尼筛法的核心！在 CP 中，预计算质数并重复使用，可以进一步提速。

你是否希望深入了解其中某些方法，或特定的 CP 质数问题？
