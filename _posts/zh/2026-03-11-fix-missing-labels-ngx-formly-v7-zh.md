---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 ngx-formly v7 中的缺失标签
translated: true
type: note
---

问题：从 Angular 14 升级到 Angular 21，并将 ngx-formly 从 v5/v6 升级到 v7 后，为什么表单标签消失了，以及如何修复它——特别是在读取 `field.templateOptions.label` 的自定义包装器中？

回答：

## 根本原因：ngx-formly v6+ 中的 `templateOptions` → `props` 重命名

这是升级 ngx-formly 时人们最常遇到的破坏性变更之一。从 **ngx-formly v6** 开始，`templateOptions` 被 **弃用**，改为使用 `props`。在 v7（要求 Angular ≥ 18）中，您旧代码在字段配置层面使用 `templateOptions` 可能由于向后兼容别名而部分工作，但 **直接引用 `field.templateOptions.label` 的自定义包装器和自定义字段类型会静默失败**——标签根本不会渲染。

`templateOptions` 是 `props` 的别名，用于向字段 UI 模板传递额外选项。现代传递标签的方式是 `props: { label: 'Name', required: true }`。

---

## 需要修复的 3 个地方

### 1. 字段配置（您的组件 `.ts` 文件）

**之前（Angular 14 / formly v5）：**

```ts
fields: FormlyFieldConfig[] = [
  {
    key: 'firstName',
    type: 'input',
    templateOptions: {
      label: 'First Name',
      placeholder: 'Enter name',
      required: true,
    }
  }
];
```

**之后（Angular 21 / formly v7）：**

```ts
fields: FormlyFieldConfig[] = [
  {
    key: 'firstName',
    type: 'input',
    props: {          // ← 将 templateOptions 重命名为 props
      label: 'First Name',
      placeholder: 'Enter name',
      required: true,
    }
  }
];
```

---

### 2. 自定义包装器模板（标签消失的主要原因）

如果您编写了自定义包装器，模板很可能读取 `field.templateOptions?.label` 或仅 `to.label`（旧简写）。您必须更新为使用 `props`。

**之前：**
{% raw %}

```html
<!-- my-label-wrapper.component.html -->
<label>{{ to.label }}</label>           <!-- templateOptions 的旧简写 -->
<label>{{ field.templateOptions?.label }}</label>
<ng-container #fieldComponent></ng-container>
```

{% endraw %}

**之后：**
{% raw %}

```html
<!-- my-label-wrapper.component.html -->
<label>{{ props.label }}</label>        <!-- 直接使用 props -->
<ng-container #fieldComponent></ng-container>
```

{% endraw %}

现代自定义包装器模式在模板中直接暴露 `props.label`，例如：`<h3 class="card-header">{{ props.label }}</h3>`。

---

### 3. 自定义字段类型组件

**之前：**
{% raw %}

```ts
@Component({
  template: `
    <label>{{ to.label }}</label>
    <input [formControl]="formControl" [formlyAttributes]="field">
  `
})
export class CustomInputType extends FieldType {}
```

{% endraw %}

**之后：**
{% raw %}

```ts
import { FieldType, FieldTypeConfig } from '@ngx-formly/core';

@Component({
  template: `
    <label>{{ props.label }}</label>
    <input [formControl]="formControl" [formlyAttributes]="field">
  `
})
export class CustomInputType extends FieldType<FieldTypeConfig> {}
//                                             ^^^^^^^^^^^^^^^ 同时添加泛型
```

{% endraw %}

---

### 4. 引用 `templateOptions.*` 的 `expressionProperties`

**之前：**

```ts
expressionProperties: {
  'templateOptions.label': '"Dynamic " + model.name',
  'templateOptions.disabled': 'model.isReadOnly',
}
```

**之后：**

```ts
expressions: {
  'props.label': '"Dynamic " + model.name',
  'props.disabled': 'model.isReadOnly',
}
```

---

## 迁移快速检查清单

| 旧版 (v5/v6 Angular 14) | 新版 (v7 Angular 21) |
|---|---|
| `templateOptions: { label: 'X' }` | `props: { label: 'X' }` |
| 包装器/类型模板中的 `to.label` | `props.label` |
| `field.templateOptions?.label` | `field.props?.label` |
| `expressionProperties: { 'templateOptions.label': ... }` | `expressions: { 'props.label': ... }` |
| `FieldType` (无泛型) | `FieldType<FieldTypeConfig>` |
| `_markForCheck`, `_buildForm` | `detectChanges`, `build` |

---

## 为什么 `templateOptions` 仍然存在但标签仍会丢失

尽管在数据层面 `templateOptions` 是 `props` 的别名，但 **自定义包装器模板不会自动更新**。如果您的包装器 HTML 仍为 `{{ to.label }}` 或 `{{ field.templateOptions?.label }}`，Angular 的模板引擎只会找到空值，因为：

- `to` 简写访问器在 v7 中可能已被移除或行为不同
- 模板遍历的内部绑定路径现在是 `field.props`，而非 `field.templateOptions`

字段配置的 `props: { label: '...' }` 已正确设置——标签数据存在——但 **模板无法使用旧路径读取它**，因此无内容渲染。

---

## 总结

修复方法是在整个项目中进行 **查找并替换**：

```bash
# 在 TypeScript 文件中：
templateOptions: {  →  props: {
field.templateOptions  →  field.props
'templateOptions.  →  'props.

# 在 HTML 模板文件中：
to.label  →  props.label
to.placeholder  →  props.placeholder
to.required  →  props.required
（以及所有其他 to.* 引用）
```

参考资料：

- [ngx-formly Migration from v6 to v7](https://formly.dev/docs/guide/migration)
- [ngx-formly FAQ — props vs templateOptions](https://formly.dev/docs/guide/faq/)
- [ngx-formly Custom Wrapper Guide](https://formly.dev/docs/guide/custom-formly-wrapper/)
