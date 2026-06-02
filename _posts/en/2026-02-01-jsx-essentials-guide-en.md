---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: JSX Essentials and Syntax Guide
translated: false
type: note
---

JSX (JavaScript XML) is a syntax extension for JavaScript that lets you write UI markup directly in your JavaScript files. It's most commonly associated with React, but it's actually a standalone syntax that can be transpiled for use with any framework or library.

---

## What JSX Actually Is

JSX is **not** HTML, and it's **not** a template language. It's a syntactic sugar that gets transformed (transpiled) into regular JavaScript function calls under the hood. When you write:

```jsx
const element = <h1>Hello, World!</h1>;
```

A transpiler (like Babel) converts it into:

```js
const element = React.createElement("h1", null, "Hello, World!");
```

So every piece of JSX you write is just a disguised function call that creates a description of a UI element — a plain JavaScript object called a **React element** (or virtual DOM node).

---

## Why JSX Exists

Writing `React.createElement(...)` for every single element is verbose and painful, especially for nested structures. JSX gives you a familiar, HTML-like syntax that's far more readable and maintainable — while still being fully embedded in JavaScript, which means you get all the power of the language right alongside your markup.

---

## Core Syntax Rules

JSX looks like HTML but has some important differences you need to know:

**Self-closing tags are mandatory for elements with no children.** In HTML, `<img>` is valid. In JSX, you must write `<img />`.

**`class` becomes `className`.** Since `class` is a reserved word in JavaScript, JSX uses `className` instead. Similarly, `for` becomes `htmlFor`.

**All attributes use camelCase.** For example: `onclick` → `onClick`, `tabindex` → `tabIndex`, `background-color` in inline styles becomes `backgroundColor`.

**Inline styles are objects, not strings.** You pass a JavaScript object to the `style` attribute:

{% raw %}
```jsx
// ❌ Wrong
<div style="color: red; font-size: 16px"></div>

// ✅ Correct
<div style={{ color: "red", fontSize: "16px" }}></div>
```
{% endraw %}

The double curly braces here aren't special syntax — the outer `{}` is the JSX expression delimiter, and the inner `{}` is a regular JavaScript object literal.

**Every JSX expression must have a single root element.** You can't return two sibling elements side by side without wrapping them. If you don't want an extra DOM node, use a **Fragment**:

```jsx
// ❌ Invalid
return <h1>Title</h1><p>Body</p>;

// ✅ Using a Fragment
return (
  <>
    <h1>Title</h1>
    <p>Body</p>
  </>
);
```

`<>...</>` is shorthand for `<React.Fragment>...</React.Fragment>`.

---

## Embedding JavaScript Expressions

The real power of JSX is that you can embed any valid JavaScript *expression* inside curly braces `{}`. This is what separates it from static HTML:

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

You can use ternaries, function calls, array methods — anything that returns a value:

```jsx
const isLoggedIn = true;

<div>
  {isLoggedIn ? <Dashboard /> : <LoginForm />}
</div>
```

**What you *can't* do** is use statements (like `if`, `for`, or `let x = ...`) directly inside `{}`. Only expressions are allowed. This is why you'll see patterns like ternaries and logical `&&` short-circuiting used so frequently in JSX:

```jsx
// Conditional rendering with &&
{isLoggedIn && <Dashboard />}

// This works because if isLoggedIn is false,
// the expression short-circuits and renders nothing.
```

---

## Rendering Lists

To render a list of items, you map over an array and return JSX for each element. Each item in the list **must have a unique `key` prop** — React uses this to efficiently reconcile the DOM:

```jsx
const fruits = ["Apple", "Banana", "Cherry"];

<ul>
  {fruits.map((fruit, index) => (
    <li key={index}>{fruit}</li>
  ))}
</ul>
```

Using the array index as a key works for static lists. For dynamic lists (where items can be added, removed, or reordered), use a stable unique identifier like a database ID instead.

---

## Components in JSX

One of the most powerful aspects of JSX is that it works seamlessly with **components** — reusable, composable chunks of UI. Components in JSX follow one simple rule: **their names must start with a capital letter**. This is how the transpiler knows the difference between a native HTML element and a custom component:

```jsx
// Lowercase → treated as an HTML element
<div>...</div>

// Capitalized → treated as a component
<MyButton>Click me</MyButton>
```

You pass data to components using **props** (short for "properties"), which work just like HTML attributes:

```jsx
function Greeting({ name, excited }) {
  return <h1>Hello, {name}{excited ? "!" : "."}</h1>;
}

// Usage
<Greeting name="Bob" excited={true} />
```

Props without an explicit value default to `true`, so `<Greeting excited />` is equivalent to `<Greeting excited={true} />`.

---

## Children and `props.children`

Anything you nest between a component's opening and closing tags becomes part of its `children` prop:

```jsx
function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  );
}

// Usage — anything inside Card becomes children
<Card>
  <h2>Title</h2>
  <p>Some content here.</p>
</Card>
```

This pattern is the foundation of **composition** in React — you build complex UIs by nesting and combining simple, reusable components.

---

## A Quick Summary of Common Pitfalls

| HTML Habit | JSX Equivalent |
|---|---|
| `class="btn"` | `className="btn"` |
| `for="email"` | `htmlFor="email"` |
| `<br>` | `<br />` |
| `style="color: red"` | `style={{ color: "red" }}` |
| Multiple root elements | Wrap in `<>...</>` or a parent element |
| `onclick="handler()"` | `onClick={handler}` |

---

JSX is ultimately just a more ergonomic way to describe UI structure in JavaScript. Once you internalize that every `<Tag />` is a function call under the hood, and that `{}` is your gateway to any JavaScript expression, the rest follows naturally.
