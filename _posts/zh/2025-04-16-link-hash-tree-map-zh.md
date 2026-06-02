---
audio: false
generated: true
lang: zh
layout: post
title: LinkedHashMap与TreeMap对比
translated: true
type: note
---

很好的问题！`LinkedHashMap` 和 `TreeMap` 都是 Java 中 `Map` 接口的实现，但它们具有**不同的排序策略**，并且使用**不同的底层数据结构**。

### 🌳 `TreeMap`
- **排序方式**：按照键的**自然顺序**排序（如果提供了自定义 `Comparator`，则按比较器排序）
- **数据结构**：基于**红黑树**（一种自平衡二叉搜索树）
- **性能表现**：
  - 获取/插入/删除操作的时间复杂度为 `O(log n)`
  - 始终保持键的排序状态
- **使用场景**：当需要**按键排序**时使用

### 🔗 `LinkedHashMap`
- **排序方式**：保持**插入顺序**（如果配置为访问顺序模式，则按访问顺序排序）
- **数据结构**：基于**哈希表 + 链表**的组合
- **性能表现**：
  - 获取/插入/删除操作的时间复杂度为 `O(1)`（与 `HashMap` 相同）
  - 由于需要维护链表，内存开销略高
- **使用场景**：当需要**保持元素插入顺序**时使用

---

### ✅ 迭代器顺序
是的，它们的**迭代器顺序确实不同**：

| 映射类型       | 迭代器顺序                     |
|----------------|------------------------------------|
| `TreeMap`      | 按键排序                         |
| `LinkedHashMap`| 插入顺序（或访问顺序）          |

---

### 🔍 代码示例

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

**输出结果：**
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

如果您需要更详细的性能分析或内存使用情况说明，请随时告诉我。
