---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Angular Vitest 测试快速入门
translated: true
type: note
---

**Question:** 如何为 Angular 20+ 项目编写并运行简单的 `npm test`？

**Answer:**

在 Angular 20+ 中（实际上从 Angular ~v15–16 开始），默认的 test runner 是 **Vitest**（取代了之前的 Karma + Jasmine）。

以下是在现代 Angular 项目（2025–2026 风格）中设置和编写简单测试最常见且整洁的方法：

### 1. Angular 20+ 中最常见且推荐的方式 (Vitest + jsdom)

```bash
# 运行测试 (这是 "npm test" 实际执行的操作)
npm test

# Watch mode (建议在开发过程中使用)
npm run test:watch
```

典型的 `package.json` 脚本如下所示：

```json
"scripts": {
  "test": "ng test",
  "test:watch": "ng test --watch"
}
```

### 2. 最简单的测试示例 (2025+ 风格)

**src/app/app.component.spec.ts**

```ts
import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AppComponent],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Welcome');
  });

  it('should have welcome message in component', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app.title).toContain('angular');
  });
});
```

### 3. 更简单的方式 – 测试带有 signal input 的组件 (Angular 17+ 风格)

**src/app/counter/counter.component.ts**

{% raw %}

```ts
import { Component, input } from '@angular/core';

@Component({
  selector: 'app-counter',
  standalone: true,
  template: `
    <p>Count: {{ count() }}</p>
    <button (click)="increment()">+1</button>
  `
})
export class CounterComponent {
  count = input(0);

  increment() {
    // 通常你会在这里使用 output 或 model()
  }
}
```

{% endraw %}

**counter.component.spec.ts**

```ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CounterComponent } from './counter.component';

describe('CounterComponent', () => {
  let component: CounterComponent;
  let fixture: ComponentFixture<CounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(CounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should display initial count', () => {
    expect(fixture.nativeElement.querySelector('p').textContent)
      .toContain('Count: 0');
  });

  it('should display count = 7 when input is set', () => {
    fixture.componentRef.setInput('count', 7);
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('p').textContent)
      .toContain('Count: 7');
  });
});
```

### 快速清单 – 现代 Angular 测试 (2025+)

| 需求 | 推荐方案 | 命令 |
| ----------------------------------- | -------------------------------------------------- | --------------------------- |
| 默认 Angular 18–20+ 配置 | Vitest + jsdom | `ng test` |
| 运行一次 (CI) | Headless mode | `npm test` |
| 开发 + watch | 交互式 watch mode | `npm run test:watch` |
| 仅测试一个文件 | Focus file | `ng test --include=**/*counter*` |
| 跳过组件样式测试 | `--include=**/*.spec.ts` | 更快的 CI |
| 使用 Jest 代替？ | 可行但不再是默认选项 | 需要手动配置 |

### 总结 – 最简单的开始方式

1. 直接运行：

   ```bash
   npm test
   ```

2. 或使用 watch mode（强烈推荐）：

   ```bash
   npm run test:watch
   ```

3. 按照上面的示例编写测试 → 它们在 Angular 17/18/19/20+ 中均可正常工作

祝测试愉快！

**References:**

- None needed for this Angular core knowledge question
