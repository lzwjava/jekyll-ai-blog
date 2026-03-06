---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular Components Modules Standalone Explained
translated: false
type: note
---

**Question:** In Angular 21, what are Components and Modules, and what does "standalone" mean?

---

**Answer:**

## 1. What is a Component in Angular?

A **Component** is the fundamental building block of an Angular application. It controls a portion of the UI (a "view") and consists of three parts:

- **TypeScript class** — contains the logic and data
- **HTML template** — defines what is rendered
- **CSS styles** — defines how it looks

Every Angular app is a tree of components. You define one with the `@Component` decorator:

```typescript
@Component({
  selector: 'app-hello',
  template: `<h1>Hello World</h1>`,
  standalone: true
})
export class HelloComponent {}
```

---

## 2. What is a Module (NgModule) in Angular?

A **Module** (`NgModule`) was the traditional way to group and organize related components, directives, pipes, and services. Before standalone components existed, **every component had to be declared inside an NgModule** before it could be used.

```typescript
// OLD way — NgModule-based
@NgModule({
  declarations: [UserComponent],
  imports: [CommonModule],
  exports: [UserComponent]
})
export class UserModule {}
```

The concept of a module in Angular seemed unnecessary and made it a bit harder for beginners to learn Angular from scratch — it was one extra concept to learn, and it was not clear why it was needed.

---

## 3. What Does "Standalone" Mean?

Standalone components are self-contained Angular components that do not require an NgModule to function. Before this feature, every component had to be declared inside an NgModule, which added complexity and dependencies.

With a standalone component, you declare your dependencies **directly inside the component itself** using the `imports` array:

```typescript
// Angular 21 way — Standalone
@Component({
  selector: 'app-user',
  standalone: true,           // <-- this makes it standalone
  imports: [CommonModule],    // <-- dependencies go here
  template: `<h2>User Works!</h2>`
})
export class UserComponent {}
```

---

## 4. Timeline: How Standalone Became the Default

| Angular Version | What Changed |
|---|---|
| v14 | Standalone introduced as developer preview |
| v15–v18 | Standalone stabilized, recommended by Angular team |
| **v19** | Starting from Angular v19, components, directives, and pipes are **standalone by default**. |
| **v21** | Angular 21 focuses on **standalone-first architecture**, simplification, performance, and modern reactive patterns. |

---

## 5. In Angular 21: Do You Still Write `standalone: true`?

By default, Angular components are standalone, meaning that you can directly add them to the `imports` array of other components. Components created with an earlier version of Angular may instead specify `standalone: false` in their `@Component` decorator.

So in Angular 21:
- You **no longer need to write** `standalone: true` — it is the default
- You only write `standalone: false` if you want the old NgModule behavior
- NgModules are **not deprecated**, but they are no longer recommended for new code

---

## 6. Benefits of Standalone (vs NgModule)

Standalone components have revolutionized development workflows by eliminating NgModule boilerplate, enabling clearer dependency management, improving performance through better tree-shaking, simplifying project structure, and enhancing modularity, reusability, and testability.

In summary:

| Feature | NgModule (Old) | Standalone (Angular 21) |
|---|---|---|
| Declare component | Must be in NgModule | Not required |
| Import dependencies | In the module | Directly in the component |
| Lazy loading | Module-level | Component-level (simpler) |
| Boilerplate | High | Minimal |
| Testing | Module setup needed | Simpler, no module needed |

---

## References

- [Angular Official Docs — Standalone Components](https://angular.dev/reference/migrations/standalone)
- [Angular Official Docs — Anatomy of Components](https://angular.dev/guide/components)
- [Angular Blog — The Future is Standalone](https://blog.angular.dev/the-future-is-standalone-475d7edbc706)
- [Angular 21 — What's New, What's Changed](https://dev.to/mridudixit15/angular-21-whats-new-whats-changed-3fl3)
- [GeeksforGeeks — Standalone Components in Angular](https://www.geeksforgeeks.org/angular-js/standalone-components-in-angular/)