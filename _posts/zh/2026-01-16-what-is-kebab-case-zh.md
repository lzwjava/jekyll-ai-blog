---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 什么是短横线命名法？
translated: true
type: note
---

**Question:** 什么是 kebab case？

**Answer:**

Kebab case（也称为 **kebab-case**、**kebab style** 或 **dash case**）是一种命名规范，其特点是：

- 单词全部由 **lowercase**（小写）组成
- 单词之间通过 **hyphens**（连字符 `-`）连接

**Examples:**

```text
my-variable-name
user-profile-picture
api-key-secret
dark-mode-toggle
get-user-by-id
background-color-red-500
```

### Comparison with other common naming conventions

| Naming style     | Example                     | Description                              | Common usage                              |
|------------------|-----------------------------|------------------------------------------|--------------------------------------------|
| kebab-case       | user-profile-picture        | lowercase + hyphens                      | CSS classes, HTML attributes, URLs        |
| snake_case       | user_profile_picture        | lowercase + underscores                  | Python, Ruby, Rust, PostgreSQL            |
| camelCase        | userProfilePicture          | first word lowercase, others capitalized | JavaScript variables, JSON keys           |
| PascalCase       | UserProfilePicture          | every word capitalized                   | Java, C#, TypeScript class names          |
| SCREAMING_SNAKE_CASE | USER_PROFILE_PICTURE   | uppercase + underscores                  | Constants, environment variables          |

### Where kebab-case is most commonly used (2025–2026)

- CSS class names 和 IDs

  ```css
  .card-header-title { … }
  .is-active { … }
  ```

- HTML data attributes

  ```html
  <div data-user-id="123" data-created-at="2025-01-01"></div>
  ```

- URL slugs

  ```text
  https://example.com/blog/how-to-learn-rust-in-2026
  ```

- 许多现代 CSS-in-JS 库及 utility-first frameworks
  （Tailwind CSS, UnoCSS, Panda CSS 等）
- Git branch names（非常常见的模式）
  `feature/add-dark-mode-toggle`

**Quick memory tip:**
想象一下真实的 kebab（烤肉串）—— 每一块肉被 **sticks**（签子）分隔 → 每个单词被 **dashes**（短横线）分隔。

**References:**

- None needed (this is standard programming terminology)
