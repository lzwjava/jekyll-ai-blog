---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular ngModel Two Way Binding Guide
translated: false
type: note
---

**Question:** How does Angular's ngModel work?

**Answer:**

`ngModel` is a **directive** from `@angular/forms` that enables **two-way data binding** between an HTML form control (like `<input>`, `<select>`, `<textarea>`) and a property in your Angular component.

It is the key mechanism used in **template-driven forms**.

### Core Purpose of `ngModel`

- Creates and manages a `FormControl` instance automatically (behind the scenes)
- Keeps the **input value** ↔ **component property** in sync
- Provides built-in **validation state** tracking (valid/invalid, touched/dirty, errors…)
- Registers the control with the parent form (if inside `<form>` with `ngForm`)

### Most Common Syntax (Two-way Binding – "Banana in a Box")

```html
<input [(ngModel)]="username" name="username" required>

<!-- Equivalent expanded form -->
<input [ngModel]="username" (ngModelChange)="username = $event" name="username">
```

- `[(ngModel)]` is syntactic sugar
- Left part → property binding (`[ngModel]`)
- Right part → event binding (`(ngModelChange)`)

### How It Works Internally (Simplified Flow)

1. Angular sees `[(ngModel)]="username"`
2. `NgModel` directive is activated on the `<input>`
3. It creates a `FormControl` instance
4. It reads the initial value from the component (`username`) and sets it on the input (model → view)
5. It attaches a **value accessor** (usually `DefaultValueAccessor` for native inputs)
6. When user types → browser dispatches `input` / `change` event
7. `NgModel` catches it → updates `FormControl` value
8. `FormControl` emits value change
9. `NgModel` calls the setter → updates component property (`username`)
10. Change detection runs → view updates if needed

### Important Requirements

You **must** import `FormsModule`:

```ts
// app.module.ts or standalone imports
import { FormsModule } from '@angular/forms';

@NgModule({
  imports: [
    FormsModule,
    // ...
  ]
})
```

or in standalone component:

```ts
@Component({
  standalone: true,
  imports: [FormsModule],
  // ...
})
```

### One-way Binding Variations

```html
<!-- Only model → view -->
<input [ngModel]="username">

<!-- Only view → model (rarely used alone) -->
<input (ngModelChange)="username = $event">
```

### Template-driven Form Example

```html
<form #f="ngForm" (ngSubmit)="onSubmit(f.value)">
  <input 
    type="email"
    name="email"
    [(ngModel)]="user.email"
    required
    email
    #emailCtrl="ngModel">

  <div *ngIf="emailCtrl.invalid && emailCtrl.touched">
    Please enter a valid email
  </div>

  <button type="submit" [disabled]="f.invalid">Sign Up</button>
</form>
```

### Modern Alternatives (Angular 17+)

- **Signal inputs + `model()`** (preferred in many new components)

```ts
email = model<string>('');           // two-way
emailInput = model<string | null>(); // nullable two-way
```

```html
<input [model]="emailInput()" />
```

- **Reactive Forms** (`FormControl`, `FormGroup`) — usually recommended for complex forms

### Quick Summary Table

| Syntax                     | Direction          | Use Case                              |
|----------------------------|--------------------|---------------------------------------|
| `[(ngModel)]="prop"`       | Two-way            | Classic template-driven forms         |
| `[ngModel]="prop"`         | Model → View       | Display-only or one-way               |
| `(ngModelChange)="…"`      | View → Model       | Custom handling on change             |
| `model()` + signal         | Two-way (modern)   | Signal-based components (17+)         |
| `formControlName`          | —                  | Reactive forms (no `ngModel`)         |

`ngModel` is still widely used, especially in simpler forms and legacy code, but many new Angular applications lean toward **reactive forms** or **signal + model()** for better type safety and testability.

**References:**

- [NgModel - Official Angular Documentation](https://angular.dev/api/forms/NgModel)
- [Two-way binding syntax explanation](https://angular.dev/guide/templates/two-way-binding)
- [Template-driven forms guide](https://angular.dev/guide/forms)