---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix NgBootstrap 20 Pagination Imports
translated: false
type: note
---

**Question:** How to fix the ng-bootstrap 20 issue "cannot find module '@ng-bootstrap/ng-bootstrap/pagination' or its corresponding type declarations" when using it together with Angular 21?

**Answer:**

This error usually appears because **ng-bootstrap v20** introduced **component entry points** (a new way to import individual components), and many codebases still use the old import style or mix both approaches incorrectly.

In **ng-bootstrap v19 and earlier**, people commonly imported like this:

```ts
import { NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';
```

Or directly:

```ts
import { NgbPagination } from '@ng-bootstrap/ng-bootstrap';
```

Starting with **ng-bootstrap v20** (which supports Angular 21), the library added **secondary entry points** for better tree-shaking and faster builds. The correct modern import style for standalone components (recommended in Angular 17+) is:

```ts
import { NgbPagination } from '@ng-bootstrap/ng-bootstrap/pagination';
```

### How to fix it

1. **Change your imports** for pagination-related components:

   Replace:

   ```ts
   import { NgbPagination } from '@ng-bootstrap/ng-bootstrap';
   // or
   import { NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';
   ```

   With:

   ```ts
   import {
     NgbPagination,
     NgbPaginationEllipsis,
     NgbPaginationFirst,
     NgbPaginationLast,
     NgbPaginationNext,
     NgbPaginationNumber,
     NgbPaginationPrevious,
     NgbPaginationPages
   } from '@ng-bootstrap/ng-bootstrap/pagination';
   ```

2. **Update your component / standalone imports array** (most common case in Angular 17+):

   ```ts
   @Component({
     standalone: true,
     imports: [
       NgbPagination,           // ← add only what you actually use
       // NgbPaginationFirst,
       // NgbPaginationNext,
       // etc.
     ],
     template: `
       <ngb-pagination
         [collectionSize]="totalItems"
         [(page)]="currentPage"
         [pageSize]="pageSize">
       </ngb-pagination>
     `
   })
   export class PaginationExampleComponent {
     // ...
   }
   ```

3. **If you still use NgModule-based architecture** (less common in 2025–2026):

   You can continue importing the full module:

   ```ts
   import { NgbPaginationModule } from '@ng-bootstrap/ng-bootstrap';
   ```

   ```ts
   @NgModule({
     imports: [NgbPaginationModule, /* ... */],
     // ...
   })
   export class FeatureModule {}
   ```

   But the **preferred** way is now standalone + secondary entry points.

### Quick compatibility check

- `@ng-bootstrap/ng-bootstrap@20.x` → designed for **Angular ^21.0.0**
- Make sure your `package.json` has:

  ```json
  "@ng-bootstrap/ng-bootstrap": "^20.0.0",
  "@angular/core": "^21.0.0"
  ```

- Run `npm install` or `pnpm install` again after changing versions/imports.

### Summary – most likely fixes (pick one)

- Old code using `from '@ng-bootstrap/ng-bootstrap'` → change to `from '@ng-bootstrap/ng-bootstrap/pagination'`
- Using full `NgbModule` import → replace with individual standalone imports (best practice)
- Typo in path or mixing both styles → normalize to secondary entry points

After applying the correct import path, clean the cache (`npm cache clean --force`), delete `node_modules`, and reinstall dependencies if the error persists.

**References:**

- [https://ng-bootstrap.github.io/#/getting-started](https://ng-bootstrap.github.io/#/getting-started)
- [https://github.com/ng-bootstrap/ng-bootstrap/releases](https://github.com/ng-bootstrap/ng-bootstrap/releases)
- [https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md](https://github.com/ng-bootstrap/ng-bootstrap/blob/master/CHANGELOG.md)
- [https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap](https://www.npmjs.com/package/@ng-bootstrap/ng-bootstrap)
