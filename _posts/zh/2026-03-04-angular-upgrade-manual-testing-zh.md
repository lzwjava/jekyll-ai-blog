---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Angular 升级手动测试指南
translated: true
type: note
---

问题：如果前端应用从 Angular 9 升级到 Angular 14，应该如何进行手动测试，以及应该关注应用的哪些方面？

答案：

从 **Angular 9 → 14** 升级跨越五个主要版本（10、11、12、13、14），因此即使自动化迁移（ng update）运行成功，也可能出现许多细微的视觉/行为回归。手动探索性测试变得非常重要。

### 推荐的手动测试方法

1. 升级稳定后（构建成功、启动、无控制台错误），**对整个应用进行 Smoke test**。
2. **端到端跟随主要 user journeys**（happy paths + common error paths）。
3. **尽可能并排比较行为**（旧 Angular 9 版本 vs 新 Angular 14 版本）。
4. **使用不同的浏览器**（Chrome、Firefox、Edge、Safari）——特别是检查移动视口 / responsive design。
5. **使用真实数据测试**（staging 环境、生产级数据）——合成数据往往隐藏问题。
6. **特别注意慢速 / 数据密集 / 动画密集的屏幕**。
7. **记录升级前后关键流程的简短 screencasts**——更容易发现回归。
8. **在最终 UAT 阶段涉及领域 / 业务用户**——开发者往往错过“感觉不对”的问题。

### 手动测试期间重点关注的领域

| Priority | Area | What Exactly to Check / Common Breakage Points (9→14) | Why It Breaks Frequently |
| -------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| ★★★★★ | **Routing & Navigation** | • Deep linking<br>• 后退/前进浏览器按钮<br>• Lazy-loaded modules 是否正确加载？<br>• Guards / resolvers<br>• Auxiliary routes（如果使用） | pathMatch 默认值变得更严格，resolver 行为改变，许多 router 生命周期调整 |
| ★★★★★ | **Forms (Template-driven + Reactive)** | • 验证消息在正确时间出现<br>• Disabled / readonly 状态<br>• Custom validators / async validators<br>• Form value / status 变化正确传播<br>• Dirty / touched / pristine 标志 | Angular 14 引入更严格的类型检查 → 细微的强制转换 bug 浮出水面 |
| ★★★★☆ | **Change Detection & Performance** | • UI **不**闪烁 / 不必要重渲染<br>• 无限 change detection 循环（控制台警告）<br>• 慢速列表 / 大型表格仍可使用？<br>• *ngIf / ngSwitch 内的组件正确更新 | Ivy + 更严格的 change detection + 新 zone.js 行为 |
| ★★★★☆ | **Templates & Directives** | • 结构化指令（*ngIf、*ngFor、*ngSwitch）<br>• Custom structural / attribute directives<br>• @Input / @Output 绑定<br>• 双向绑定 [(ngModel)] | 新的 template type checking 更严格，一些旧模式现在被警告 / 破坏 |
| ★★★★☆ | **HTTP / Interceptors / API calls** | • 所有 HTTP 调用仍正常工作<br>• Interceptors 正确修改 / 捕获错误<br>• 请求期间的加载 spinner / disabled 状态<br>• 错误处理 UI（toast、modal、内联） | HttpClient 变更 + RxJS 更新（v6 → v7） |
| ★★★★☆ | **Third-party libraries & Components** | • Angular Material → 检查 theme、typography、density<br>• Charts（ng2-charts、highcharts-angular…）<br>• Tables（ag-grid、prime-ng、material table）<br>• Modals / dialogs / overlays<br>• Date pickers / file upload components | 许多库有主要版本跳跃 + 破坏性变更 |
| ★★★☆☆ | **Animations & Transitions** | • Enter / leave animations<br>• Route animations<br>• @.disabled / :increment / :decrement | Animation DSL 有修复 & 弃用 |
| ★★★☆☆ | **Internationalization (i18n)** | • 翻译仍加载<br>• Plural / gender 规则正确<br>• RTL 语言（如果支持） | i18n 工具 & 提取改进 → 旧提取可能破坏 |
| ★★★☆☆ | **Accessibility (a11y)** | • Screen reader 行为<br>• Focus 管理（modals、menus）<br>• 键盘导航<br>• ARIA 属性 | 一些旧模式现在被扩展诊断标记 |
| ★★★☆☆ | **Browser Console & Warnings** | • 无红色错误<br>• 无黄色 deprecation / Ivy / zone.js 警告<br>• 无 "ExpressionChangedAfterItHasBeenCheckedError" | 许多旧模式现在产生警告 |
| ★★☆☆☆ | **Build & Bundle Size** | • 应用仍合理快速加载<br>• Bundle size 无巨大回归 | Ivy + differential loading 变更 + tree-shaking 改进 |
| ★★☆☆☆ | **Edge Cases** | • 空状态<br>• 非常长的内容 / 溢出<br>• 非常大的表单 / 列表<br>• 离线模式（如果实现）<br>• 复制粘贴 / 拖放功能 | 通常不被单元测试覆盖 |

### 测试人员快速检查清单摘要

- [ ] 登录 / 认证流程（包括社交登录，如果有）
- [ ] 主要导航 + 侧边栏 / 顶栏
- [ ] 主要实体的 CRUD 操作
- [ ] 搜索 / 过滤 / 排序
- [ ] 表单提交 + 验证
- [ ] 文件上传 / 下载（如果存在）
- [ ] 任何实时 / 轮询 / websocket 功能
- [ ] 导出到 Excel/PDF
- [ ] 手机/平板/桌面上的 responsive design
- [ ] 浏览器后退/前进/刷新行为

遵循官方 **Angular Update Guide**（<https://angular.dev/update-guide）并阅读> 10–14 版本的 release notes / breaking changes 摘要。

仔细的手动测试 + 良好的前后比较通常是“在我机器上能工作”和“生产环境崩溃”之间的区别。

引用：

- [Angular Update Guide](https://angular.dev/update-guide)
- [Angular 14 Release Notes & Breaking Changes Discussion](https://github.com/angular/angular/blob/main/CHANGELOG.md)（查找 v10 到 v14 部分）
