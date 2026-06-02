---
audio: false
generated: true
image: false
lang: en
layout: post
title: AG Grid Sorting and Filtering Guide
translated: false
type: note
---

Question: How to use filterable and sortable features in AG Grid?

Answer:

In **AG Grid**, making columns **sortable** and **filterable** is controlled mainly through properties in your `columnDefs` (or `defaultColDef` for global defaults).

### Basic Setup – Most Common Way

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

### Quick Summary of Key Properties

| Property       | Type              | What it does                                      | Default    | Common values                          |
|----------------|-------------------|----------------------------------------------------|------------|----------------------------------------|
| `sortable`     | `boolean`         | Allows sorting by clicking column header           | `true`     | `true` / `false`                       |
| `filter`       | `boolean \| string \| object` | Enables filtering for the column              | `false`    | `true`, `'agTextColumnFilter'`, `'agNumberColumnFilter'`, `'agDateColumnFilter'`, `'agSetColumnFilter'` |
| `floatingFilter`| `boolean`         | Shows mini filter box under header                 | `false`    | Usually set `true` in `defaultColDef`  |

### Most Popular Filter Types

- `true` or `'agTextColumnFilter'` → classic text contains/equals/starts with (default in Community)
- `'agNumberColumnFilter'` → number comparison (>, <, between, etc.)
- `'agDateColumnFilter'` → date picker + comparisons
- `'agSetColumnFilter'` → Excel-like checklist of unique values (very popular – Enterprise by default)

### Minimal Working Example (Vanilla JS)

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

### Quick Tips

- Want filter **and** sort on almost every column? → Use `defaultColDef: { sortable: true, filter: true, floatingFilter: true }`
- Disable for specific column? → `sortable: false` or `filter: false`
- Need custom filter logic? → Create custom filter component
- Using **React/Angular/Vue**? → Syntax is almost identical (just wrap in component)

References:

- [AG Grid Row Sorting](https://www.ag-grid.com/javascript-data-grid/row-sorting)
- [AG Grid Column Filters](https://www.ag-grid.com/javascript-data-grid/filtering)
- [AG Grid Column Definitions](https://www.ag-grid.com/javascript-data-grid/column-definitions)
- [AG Grid Set Filter](https://www.ag-grid.com/javascript-data-grid/filter-set)
