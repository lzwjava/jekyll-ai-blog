---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing Massive Dropdown Performance
translated: false
type: note
---

Question: How to improve the speed of loading and displaying 100k+ possible values in an ngb-modal for selecting one value (like SWIFT code or branch code), where currently loading all records takes 6 minutes, and the filter is a pure frontend filter?

Answer:

Loading 100,000+ items all at once in the browser and rendering them (even in a simple `<select>` or custom dropdown inside an ngb-modal) is almost always a bad idea. Modern browsers struggle with creating tens of thousands of DOM elements — this causes long render times, high memory usage, and sluggish behavior (your 6-minute case is extreme but not surprising).

Here are the most realistic ways to make this fast (aiming for < 2–3 seconds open time):

### Recommended Approaches (ranked by preference)

1. **Server-side filtering + typeahead / search-as-you-type (best long-term solution)**
   - Remove the "load all" concept completely.
   - Use a searchable dropdown (e.g. **ng-select**, **mat-autocomplete**, or custom input + dropdown).
   - When the user types 2–4 characters → send API request with the search term.
   - Backend returns only the matching 20–200 items (very fast).
   - Display those results.
   - Bonus: most libraries support debouncing, caching recent searches, and showing "loading..." state.

   → This is how almost every modern banking/fintech app handles SWIFT codes, IBANs, branch lists, airport codes, etc.

2. **Virtual scrolling dropdown (good if you really want to allow browsing the full list)**
   Use a dropdown component that supports **virtual scrolling** so only ~10–50 items are rendered in the DOM at any time — even if the list has 100k+ items.

   Popular options in Angular (2025–2026 era):

   - **ng-select** with virtualScroll enabled (very good support)
   - **Angular Material mat-select** + **cdk-virtual-scroll-viewport** (requires custom wrapper or community examples)
   - **PrimeNG p-dropdown** with virtual scrolling
   - **DevExtreme**, **Kendo UI**, **Syncfusion** dropdowns (commercial but very performant)

   Example conceptual structure with ng-select:

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

   You still need to decide how to feed the data:

   - Option A: Load all 100k once (still heavy — ~10–30 MB JSON + parse time)
   - Option B: Infinite virtual scroll (load pages of 200–500 items on scroll → backend pagination)

   → Virtual scroll + pagination is usually the sweet spot if full browsing is required.

3. **Lazy-load full list only when explicitly requested ("Load all" button)**
   Your current idea is reasonable as a fallback, but improve it:

   - Default state: show search input + message "Type to search" (no list loaded)
   - Show "Load all (100k items)" button → disabled by default or hidden
   - When user clicks → show spinner → load full list → enable filter
   - Use virtual scrolling even in this mode (otherwise same problem again)

   Many users will never click it if search works well.

4. **Hybrid (very pragmatic compromise)**
   - On modal open → load first 1,000–2,000 most common / recent / alphabetically first items
   - Show search box that filters the loaded items instantly (fast)
   - Show "Show more…" or "Load full list (slow)" button at the bottom
   - If user really needs rare value → they click and wait once

### Quick wins even without changing architecture

- Use **`ChangeDetectionStrategy.OnPush`** on the modal component
- Avoid complex templates inside ngFor (keep it minimal: code + name)
- Use **`trackBy`** function on any *ngFor
- Debounce filter input if it's custom
- Compress JSON (gzip/brotli on server) — 100k items can shrink a lot
- Profile with Chrome DevTools → usually 80%+ time is DOM creation & Angular change detection

### Summary – Suggested Priority Order

1. Move to **server-side search / typeahead** (fastest user experience, scalable)
2. If full list browsing is mandatory → **virtual scrolling + server pagination**
3. As compromise → initial 1000–5000 items + "Load all" with virtual scroll

Most financial applications choose option 1 for fields like SWIFT / branch / BIC codes because users almost always know (part of) the code they want.

References:

- [Improving Angular Material Select and Autocomplete for 100k+ data with virtual scroll](https://medium.com/h7w/optimizing-angular-material-select-and-autocomplete-for-huge-dataset-70ff161d6797)
- [ng-select virtual scrolling documentation and large dataset handling](https://github.com/ng-select/ng-select)
- [Angular CDK Virtual Scrolling for large lists](https://material.angular.io/cdk/scrolling/overview)
- [Performance issues with large dropdowns in Angular](https://stackoverflow.com/questions/50578003/angular-select-with-large-dataset)
