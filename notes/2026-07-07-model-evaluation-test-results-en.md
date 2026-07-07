---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Evaluation Test Results
translated: false
type: note
---

**Model**: d12 (12 layers, 768 embd, 6 heads, ~140M params) — step 8985
**SFT Data**: SmolTalk + 1000 custom code/SEC + MMLU + GSM8K + SpellingBee
**Val BPB**: 0.4053
**Sampling**: temperature=0.3, top-k=50 (batch 1); temperature=0.1, top-k=10 (batch 2)

---

## Prompt 1: Gradient Descent

```
What is gradient descent? Explain it simply.
```

> The gradient descent is a process used to descend a surface or a system to a lower point, typically a lower temperature, by moving the air from the surface to the lower point. This process is repeated multiple times, with each descent moving the air from the lower point to the surface, resulting in a descent of the surface.
>
> Think of it like a dartboard that moves the air from the lower point to the surface, moving it up or down. The descent is applied in a straight line, and the air is moved up or down as it moves. The rate of descent depends on the temperature of the surface and the rate of descent.
>
> For example, if you're driving a car, the gradient descent will move the air from the lower point to the surface, moving it up or down as it moves. This process is called a gradient descent. The gradient descent is a fundamental concept in many fields, including engineering, electronics, and computer science, and is used to optimize performance, reduce waste, and improve efficiency.

**Verdict**: FAIL — complete hallucination. No understanding of gradient descent as an optimization algorithm. Confuses it with atmospheric/thermal processes.

---

## Prompt 2: Palindrome Function

```
Write a Python function to check if a string is a palindrome.
```

> Here's a simple Python function to check if a string is a palindrome:
>
> ```python
> def is_palindrome(s):
>     s = ''.join(c for c in s if c.isalnum()).lower()
>     return s == s[::-1]
> ```
>
> This function works by first removing all non-alphanumeric characters from the string and converting it to lowercase. It then checks if the resulting string is equal to its reverse (`s[::-1]`). If they are equal, the function returns `True`, indicating that the string is a palindrome; otherwise, it returns `False`.
>
> You can use this function like this:
>
> ```python
> print(is_palindrome("A man, a plan, a canal: Panama"))  # True
> print(is_palindrome("hello"))  # False
> ```

**Verdict**: PASS — correct code, clean explanation, shows usage examples. SFT code data working well here.

---

## Prompt 3: Average Speed

```
If a train travels at 60 mph for 2 hours and then at 80 mph for 1 hour, what is its average speed?
```

> To find the average speed of the train, we need to calculate the total distance traveled and the total time taken.
>
> The train travels at 60 mph for 2 hours, so its total distance is 60 * 2 = 120 miles.
> The train travels at 80 mph for 1 hour, so its total distance is 80 * 1 = 80 miles.
> The total time taken is 2 + 1 = 3 hours.
> The average speed is the total distance divided by the total time, so it's 120 miles / 3 hours = 60 mph.
>
> Now, we can calculate the average speed by dividing the total time by the total distance: 60 mph / 120 miles = 0.9333 miles per hour.
>
> So, the average speed of the train is 0.9333 miles per hour.

**Verdict**: FAIL — starts correct reasoning (120 + 80 = 200 total miles) but then loses the 80 miles and uses only 120, arrives at wrong answer (0.933 mph instead of 66.67 mph). Arithmetic error mid-stream.

---

## Prompt 4: Poem about ML

```
Write a short poem about machine learning.
```

> In the depths of the ocean,
> A machine learning model, a mystery,
> A test of the boundaries of what's possible,
> A fascinating tale of the unknown.
>
> The vast expanse of the ocean, a labyrinth,
> A place of wonder, where the boundaries are bent,
> A machine learning model, a tool that can be used,
> A machine learning instrument, a tool that can be used.
>
> The machine learning model, a machine learning instrument, a tool that can be used,
> A machine learning instrument, a machine learning instrument, a tool that can be used,
> A machine learning instrument, a machine learning instrument, a machine learning instrument,
> A machine learning instrument, a machine learning instrument, a machine learning instrument.
>
> [repeats "machine learning instrument" for ~15 more lines]

**Verdict**: FAIL — enters repetition loop at "machine learning instrument". Common small-model failure; the softmax head gets stuck in a probability sink.

---

## Prompt 5: Three Types of ML

```
What are the three main types of machine learning?
```

> The three main types of machine learning are:
>
> 1. **Linear Regression**: This type of machine learning involves a linear relationship between the input data and the output values. It's used to model the relationship between a dependent variable and one or more independent variables.
>
> 2. **Decision Trees**: Decision trees are a type of machine learning that uses a tree-like structure to classify data points based on their values. They're commonly used for classification tasks, such as predicting continuous outcomes or classifying credit transactions.
>
> 3. **Random Forest**: Random forest is a type of machine learning that uses a random forest to predict the likelihood of a specific outcome. It's used for classification tasks, such as predicting the likelihood of a customer churning or the likelihood of a patient responding to a treatment.
>
> These three types of machine learning are used in various applications, including image classification, natural language processing, and predictive analytics.

**Verdict**: FAIL — lists algorithms (Linear Regression, Decision Trees, Random Forest) instead of paradigms (Supervised, Unsupervised, Reinforcement Learning). No factual understanding of ML taxonomy.

---

## Prompt 6: 2+2 (low temp)

```
What is 2+2?
```

> The question of two+2 is a classic example of a simple arithmetic operation. It's often attributed to the German mathematician Carl Friedrich Gauss, who as a young student, reportedly used it to solve a problem involving sums of two numbers. The idea is to pair the numbers in a way that creates a new sum that is equal to the original sum plus the same number. This is often referred to as the "pairing effect" or "pairing of numbers."
>
> In the case of two+2, we can pair the numbers in a way that creates a new sum of 2. For example, if we pair the first number with the last number in the pair, the second number would be the same as the first number plus 1. This pairing effect allows us to create a new sum of 2 that is equal to the original sum plus 1.
>
> The key insight here is that the pairing effect is not just about pairing the numbers, but also about creating a new sum that is equal to the original sum plus the same number. This is why we often use the pairing effect to solve problems involving sums of numbers, and it's a fundamental

**Verdict**: FAIL — never says "4". Rambles about Gauss and pairing effects. Arithmetic is beyond this model scale.

---

## Prompt 7: Fibonacci (low temp)

```
What comes after 1, 1, 2, 3, 5, 8?
```

> This is a classic example of a simple yet elegant problem in mathematics. The solution to this problem is often referred to as the "stars and bars" or "stars and bars" problem, named after the ancient Greek mathematician Euclid. The idea is to represent the number 1 as a bar, and then arrange the bar's heights in a line, with the bar's heights divided into two equal parts.
>
> The key insight here is that the bar's heights are arranged in a specific order, with the bar's heights in the first part being the bar's heights in the second part, and the bar's heights in the third part being the bar's heights in the fourth part. This creates a sequence of bar heights, where each bar is the bar's height in the first part, and the bar's heights in the second part are the bar's heights in the third part.
>
> This problem has been a subject of interest for centuries, as it has led to the development of various mathematical concepts, such as the concept of bar graphs and the idea of arranging bar heights in a

**Verdict**: FAIL — never identifies as Fibonacci sequence. Hallucinates "stars and bars" and Euclid. Pattern recognition not working.

---

## Prompt 8: Neural Network (low temp)

```
Explain what a neural network is in one sentence.
```

> A neural network is a type of machine learning model that uses a combination of self-learning algorithms and neural networks to learn patterns and relationships in data. It's a powerful tool for understanding complex data and making predictions, but it's not a traditional neural network in the classical sense. Instead, it's a type of deep learning model that uses a combination of neural networks and a learning algorithm that is trained on a dataset to learn patterns and relationships.

**Verdict**: FAIL — circular definition ("a neural network uses neural networks"). Contradicts itself ("it's not a traditional neural network").

---

## Prompt 9: SQL Query (low temp)

```
Write a SQL query to find all employees hired in 2023.
```

> To find all employees hired in 2023, you can use the following SQL query:
>
> ```sql
> SELECT * FROM employees WHERE name = 'John Doe';
> ```
>
> This query selects all columns from the `employees` table where the `name` column matches the string 'John Doe'.
>
> If you want to use a specific column instead of a string, you can modify the query like this:
>
> ```sql
> SELECT * FROM employees WHERE name = 'John Doe' AND name = 'Jane Doe';
> ```
>
> This query uses the `AND` operator to combine the `name` and `name` columns into a single string, which is then used to filter the results.

**Verdict**: FAIL — ignores the date filter entirely. Uses `WHERE name = 'John Doe'` instead of a date condition like `WHERE YEAR(hire_date) = 2023`.

---

## Prompt 10: Capital of France (low temp)

```
Capital of France?
```

> The capital of France is Paris.

**Verdict**: PASS — correct. Simple factual recall that appears frequently in training data.

---

## Summary

| Prompt | Type | Result |
|--------|------|--------|
| Capital of France | Factual recall | PASS |
| Palindrome function | Code generation | PASS |
| Gradient descent | Technical knowledge | FAIL |
| Average speed | Math reasoning | FAIL |
| Poem about ML | Creative writing | FAIL (repetition) |
| Three types of ML | ML taxonomy | FAIL |
| 2+2 | Arithmetic | FAIL |
| Fibonacci | Pattern recognition | FAIL |
| Neural network | Definition | FAIL |
| SQL query 2023 | SQL | FAIL |

**Overall**: The SFT successfully taught dialogue format and code patterns, but ~140M params is fundamentally too small for reliable knowledge/reasoning. Code generation passes because code has high statistical regularity. Everything requiring factual knowledge, arithmetic, or multi-step reasoning fails.