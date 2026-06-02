---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Angular Vitest Testing Quick Start
translated: false
type: note
---

**Question:** How to write and run simple `npm test` for an Angular 20+ project?

**Answer:**

In Angular 20+ (and actually since Angular ~v15–16), the default test runner is **Vitest** (instead of Karma + Jasmine).

Here are the most common and clean ways to set up and write simple tests in a modern Angular project (2025–2026 style):

### 1. Most common & recommended way in Angular 20+ (Vitest + jsdom)

```bash
# Run tests (this is what "npm test" does)
npm test

# Watch mode (recommended during development)
npm run test:watch
```

Typical `package.json` scripts look like this:

```json
"scripts": {
  "test": "ng test",
  "test:watch": "ng test --watch"
}
```

### 2. Simplest possible test example (2025+ style)

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

### 3. Even simpler – testing a component with signal input (Angular 17+ style)

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
    // normally you'd use output or model() here
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

### Quick checklist – modern Angular testing (2025+)

| What you want                     | Recommended approach                           | Command                   |
|-----------------------------------|--------------------------------------------------|---------------------------|
| Default Angular 18–20+ setup      | Vitest + jsdom                                   | `ng test`                 |
| Run once (CI)                     | Headless mode                                    | `npm test`                |
| Develop + watch                   | Interactive watch mode                           | `npm run test:watch`      |
| Test only one file                | Focus file                                       | `ng test --include=**/*counter*` |
| Skip component styles             | `--include=**/*.spec.ts`                         | faster CI                 |
| Use Jest instead?                 | Possible but not default anymore                 | requires manual setup     |

### Summary – simplest way to start

1. Just run:
   ```bash
   npm test
   ```

2. Or in watch mode (strongly recommended):
   ```bash
   npm run test:watch
   ```

3. Write tests like the examples above → they work in Angular 17/18/19/20+

Happy testing!

**References:**

- None needed for this Angular core knowledge question
