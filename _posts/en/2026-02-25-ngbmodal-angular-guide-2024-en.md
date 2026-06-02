---
audio: false
generated: true
image: false
lang: en
layout: post
title: NgbModal Angular Guide 2024
translated: false
type: note
---

**Question:** How to use NgbModal in Angular?

**Answer:**

Here’s a clear, modern (2024–2025) way to use **NgbModal** from **@ng-bootstrap/ng-bootstrap** in Angular (works with Angular 16, 17, 18, 19).

### 1. Installation

```bash
npm install @ng-bootstrap/ng-bootstrap
# or
yarn add @ng-bootstrap/ng-bootstrap
```

You also need Bootstrap CSS (choose one):

```bash
npm install bootstrap
```

### 2. Add to your module (most common way – standalone is also possible)

```ts
// app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { ExampleModalComponent } from './example-modal/example-modal.component';

@NgModule({
  declarations: [
    AppComponent,
    ExampleModalComponent
  ],
  imports: [
    BrowserModule,
    NgbModule,           // ← important
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

**Standalone components (Angular 17+ recommended way)**

```ts
// app.config.ts or main.ts
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideNgxBootstrap } from '@ng-bootstrap/ng-bootstrap';  // if using provide style

bootstrapApplication(AppComponent, {
  providers: [
    provideAnimations(),
    importProvidersFrom(NgbModule),
  ]
});
```

### 3. Create the modal content component

{% raw %}

```ts
// confirm-dialog.component.ts
import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,                    // ← recommended in 2024+
  template: `
    <div class="modal-header">
      <h4 class="modal-title">{{ title }}</h4>
      <button type="button" class="btn-close" aria-label="Close" (click)="activeModal.dismiss()"></button>
    </div>
    <div class="modal-body">
      <p>{{ message }}</p>
    </div>
    <div class="modal-footer">
      <button type="button" class="btn btn-outline-secondary" (click)="activeModal.dismiss()">Cancel</button>
      <button type="button" class="btn btn-danger" (click)="activeModal.close(true)">Delete</button>
    </div>
  `
})
export class ConfirmDialogComponent {
  @Input() title = 'Confirm';
  @Input() message = 'Are you sure?';

  constructor(public activeModal: NgbActiveModal) {}
}
```

{% endraw %}

### 4. Open the modal from any component

```ts
// parent.component.ts
import { Component } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ConfirmDialogComponent } from './confirm-dialog.component';

@Component({
  selector: 'app-parent',
  template: `
    <button class="btn btn-danger" (click)="openConfirm()">Delete user</button>
  `,
  standalone: true,
  imports: [/* ... */]
})
export class ParentComponent {

  constructor(private modalService: NgbModal) {}

  openConfirm() {
    const modalRef = this.modalService.open(ConfirmDialogComponent, {
      size: 'md',                // 'sm', 'lg', 'xl'
      centered: true,
      backdrop: 'static',        // click outside doesn't close
      keyboard: false            // ESC doesn't close
    });

    // Pass data to modal (optional)
    modalRef.componentInstance.title = 'Remove user';
    modalRef.componentInstance.message = 'Do you really want to delete this account?';

    // Handle result
    modalRef.result
      .then((result) => {
        if (result === true) {
          console.log('User clicked Delete → perform delete');
          // call your delete service here
        }
      })
      .catch(() => {
        console.log('Modal dismissed (cancel or ESC)');
      });
  }
}
```

### 5. Most popular modern patterns (2024–2025)

**Pattern A – Very clean with strong typing (recommended)**

```ts
openDeleteModal(): void {
  const modal = this.modalService.open(ConfirmDialogComponent, {
    centered: true,
    backdrop: 'static'
  });

  modal.componentInstance.title = 'Delete Item';
  modal.componentInstance.message = 'This action cannot be undone.';

  modal.result.then(
    (confirmed: boolean) => {
      if (confirmed) this.deleteItem();
    },
    () => {} // dismissed
  );
}
```

**Pattern B – Reusable confirm helper (very popular)**

```ts
async confirm(title: string, message: string): Promise<boolean> {
  const modalRef = this.modalService.open(ConfirmDialogComponent);
  modalRef.componentInstance.title = title;
  modalRef.componentInstance.message = message;

  return modalRef.result.catch(() => false);
}

// Usage:
if (await this.confirm('Delete?', 'Really delete this?')) {
  // delete logic
}
```

### Quick reference – useful NgbModal options

```ts
this.modalService.open(component, {
  size: 'lg',              // sm / md (default) / lg / xl
  centered: true,
  scrollable: true,
  backdrop: true | false | 'static',
  keyboard: true | false,
  windowClass: 'my-custom-modal',
  backdropClass: 'my-backdrop',
  modalDialogClass: 'my-dialog-class'
});
```

Good luck!

**References:**

- <https://ng-bootstrap.github.io/#/components/modal/examples>
- <https://ng-bootstrap.github.io/#/components/modal/api>

(no other external references needed for basic usage)
