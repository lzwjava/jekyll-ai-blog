---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Angular Standalone Components Explained
translated: false
type: note
---

**Question: How to understand standalone components in Angular?**

**Answer:**

Standalone components are one of the most important changes in modern Angular (introduced in Angular 14 as developer preview, became production-ready in Angular 15, and became the recommended default way of writing components starting with Angular 16+).

### What “Standalone” Actually Means

A **standalone component** is a component that:

- Does **not** belong to any NgModule
- Declares its own **dependencies** directly (other components, directives, pipes, services…)
- Can be used **directly** in routing, in another component’s template, or as an entry point

In short: it removes the need for the classic NgModule boilerplate in most cases.

### Classic (NgModule-based) way – before standalone

```ts
// classic.component.ts
@Component({
  selector: 'app-classic',
  template: `<h1>Hello</h1>`,
  standalone: false   // ← default / not needed
})
export class ClassicComponent {}

// You MUST declare it inside a module
@NgModule({
  declarations: [ClassicComponent],
  imports: [CommonModule, FormsModule],
  exports: [ClassicComponent]
})
export class SomeModule {}
```

### Standalone way – modern Angular (2023–2026 style)

```ts
// modern.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { HighlightDirective } from './highlight.directive';

@Component({
  selector: 'app-modern',
  standalone: true,                           // ← this is the key line
  imports: [                                  // ← list everything this component needs
    CommonModule,
    FormsModule,
    MatButtonModule,
    HighlightDirective,                       // ← can import other standalone components/directives
    // You can also import whole NgModules if needed (transition period)
  ],
  template: `
    <h1>Hello from standalone!</h1>
    <input type="text" [(ngModel)]="name">
    <button mat-button>Click</button>
  `
})
export class ModernComponent {
  name = 'Angular';
}
```

### How Standalone Components Are Used (no NgModule needed)

1. **In the router** (most common use-case today)

```ts
const routes: Routes = [
  { path: 'home', component: HomeComponent },           // ← standalone component
  { path: 'profile', component: ProfileComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' }
];
```

2. **Inside another component’s template**

```html
<!-- parent.component.html -->
<app-modern></app-modern>
<app-user-card [user]="currentUser"></app-user-card>
```

3. **As the root component** (bootstrapApplication)

```ts
// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { AppComponent } from './app.component';
import { routes } from './app.routes';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes)
  ]
});
```

### Quick Comparison Table – NgModule vs Standalone

| Aspect                     | NgModule-based (classic)               | Standalone (modern)                          |
|----------------------------|----------------------------------------|----------------------------------------------|
| Needs an NgModule?         | Yes, always                            | No                                           |
| Where do you list imports? | In the NgModule                        | Directly in `@Component({ imports: […] })`  |
| Reusability                | Need to export from module             | Can be imported directly anywhere            |
| Boilerplate                | High (module + declarations + exports) | Very low                                     |
| Tree-shaking               | Worse                                  | Better (especially with lazy-loading)        |
| Learning curve (new devs)  | Steep because of modules               | Much easier – feels like React/Vue/Solid     |
| Recommended in 2025–2026?  | Only for legacy or very large monorepos| Yes – default for new projects               |

### Mental Model – Think of Standalone Like This

> A standalone component is like a small, self-contained mini-application:
>
> - It says “I need these pieces to work”
> - Angular’s compiler bundles exactly those pieces
> - No central “module registry” anymore

It’s very close to how components work in React, Vue, Svelte, etc.

### Best Way to Start Understanding in Practice (2026)

1. Create a new project with standalone (default since Angular 17):

```bash
ng new my-app --standalone
```

2. Generate components as standalone (default behavior now):

```bash
ng g component user-card    # → creates standalone: true automatically
```

3. Look at the generated code → you will almost never see `declarations: []` or NgModules anymore.

That’s the quickest way to “feel” what standalone means.

Standalone is not just a syntax — it’s Angular’s shift to a simpler, more modern component model that removes most of the module ceremony while keeping all the powerful features (dependency injection, lazy-loading, etc.).

**References:**

- <https://angular.dev/guide/standalone-components>
- <https://blog.angular.dev/introducing-standalone-components-58a418173aa3>
- <https://blog.angular.dev/angular-v17-is-now-available-8c4c0d8d3169>
- <https://angular.love/standalone-components-in-angular>
