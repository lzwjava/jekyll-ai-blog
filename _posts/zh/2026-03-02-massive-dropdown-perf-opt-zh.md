---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 优化海量下拉菜单性能
translated: true
type: note
---

问题：如何改进在 ngb-modal 中加载和显示 100k+ 可能值以选择一个值（如 SWIFT code 或 branch code）的速度，目前加载所有记录需要 6 分钟，并且过滤是纯前端过滤？

回答： 

在浏览器中一次性加载 100,000+ 项并渲染它们（即使是在简单的 `<select>` 或 ngb-modal 中的自定义下拉菜单）几乎总是一个坏主意。现代浏览器在创建数万个 DOM 元素时会遇到困难——这会导致漫长的渲染时间、高内存使用和迟钝的行为（你的 6 分钟情况极端但并不令人惊讶）。

以下是最实际的加速方法（目标是打开时间 < 2–3 秒）：

### 推荐方法（按优先级排序）

1. **服务器端过滤 + typeahead / 边输入边搜索（最佳长期解决方案）**  
   - 完全移除“加载全部”的概念。
   - 使用可搜索的下拉菜单（例如 **ng-select**、**mat-autocomplete** 或自定义输入 + 下拉菜单）。
   - 当用户输入 2–4 个字符时 → 发送 API 请求并携带搜索词。
   - 后端仅返回匹配的 20–200 项（非常快）。
   - 显示这些结果。
   - 额外优势：大多数库支持防抖、缓存最近搜索以及显示“加载中...”状态。

   → 这几乎是每个现代银行/金融科技应用处理 SWIFT codes、IBANs、分支列表、机场代码等的做法。

2. **虚拟滚动下拉菜单（如果你真的想允许浏览完整列表，这是个好选择）**  
   使用支持 **virtual scrolling** 的下拉组件，这样任何时候 DOM 中仅渲染 ~10–50 项——即使列表有 100k+ 项。

   Angular 中的流行选项（2025–2026 时代）：

   - **ng-select** 启用 virtualScroll（支持非常好）
   - **Angular Material mat-select** + **cdk-virtual-scroll-viewport**（需要自定义包装器或社区示例）
   - **PrimeNG p-dropdown** 支持虚拟滚动
   - **DevExtreme**、**Kendo UI**、**Syncfusion** 下拉菜单（商业但性能极佳）

   使用 ng-select 的概念结构示例：

   ```html
   <ng-select [items]="items$ | async"
              [virtualScroll]="true"
              bindLabel="name"
              bindValue="code"
              [loading]="loading"
              (scroll)="onScroll($event)"
              placeholder="Search SWIFT / Branch code">
   </ng-select>
   ```

   你仍需决定如何提供数据：

   - 选项 A：一次性加载全部 100k（仍很重 — ~10–30 MB JSON + 解析时间）
   - 选项 B：无限虚拟滚动（滚动时加载 200–500 项页面 → 后端分页）

   → 虚拟滚动 + 分页通常是需要完整浏览时的最佳平衡点。

3. **仅在明确请求时延迟加载完整列表（“加载全部”按钮）**  
   你当前的思路作为后备方案合理，但可以改进：

   - 默认状态：显示搜索输入 + 消息“输入以搜索”（未加载列表）
   - 显示“加载全部 (100k 项)”按钮 → 默认禁用或隐藏
   - 用户点击时 → 显示 spinner → 加载完整列表 → 启用过滤
   - 即使在此模式下也使用虚拟滚动（否则又会出现同样问题）

   如果搜索效果好，许多用户永远不会点击它。

4. **混合方案（非常务实的折中）**  
   - 模态框打开时 → 加载前 1,000–2,000 个最常见/最近/字母序前面的项
   - 显示搜索框，可即时过滤已加载项（快速）
   - 在底部显示“显示更多…”或“加载完整列表 (慢)”按钮
   - 如果用户真的需要稀有值 → 他们点击并等待一次

### 即使不改变架构也能快速获益的方法

- 在模态组件上使用 **`ChangeDetectionStrategy.OnPush`**
- 避免 ngFor 中的复杂模板（保持最小：code + name）
- 在任何 *ngFor 上使用 **`trackBy`** 函数
- 如果是自定义过滤，则对过滤输入进行防抖
- 压缩 JSON（服务器端 gzip/brotli）——100k 项可以大幅缩小
- 使用 Chrome DevTools 性能分析 → 通常 80%+ 时间花在 DOM 创建和 Angular 变更检测上

### 总结 – 建议优先级顺序

1. 转向 **服务器端搜索 / typeahead**（最快的用户体验，可扩展）
2. 如果必须浏览完整列表 → **虚拟滚动 + 服务器分页**
3. 作为折中 → 初始 1000–5000 项 + 使用虚拟滚动的“加载全部”

大多数金融应用为 SWIFT / branch / BIC codes 等字段选择选项 1，因为用户几乎总是知道他们想要的（部分）代码。

参考资料：  

- [Improving Angular Material Select and Autocomplete for 100k+ data with virtual scroll](https://medium.com/h7w/optimizing-angular-material-select-and-autocomplete-for-huge-dataset-70ff161d6797)
- [ng-select virtual scrolling documentation and large dataset handling](https://github.com/ng-select/ng-select)
- [Angular CDK Virtual Scrolling for large lists](https://material.angular.io/cdk/scrolling/overview)
- [Performance issues with large dropdowns in Angular](https://stackoverflow.com/questions/50578003/angular-select-with-large-dataset)