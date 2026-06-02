---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: iOS开发中的NSArray概述
translated: true
type: note
---

### 什么是 NSArray？

`NSArray` 是苹果 Foundation 框架中的一个类，属于 iOS SDK（以及 macOS 等）的一部分。它表示一个不可变的、有序的对象集合，类似于其他语言中的数组。这意味着一旦创建了 `NSArray`，你就无法添加、删除或替换元素——只能从中读取数据。在 Objective-C 的 iOS 应用开发中，它通常用于存储和管理数据列表，比如用户偏好设置、数据库查询结果或 UI 元素。

主要特性：
- **不可变**：创建后大小和内容固定（可变版本使用 `NSMutableArray`）。
- **对象类型安全**：存储指向 Objective-C 对象的指针（例如 `NSString`、`NSNumber`、自定义类）。它不直接支持基本数据类型——需要将它们包装在 `NSNumber` 或类似类中。
- **索引访问**：通过整数索引（从 0 开始）访问元素。
- **线程安全**：通常并发读取是安全的，但不支持写入（因为它是不可变的）。
- **集成性**：与其它 Foundation 类（如 `NSDictionary`、`NSString`）和 Cocoa Touch UI 组件无缝协作。

在 Swift 中，`NSArray` 会被桥接到 `Array`，但如果你在使用 Objective-C（常见于遗留的 iOS 代码），你会直接使用 `NSArray`。

### 如何在 iOS 中使用 NSArray

在 iOS 项目中使用 `NSArray`：
1. 导入 Foundation 框架（通常在 iOS 应用中默认已包含）。
   ```objc
   #import <Foundation/Foundation.h>
   ```

2. **创建 NSArray**：
   - 字面量语法（iOS 6+）：`@[对象1, 对象2, ...]`
   - 初始化方法：`[[NSArray alloc] initWithObjects:对象1, 对象2, nil]`
   - 从 C 数组创建：`initWithArray:copyItems:`

   示例：
   ```objc
   NSArray *fruits = @[@"apple", @"banana", @"cherry"];
   // 或者：
   NSArray *numbers = [[NSArray alloc] initWithObjects:@1, @2, @3, nil];
   ```

3. **访问元素**：
   - `objectAtIndex:` 用于获取项。
   - `count` 用于获取长度。
   - `firstObject` / `lastObject` 用于获取首尾元素。
   - `containsObject:` 用于检查是否存在。

   示例：
   ```objc
   NSString *firstFruit = [fruits objectAtIndex:0]; // "apple"
   NSUInteger count = [fruits count]; // 3
   BOOL hasOrange = [fruits containsObject:@"orange"]; // NO
   ```

4. **遍历**：
   - 快速枚举：`for (id obj in array) { ... }`
   - `enumerateObjectsUsingBlock:` 用于基于块的遍历（iOS 4+）。

   示例：
   ```objc
   for (NSString *fruit in fruits) {
       NSLog(@"Fruit: %@", fruit);
   }
   ```

5. **常见操作**：
   - 排序：`sortedArrayUsingSelector:` 或 `sortedArrayUsingComparator:`。
   - 过滤：`filteredArrayUsingPredicate:`（与 NSPredicate 配合使用）。
   - 连接：`componentsJoinedByString:` 用于字符串。
   - 写入文件：`writeToFile:atomically:`。

   示例（过滤）：
   ```objc
   NSPredicate *predicate = [NSPredicate predicateWithFormat:@"length > 5"];
   NSArray *longFruits = [fruits filteredArrayUsingPredicate:predicate];
   // 结果：@[@"banana", @"cherry"]
   ```

6. **在 iOS 上下文中**：
   - **表格视图**：将 `NSArray` 传递给 `UITableView` 的数据源方法，如 `tableView:numberOfRowsInSection:`（通过 `count`）和 `tableView:cellForRowAtIndexPath:`（通过 `objectAtIndex:`）。
   - **用户默认设置**：使用 `NSUserDefaults` 存储/检索：`[defaults setObject:array forKey:@"savedItems"];`。
   - **JSON 处理**：使用 `JSONObjectWithData:options:error:` 与 `NSData` 相互转换。

对于可变需求（例如动态添加项），切换到 `NSMutableArray`：
```objc
NSMutableArray *mutableFruits = [NSMutableArray arrayWithArray:fruits];
[mutableFruits addObject:@"date"];
```

### 提示
- 始终检查 `nil` 或边界以避免崩溃：使用 `objectAtIndex:` 时进行索引验证。
- 性能：访问为 O(1)，搜索为 O(n)。
- 现代 iOS：对于新项目，考虑使用 Swift 的 `Array`——它更具类型安全性。

[NSArray 文档](https://developer.apple.com/documentation/foundation/nsarray)
[NSMutableArray 文档](https://developer.apple.com/documentation/foundation/nsmutablearray)
