---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter Routing Guide
translated: false
type: note
---

### Overview of CodeIgniter Routing

CodeIgniter's routing system allows you to map URLs (URIs) to specific controller classes and methods, overriding the default URL pattern of `example.com/controller/method/id/`. This is useful for creating SEO-friendly URLs, handling RESTful APIs, or simply customizing how requests are processed.

The provided code snippet is from CodeIgniter's `routes.php` configuration file. It defines an associative array `$route` where each key is a URI pattern, and the value is either a string (`controller/method`) or an array specifying different behaviors by HTTP method (e.g., GET, POST). This setup supports both standard routing and method-specific routing.

I'll break down **how routes are defined**, **how they work**, and **how to use them**, based on CodeIgniter's standard behavior and the example in your code. For full details, refer to the official CodeIgniter User Guide on routing: https://codeigniter.com/userguide4/general/routing.html.

#### 1. **How to Define Routes**
Routes are defined in `application/config/routes.php` as an array. You add entries to `$route[]`. Here's the syntax:

- **Basic Route**: Maps any HTTP method to a controller/method.
  ```
  $route['uri_segment'] = 'controller/method';
  ```
  - Example: `$route['login'] = 'users/login';` means any request to `/login` routes to `Users::login()`.

- **Method-Specific Route**: For RESTful APIs, you can specify different controllers/methods per HTTP method (GET, POST, PUT, etc.). This uses an array.
  ```
  $route['uri_segment'] = array(
      'METHOD1' => 'controller/method1',
      'METHOD2' => 'controller/method2'
  );
  ```
  - Example from your code: `$route['self'] = array('POST' => 'users/update', 'GET' => 'users/self');` means:
    - POST to `/self` → `Users::update()`.
    - GET to `/self` → `Users::self()`.

- **Wildcard Placeholders**: Use regex-like patterns to capture dynamic parts of the URL (passed as parameters to the method).
  - `(:any)`: Matches any character (except slashes) – e.g., slugs or strings.
  - `(:num)` or `(\d+)`: Matches digits only – for IDs.
  - Custom regex: Wrap in parentheses, e.g., `(foo|bar)` for specific matches.
  - Examples from your code:
    - `$route['users/(\d+)']['GET'] = 'users/one/$1';`: GET `/users/123` routes to `Users::one(123)`.
    - `$route['lives/(\d+)/notify'] = 'lives/notifyLiveStart/$1';`: Any method to `/lives/123/notify` routes to `Lives::notifyLiveStart(123)`.

- **Reserved Routes**:
  - `$route['default_controller'] = 'welcome';`: The controller loaded if no URI is given (e.g., root URL → `Welcome` controller).
  - `$route['404_override'] = 'errors/page_missing';`: The controller/method for unmatched routes (custom 404).
  - `$route['translate_uri_dashes'] = FALSE;`: If TRUE, converts dashes in URIs to underscores for controller/method names (e.g., `my-controller` → `my_controller`).

- **Order Matters**: Routes are matched in the order they appear. Define specific routes (with wildcards) before general ones to avoid conflicts.
- **HTTP Methods**: If not specified, a route applies to all methods. Your code uses arrays for specificity, which is great for APIs.

**Tips for Defining Routes in Your Code**:
- Add new routes at the end, before `$route['translate_uri_dashes']`.
- Test with tools like Postman for API routes to ensure the correct controller/method is hit.
- For complex apps, group routes by section (as you've done with comments like `// users`).

#### 2. **How Routes Work**
CodeIgniter's router processes each incoming request in this order:
1. **Parse the URI**: Breaks down the URL into segments (e.g., `/users/123/edit` → segments: `users`, `123`, `edit`).
2. **Match Against Routes**: Checks the `$route` array from top to bottom. It looks for exact matches first, then patterns with wildcards.
   - If a match is found, it maps to the specified controller/method, passing dynamic parts (e.g., `123`) as method arguments.
   - If no match, it falls back to the default pattern (`Controller::method/id/`).
3. **Load Controller & Method**: CodeIgniter instantiates the controller, calls the method, and passes any URI segments or captured groups.
4. **Method-Specific Handling**: If the route is an array (like in your code), it checks the HTTP method (GET, POST, etc.) from the request.
5. **Fallback**: Unmatched requests trigger a 404, or the `$route['404_override']` if set.

**Example Flow**:
- Request: `POST https://example.com/lives`
- Matches: `$route['lives']['POST'] = 'lives/create';`
- Result: Calls `Lives::create()` with no arguments.
- If the request was `GET https://example.com/lives/456`, it would match `$route['lives/(\d+)']['GET'] = 'lives/one/$1';` → `Lives::one(456)`.

**Key Mechanics**:
- **Dynamic Parameters**: Captured groups (e.g., `$1`) are passed as args to the method. Ensure your controller method expects them.
- **Security**: Routes help prevent direct access to sensitive controllers by obscuring URLs.
- **Performance**: Simple array lookups; no major overhead unless you have hundreds of routes.

#### 3. **How to Use Routes**
Using routes means setting them up as above, then leveraging them in your application (controllers, views, etc.).

- **In Controllers**: Assume the route handles URL mapping; write methods expecting routed requests.
  - Example: For `$route['login']['POST'] = 'users/login';`, create a `Users.php` controller with a `login()` method that handles POST data (e.g., via `$this->input->post()`).

- **Generating URLs**: Use CodeIgniter's `site_url()` or `base_url()` with your route keys for links/buttons.
  - Example: In a view, `<a href="<?= site_url('login'); ?>">Login</a>` points to the routed URL, but your code defines what controller it hits.

- **Testing Routes**:
  - Use your web browser or API tools (e.g., Postman) to hit URLs like `/users/register`.
  - Check `application/logs/log-{date}.php` for errors if routes fail.
  - Add debug: Temporarily reset `$route['404_override']` and use var_dump in a test controller to see parameters.

- **RESTful Usage (Like in Your Code)**: Your routes are set up for an API-like structure. For example:
  - Creating a resource: Send POST to `/lives` → Creates a live event.
  - Reading: GET `/lives/123` → Fetch live event #123.
  - Updating: POST `/lives/123` → Update live event #123.

- **Common Pitfalls & Tips**:
  - **Duplicates**: Avoid overlapping routes (e.g., `lives` and `lives/(\d+)`); put specifics first.
  - **Methods Not Specified**: If a route is a string, it works for all HTTP methods. Use arrays for precision.
  - **For Development**: Enable CodeIgniter's Profiler (`$this->output->enable_profiler(TRUE);`) in a controller to debug routing.
  - **Version Control**: Your routes.php is in version control – changes affect routing live.
  - **Extensions**: If you need advanced features (e.g., namespace support), consider CodeIgniter 4 or third-party libraries, as CI 3 (your code) is older.

If you have specific questions about a route in your file (e.g., why `(\d+)` is used or how to add a new one), provide more details! For CodeIgniter setup, ensure `CI_VERSION` is defined in your index.php.
