---
audio: false
generated: true
image: false
lang: en
layout: post
title: Styling Select Options in Angular 21
translated: false
type: note
---

In Angular 21 (and modern Angular generally), while `ngClass` is still available, the framework has shifted toward **native class bindings** for better performance and type safety.

Since a standard HTML `<select>` only allows styling on the `<option>` elements (and even then, with limited CSS support depending on the browser), the best way to handle this is by binding classes directly to each option during your loop.

### Option 1: Using Modern Class Bindings (Recommended)
Instead of the older `[ngClass]`, you can use the `@for` control flow and direct `[class]` bindings. This is cleaner and faster in Angular 21.

{% raw %}
```html
<select>
  @for (item of options; track item.id) {
    <option [value]="item.value" [class]="item.categoryClass">
      {{ item.label }}
    </option>
  }
</select>
```
{% endraw %}

### Option 2: Using `[ngClass]` for Complex Logic
If you need to apply multiple classes based on a condition (e.g., "apply `high-priority` only if the status is 'urgent'"), `[ngClass]` is still very useful.

{% raw %}
```html
<select>
  @for (opt of dropdownOptions; track opt.id) {
    <option 
      [value]="opt.id"
      [ngClass]="{
        'text-red': opt.isUrgent,
        'bg-blue': opt.type === 'primary',
        'custom-padding': true
      }">
      {{ opt.name }}
    </option>
  }
</select>
```
{% endraw %}

### Pro-Tip: The "Dropdown Limitation"
Standard HTML `<select>` and `<option>` elements are notorious for being difficult to style (you often can't change much beyond colors and fonts).

If you need "better control" (like adding icons, custom spacing, or complex layouts inside the dropdown), consider using **Angular Aria** (new in v21) or the **CDK Listbox**. These provide "headless" logic, allowing you to build a dropdown that looks like a `div` but behaves like a `select`.

---

### Comparison of Approaches

| Feature | `[class.name]` | `[class]` (String/Array) | `[ngClass]` |
| :--- | :--- | :--- | :--- |
| **Best for** | Toggling one specific class | Replacing the whole class list | Complex conditional logic |
| **Performance** | Highest | High | Medium |
| **Angular 21 Status** | Preferred | Preferred | Supported (Legacy/Complex) |

Would you like me to show you how to implement this using the new **Angular Aria Listbox** for full CSS control?