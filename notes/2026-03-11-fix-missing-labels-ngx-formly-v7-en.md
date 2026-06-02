---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Missing Labels in ngx-formly v7
translated: false
type: note
---

Question: After upgrading from Angular 14 to Angular 21 and ngx-formly from v5/v6 to v7, why do form labels disappear, and how do you fix it — especially in custom wrappers that read `field.templateOptions.label`?

Answer:

## Root Cause: `templateOptions` → `props` Rename in ngx-formly v6+

This is one of the most common breaking changes people hit when upgrading ngx-formly. Starting from **ngx-formly v6**, `templateOptions` was **deprecated** in favor of `props`. In v7 (which requires Angular ≥ 18), your old code using `templateOptions` may still partially work at the field config level due to a backward-compat alias, but **custom wrappers and custom field types that directly reference `field.templateOptions.label` will silently fail** — the label simply won't render.

`templateOptions` is an alias to `props`, which allows passing extra options to the field UI template. The modern way to pass a label is via `props: { label: 'Name', required: true }`.

---

## The 3 Places You Need to Fix

### 1. Field Configuration (your component `.ts` file)

**Before (Angular 14 / formly v5):**

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

**After (Angular 21 / formly v7):**

```ts
fields: FormlyFieldConfig[] = [
  {
    key: 'firstName',
    type: 'input',
    props: {          // ← rename templateOptions to props
      label: 'First Name',
      placeholder: 'Enter name',
      required: true,
    }
  }
];
```

---

### 2. Custom Wrapper Templates (the primary reason labels disappear)

If you wrote a custom wrapper, the template likely reads `field.templateOptions?.label` or just `to.label` (the old shorthand). You must update it to use `props`.

**Before:**
{% raw %}

```html
<!-- my-label-wrapper.component.html -->
<label>{{ to.label }}</label>           <!-- old shorthand for templateOptions -->
<label>{{ field.templateOptions?.label }}</label>
<ng-container #fieldComponent></ng-container>
```

{% endraw %}

**After:**
{% raw %}

```html
<!-- my-label-wrapper.component.html -->
<label>{{ props.label }}</label>        <!-- use props directly -->
<ng-container #fieldComponent></ng-container>
```

{% endraw %}

The modern custom wrapper pattern exposes `props.label` directly in the template, like: `<h3 class="card-header">{{ props.label }}</h3>`.

---

### 3. Custom Field Type Components

**Before:**
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

**After:**
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
//                                             ^^^^^^^^^^^^^^^ also add generic
```

{% endraw %}

---

### 4. `expressionProperties` that reference `templateOptions.*`

**Before:**

```ts
expressionProperties: {
  'templateOptions.label': '"Dynamic " + model.name',
  'templateOptions.disabled': 'model.isReadOnly',
}
```

**After:**

```ts
expressions: {
  'props.label': '"Dynamic " + model.name',
  'props.disabled': 'model.isReadOnly',
}
```

---

## Quick Checklist for Migration

| Old (v5/v6 Angular 14) | New (v7 Angular 21) |
|---|---|
| `templateOptions: { label: 'X' }` | `props: { label: 'X' }` |
| `to.label` in wrapper/type template | `props.label` |
| `field.templateOptions?.label` | `field.props?.label` |
| `expressionProperties: { 'templateOptions.label': ... }` | `expressions: { 'props.label': ... }` |
| `FieldType` (no generic) | `FieldType<FieldTypeConfig>` |
| `_markForCheck`, `_buildForm` | `detectChanges`, `build` |

---

## Why `templateOptions` Still Exists but Labels Still Break

Even though `templateOptions` is an alias for `props` at the data layer, **custom wrapper templates are not automatically updated**. If your wrapper HTML still says `{{ to.label }}` or `{{ field.templateOptions?.label }}`, Angular's template engine simply finds nothing because:

- The `to` shorthand accessor may be removed or behave differently in v7
- The internal binding path your template walks is now `field.props`, not `field.templateOptions`

The field config's `props: { label: '...' }` is correctly set — the label data exists — but the **template can't read it** using the old path, so nothing renders.

---

## Summary

The fix is a **find-and-replace** across your project:

```bash
# In TypeScript files:
templateOptions: {  →  props: {
field.templateOptions  →  field.props
'templateOptions.  →  'props.

# In HTML template files:
to.label  →  props.label
to.placeholder  →  props.placeholder
to.required  →  props.required
(and all other to.* references)
```

References:

- [ngx-formly Migration from v6 to v7](https://formly.dev/docs/guide/migration)
- [ngx-formly FAQ — props vs templateOptions](https://formly.dev/docs/guide/faq/)
- [ngx-formly Custom Wrapper Guide](https://formly.dev/docs/guide/custom-formly-wrapper/)
