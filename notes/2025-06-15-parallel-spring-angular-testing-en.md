---
audio: false
generated: true
image: false
lang: en
layout: post
title: Parallel Spring Angular Browser Testing
translated: false
type: note
---

Got it—you want a practical way to test your Spring (Java) + Angular site in **Edge and Chrome in parallel**, mainly **manually** (with some light automation where it helps). Here’s a field-tested workflow that avoids wide tables.

---

# 1) Set up clean, comparable browsers

* **Install latest stable** Chrome and Edge. Keep a note of versions.
* Create **separate clean profiles** for testing in each:

  * Chrome: `chrome --user-data-dir=/tmp/chrome-qa --no-first-run`
  * Edge: `msedge --user-data-dir=/tmp/edge-qa --no-first-run`
* Match **zoom (100%)**, **DPR**, **language**, **OS theme**, **font packs**, and turn off extensions.
* Pin both browsers side-by-side (two monitors if possible). Use the same **viewport** (e.g., 1440×900).

---

# 2) Prepare a stable backend + realistic data

* Spin up your Spring backend in **staging mode** with deterministic seed data.
* Prefer **immutable test accounts** and a **known dataset** (e.g., Testcontainers for db snapshots or Flyway/Liquibase seed scripts).
* For flaky dependencies, use **WireMock** stubs (HTTP) so UI behavior is repeatable.

---

# 3) Mirror interactions across browsers (manual, but synced)

For genuinely parallel manual testing, mirror clicks/scrolls/typing from one browser to the other:

* Use **Browsersync** as a local proxy to **sync interactions**:

  ```bash
  npm i -g browser-sync
  browser-sync start --proxy "http://localhost:4200" --files "dist/**/*" --open "external"
  ```

  Open the proxied URL in **Chrome** and **Edge**; scrolls, clicks, and form inputs will mirror.
  (Great for layout diffs, hover/focus checks, and quick flows.)

> If you can’t proxy (auth constraints, corporate network), run two windows and keep a tight **step list** (below) plus a screen recorder split-view.

---

# 4) Cross-browser checklist (run both at once)

Work through this **in parallel**—same step in both browsers before moving on.

* **Bootstrap & fonts:** Flash of unstyled content (FOUC), icon fonts, fallback fonts.
* **Layout:** Flex/grid gaps, sticky headers/footers, overflow/ellipsis, RTL/L10n text wrapping.
* **Forms:** Autofill, placeholders, validation messages, number/date inputs, IME/Chinese input, copy/paste.
* **Focus/keyboard:** Tab order, focus ring visibility, `:focus-visible` vs `:focus`, Enter/Esc behaviors, shortcuts.
* **Hover/active:** Menus, tooltips, ripple effects, Angular Material state classes.
* **File & downloads:** File input accept filters, drag-and-drop, download prompts.
* **Auth/session:** Cookies, SameSite, storage isolation across tabs, session timeout and refresh token flows.
* **Routing:** Deep links, hard refresh on a nested route, 404 fallback.
* **Caching:** Service Worker update cycle, stale assets busting, offline page behavior.
* **Media & APIs:** getUserMedia/clipboard, notifications permissions.
* **Accessibility quick pass:** Landmarks/roles, color contrast (DevTools), keyboard-only nav.
* **Performance sanity:** DevTools Performance, check long tasks, and Lighthouse in **both** browsers.

Tip: Keep **DevTools open** (F12) in both, docked to bottom, and compare **Console** warnings (framework + CSP + deprecation messages).

---

# 5) Angular specifics that often differ

* **Change detection & async:** Microtask timing can surface race conditions differently; watch spinners and “Save” buttons for double-click issues.
* **Zone.js errors:** Unhandled promise rejections in one browser but not the other—check console.
* **Angular Material themes:** Verify dark/light tokens, high-contrast mode, and focus outlines (Edge often renders focus slightly differently).
* **i18n pipes & date formats:** Locale differences with `DatePipe` and `Intl` in Chromium variants.

---

# 6) Spring backend gotchas

* **CORS & redirects:** Same rules but **Edge sometimes surfaces CORS preflight issues** earlier in dev; verify `OPTIONS` responses and headers.
* **Content-Type & compression:** Check `application/json;charset=UTF-8` vs `application/json`; verify gzip/br—mismatches may show as “Failed to load” in one browser first.
* **Security headers:** CSP, HSTS, X-Frame-Options—harsher policies can block inline scripts/styles differently.

---

# 7) Make “manual” repeatable with a thin layer of automation

Even if you don’t want full E2E, set up a **short, fast** browser harness so CI can run both Chrome and Edge on every PR. You’ll catch regressions earlier and lighten your manual pass.

### Option A: Playwright (my top pick for Angular apps)

* One test runner, launches **Chrome Stable** and **Microsoft Edge** channels, runs **in parallel**.
* `npm i -D @playwright/test`
* `npx playwright install chromium`
* `playwright.config.ts` example:

  ```ts
  import { defineConfig, devices } from '@playwright/test';

  export default defineConfig({
    testDir: './e2e',
    workers: 4, // parallelism
    use: {
      baseURL: 'http://localhost:4200',
      trace: 'retain-on-failure',
    },
    projects: [
      {
        name: 'Chrome Stable',
        use: { ...devices['Desktop Chrome'], channel: 'chrome' },
      },
      {
        name: 'Microsoft Edge',
        use: { ...devices['Desktop Edge'], channel: 'msedge' },
      },
    ],
  });
  ```

  Minimal smoke spec (`e2e/smoke.spec.ts`):

  ```ts
  import { test, expect } from '@playwright/test';

  test('home loads and login works', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('Password123!');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await expect(page.getByText('Dashboard')).toBeVisible();
  });
  ```

  Run: `npx playwright test`

### Option B: Cypress (Chromium family, runs Chrome & Edge)

* Parallelization via CI matrix (or Cypress Dashboard).
* In CI, run:

  * `cypress run --browser chrome`
  * `cypress run --browser edge`
* Keep specs tiny (smoke only) to stay “manual-first”.

### Option C: Selenium Grid (if you already use Selenium)

* Dockerised Grid runs **chromium/edge nodes** concurrently.

  ```yaml
  # docker-compose.yml
  services:
    selenium-hub:
      image: selenium/hub:4
      ports: ["4444:4444"]
    chrome:
      image: selenium/node-chrome:4
      shm_size: 2gb
      depends_on: [selenium-hub]
      environment: [SE_EVENT_BUS_HOST=selenium-hub]
    edge:
      image: selenium/node-edge:4
      shm_size: 2gb
      depends_on: [selenium-hub]
      environment: [SE_EVENT_BUS_HOST=selenium-hub]
  ```

  Point your WebDriver tests at `http://localhost:4444/wd/hub` and run suites in parallel.

---

# 8) CI “parallel by default”

* Use a **matrix** job (Chrome/Edge) and run your Playwright/Cypress smoke in parallel.
* Fail-fast to save time; attach **traces/videos** for the failing browser.
* Nightly, run a slightly broader set and a **Lighthouse** pass on both browsers.

---

# 9) Fast triage when they differ

* Grab **HAR** from each browser, diff responses (status, headers, caching).
* Compare **computed styles** for the broken element (DevTools → Styles → Computed).
* Toggle **reduced motion** and **forced colors** to reveal accessibility CSS issues.
* Clear **site data** (Application panel) and retest to rule out stale SW/caches.

---

# 10) Minimal artifacts to keep

* One **shared checklist** (markdown) of your cross-browser checks.
* A **version ledger**: app commit, Chrome/Edge versions, OS, important flags.
* Attach **screenshots** (same viewport) for any visual difference you accept as “won’t fix”.

---

If you want, I can generate a ready-to-run **Playwright skeleton** for your Angular app (with `npm scripts`, CI matrix, and two smoke specs), or a **Browsersync script** tailored to your dev server setup.
