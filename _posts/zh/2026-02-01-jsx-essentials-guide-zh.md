---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: JSX 基础知识与语法指南
translated: true
type: note
---

JSX (JavaScript XML) 是 JavaScript 的一种语法扩展，允许你在 JavaScript 文件中直接编写 UI 标记。它最常与 React 相关联，但实际上它是一种独立的语法，可以通过 transpile 转换为任何 framework 或 library 使用。

---

## JSX 的本质是什么

JSX **不是** HTML，也**不是**一种模板语言。它是一种语法糖，在底层会被转换（transpile）为常规的 JavaScript function calls。当你编写：

```jsx
const element = <h1>Hello, World!</h1>;
```

transpiler（如 Babel）会将其转换为：

```js
const element = React.createElement("h1", null, "Hello, World!");
```

因此，你编写的每一段 JSX 都只是一个伪装的 function call，它创建了一个 UI 元素的描述 —— 一个被称为 **React element**（或 virtual DOM 节点）的普通 JavaScript object。

---

## 为什么存在 JSX

为每一个元素都编写 `React.createElement(...)` 是非常冗长且痛苦的，尤其是对于嵌套结构。JSX 为你提供了一种熟悉的、类似 HTML 的语法，它的可读性和可维护性要高得多 —— 同时它仍然完全嵌入在 JavaScript 中，这意味着你可以在标记旁发挥该语言的所有能力。

---

## 核心语法规则

JSX 看起来像 HTML，但有一些你需要了解的重要区别：

**对于没有子元素的元素，自闭合标签（Self-closing tags）是强制性的。** 在 HTML 中，`<img>` 是有效的。在 JSX 中，你必须写成 `<img />`。

**`class` 变为 `className`。** 由于 `class` 是 JavaScript 中的保留字，JSX 改用 `className`。同样地，`for` 变为 `htmlFor`。

**所有属性（attributes）都使用 camelCase。** 例如：`onclick` → `onClick`，`tabindex` → `tabIndex`，inline styles 中的 `background-color` 变为 `backgroundColor`。

**Inline styles 是 objects，而不是 strings。** 你需要向 `style` 属性传递一个 JavaScript object：

{% raw %}

```jsx
// ❌ 错误
<div style="color: red; font-size: 16px"></div>

// ✅ 正确
<div style={{ color: "red", fontSize: "16px" }}></div>
```

{% endraw %}

这里的双大括号并不是特殊的语法 —— 外层的 `{}` 是 JSX 表达式的分隔符，内层的 `{}` 是一个常规的 JavaScript object literal。

**每个 JSX 表达式必须有一个单一的根元素（root element）。** 你不能在不进行包装的情况下并列返回两个兄弟元素。如果你不想增加额外的 DOM 节点，可以使用 **Fragment**：

```jsx
// ❌ 无效
return <h1>Title</h1><p>Body</p>;

// ✅ 使用 Fragment
return (
  <>
    <h1>Title</h1>
    <p>Body</p>
  </>
);
```

`<>...</>` 是 `<React.Fragment>...</React.Fragment>` 的简写。

---

## 嵌入 JavaScript 表达式

JSX 的真正强大之处在于你可以在大括号 `{}` 中嵌入任何有效的 JavaScript *expression*。这是它与静态 HTML 的区别所在：

```jsx
const name = "Alice";
const age = 30;

const greeting = (
  <div>
    <h1>Hello, {name}!</h1>
    <p>You are {age} years old.</p>
    <p>Next year you'll be {age + 1}.</p>
  </div>
);
```

你可以使用 ternaries（三元运算符）、function calls、array methods —— 任何返回值的操作：

```jsx
const isLoggedIn = true;

<div>
  {isLoggedIn ? <Dashboard /> : <LoginForm />}
</div>
```

**你不能做的是**在 `{}` 中直接使用 statements（如 `if`、`for` 或 `let x = ...`）。只有 expressions 是允许的。这就是为什么你会经常在 JSX 中看到 ternaries 和逻辑 `&&` 短路运行模式的原因：

```jsx
// 使用 && 进行条件渲染
{isLoggedIn && <Dashboard />}

// 这之所以有效，是因为如果 isLoggedIn 为 false，
// 表达式会短路并不渲染任何内容。
```

---

## 渲染列表

要渲染一个项目列表，你可以对 array 进行 map 操作并为每个元素返回 JSX。列表中的每个项目 **必须有一个唯一的 `key` prop** —— React 利用它来高效地 reconcile DOM：

```jsx
const fruits = ["Apple", "Banana", "Cherry"];

<ul>
  {fruits.map((fruit, index) => (
    <li key={index}>{fruit}</li>
  ))}
</ul>
```

对于静态列表，使用 array index 作为 key 是可行的。对于 dynamic lists（可能会添加、删除或重新排序项目），请改用稳定的唯一标识符，例如数据库 ID。

---

## JSX 中的组件（Components）

JSX 最强大的功能之一是它可以与 **components**（可重用、可组合的 UI 块）无缝协作。JSX 中的组件遵循一条简单的规则：**它们的名称必须以大写字母开头**。这就是 transpiler 区分原生 HTML 元素和自定义组件的方式：

```jsx
// 小写 → 被视为 HTML 元素
<div>...</div>

// 首字母大写 → 被视为组件
<MyButton>Click me</MyButton>
```

你使用 **props**（"properties" 的缩写）向组件传递数据，其用法与 HTML 属性完全相同：

```jsx
function Greeting({ name, excited }) {
  return <h1>Hello, {name}{excited ? "!" : "."}</h1>;
}

// 使用方式
<Greeting name="Bob" excited={true} />
```

没有显式值的 props 默认为 `true`，因此 `<Greeting excited />` 等同于 `<Greeting excited={true} />`。

---

## Children 与 `props.children`

嵌套在组件开始标签和结束标签之间的任何内容都会成为其 `children` prop 的一部分：

```jsx
function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  );
}

// 使用方式 —— Card 内部的任何内容都会成为 children
<Card>
  <h2>Title</h2>
  <p>Some content here.</p>
</Card>
```

这种模式是 React 中 **composition**（组合）的基础 —— 你通过嵌套和组合简单的、可重用的组件来构建复杂的 UI。

---

## 常见错误点快速总结

| HTML 习惯 | JSX 等效写法 |
| --- | --- |
| `class="btn"` | `className="btn"` |
| `for="email"` | `htmlFor="email"` |
| `<br>` | `<br />` |
| `style="color: red"` | `style={{ color: "red" }}` |
| 多个根元素 | 包装在 `<>...</>` 或父元素中 |
| `onclick="handler()"` | `onClick={handler}` |

---

归根结底，JSX 只是在 JavaScript 中描述 UI 结构的一种更符合人体工程学的方式。一旦你理解了每一个 `<Tag />` 在底层都是一个 function call，并且 `{}` 是你通往任何 JavaScript expression 的入口，剩下的内容也就顺理成章了。
