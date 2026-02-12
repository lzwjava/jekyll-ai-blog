---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: AG Grid Upgrade Guide v20 to 30+
translated: false
type: note
---

**Question:** Compare AG Grid 20+ version and AG Grid 30+ version. If we upgrade it, then how to fix errors, how to upgrade it?

**Answer:**

AG Grid version 20 (around early 2019) is significantly older than version 30+ (version 30 released in mid-2023, with current versions in 2026 reaching 35+). Upgrading from v20.x to v30+ represents a **major jump** across roughly 10 major releases, involving many new features, performance improvements, better TypeScript support, modern theming, and several breaking changes.

### Key Differences (v20+ vs v30+)

- **New Features in v30+ (not in v20):**
  - Cell data types with automatic type inference
  - Built-in cell editors (richer editing experience)
  - Group footer rows for server-side row model
  - Export row groups to Excel with current expanded/collapsed state
  - Advanced filtering improvements (boolean expressions in later minors)
  - Modern theming system using CSS variables (introduced around v28)
  - Better module registration (per-grid instead of global)
  - Improved React/Angular/Vue integration and Ivy support
  - Many performance and accessibility enhancements

- **Breaking Changes and Removals:**
  - Deprecated APIs from v20–v29 were removed (e.g., old module systems, certain properties/methods)
  - Module registration changed dramatically around v22–v23 (shift to `@ag-grid-community/all-modules` or `@ag-grid-enterprise/all-modules`)
  - Theming moved from old Sass-based to CSS variable-based (major shift around v28+)
  - TypeScript requirements increased (v29+ needs newer TS versions)
  - Column defaults changed (e.g., sortable/resizable true by default in later versions)
  - Some component registrations and grid option behaviors updated

- **Benefits of Upgrading:**
  - Much better performance with large datasets
  - Modern framework compatibility (e.g., Angular 16+, React 18+)
  - New enterprise features (if using Enterprise)
  - Future-proof code (v20 is no longer supported)

### How to Upgrade from AG Grid v20+ to v30+

Upgrading directly from v20 to v30+ in one step is **not recommended** due to cumulative breaking changes. Follow an incremental approach.

1. **Recommended Upgrade Path:**
   - v20 → v22/v23 (big module system change)
   - Then v23 → v27/v28 (theming and Angular/React updates)
   - Then v28 → v29
   - Then v29 → v30
   - Finally to latest (v35+)

2. **Preparation Steps:**
   - Check your current framework (React, Angular, Vue, plain JS) and its version compatibility with target AG Grid version
   - Backup your project
   - Review the official changelog for each major version: https://www.ag-grid.com/changelog/

3. **Upgrade Steps (General):**
   - Update package.json dependencies:
     - For Community: `"ag-grid-community": "^30.0.0"` (or latest)
     - For Enterprise: `"ag-grid-enterprise": "^30.0.0"`
     - Framework wrapper (e.g., `"ag-grid-angular": "^30.0.0"`, `"ag-grid-react": "^30.0.0"`)
   - Remove old imports like `ag-grid` or individual modules if using the all-in-one packages
   - Run `npm install` or `yarn install`
   - Fix TypeScript errors (update tsconfig if needed; v30+ often requires TS 4.3+)
   - Update grid setup code (e.g., module registration, theme inclusion)

4. **Common Errors and Fixes:**
   - **Module not found / registration errors** — Switch to `import 'ag-grid-enterprise';` or use all-modules package. Old global registration was removed.
   - **Theming issues (styles missing/broken)** — Migrate to new CSS variable theming (import new theme CSS, update class names like `ag-theme-alpine`)
   - **Property/method not found** — Search changelog for removed/deprecated items; replace with new equivalents (e.g., old API → new API)
   - **TypeScript type errors** — Provide explicit types (e.g., for `columnDefs: ColDef[]`)
   - **Custom cell renderers/editors broken** — Check if params changed; update to new interfaces
   - **Framework-specific issues** — For Angular: remove `.withComponents()` if present (post-v28); for React: check functional component hooks

5. **Tools to Help:**
   - AG Grid provides **Codemods** starting from v31+ (automate some migrations)
   - Use the migration guides for each major version (e.g., upgrading-to-ag-grid-30)
   - Test thoroughly — features like Excel export, server-side model, and custom components often need attention

**Recommendation:** Upgrade incrementally (one or two major versions at a time) and use the official migration guides for each step. Start by going to the latest v30.x or directly to current version (v35+) if your codebase allows, but expect 1–several days of work depending on usage complexity.

**References:**

- [Upgrading to AG Grid 30](https://www.ag-grid.com/javascript-data-grid/upgrading-to-ag-grid-30)
- [AG Grid Migration Guides Overview](https://www.ag-grid.com/javascript-data-grid/migration)
- [What's New in AG Grid 30](https://blog.ag-grid.com/whats-new-in-ag-grid-30/)
- [AG Grid Changelog](https://www.ag-grid.com/changelog)