---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular Service and Component Placement Guide
translated: false
type: note
---

Question: In Angular (latest/v21), if a component has `standalone: false`, where should its related service be declared — in `imports`, `declarations`, or both?

Answer:

This is a question about two **different, separate concerns** in Angular's NgModule system. You need to clearly distinguish between:

1. **The component itself** (with `standalone: false`)
2. **The service used by the component**

These two things go into **completely different arrays** in `@NgModule`.

---

## Rule Summary

| Thing to register | Where it goes in `@NgModule` |
|---|---|
| A component / directive / pipe with `standalone: false` | `declarations` |
| A service (or any provider) | `providers` |
| A standalone component / NgModule / pipe you want to use in templates | `imports` |

---

## Detailed Explanation

### 1. Component with `standalone: false` → goes into `declarations`

The `declarations` property of `@NgModule` metadata declares the components, directives, and pipes that belong to the NgModule. A component must be marked with `standalone: false` so that it can be declared in an NgModule.

```typescript
@Component({
  selector: 'my-comp',
  standalone: false,
  template: `...`
})
export class MyComponent {}

@NgModule({
  declarations: [MyComponent], // ✅ component goes HERE
})
export class MyModule {}
```

---

### 2. Service → goes into `providers` (NOT `imports` or `declarations`)

When a component or service requests a dependency, Angular's dependency injection system looks for a provider that can provide that dependency. Services are registered in the `providers` array of `@NgModule`.

```typescript
@NgModule({
  declarations: [MyComponent],
  providers: [MyService], // ✅ service goes HERE
})
export class MyModule {}
```

---

### 3. Best Practice: Use `providedIn: 'root'` on the service itself

The most recommended approach in modern Angular is to avoid putting the service in any module's `providers` array at all. Instead, decorate the service with `providedIn: 'root'`:

```typescript
@Injectable({
  providedIn: 'root' // ✅ automatically available everywhere
})
export class MyService {}
```

Using `providedIn: 'root'` in the `@Injectable` decorator handles most common use cases and makes the service globally available without needing to manually add it to any `providers` array.

---

### 4. What does `imports` do then?

`imports` in `@NgModule` is **only for bringing in other NgModules or standalone components/directives/pipes** so their exported declarations become available in your templates.

```typescript
@NgModule({
  imports: [CommonModule, RouterModule], // ✅ other modules / standalone components
  declarations: [MyComponent],          // ✅ non-standalone components/pipes/directives
  providers: [MyService],               // ✅ services / providers
})
export class MyModule {}
```

---

### Complete Example

{% raw %}

```typescript
// my.service.ts
@Injectable({ providedIn: 'root' })
export class MyService {}

// my.component.ts
@Component({
  selector: 'my-comp',
  standalone: false,
  template: `<p>{{ data }}</p>`
})
export class MyComponent {
  constructor(private svc: MyService) {} // injected via DI
}

// my.module.ts
@NgModule({
  declarations: [MyComponent], // component declared here
  imports: [CommonModule],     // other modules imported here
  // MyService does NOT need to be here because providedIn: 'root' is used
})
export class MyModule {}
```

{% endraw %}

---

### Final Answer

- **`declarations`** → for the `standalone: false` component itself
- **`providers`** → for any service if you need module-scoped injection
- **`imports`** → for other NgModules or standalone pieces used in templates
- **Never put a service in `declarations` or `imports`** — that will cause an error

References:

- [https://angular.dev/guide/ngmodules/overview](https://angular.dev/guide/ngmodules/overview)
- [https://angular.dev/guide/di/defining-dependency-providers](https://angular.dev/guide/di/defining-dependency-providers)
- [https://angular.dev/guide/components](https://angular.dev/guide/components)
