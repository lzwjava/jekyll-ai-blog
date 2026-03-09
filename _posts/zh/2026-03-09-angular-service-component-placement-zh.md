---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 服务和组件放置指南
translated: true
type: note
---

**问题**：在 Angular (latest/v21) 中，如果一个组件有 `standalone: false`，其相关的 service 应该声明在 `imports`、`declarations` 中，还是两者都有？

**回答**：

这是一个关于 Angular 的 NgModule 系统中的**两个不同、独立的关注点**的问题。您需要清楚地区分以下两点：

1. **组件本身**（具有 `standalone: false`）
2. **组件使用的 service**

这两者在 `@NgModule` 中进入**完全不同的数组**。

---

## 规则总结

  
| 要注册的事物 | 在 `@NgModule` 中的位置 |
|---|---|
| 具有 `standalone: false` 的 component / directive / pipe | `declarations` |
| service（或任何 provider） | `providers` |
| 在模板中要使用的 standalone component / NgModule / pipe | `imports` |

---

## 详细解释

### 1. 具有 `standalone: false` 的组件 → 放入 `declarations`

`@NgModule` 元数据的 `declarations` 属性声明属于该 NgModule 的 components、directives 和 pipes。组件必须标记为 `standalone: false`，才能在 NgModule 中声明。

```typescript
@Component({
  selector: 'my-comp',
  standalone: false,
  template: `...`
})
export class MyComponent {}

@NgModule({
  declarations: [MyComponent], // ✅ 组件放入此处
})
export class MyModule {}
```

---

### 2. service → 放入 `providers`（**不是** `imports` 或 `declarations`）

当组件或 service 请求依赖时，Angular 的依赖注入系统会查找可以提供该依赖的 provider。Services 在 `@NgModule` 的 `providers` 数组中注册。

```typescript
@NgModule({
  declarations: [MyComponent],
  providers: [MyService], // ✅ service 放入此处
})
export class MyModule {}
```

---

### 3. 最佳实践：在 service 本身上使用 `providedIn: 'root'`

在现代 Angular 中，最推荐的方法是完全避免将 service 放入任何模块的 `providers` 数组中。相反，使用 `providedIn: 'root'` 来装饰 service：

```typescript
@Injectable({
  providedIn: 'root' // ✅ 自动在所有地方可用
})
export class MyService {}
```

在 `@Injectable` 装饰器中使用 `providedIn: 'root'` 可以处理大多数常见用例，使 service 全局可用，而无需手动添加到任何 `providers` 数组。

---

### 4. 那么 `imports` 是做什么用的？

`@NgModule` 中的 `imports` **仅用于引入其他 NgModules 或 standalone components/directives/pipes**，以便它们的导出声明在您的模板中可用。

```typescript
@NgModule({
  imports: [CommonModule, RouterModule], // ✅ 其他模块 / standalone components
  declarations: [MyComponent],          // ✅ 非 standalone components/pipes/directives
  providers: [MyService],               // ✅ services / providers
})
export class MyModule {}
```

---

### 完整示例

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
  constructor(private svc: MyService) {} // 通过 DI 注入
}

// my.module.ts
@NgModule({
  declarations: [MyComponent], // 组件在此声明
  imports: [CommonModule],     // 其他模块在此导入
  // MyService 不需要在此处，因为使用了 providedIn: 'root'
})
export class MyModule {}
```

---

### 最终答案

- **`declarations`** → 用于 `standalone: false` 的组件本身
- **`providers`** → 用于需要模块作用域注入的任何 service
- **`imports`** → 用于模板中使用的其他 NgModules 或 standalone 组件
- **切勿将 service 放入 `declarations` 或 `imports`** — 这会导致错误

**参考资料**：

- [https://angular.dev/guide/ngmodules/overview](https://angular.dev/guide/ngmodules/overview)
- [https://angular.dev/guide/di/defining-dependency-providers](https://angular.dev/guide/di/defining-dependency-providers)
- [https://angular.dev/guide/components](https://angular.dev/guide/components)