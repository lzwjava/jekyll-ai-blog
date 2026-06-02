---
audio: false
generated: true
lang: en
layout: post
title: Design Routes in Angular
translated: false
type: note
---

Okay, let's break down how to design routes in Angular for easy refreshing, sub-routes, and handling query parameters.

**1. Easy Refresh and Staying on the Same Page**

Angular's default routing mechanism is designed to handle this seamlessly. When you navigate to a specific route in your Angular application, the browser's URL changes. This URL represents the current state of your application. When you refresh the page, the browser makes a request to the server for the resource associated with that URL. Angular's routing module then takes over and renders the component associated with that route.

**Key points:**

* **Correct Route Configuration:** Ensure your routes are correctly defined in your `AppRoutingModule` (or any other routing module you've created). Each path should be associated with a specific component.
* **Server-Side Configuration (for Deep Linking):** If you are using "path location strategy" (which is the default), your server needs to be configured to serve the `index.html` file for all application routes. This allows Angular to handle the routing on the client-side even when you directly access a deep link or refresh.

**Example `AppRoutingModule`:**

```typescript
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ProductListComponent } from './product-list/product-list.component';
import { ProductDetailComponent } from './product-detail/product-detail.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'products', component: ProductListComponent },
  { path: 'products/:id', component: ProductDetailComponent }, // Route with a parameter
  { path: '**', redirectTo: '' } // Wildcard route for unknown paths
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
```

In this example:

* When you navigate to `/products`, the `ProductListComponent` will be rendered. If you refresh the page, you'll still be on the `ProductListComponent`.
* When you navigate to `/products/123`, the `ProductDetailComponent` will be rendered, and the `id` parameter will be accessible within the component. Refreshing will keep you on the same product detail page.

**2. Designing Sub-routes (Child Routes)**

Sub-routes, or child routes, allow you to create nested layouts within your application. This is useful for sections where you have a parent component that acts as a container for other related components.

**Example:** Let's say you have an "Admin" section with "Users" and "Settings" sub-sections.

**Steps:**

1. **Create Parent and Child Components:**

    ```bash
    ng generate component admin
    ng generate component users
    ng generate component settings
    ```

2. **Configure Child Routes in the Parent's Routing Module (or the main `AppRoutingModule`):**

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
          { path: '', redirectTo: 'users', pathMatch: 'full' } // Default child route
        ]
      }
    ];

    @NgModule({
      imports: [RouterModule.forChild(adminRoutes)], // Use forChild for feature modules
      exports: [RouterModule]
    })
    export class AdminRoutingModule { }
    ```

    **Alternatively, you can define them in your `AppRoutingModule`:**

    ```typescript
    // In AppRoutingModule
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

3. **Add `<router-outlet>` in the Parent Component's Template (`admin.component.html`):**

    ```html
    <h1>Admin Dashboard</h1>
    <nav>
      <a routerLink="users" routerLinkActive="active">Users</a> |
      <a routerLink="settings" routerLinkActive="active">Settings</a>
    </nav>
    <hr>
    <router-outlet></router-outlet> ```

**Explanation:**

* The `children` array within the `admin` route defines the sub-routes.
* The `path` for the child routes is relative to the parent route (`/admin`).
* When you navigate to `/admin/users`, the `AdminComponent` will be rendered, and the `UsersComponent` will be displayed within the `<router-outlet>` of the `AdminComponent`.
* `redirectTo: 'users', pathMatch: 'full'` in the `admin` route ensures that when you navigate to just `/admin`, it will automatically redirect to `/admin/users`.

**3. Designing Routes with Query Parameters**

Query parameters are used to pass optional information to a route. They appear in the URL after a question mark (`?`) and are key-value pairs separated by ampersands (`&`).

**Example:** A product list page where you can filter by category.

**Steps:**

1. **Configure the Route (No special configuration needed for query parameters):**

    ```typescript
    // In AppRoutingModule
    const routes: Routes = [
      { path: 'products', component: ProductListComponent },
      // ... other routes
    ];
    ```

2. **Navigate with Query Parameters:** You can navigate to the route with query parameters using the `Router` service:

    ```typescript
    import { Router } from '@angular/router';
    import { Component } from '@angular/core';

    @Component({
      selector: 'app-filter',
      template: `
        <button (click)="filterProducts('electronics')">Electronics</button>
        <button (click)="filterProducts('clothing')">Clothing</button>
      `
    })
    export class FilterComponent {
      constructor(private router: Router) {}

      filterProducts(category: string) {
        this.router.navigate(['/products'], { queryParams: { category: category } });
      }
    }
    ```

3. **Access Query Parameters in the Component:** Use the `ActivatedRoute` service to access the query parameters:

    ```typescript
    import { Component, OnInit } from '@angular/core';
    import { ActivatedRoute } from '@angular/router';

    @Component({
      selector: 'app-product-list',
      template: `
        <h2>Product List</h2>
        <p>Filtering by category: {{ categoryFilter }}</p>
        <ul>
          <li *ngFor="let product of products">
            {{ product.name }}
          </li>
        </ul>
      `
    })
    export class ProductListComponent implements OnInit {
      products: any[] = [
        { id: 1, name: 'Laptop', category: 'electronics' },
        { id: 2, name: 'T-Shirt', category: 'clothing' },
        { id: 3, name: 'Headphones', category: 'electronics' },
        { id: 4, name: 'Jeans', category: 'clothing' }
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

**Explanation:**

* When the "Electronics" button is clicked, the application navigates to `/products?category=electronics`.
* In the `ProductListComponent`, the `ActivatedRoute` service provides an `queryParams` observable. We subscribe to this observable to get the current query parameters.
* `params['category']` retrieves the value of the `category` query parameter.
* When the page is refreshed with the query parameters in the URL, the `ngOnInit` lifecycle hook will execute again, and the component will re-subscribe to the `queryParams`, ensuring the filter is applied even after a refresh.

**In summary:**

* Angular's routing handles refreshing and staying on the same page by default, provided your routes are correctly configured and your server is set up for deep linking.
* Sub-routes are designed using the `children` array in your route configuration and the `<router-outlet>` directive in the parent component's template.
* Query parameters are appended to the URL and can be accessed in your components using the `ActivatedRoute` service's `queryParams` observable. This ensures that any state managed through query parameters is preserved even after a page refresh.
