---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 有争议的地图和词典观点
translated: true
type: note
---

问题：关于编程中的 map/dictionary，有哪些不受欢迎的观点？

回答：

以下是一些关于 map/dictionary，资深程序员经常会为之辩护（而大多数人不同意或觉得极端）的、真正不受欢迎或有争议的观点：

- **Map 不应是默认集合**
  许多经验丰富的开发者认为，首先使用哈希 map 是一种代码异味。带有整数索引的数组/向量或排序结构通常更快、占用内存更少，并且具有更好的缓存局部性。Map 鼓励“字符串类型”（stringly-typed）或草率的数据建模（例如，使用任意键而不是适当的结构体/类）。

- **有序字典（例如 LinkedHashMap、Rust 的 IndexMap、Go 1.9 之后的 map）几乎总是一个错误**
  保留插入顺序看起来很方便，但这会隐藏 API 中的非确定性，并鼓励依赖偶然的顺序。真正的有序数据应该放在向量/数组中 + 显式排序，而不是哈希表的副作用。

- **JSON 对象 { } 也不应该是有序的**
  大量 bug 和互操作性问题源于人们假设 JSON 对象键的顺序很重要。大多数实现现在保留顺序（自 ES2015、JSON 规范更改以来）这一事实受到一些底层开发人员的诟病。

- **空/不存在的键应该抛出异常，而不是返回 null/nil/None**
  像 Python (`dict.get`) 或 JavaScript 这样在键缺失时默默返回 `undefined`/`None` 的语言，鼓励编写充满 `if x is not None` 的防御性代码。Go 的 `value, ok := map[key]` 逗号惯用法或 Rust 的 `.get()` 返回 `Option` 是严格更好的；默默失败会养成坏习惯。

- **对于小 N (< ~20 个元素)，哈希表被高估了**
  在实践中，对于小型数据集，对一个对数组进行线性搜索或使用 switch/if-else 阶梯通常更快，因为有分支预测且没有哈希开销。一些 C++ 开发者会直接编写一个 15 个 case 的 `switch`，而不是使用 `std::unordered_map`。

- **语言提供的字典字面量是有害的**
  它们使得创建ad-hoc匿名结构体过于容易。最终导致代码库中充满了 `{ "foo": 1, "bar": "x" }` 而不是适当的类型。像 Go (在某些上下文中没有带类型推断的 map 字面量) 或 Rust (要求你显式构建 HashMap) 这样的语言迫使你深思熟虑。

- **迭代顺序应该明确地是非确定性的**
  Python 在 3.6+ 中随机化字典顺序是一件好事。仍然保证插入顺序的语言（PHP、Ruby、现代 JS）使得编写偶然依赖顺序的代码过于容易，这种代码只在哈希函数重新播种时才会在负载下失败。

- **带有不可哈希键的 map（例如，在 Python 中以列表或其他 map 为键）是纯粹的邪恶**
  它们存在，人们使用它们，然后想知道为什么序列化、相等性或调试变得不可能。

这些观点往往来自系统程序员、编译器作者，或那些维护过大型代码库的人，在这些代码库中，“随便使用一个 dict”变成了一场技术债务噩梦。

参考文献：

- [The “Stringly Typed” Problem](https://blog.codinghorror.com/new-programming-jargon/#stringly-typed)
- [Python 3.6+ dict order randomization rationale](https://mail.python.org/pipermail/python-dev/2017-December/151283.html)
- [Go maps are intentionally unordered](https://go.dev/blog/maps)
