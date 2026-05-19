---
audio: false
generated: true
lang: zh
layout: post
title: Angular 中的路由设计
translated: true
type: note
---

好的，我们来分解如何在 Angular 中设计路由，以实现轻松刷新、支持子路由和处理查询参数。

**1. 轻松刷新并停留在同一页面**

Angular 的默认路由机制旨在无缝处理此问题。当你导航到 Angular 应用程序中的特定路由时，浏览器的 URL 会发生变化。此 URL 代表应用程序的当前状态。当你刷新页面时，浏览器会向服务器请求与该 URL 关联的资源。然后，Angular 的路由模块接管并渲染与该路由关联的组件。

**关键点：**

*   **正确的路由配置：** 确保在你的 `AppRoutingModule`（或你创建的任何其他路由模块）中正确定义了路由。每个路径都应关联到特定的组件。
*   **服务器端配置（用于深度链接）：** 如果你使用"路径位置策略"（这是默认策略），则需要将你的服务器配置为对所有应用程序路由提供 `index.html` 文件。这允许 Angular 在客户端处理路由，即使你直接访问深层链接或刷新页面也是如此。

**示例 `AppRoutingModule`：**

```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ProductListComponent } from './product-list/product-list.component';
import { ProductDetailComponent } from './product-detail/product-detail.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'products', component: ProductListComponent },
  { path: 'products/:id', component: ProductDetailComponent }, // 带参数的路由
  { path: '**', redirectTo: '' } // 用于未知路径的通配符路由
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

在这个例子中：

*   当你导航到 `/products` 时，将渲染 `ProductListComponent`。如果你刷新页面，你仍然会停留在 `ProductListComponent` 上。
*   当你导航到 `/products/123` 时，将渲染 `ProductDetailComponent`，并且可以在组件内部访问 `id` 参数。刷新将使你停留在同一产品详情页面。

**2. 设计子路由**

子路由允许你在应用程序中创建嵌套布局。这对于那些拥有一个作为其他相关组件容器的父组件的部分非常有用。

**示例：** 假设你有一个带有"用户"和"设置"子部分的"管理"部分。

**步骤：**

1.  **创建父组件和子组件：**
    ```bash
    ng generate component admin
    ng generate component users
    ng generate component settings
    ```

2.  **在父级的路由模块（或主 `AppRoutingModule`）中配置子路由：**

    ```typescript
    import { NgModule } from '@angular/core';
    import { RouterModule, Routes } from '@angular/router';
    import { AdminComponent } from './admin/admin.component';
    import { UsersComponent } from './users/users.component';
    import { SettingsComponent } from './settings/settings.component';

    const adminRoutes: Routes = [
      {
        path: 'admin',
        component: AdminComponent,
        children: [
          { path: 'users', component: UsersComponent },
          { path: 'settings', component: SettingsComponent },
          { path: '', redirectTo: 'users', pathMatch: 'full' } // 默认子路由
        ]
      }
    ];

    @NgModule({
      imports: [RouterModule.forChild(adminRoutes)], // 对特性模块使用 forChild
      exports: [RouterModule]
    })
    export class AdminRoutingModule { }
    ```

    **或者，你可以在 `AppRoutingModule` 中定义它们：**

    ```typescript
    // 在 AppRoutingModule 中
    const routes: Routes = [
      { path: '', component: HomeComponent },
      {
        path: 'admin',
        component: AdminComponent,
        children: [
          { path: 'users', component: UsersComponent },
          { path: 'settings', component: SettingsComponent },
          { path: '', redirectTo: 'users', pathMatch: 'full' }
        ]
      },
      { path: 'products', component: ProductListComponent },
      { path: 'products/:id', component: ProductDetailComponent },
      { path: '**', redirectTo: '' }
    ];
    ```

3.  **在父组件的模板 (`admin.component.html`) 中添加 `<router-outlet>`：**

    ```html
    <h1>管理仪表板</h1>
    <nav>
      <a routerLink="users" routerLinkActive="active">用户</a> |
      <a routerLink="settings" routerLinkActive="active">设置</a>
    </nav>
    <hr>
    <router-outlet></router-outlet>
    ```

**解释：**

*   `admin` 路由内的 `children` 数组定义了子路由。
*   子路由的 `path` 是相对于父路由 (`/admin`) 的。
*   当你导航到 `/admin/users` 时，将渲染 `AdminComponent`，并且 `UsersComponent` 将显示在 `AdminComponent` 的 `<router-outlet>` 内。
*   `admin` 路由中的 `redirectTo: 'users', pathMatch: 'full'` 确保当你导航到 `/admin` 时，它会自动重定向到 `/admin/users`。

**3. 设计带查询参数的路由**

查询参数用于向路由传递可选信息。它们出现在 URL 中的问号 (`?`) 之后，并且是由与号 (`&`) 分隔的键值对。

**示例：** 一个可以按类别过滤的产品列表页面。

**步骤：**

1.  **配置路由（查询参数无需特殊配置）：**

    ```typescript
    // 在 AppRoutingModule 中
    const routes: Routes = [
      { path: 'products', component: ProductListComponent },
      // ... 其他路由
    ];
    ```

2.  **使用查询参数导航：** 你可以使用 `Router` 服务导航到带有查询参数的路由：

    ```typescript
    import { Router } from '@angular/router';
    import { Component } from '@angular/core';

    @Component({
      selector: 'app-filter',
      template: `
        <button (click)="filterProducts('electronics')">电子产品</button>
        <button (click)="filterProducts('clothing')">服装</button>
      `
    })
    export class FilterComponent {
      constructor(private router: Router) {}

      filterProducts(category: string) {
        this.router.navigate(['/products'], { queryParams: { category: category } });
      }
    }
    ```

3.  **在组件中访问查询参数：** 使用 `ActivatedRoute` 服务访问查询参数：

{% raw %}
    ```typescript
    import { Component, OnInit } from '@angular/core';
    import { ActivatedRoute } from '@angular/router';

    @Component({
      selector: 'app-product-list',
      template: `
        <h2>产品列表</h2>
        <p>按类别过滤：{{ categoryFilter }}</p>
        <ul>
          <li *ngFor="let product of filteredProducts">
            {{ product.name }}
          </li>
        </ul>
      `
    })
    export class ProductListComponent implements OnInit {
      products: any[] = [
        { id: 1, name: '笔记本电脑', category: 'electronics' },
        { id: 2, name: 'T恤', category: 'clothing' },
        { id: 3, name: '耳机', category: 'electronics' },
        { id: 4, name: '牛仔裤', category: 'clothing' }
      ];
      categoryFilter: string | null = null;
      filteredProducts: any[] = [];

      constructor(private route: ActivatedRoute) {}

      ngOnInit(): void {
        this.route.queryParams.subscribe(params => {
          this.categoryFilter = params['category'];
          this.filterProductsByCategory();
        });
      }

      filterProductsByCategory() {
        if (this.categoryFilter) {
          this.filteredProducts = this.products.filter(
            product => product.category.toLowerCase() === this.categoryFilter?.toLowerCase()
          );
        } else {
          this.filteredProducts = this.products;
        }
      }
    }
    ```
{% endraw %}

**解释：**

*   当点击"电子产品"按钮时，应用程序会导航到 `/products?category=electronics`。
*   在 `ProductListComponent` 中，`ActivatedRoute` 服务提供了一个 `queryParams` 可观察对象。我们订阅这个可观察对象以获取当前的查询参数。
*   `params['category']` 检索 `category` 查询参数的值。
*   当使用 URL 中的查询参数刷新页面时，`ngOnInit` 生命周期钩子将再次执行，组件将重新订阅 `queryParams`，确保即使在刷新后也能应用过滤器。

**总结：**

*   Angular 的路由默认处理刷新和停留在同一页面，前提是你的路由配置正确并且服务器已为深度链接设置好。
*   子路由是使用路由配置中的 `children` 数组和父组件模板中的 `<router-outlet>` 指令来设计的。
*   查询参数附加到 URL，并且可以使用 `ActivatedRoute` 服务的 `queryParams` 可观察对象在你的组件中访问。这确保了通过查询参数管理的任何状态即使在页面刷新后也能保留。