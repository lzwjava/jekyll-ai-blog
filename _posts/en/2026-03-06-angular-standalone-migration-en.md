---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular Standalone Migration Guide
translated: false
type: note
---

Question: How do you migrate an NgModule-based Angular application to standalone components?

Answer:

## Overview

There are two approaches: **automatic migration** using Angular's built-in schematic (recommended), and **manual migration** for doing it component by component. Both are covered below.

---

## Approach 1: Automatic Migration (Recommended)

The migration process is composed of three steps. You must run it multiple times and check manually that the project builds and behaves as expected after each step.

### Prerequisites

Your project must:

- Be on **Angular 15.2.0 or later**
- Build without any compilation errors
- Be on a **clean Git branch** with all work saved

### Step 1 — Convert all components, directives, and pipes to standalone

```bash
ng g @angular/core:standalone
# Select: "Convert all components, directives and pipes to standalone"
```

This automatically adds `standalone: true` to every component, directive, and pipe, and moves their dependencies into the `imports` array.

**Before:**

```typescript
@Component({
  selector: 'app-example',
  templateUrl: './example.component.html',
  styleUrls: ['./example.component.css']
})
export class ExampleComponent {}
```

**After:**

```typescript
@Component({
  selector: 'app-example',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './example.component.html',
  styleUrls: ['./example.component.css']
})
export class ExampleComponent {}
```

✅ Verify the app still builds and runs, then commit.

---

### Step 2 — Remove unnecessary NgModule classes

```bash
ng g @angular/core:standalone
# Select: "Remove unnecessary NgModule classes"
```

This removes NgModule instances, marks components as standalone, and moves now-standalone components to direct imports of other standalone components where they are used.

> ⚠️ Note: Certain modules, particularly `SharedModule`s, may persist after the schematic execution because the schematic cannot tell if it is safe to remove them. You may need to remove those manually.

✅ Verify the app still builds and runs, then commit.

---

### Step 3 — Bootstrap using standalone APIs

```bash
ng g @angular/core:standalone
# Select: "Bootstrap the project using standalone APIs"
```

This step converts any usages of `bootstrapModule` to the new standalone-based `bootstrapApplication`. It also removes `standalone: false` from the root component and deletes the root NgModule. If the root module has any providers or imports, the migration attempts to copy as much of this configuration as possible into the new bootstrap call.

Your `main.ts` will change from:

```typescript
// OLD — NgModule bootstrap
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

platformBrowserDynamic().bootstrapModule(AppModule);
```

To:

```typescript
// NEW — Standalone bootstrap
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';

bootstrapApplication(AppComponent, appConfig);
```

✅ Verify the app, run lint + format checks, then commit.

---

## Approach 2: Manual Migration (Step-by-Step)

If you prefer to migrate incrementally, here is how to do it manually for each component:

### 1. Add `standalone: true` and move imports to the component

```typescript
// BEFORE — component declared in a module
@Component({
  selector: 'app-user',
  templateUrl: './user.component.html'
})
export class UserComponent {}

// user.module.ts
@NgModule({
  declarations: [UserComponent],
  imports: [CommonModule, FormsModule]
})
export class UserModule {}
```

```typescript
// AFTER — standalone component
@Component({
  selector: 'app-user',
  standalone: true,
  imports: [CommonModule, FormsModule],  // moved here
  templateUrl: './user.component.html'
})
export class UserComponent {}
```

### 2. Fix service injection

Use the `providedIn: 'root'` option in services to ensure they're available globally. For feature-specific services, provide them at the component level using the `providers` array.

```typescript
@Injectable({
  providedIn: 'root'  // globally available, no module needed
})
export class UserService {
  getData() { return 'data'; }
}
```

### 3. Fix lazy loading — use `loadComponent` instead of `loadChildren`

```typescript
// OLD — lazy loaded module
{
  path: 'shop',
  loadChildren: () => import('./shop/shop.module').then(m => m.ShopModule)
}

// NEW — lazy loaded standalone component
{
  path: 'shop',
  loadComponent: () => import('./shop/shop.component').then(m => m.ShopComponent)
}
```

### 4. Replace `RouterModule.forRoot()` and `HttpClientModule` in `app.config.ts`

```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient()
  ]
};
```

---

## Summary of Key Changes

| Old NgModule Way | New Standalone Way |
|---|---|
| `declarations: [XComponent]` in module | `standalone: true` in component |
| `imports: [X]` in module | `imports: [X]` in component |
| `bootstrapModule(AppModule)` | `bootstrapApplication(AppComponent, appConfig)` |
| `RouterModule.forRoot(routes)` | `provideRouter(routes)` |
| `HttpClientModule` | `provideHttpClient()` |
| `loadChildren` for lazy loading | `loadComponent` for lazy loading |

---

## After Migration — Optional Enforcement

Consider adding the `strictStandalone` option in `tsconfig.json` to enforce authoring only standalone components in the future.

```json
// tsconfig.json
{
  "angularCompilerOptions": {
    "strictStandalone": true
  }
}
```

---

References:

- [Angular Official Docs — Migrate to Standalone](https://angular.dev/reference/migrations/standalone)
- [Migrating a Large Angular App to Standalone — AngularSpace](https://www.angularspace.com/migrating-a-large-angular-application-to-standalone/)
- [Migrating a Modular Angular App to Standalone — Medium](https://medium.com/@sehban.alam/migrating-a-modular-angular-app-to-standalone-components-a-comprehensive-guide-4cbed7482731)
- [Angular Standalone Migration Schematic README — GitHub](https://github.com/angular/angular/blob/main/packages/core/schematics/ng-generate/standalone-migration/README.md)
