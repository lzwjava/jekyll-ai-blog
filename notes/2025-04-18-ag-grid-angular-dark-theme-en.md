---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: AG Grid Angular Dark Theme Guide
translated: false
type: note
---

Got it — you’re asking about **Alpine Dark Theme** in **AG Grid** when using it in an **Angular application**.

---

### 🔹 What is Alpine Dark Theme?
AG Grid provides several built-in themes for styling the grid.
One of them is the **Alpine** theme, which comes in both **light** and **dark** variants:

- `ag-theme-alpine` → Alpine Light theme (default modern look).
- `ag-theme-alpine-dark` → Alpine Dark theme.

So, **Alpine Dark** theme is simply the dark mode variant of AG Grid’s Alpine theme.

---

### 🔹 Using Alpine Dark Theme in Angular + AG Grid

1. **Install AG Grid Packages**
   ```bash
   npm install ag-grid-community ag-grid-angular
   ```
   (If you want enterprise features, also add `ag-grid-enterprise`.)

---

2. **Import AG Grid Module in Angular**
   In your `app.module.ts`:
   ```ts
   import { AgGridModule } from 'ag-grid-angular';
   import { NgModule } from '@angular/core';
   import { BrowserModule } from '@angular/platform-browser';

   import { AppComponent } from './app.component';

   @NgModule({
     declarations: [AppComponent],
     imports: [
       BrowserModule,
       AgGridModule
     ],
     providers: [],
     bootstrap: [AppComponent]
   })
   export class AppModule {}
   ```

---

3. **Include AG Grid Styles**
   In `angular.json`, under `styles`, add the CSS for Alpine Dark:
   ```json
   "styles": [
     "node_modules/ag-grid-community/styles/ag-grid.css",
     "node_modules/ag-grid-community/styles/ag-theme-alpine-dark.css",
     "src/styles.css"
   ]
   ```

---

4. **Apply the Theme in Template**
   In your `app.component.html`:
   ```html
   <ag-grid-angular
     style="width: 100%; height: 500px;"
     class="ag-theme-alpine-dark"
     [rowData]="rowData"
     [columnDefs]="columnDefs"
     [defaultColDef]="defaultColDef"
   ></ag-grid-angular>
   ```

---

5. **Define Data in Component**
   In `app.component.ts`:
   ```ts
   import { Component } from '@angular/core';
   import { ColDef } from 'ag-grid-community';

   @Component({
     selector: 'app-root',
     templateUrl: './app.component.html',
     styleUrls: ['./app.component.css']
   })
   export class AppComponent {
     columnDefs: ColDef[] = [
       { field: 'make', sortable: true, filter: true },
       { field: 'model', sortable: true, filter: true },
       { field: 'price', sortable: true, filter: true }
     ];

     rowData = [
       { make: 'Toyota', model: 'Celica', price: 35000 },
       { make: 'Ford', model: 'Mondeo', price: 32000 },
       { make: 'Porsche', model: 'Boxster', price: 72000 }
     ];

     defaultColDef: ColDef = {
       flex: 1,
       minWidth: 100,
       resizable: true
     };
   }
   ```

---

### 🔹 Switching between Alpine Light & Dark Theme
You can dynamically switch themes just by changing the class on the grid container:

{% raw %}
```html
<ag-grid-angular
  class="{{ isDark ? 'ag-theme-alpine-dark' : 'ag-theme-alpine' }}"
  ...
></ag-grid-angular>
```
{% endraw %}

And in your component:
```ts
isDark = true;
```

---

✅ That’s it! Now your AG Grid in Angular will be styled with the **Alpine Dark Theme**.

---

Would you like me to also show you **how to toggle between dark/light themes at runtime** (like a dark mode switch), or is a static dark grid enough?
