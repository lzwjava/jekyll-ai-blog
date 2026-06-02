---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter REST API Configuration Guide
translated: false
type: note
---

Below, I'll provide a clear, step-by-step guide to understanding and using the CodeIgniter REST API configuration file you shared (`application/config/rest.php`). This file configures the behavior of the REST_Controller library (a popular PHP library for building RESTful APIs in CodeIgniter), such as Phil Sturgeon's REST library (now maintained as part of the CodeIgniter framework in some versions).

I'll explain:

- What the library does and key prerequisites.
- How to set up and use it.
- Key configuration options from your file (with examples).
- A simple usage example.
- Tips for common pitfalls and security.

If your question is specifically about one aspect (e.g., authentication or limits), feel free to clarify for more targeted advice!

### 1. **Prerequisites and Setup**

- **What is it?** This is the REST_Controller library for CodeIgniter (a PHP framework). It lets you build RESTful APIs (e.g., endpoints that respond in JSON/XML on GET/POST requests) by extending your controllers from `REST_Controller`. Your config file controls global settings like authentication, response formats, rate limiting, and security.

- **Requirements:**
  - CodeIgniter 3.x (or compatible version; this config is for older versions around 3.x).
  - Install the REST_Controller library if not already in your CodeIgniter install (you can download it from GitHub: `chriskacerguis/codeigniter-restserver`). Place the library files in `application/libraries/` and autoload it in `application/config/autoload.php`:

       ```php
       $autoload['libraries'] = ['rest_controller'];
       ```

  - Database setup (optional; needed for features like API keys, logging, or limits). Run the SQL schemas provided in the config comments (e.g., for tables like `keys`, `logs`, `access`, `limits`).
  - Enable pretty URLs in CodeIgniter (`application/config/routes.php`) for clean API endpoints like `/api/users`.
  - Your `rest.php` config file should be placed in `application/config/` and autoloaded in `application/config/autoload.php`:

       ```php
       $autoload['config'] = ['rest'];
       ```

- **Basic Installation Steps:**
     1. Download and unzip CodeIgniter.
     2. Add the REST_Controller library files.
     3. Copy your provided `rest.php` to `application/config/`.
     4. Set up routes in `routes.php` (e.g., `$route['api/(:any)'] = 'api/$1';` to map `/api/users` to a controller).
     5. Create API controllers (see example below).
     6. Test with a tool like Postman or curl.

### 2. **Key Configuration Options**

I'll summarize the main settings from your config file, grouped by purpose. These control global behavior. You can modify them to suit your needs (e.g., enable HTTPS or change default formats).

- **Protocol and Output:**
  - `$config['force_https'] = FALSE;`: Forces all API calls to use HTTPS. Set to `TRUE` for production security.
  - `$config['rest_default_format'] = 'json';`: Default response format (options: json, xml, csv, etc.). Requests can override via URL (e.g., `/api/users.format=xml`).
  - `$config['rest_supported_formats']`: List of allowed formats. Remove unwanted ones for security.
  - `$config['rest_ignore_http_accept'] = FALSE;`: Ignore client HTTP Accept headers to speed up responses (useful if you always use `$this->rest_format` in code).

- **Authentication (Security):**
  - `$config['rest_auth'] = FALSE;`: Main auth mode. Options:
    - `FALSE`: No auth required.
    - `'basic'`: HTTP Basic Auth (username/password in base64 headers).
    - `'digest'`: More secure digest auth.
    - `'session'`: Check for a PHP session variable.
  - `$config['auth_source'] = 'ldap';`: Where to check credentials (e.g., config array, LDAP, custom library).
  - `$config['rest_valid_logins'] = ['admin' => '1234'];`: Simple username/password array (ignored if using LDAP).
  - `$config['auth_override_class_method']`: Override auth for specific controllers/methods (e.g., `'users' => 'view' => 'basic'`).
  - `$config['auth_library_class/function']`: If using a custom library, specify the class/method for validation.
  - IP controls:
    - `$config['rest_ip_whitelist_enabled/blacklist_enabled']`: Base IP filtering on your API.
    - Useful for restricting access (e.g., whitelist your app's IPs).

- **API Keys (Optional Security Layer):**
  - `$config['rest_enable_keys'] = FALSE;`: Enables API key checking (stored in DB table `keys`). Clients must send keys in headers (e.g., `X-API-KEY`).
  - `$config['rest_key_column/name/length']`: Customize key fields and header name.
  - Pair with `$config['rest_enable_access']` to restrict keys to specific controllers/methods.

- **Logging and Limits:**
  - `$config['rest_enable_logging/limits'] = FALSE;`: Enable DB-based logging of requests (URI, params, etc.) or rate limiting (e.g., X calls per hour per key).
  - Tables: `logs`, `limits` (run the SQL in comments to create them).
  - `$config['rest_limits_method']`: How to apply limits (by API key, URL, etc.).
  - Customize per method in controllers (e.g., `$this->method['get']['limit'] = 100;`).

- **Other:**
  - `$config['rest_ajax_only'] = FALSE;`: Restrict to AJAX requests only (returns 505 error otherwise).
  - `$config['rest_language'] = 'english';`: Language for error messages.

To modify: Edit `rest.php` and restart your app. Test changes carefully!

### 3. **How to Use It: Step-by-Step Usage**

Once set up, create API endpoints by building controllers that extend `REST_Controller`. Here's a high-level process:

1. **Create a Controller:**
   - In `application/controllers/`, create `Api.php` (or e.g., `Users.php` for a specific resource):

     ```php
     <?php
     defined('BASEPATH') OR exit('No direct script access allowed');
     require_once(APPPATH . 'libraries/REST_Controller.php');

     class Api extends REST_Controller {
         public function __construct() {
             parent::__construct();
             // Optional: Set auth, limits per method
             $this->load->database();
             $this->method['index_get']['limit'] = 100; // 100 requests/hour
         }

         // GET /api
         public function index_get() {
             $data = ['message' => 'Welcome to the API', 'status' => 'success'];
             $this->response($data, REST_Controller::HTTP_OK);
         }

         // POST /api/users
         public function users_post() {
             $data = $this->input->post(); // Get POST data
             if (empty($data['name'])) {
                 $this->response(['error' => 'Name required'], REST_Controller::HTTP_BAD_REQUEST);
             }
             // Process (e.g., insert into DB)
             $this->response(['message' => 'User created'], REST_Controller::HTTP_CREATED);
         }

         // PUT /api/users/{id}
         public function users_put($id) {
             $data = $this->put(); // Get PUT data
             // Update user with $id
             $this->response(['message' => 'User updated'], REST_Controller::HTTP_OK);
         }

         // etc. for DELETE
     }
     ```

2. **Send Requests:**
   - Use any HTTP client:
     - GET: `curl http://yourdomain.com/api` → Returns JSON {"message": "Welcome to the API", "status": "success"}
     - POST: `curl -X POST http://yourdomain.com/api/users -d "name=John"` → Creates a user.
   - Include headers if using auth/keys (e.g., `Authorization: Basic base64(user:pass)` or `X-API-KEY: yourkey`).

3. **Test and Debug:**
   - Check CodeIgniter logs for errors.
   - If auth fails, ensure credentials are set correctly.
   - For limits/logging, query your DB tables.

### 4. **Common Tips and Best Practices**

- **Security:** Always use HTTPS in production (`force_https = TRUE`). Enable keys if exposing to external clients. Sanitize inputs to prevent SQL injection.
- **Errors:** Responses include `status` and `error` fields (customizable in config). Use CodeIgniter's profiler for debugging.
- **Performance:** If logging/limits are enabled, your DB will handle queries—monitor for slow performance.
- **Upgrading:** This config is for older CodeIgniter versions. For CI 4, use their built-in API resources (this setup may need tweaks).
- **Troubleshooting:**
  - "No response"? Check routes, autoload, and library paths.
  - Auth issues? Verify `$auth_source` and credentials.
  - Format errors? Ensure your format is in `rest_supported_formats`.
- **Resources:** Docs at codeigniter-restserver.org. For CI4 migration, see official docs.

If this doesn't answer your exact question or you need code for a specific use case (e.g., enabling OAuth), provide more details!
