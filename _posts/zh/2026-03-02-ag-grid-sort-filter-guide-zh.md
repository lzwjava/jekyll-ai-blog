---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AG Grid 排序和筛选指南
translated: true
type: note
---

问题：如何在 AG Grid 中使用可过滤和可排序功能？

答案：

在 **AG Grid** 中，使列具有 **sortable** 和 **filterable** 功能，主要通过 `columnDefs` 中的属性控制（或使用 `defaultColDef` 设置全局默认值）。

### 基本设置 – 最常见方法

```ts
// Example in TypeScript / JavaScript (React, Angular, Vue, Vanilla – all similar)
const columnDefs = [
  { 
    field: 'name', 
    headerName: 'Full Name',
    sortable: true,          // enables sorting (click header to sort)
    filter: true             // enables filtering (usually Text filter by default)
  },
  { 
    field: 'age', 
    headerName: 'Age',
    sortable: true,
    filter: 'agNumberColumnFilter'  // Number filter (better for numbers)
  },
  { 
    field: 'country', 
    headerName: 'Country',
    sortable: false,         // sorting disabled
    filter: 'agSetColumnFilter'     // Set filter (Excel-like list of values)
  },
  { 
    field: 'city', 
    sortable: true,
    filter: false            // filtering disabled
  }
];

// Grid options (important parts)
const gridOptions = {
  columnDefs: columnDefs,
  defaultColDef: {
    sortable: true,          // make ALL columns sortable by default
    filter: true,            // make ALL columns filterable by default
    floatingFilter: true,    // shows small filter input under header (very useful)
    resizable: true,
    flex: 1
  },
  // ... other options
};
```

### 关键属性快速总结

| 属性            | 类型                      | 作用                                               | 默认值   | 常见值                                   |
|-----------------|---------------------------|----------------------------------------------------|----------|------------------------------------------|
| `sortable`      | `boolean`                 | 允许点击列头进行排序                               | `true`   | `true` / `false`                         |
| `filter`        | `boolean \| string \| object` | 为列启用过滤                               | `false`  | `true`、`'agTextColumnFilter'`、` 'agNumberColumnFilter'`、` 'agDateColumnFilter'`、` 'agSetColumnFilter'` |
| `floatingFilter`| `boolean`                 | 在列头下方显示小型过滤框                           | `false`  | 通常在 `defaultColDef` 中设置为 `true`   |

### 最受欢迎的过滤器类型

- `true` 或 `'agTextColumnFilter'` → 经典文本包含/等于/开头匹配（Community 版默认）
- `'agNumberColumnFilter'` → 数字比较（>、<、之间等）
- `'agDateColumnFilter'` → 日期选择器 + 比较
- `'agSetColumnFilter'` → Excel 风格的唯一值检查列表（非常受欢迎 – Enterprise 版默认）

### 最小工作示例（Vanilla JS）

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.js"></script>
</head>
<body>
  <div id="myGrid" style="height: 400px; width:100%;" class="ag-theme-quartz"></div>

  <script>
    const gridOptions = {
      columnDefs: [
        { field: 'athlete', sortable: true, filter: true },
        { field: 'age', sortable: true, filter: 'agNumberColumnFilter' },
        { field: 'country', sortable: true, filter: 'agSetColumnFilter' },
        { field: 'year', sortable: true, filter: false }
      ],
      defaultColDef: {
        sortable: true,
        filter: true,
        floatingFilter: true,
        flex: 1
      },
      rowData: [ /* your data array */ ]
    };

    new agGrid.Grid(document.querySelector('#myGrid'), gridOptions);
  </script>
</body>
</html>
```

### 快速提示

- 希望几乎所有列都具有过滤 **和** 排序功能？→ 使用 `defaultColDef: { sortable: true, filter: true, floatingFilter: true }`
- 为特定列禁用？→ `sortable: false` 或 `filter: false`
- 需要自定义过滤逻辑？→ 创建自定义过滤组件
- 使用 **React/Angular/Vue**？→ 语法几乎相同（只需包装在组件中）

参考资料：  

- [AG Grid Row Sorting](https://www.ag-grid.com/javascript-data-grid/row-sorting)
- [AG Grid Column Filters](https://www.ag-grid.com/javascript-data-grid/filtering)
- [AG Grid Column Definitions](https://www.ag-grid.com/javascript-data-grid/column-definitions)
- [AG Grid Set Filter](https://www.ag-grid.com/javascript-data-grid/filter-set)