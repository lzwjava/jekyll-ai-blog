---
audio: false
generated: true
lang: en
layout: post
title: LinkedHashMap vs TreeMap
translated: false
type: note
---

Great question! Both `LinkedHashMap` and `TreeMap` are implementations of the `Map` interface in Java, but they have **different ordering strategies** and use **different underlying data structures**.

### 🌳 `TreeMap`
- **Ordering**: Sorted by **natural order** of the keys (or by a custom `Comparator` if provided).
- **Data Structure**: Backed by a **Red-Black Tree** (a type of self-balancing binary search tree).
- **Performance**:
  - `O(log n)` for get/put/remove
  - Sorted order maintained at all times
- **Use Case**: When you need **sorted keys**.

### 🔗 `LinkedHashMap`
- **Ordering**: Maintains **insertion order** (or optionally access order if configured that way).
- **Data Structure**: Backed by a **hash table + linked list**.
- **Performance**:
  - `O(1)` for get/put/remove (like `HashMap`)
  - Slightly more memory overhead due to the linked list
- **Use Case**: When you care about **the order in which entries were added**.

---

### ✅ Iterator Order
Yes, their **iterator order will be different**:

| Map Type       | Iterator Order                     |
|----------------|------------------------------------|
| `TreeMap`      | Sorted by keys                     |
| `LinkedHashMap`| Insertion order (or access order)  |

---

### 🔍 Example

```java
Map<String, Integer> treeMap = new TreeMap<>();
Map<String, Integer> linkedMap = new LinkedHashMap<>();

treeMap.put("banana", 2);
treeMap.put("apple", 3);
treeMap.put("cherry", 1);

linkedMap.put("banana", 2);
linkedMap.put("apple", 3);
linkedMap.put("cherry", 1);

System.out.println("TreeMap:");
for (String key : treeMap.keySet()) {
    System.out.println(key);
}

System.out.println("LinkedHashMap:");
for (String key : linkedMap.keySet()) {
    System.out.println(key);
}
```

**Output:**
```
TreeMap:
apple
banana
cherry

LinkedHashMap:
banana
apple
cherry
```

Let me know if you want a breakdown of performance or memory usage in more detail.
