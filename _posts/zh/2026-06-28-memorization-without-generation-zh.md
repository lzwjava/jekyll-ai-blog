---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 记忆而不生成
translated: true
type: note
---

以下是全部5个测试的总结：

== 测试 1：Java BST（长提示，search 方法的延续）==
结果：混合。提示被逐字复现（很好），但一旦到达延续点，就生成了无意义的 Java 代码：`return;`，混乱的方法签名如 `public String get(String source)`，随机 token 如 `Property.TrveradataValue`。结构（缩进、花括号）大致保留，但逻辑是垃圾。

== 测试 2：Python MiniGPT（长提示，训练循环后的延续）==
结果：这批中最好的。整个提示几乎逐字复现，包括完整的训练循环、检查点保存和模型加载。在 "Model loaded successfully!" 之后的内容退化为垃圾（`data_size(t.last, self.get_size())`）。对于一个 124M 模型来说，这是对 Python 模式还算不错的记忆。

== 测试 3：Flask Web 应用（长提示，错误处理后的延续）==
结果：提示的记忆良好（用户路由、错误处理程序、主块都正确复现）。在 `app.run(debug=True, port=5000)` 之后的延续完全是胡言乱语：`def = assert_user_text): data = get_action.get_to_get_get_string(...)`。

== 测试 4：短提示 "def quicksort(arr):"（3 个样本）==
结果：完全失败。所有 3 个样本只产生了空白和随机标点。模型无法从短提示生成有意义的 Python 代码。

== 测试 5：Java HashMap（长提示，put 方法后的延续）==
结果：提示逐字复现，延续是垃圾：`return self.copy(J,);` —— 将 Python 语法混入 Java。然后是随机 token。

== 结论 ==
该模型学会了记忆训练中见过的长代码块（复现接近完美），但几乎不具备对新代码的生成能力。短提示产生胡言乱语。即使在长上下文中，一旦超出记忆区域，输出会立即退化为随机 token 和跨语言污染。

这对于一个在 14B token 代码上训练的 124M 模型来说是预期行为——它更像是一个代码记忆模型，而不是代码生成模型。验证损失 3.466 确认了它没有充分学习到分布，无法生成合理的代码。
