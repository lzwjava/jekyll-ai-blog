---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 的干净分离三元组
translated: true
type: note
---

**Angular** 使用 **components**、**services** 和 **HTML templates**，因为它严格遵循 **separation of concerns** 原则——这使得大型应用更容易维护、测试、扩展和复用。

以下是 **每个部分存在的原因** 以及 **它们之间如何关联** 的清晰分解（2025–2026 现代 Angular 风格）：

| Part          | What it is                              | Main responsibility                              | Why Angular needs it separately                  | Lives in file(s)              |
|---------------|-----------------------------------------|--------------------------------------------------|---------------------------------------------------|-------------------------------|
| **Component** | TypeScript class + decorator            | 控制 **behavior** + **orchestrates** 视图        | UI 逻辑、用户事件、屏幕该部分的数据流             | `*.component.ts`             |
| **Template**  | HTML (+ Angular syntax)                 | 定义 **用户看到的内容**（结构 + bindings）       | 纯展示 / 标记语言                                 | `*.component.html`           |
| **Service**   | TypeScript class + `@Injectable()`      | 处理 **business logic**、**data**、**HTTP**、共享状态、计算 | 可复用性 + 可测试性 + 干净的 components           | `*.service.ts`               |

### 真实关系——它们如何协同工作

将 **component** 视为屏幕一小块的 **智能经理**：

```
用户看到 → Template (HTML)  ←──┐
                                 │  data binding / events
                                 ↓
                         Component (.ts class)
                                 ↑
         Business logic / data ←─┘
                                 │
                           Service(s)
```

**示例：Product List 页面**

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

### 为什么不把所有内容都放在 component 里面？

| If you do this...                             | Problems you get later                                 |
|-----------------------------------------------|-----------------------------------------------------------------|
| HTTP 调用、localStorage、复杂逻辑放在 component 内部 | Component 变得巨大（300–1000+ 行），难以测试                  |
| 相同的 HTTP / business logic 复制到 5 个 components 中 | 违反 **DRY**，一处 bug → 需要修复 5 处                        |
| Business logic 与 presentation logic 混合            | 很难单独 unit-test UI 与逻辑                                  |
| 无法复用数据获取 / 计算逻辑                           | 最终到处都是重复代码                                          |

### 快速总结——现代 Angular 的黄金法则

- **Template (HTML)** → “它 **看起来** 怎么样？”
- **Component (.ts)** → “这个屏幕 **如何行为**？显示什么数据？点击时发生什么？”
- **Service (.ts)** → “如何 **获取/转换/共享** 数据？**business rule** 是什么？”

**Component 拥有 template**  
**Service 被多个 components 拥有**（或整个应用）

这种结构是 Angular 应用即使增长到数百个 components 仍能保持可维护性的主要原因。

这种分离现在有意义了吗？想要一个更具体的 signals / forms / routing 示例吗？😄