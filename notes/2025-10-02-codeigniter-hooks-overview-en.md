---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: CodeIgniter Hooks Overview
translated: false
type: note
---

### What Are Hooks in CodeIgniter?

Hooks in CodeIgniter are a way to extend the framework's functionality without modifying its core files. They allow you to run custom code at specific points in the execution cycle, such as before or after loading controllers, overriding output, or caching. This preserves upgradeability by separating your code from the official codebase.

Hooks are defined in `application/config/hooks.php` and enabled in `application/config/config.php` by setting `$config['enable_hooks'] = TRUE;`.

### Enabling Hooks

1. Open `application/config/config.php`.
2. Set the config variable:
   ```php
   $config['enable_hooks'] = TRUE;
   ```
   This tells CodeIgniter to check and execute the hooks file.

### Defining Hooks

Hooks are configured as an array of arrays in `application/config/hooks.php`. Each hook array specifies:
- `class`: (Required) The class name (must match the filename).
- `function`: (Required) The method name in the class.
- `filename`: (Required) The filename of the class (without .php).
- `filepath`: (Optional) The folder path to the file, defaulting to `application/hooks/`.
- `params`: (Optional) An array of parameters to pass to the method.

Place your hook classes in `application/hooks/`.

### Hook Points

CodeIgniter provides these predefined points where hooks can execute:
- **pre_system**: Runs before the system is loaded (nothing else has run yet).
- **pre_controller**: Runs right before the controller is called.
- **post_controller_constructor**: Runs after the controller is instantiated but before its methods execute.
- **post_controller**: Runs after the controller finishes.
- **display_override**: Runs instead of outputting to the browser (overrides _display create/exit controller file).
- **cache_override**: Runs instead of loading the cache (overrides _display the cache).
- **post_system**: Runs after the web page is completely sent to the browser.

### Example Usage

Suppose you want to log every request before the controller runs. Create a hook for `pre_controller`.

1. Create the file `application/hooks/my_hook.php`:
   ```php
   <?php
   class My_hook {
       public function log_request() {
           // Example: Log to a file or database
           log_message('info', 'Controller about to be called: ' . $this->uri->uri_string());
       }
   }
   ```

2. In `application/config/hooks.php`, add:
   ```php
   $hook['pre_controller'] = array(
       'class' => 'My_hook',
       'function' => 'log_request',
       'filename' => 'my_hook.php',
       'filepath' => 'hooks', // Optional, defaults to application/hooks/
       'params' => array() // Optional parameters
   );
   ```

Now, every time a controller is about to run, `log_request` will execute.

### Best Practices
- Use hooks sparingly; if possible, extend controllers or use libraries instead.
- Always test hooks in a development environment to ensure they don't interfere with core logic.
- For more details, refer to the official CodeIgniter user guide on hooks.
