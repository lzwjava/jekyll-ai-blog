---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 王垠的编程智慧
translated: true
type: note
---

**问题：** https://www.infoq.cn/article/wisdom-of-programming 这篇文章说了什么？

**回答：**

这篇文章标题为 **"编程的智慧" (The Wisdom of Programming)**，作者 **Wang Yin (王垠)**，发表于 **InfoQ China** 的 **2016年8月29日**。阅读时长约70分钟（~21,000个汉字）。Wang Yin 是一位著名的且有主见的中国程序员/博主。本文分享了他个人编程哲学和高品质代码编写中宝贵的经验教训。以下是对所有主要主题的全面总结：

---

## 1. 反复打磨你的代码

王垠认为，提高编程技能的最有效方法是**反复修改和打磨代码**，而不仅仅是写更多的代码。他将此比作作家会丢弃比发表更多的内容——伟大的程序员删除的代码比保留的更多。你无法一蹴而就写出完美的代码；洞见会随着时间逐渐显现。

---

## 2. 编写优雅的代码

优雅的代码有两个关键的结构特征：

- **盒状结构**：代码整齐嵌套和组织，像抽屉里的标签隔间。
- **树状结构**：逻辑像树一样清晰分支。他指出，他的 `if` 语句几乎总是有**两个分支**（if + else），使逻辑明确且穷尽。

---

## 3. 编写模块化的代码

真正的模块化是**逻辑上的，而不是物理上的**。将代码拆分成许多文件/目录并不能使其模块化。模块化的真正工具是**function**——function 有明确定义的输入（parameters）和输出（return values）。他推荐：

- **保持 function 简短**（少于 ~40 行，能在一屏内显示而无需滚动）。
- **创建小的辅助 function**——即使是2行的辅助函数也能极大简化主逻辑。
- **每个 function 应只做一件事**——避免多用途 function 根据条件进行内部分支。
- **避免使用 global variables 或 class members 在 function 间传递数据**——改用 local variables 和 parameters。

---

## 4. 编写可读的代码

真正优雅的代码**几乎不需要注释**。过度注释实际上有害——注释会过时并 clutter 代码。相反，通过以下方式使代码自解释：

- **有意义的 function 和 variable 名称**——名称应描述逻辑。
- **将 local variables 保持在使用位置附近**——不要在 function 开头声明所有变量。
- **local variable 名称保持简短**——当 variable 在附近使用时，上下文使短名称足够。
- **不要复用 local variables**——为每个不同值定义新 variable；这澄清了 scope 和 intent。
- **将复杂逻辑提取到辅助 function**——用名称良好的 function 调用替换一坨晦涩代码。
- **将复杂表达式提取到中间 variables**——避免深度嵌套的 function 调用。
- **在逻辑边界处断行**——不要依赖 IDE 的自动换行，后者会在任意位置断行。

他警告不要让代码看起来像自然语言（例如 Chai.js 的 assertion 风格），这实际上降低了清晰度。

---

## 5. 编写简单的代码

不要盲目使用语言的每个特性。坚持可靠、经战火考验的子集。具体规则：

- **避免 `i++` / `++i` / `i--` / `--i`**——这些混合了读和写操作，是历史性的设计错误。用显式的两步操作替换（例如 `int t = i; i += 1; foo(t);`），除非在简单的 `for` 循环更新表达式中。
- **绝不省略 curly braces**——即使单行 `if` body 也应始终有 `{}`，以避免后续添加新行时的“视觉错觉” bug。
- **使用 parentheses 澄清 operator precedence**——不要依赖读者知道晦涩的 precedence 规则（例如 bitshift `<<` 的 precedence 低于 `+`）。
- **避免在循环中使用 `continue` 和 `break`**——它们使循环终止条件复杂。通过以下方式消除它们：
  - 将 `continue` 的条件反转成 `if` 块。
  - 将 `break` 条件合并到 `while` header。
  - 用 `return` 替换 `break`。
  - 将复杂循环体提取到辅助 function。

---

## 6. 编写直接/直观的代码

即使显得更长，也选择更清晰、更显式的写法。例如，避免滥用 short-circuit evaluation（`&&`、`||`）作为 `if` 语句的替代。这很 confusing，因为 logical OR/AND 是为效率而设计，而不是控制流的可读性。

而非：
```javascript
if (action1() || action2() && action3()) { ... }
```
写成显式版本：
```java
if (!action1()) {
  if (action2()) {
    action3();
  }
}
```

---

## 7. 编写防弹的代码

**每个 `if` 语句都应有**两个分支**，迫使自己考虑所有情况。不要省略 `else` 分支并依赖“fall-through”控制流——这会创建难以验证正确的 spaghetti logic。显式处理每个可能的结果。

---

## 8. 正确处理错误

- 不要忽略 function 的 return values（例如 Unix `read()` 返回 `-1`）。
- 不要使用过于宽泛的 `catch (Exception e) {}`——这会 silently swallow 意外错误。
- 捕获你预期的**特定** exception 类型。
- 保持 `try` 块小——尽可能每个 function 调用一个 try/catch，以 pinpoint 哪个调用失败了。
- 在错误发生处处理它们，而不是无休止地向上 re-throwing。

---

## 9. 正确处理空指针

- **尽量少产生 null**——对于“未找到”，使用 exceptions（例如 `NotFoundException`）而不是返回 null。
- **绝不捕获 `NullPointerException`**——改修根源。
- **绝不将 null 放入 collections**（List、Map、Set）——这会导致难以追踪的 bug。
- **在收到 nullable 值的位置立即检查 null**，并有意义地处理，而不是将 null 向上游传递。
- **function 作者应 aggressively 拒绝 null parameters**——使用 `Objects.requireNonNull()` 在 null 输入时立即 crash。
- 使用 **`@NotNull` / `@Nullable` annotations**（IntelliJ）进行 static analysis。
- 小心地使用 **`Optional` types**（Java 8 / Swift）——益处仅在使用“atomic”模式（一次操作检查 + unwrap）时才有，而不是分别调用 `isPresent()` + `get()`（这只是换个名字的 null 检查）。

---

## 10. 防止过度工程

过度工程的迹象：
- 在解决当前问题前想得太远。
- 在有 working code 前痴迷“code reuse”。
- 过度的 test scaffolding 使简单代码复杂化。

他的原则：
- **先解决手头问题**，然后考虑未来可扩展性。
- **先写 working code**，然后考虑 reuse。
- **先写简单、明显正确的代码**，然后考虑 testing。

他区分了“无明显 bug 的代码”（复杂代码 + 很多 tests）和“明显无 bug 的代码”（简单、直接的代码），并倡导后者。

---

**参考：**

- [https://www.infoq.cn/article/wisdom-of-programming](https://www.infoq.cn/article/wisdom-of-programming)
