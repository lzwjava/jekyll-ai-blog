---
audio: false
generated: true
image: false
lang: en
layout: post
title: Angular’s Clean Separation Triad
translated: false
type: note
---

**Angular** uses **components**, **services**, and **HTML templates** because it follows the **separation of concerns** principle very strictly — this makes large applications much easier to maintain, test, scale, and reuse.

Here's a clear breakdown of **why each exists** and **how they relate** to each other (2025–2026 modern Angular style):

| Part          | What it is                              | Main responsibility                              | Why Angular needs it separately                  | Lives in file(s)              |
|---------------|-----------------------------------------|--------------------------------------------------|---------------------------------------------------|-------------------------------|
| **Component** | TypeScript class + decorator            | Controls **behavior** + **orchestrates** the view | UI logic, user events, data flow for that piece of screen | `*.component.ts`             |
| **Template**  | HTML (+ Angular syntax)                 | Defines **what the user sees** (structure + bindings) | Pure presentation / markup                        | `*.component.html`           |
| **Service**   | TypeScript class + `@Injectable()`      | Handles **business logic**, **data**, **HTTP**, shared state, calculations | Reusability + testability + clean components      | `*.service.ts`               |

### Real relationship — how they work together

Think of a **component** as a **smart manager** of a small piece of screen:

```
User sees → Template (HTML)  ←──┐
                                 │  data binding / events
                                 ↓
                         Component (.ts class)
                                 ↑
         Business logic / data ←─┘
                                 │
                           Service(s)
```

**Example: Product List page**

```ts
// product-list.component.ts          ← Component
import { Component } from '@angular/core';
import { ProductService } from './product.service';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css'],
  standalone: true,                    // modern style
  imports: [CommonModule, ProductCardComponent]
})
export class ProductListComponent {
  products$ = this.productService.getProducts();   // ← uses service

  constructor(private productService: ProductService) {}
}
```

```html
<!-- product-list.component.html -->     ← Template (HTML)
<div class="grid">
  @for (product of products$ | async; track product.id) {
    <app-product-card [product]="product" />
  }
  @empty {
    <p>No products found</p>
  }
</div>
```

```ts
// product.service.ts                   ← Service
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ProductService {
  constructor(private http: HttpClient) {}

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>('/api/products');
  }

  addToCart(product: Product) { … }
  calculateDiscount(price: number) { … }
}
```

### Why not put everything inside the component?

| If you do this...                             | Problems you get later                                 |
|-----------------------------------------------|-----------------------------------------------------------------|
| HTTP calls, localStorage, complex logic inside component | Component becomes huge (300–1000+ lines), hard to test |
| Same HTTP / business logic copied in 5 components     | Violates **DRY**, bug in one place → have to fix 5 places     |
| Business logic mixed with presentation logic          | Very hard to unit-test UI vs logic separately                  |
| Can't reuse data-fetching / calculation logic         | You end up with duplicated code everywhere                     |

### Quick summary — the golden rule in modern Angular

- **Template (HTML)** → "What does it **look like**?"
- **Component (.ts)** → "How does it **behave** for this screen? What data do I show? What happens on click?"
- **Service (.ts)** → "How do I **get/transform/share** data? What's the **business rule**?"

**Component owns the template**
**Service is owned by many components** (or the whole app)

This structure is the main reason Angular applications can stay maintainable even when they grow to hundreds of components.

Does this separation make sense now? Want a more concrete example with signals / forms / routing? 😄
