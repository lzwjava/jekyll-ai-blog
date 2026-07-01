---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-sonnet-4
title: Playwright End-to-End Testing Guide
translated: false
type: note
---

## What is Playwright?

Playwright is a modern end-to-end testing framework developed by Microsoft that enables reliable testing of web applications across multiple browsers (Chromium, Firefox, and WebKit). It provides a unified API for automating web pages and is designed to handle modern web app challenges like single-page applications, dynamic content, and complex user interactions.

## Key Features

- **Cross-browser testing**: Supports Chromium, Firefox, and WebKit
- **Fast execution**: Runs tests in parallel by default
- **Auto-wait**: Automatically waits for elements to be ready
- **Network interception**: Mock APIs and capture network requests
- **Mobile testing**: Test mobile web apps with device emulation
- **Screenshots and videos**: Built-in visual testing capabilities
- **Debugging tools**: Comprehensive debugging with trace viewer

## Installation and Setup

### Basic Installation

```bash
# Install Playwright
npm init playwright@latest

# Or add to existing project
npm install -D @playwright/test

# Install browsers
npx playwright install
```

### Project Structure

```
tests/
  example.spec.js
playwright.config.js
package.json
```

### Configuration (playwright.config.js)

```javascript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Writing Your First Test

### Basic Test Structure

```javascript
import { test, expect } from '@playwright/test';

test('basic test example', async ({ page }) => {
  // Navigate to page
  await page.goto('https://example.com');

  // Interact with elements
  await page.click('button');
  await page.fill('input[name="username"]', 'testuser');

  // Assertions
  await expect(page.locator('h1')).toHaveText('Welcome');
  await expect(page).toHaveURL(/dashboard/);
});
```

### Common Actions

#### Navigation

```javascript
await page.goto('https://example.com');
await page.goBack();
await page.goForward();
await page.reload();
```

#### Element Interactions

```javascript
// Click elements
await page.click('button');
await page.click('text=Submit');
await page.click('#login-btn');

// Fill forms
await page.fill('input[name="email"]', 'user@example.com');
await page.type('textarea', 'Hello world');
await page.selectOption('select', 'option-value');

// Check/uncheck
await page.check('input[type="checkbox"]');
await page.uncheck('input[type="checkbox"]');
```

#### Waiting and Timeouts

```javascript
// Wait for elements
await page.waitForSelector('.loading-spinner', { state: 'hidden' });
await page.waitForURL('**/dashboard');
await page.waitForResponse('**/api/users');

// Wait for custom conditions
await page.waitForFunction(() => window.myApp.isReady);
```

## Advanced Testing Patterns

### Page Object Model

```javascript
// pages/LoginPage.js
export class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('input[name="email"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.loginButton = page.locator('button[type="submit"]');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

// tests/login.spec.js
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto('/login');
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

### API Testing

```javascript
test('API testing', async ({ request }) => {
  // POST request
  const response = await request.post('/api/users', {
    data: {
      name: 'John Doe',
      email: 'john@example.com'
    }
  });

  expect(response.ok()).toBeTruthy();
  const userData = await response.json();
  expect(userData.name).toBe('John Doe');
});
```

### Network Mocking

```javascript
test('mock API responses', async ({ page }) => {
  // Mock API response
  await page.route('**/api/users', async route => {
    const json = [{ id: 1, name: 'Mock User' }];
    await route.fulfill({ json });
  });

  await page.goto('/users');
  await expect(page.locator('.user-name')).toHaveText('Mock User');
});
```

### Visual Testing

```javascript
test('visual comparison', async ({ page }) => {
  await page.goto('/dashboard');

  // Full page screenshot
  await expect(page).toHaveScreenshot('dashboard.png');

  // Element screenshot
  await expect(page.locator('.header')).toHaveScreenshot('header.png');
});
```

## Test Organization and Best Practices

### Test Hooks

```javascript
import { test, expect } from '@playwright/test';

test.describe('User Management', () => {
  test.beforeEach(async ({ page }) => {
    // Run before each test
    await page.goto('/login');
    await page.fill('[name="email"]', 'admin@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
  });

  test.afterEach(async ({ page }) => {
    // Clean up after each test
    await page.evaluate(() => localStorage.clear());
  });

  test('should create new user', async ({ page }) => {
    // Test implementation
  });
});
```

### Fixtures and Test Context

```javascript
// fixtures/auth.js
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Login before test
    await page.goto('/login');
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');

    await use(page);

    // Cleanup after test
    await page.goto('/logout');
  },
});

// In test file
import { test, expect } from '../fixtures/auth';

test('authenticated user actions', async ({ authenticatedPage }) => {
  await expect(authenticatedPage.locator('.welcome')).toBeVisible();
});
```

## Running Tests

### Command Line Options

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/login.spec.js

# Run tests in headed mode
npx playwright test --headed

# Run tests in specific browser
npx playwright test --project=firefox

# Run tests with debugging
npx playwright test --debug

# Run tests in parallel
npx playwright test --workers=4
```

### Test Reports

```bash
# Generate HTML report
npx playwright show-report

# View trace files
npx playwright show-trace trace.zip
```

## Playwright vs Selenium

### Architecture Differences

| Feature | Playwright | Selenium |
| --------- | ------------ | ---------- |
| **Architecture** | Direct browser communication | WebDriver protocol |
| **Browser Support** | Chromium, Firefox, WebKit | Chrome, Firefox, Safari, Edge, IE |
| **Installation** | Single package with browsers | Separate driver downloads |
| **Language Support** | JavaScript, Python, Java, C# | Most programming languages |

### Performance Comparison

**Playwright Advantages:**

- **Faster execution**: Direct browser API communication eliminates WebDriver overhead
- **Parallel by default**: Built-in parallel test execution
- **Auto-wait**: Intelligent waiting without explicit waits
- **Network control**: Built-in request/response interception

**Selenium Advantages:**

- **Mature ecosystem**: Extensive community and third-party tools
- **Language flexibility**: Support for more programming languages
- **Browser coverage**: Supports older browsers like Internet Explorer
- **Industry standard**: Widely adopted with extensive documentation

### Feature Comparison

#### Test Reliability

```javascript
// Playwright - Auto-wait built-in
await page.click('button'); // Waits for element to be clickable

// Selenium - Manual waits required
await driver.wait(until.elementIsVisible(button));
await driver.wait(until.elementToBeClickable(button));
await button.click();
```

#### Mobile Testing

```javascript
// Playwright - Built-in mobile emulation
const context = await browser.newContext({
  ...devices['iPhone 13']
});

// Selenium - Requires additional setup
const options = new chrome.Options();
options.addArguments('--user-agent=iPhone...');
```

#### Network Handling

```javascript
// Playwright - Native network interception
await page.route('**/api/**', route => route.abort());

// Selenium - Requires proxy setup
const proxy = new Proxy();
proxy.setHttpProxy('localhost:8080');
```

### Migration Considerations

**When to Choose Playwright:**

- New projects or greenfield applications
- Modern web apps with SPA architecture
- Need for fast, reliable test execution
- Team primarily uses JavaScript/TypeScript
- Requirement for built-in visual testing

**When to Stick with Selenium:**

- Large existing test suites
- Need for specific browser/OS combinations
- Team expertise in non-JavaScript languages
- Integration with existing CI/CD pipelines
- Testing legacy applications

### Code Comparison Example

```javascript
// Playwright
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});

// Selenium (JavaScript)
const { Builder, By, until } = require('selenium-webdriver');

describe('login flow', () => {
  let driver;

  beforeEach(async () => {
    driver = await new Builder().forBrowser('chrome').build();
  });

  afterEach(async () => {
    await driver.quit();
  });

  it('should login successfully', async () => {
    await driver.get('http://localhost:3000/login');
    await driver.findElement(By.name('email')).sendKeys('user@example.com');
    await driver.findElement(By.name('password')).sendKeys('password');
    await driver.findElement(By.css('button[type="submit"]')).click();
    await driver.wait(until.urlContains('/dashboard'));
  });
});
```

## Conclusion

Playwright represents a modern approach to end-to-end testing with significant advantages in speed, reliability, and developer experience. While Selenium remains a solid choice for established projects and specific use cases, Playwright's architecture and feature set make it particularly well-suited for testing modern web applications. The choice between them should be based on your specific project requirements, existing infrastructure, and team expertise.
