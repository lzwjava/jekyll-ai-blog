---
audio: false
generated: true
image: false
lang: en
layout: post
title: Efficient Prime Number Algorithms Guide
translated: false
type: note
---

Great to hear you’re thinking about efficient prime number algorithms—this is a classic and essential topic in competitive programming (CP)! Here’s a breakdown of the most common tasks and efficient methods, with Python examples.

---

## **1. Checking if a Number is Prime**
### **Fast Method: Trial Division up to √n**
- **Idea:** A number `n` is prime if it’s not divisible by any number from 2 to √n.
- **Optimizations:**
  - Skip even numbers after checking 2.
  - Only check up to √n.

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

## **2. Generating All Primes up to `s` (Sieve of Eratosthenes)**
### **Fast Method: Sieve of Eratosthenes**
- **Idea:** Mark non-primes by iterating through multiples of each prime starting from 2.
- **Optimizations:**
  - Start marking from `i*i` (smaller multiples are already marked by smaller primes).
  - Use a boolean array for O(1) lookups.

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

## **3. Typical CP Tasks Involving Primes**
### **Common Problems:**
- **Prime factorization** (e.g., for GCD, LCM, or modular arithmetic).
- **Counting primes in a range** (e.g., for number theory problems).
- **Goldbach’s conjecture** (express even numbers as sums of two primes).
- **Euler’s totient function** (count numbers coprime to `n`).
- **Modular exponentiation** (e.g., for cryptography or hashing).

---

## **4. Further Optimizations**
- **Segmented Sieve:** For very large ranges (e.g., 1e12), use a segmented sieve to reduce memory usage.
- **Miller-Rabin Primality Test:** For probabilistic primality testing (useful for very large numbers).
- **Precompute Primes:** In CP, precompute primes up to a limit (e.g., 1e6) at the start of your program for repeated use.

---

## **Example: Prime Factorization**
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

## **Summary Table**

| Task                     | Method                     | Time Complexity       |
|--------------------------|----------------------------|-----------------------|
| Check if `n` is prime    | Trial division (√n)        | O(√n)                 |
| Generate primes up to `s`| Sieve of Eratosthenes      | O(n log log n)        |
| Prime factorization      | Trial division             | O(√n)                 |

---

### **Your Thoughts?**
You mentioned using multiples of existing primes to exclude non-primes—this is exactly what the Sieve of Eratosthenes does! For even faster results in CP, precompute primes and reuse them.

Would you like a deeper dive into any of these methods or a specific CP problem involving primes?
