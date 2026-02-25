---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NgbModal Angular 指南 2024
translated: true
type: note
---

**问题：** 如何在 Angular 中使用 NgbModal？

**答案：**

以下是在 Angular 中使用 **@ng-bootstrap/ng-bootstrap** 中的 **NgbModal** 的清晰、现代（2024–2025）方法（适用于 Angular 16、17、18、19）。

### 1. 安装

```bash
npm install @ng-bootstrap/ng-bootstrap
# or
yarn add @ng-bootstrap/ng-bootstrap
```

您还需要 Bootstrap CSS（选择其中之一）：

```bash
npm install bootstrap
```

### 2. 添加到您的模块（最常见的方式 – 也可以使用 standalone）

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
    NgbModule,           // ← 重要
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

**Standalone 组件（Angular 17+ 推荐方式）**

```ts
// app.config.ts or main.ts
import { provideAnimations } from '@angular/platform-browser/animations';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';  // 如果使用 provide 样式

bootstrapApplication(AppComponent, {
  providers: [
    provideAnimations(),
    importProvidersFrom(NgbModule),
  ]
});
```

### 3. 创建模态框内容组件

```ts
// confirm-dialog.component.ts
import { Component, Input } from '@angular/core';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,                    // ← 2024+ 推荐
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

### 4. 从任何组件打开模态框

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
      backdrop: 'static',        // 点击外部不会关闭
      keyboard: false            // ESC 不会关闭
    });

    // 向模态框传递数据（可选）
    modalRef.componentInstance.title = 'Remove user';
    modalRef.componentInstance.message = 'Do you really want to delete this account?';

    // 处理结果
    modalRef.result
      .then((result) => {
        if (result === true) {
          console.log('User clicked Delete → perform delete');
          // 在此处调用您的删除服务
        }
      })
      .catch(() => {
        console.log('Modal dismissed (cancel or ESC)');
      });
  }
}
```

### 5. 最受欢迎的现代模式（2024–2025）

**模式 A – 非常简洁且具有强类型（推荐）**

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
    () => {} // 已取消
  );
}
```

**模式 B – 可重用的确认助手（非常受欢迎）**

```ts
async confirm(title: string, message: string): Promise<boolean> {
  const modalRef = this.modalService.open(ConfirmDialogComponent);
  modalRef.componentInstance.title = title;
  modalRef.componentInstance.message = message;

  return modalRef.result.catch(() => false);
}

// 用法：
if (await this.confirm('Delete?', 'Really delete this?')) {
  // 删除逻辑
}
```

### 快速参考 – 有用的 NgbModal 选项

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

祝好运！

**参考资料：**

- https://ng-bootstrap.github.io/#/components/modal/examples
- https://ng-bootstrap.github.io/#/components/modal/api

（基本用法无需其他外部参考）