---
audio: false
generated: true
lang: en
layout: post
title: Angular Errors
translated: false
type: note
---

When working with Angular, developers often encounter specific exceptions and errors. Below is a categorized list of common issues, their causes, and solutions:

---

### **Template & Data Binding Errors**

1. **`ExpressionChangedAfterItHasBeenCheckedError`**
   - **Cause**: Changing component data after Angular's change detection cycle (e.g., in `ngAfterViewInit` or `ngOnChanges`).
   - **Fix**: Use `ChangeDetectorRef.detectChanges()` or ensure data changes occur before change detection completes.

2. **`Cannot read property 'X' of undefined`**
   - **Cause**: Accessing uninitialized object properties in templates (e.g., `{{ user.name }}` when `user` is `null`).
   - **Fix**: Use the safe navigation operator (`{{ user?.name }}`) or initialize objects properly.

3. **`Can't bind to 'X' since it isn't a known property of 'Y'`**
   - **Cause**: Missing component/directive declaration or typo in property name.
   - **Fix**: Import the directive/component into the module or check for typos.

---

### **Dependency Injection (DI) Errors**

4. **`NullInjectorError: No provider for XService`**
   - **Cause**: Service not provided in module/component or circular dependency.
   - **Fix**: Add the service to the `providers` array of the module/component.

5. **`No value accessor for form control`**
   - **Cause**: Custom form control missing `ControlValueAccessor` implementation or incorrect `formControlName` binding.
   - **Fix**: Implement `ControlValueAccessor` for custom controls or check form bindings.

---

### **TypeScript & Build Errors**

6. **`Type 'X' is not assignable to type 'Y'`**
   - **Cause**: Type mismatches (e.g., wrong data type passed to a component).
   - **Fix**: Ensure types align or use type assertions (if intentional).

7. **`ERROR in Cannot find module 'X'`**
   - **Cause**: Missing npm package or incorrect import path.
   - **Fix**: Install the package (`npm install X`) or correct the import path.

---

### **Component & Module Errors**

8. **`Component is not part of any NgModule`**
   - **Cause**: Component not declared in a module or module not imported.
   - **Fix**: Add the component to `declarations` in its module or import the module.

9. **`ViewDestroyedError: Attempt to use a destroyed view`**
   - **Cause**: Subscriptions or async operations running after component destruction.
   - **Fix**: Unsubscribe in `ngOnDestroy` or use the `async` pipe.

---

### **HTTP & API Errors**

10. **`HttpClient provider not found`**
    - **Cause**: Missing `HttpClientModule` import in the module.
    - **Fix**: Import `HttpClientModule` in `AppModule`.

11. **CORS Issues**
    - **Cause**: Backend not allowing requests from the frontend origin.
    - **Fix**: Configure CORS on the server or use a proxy in Angular (`proxy.conf.json`).

---

### **Routing Errors**

12. **`Route not found`**
    - **Cause**: Incorrect route definition or missing lazy-loaded module.
    - **Fix**: Check route paths and lazy-load syntax (`loadChildren: () => import(...)`).

---

### **Form Errors**

13. **`FormControl not found`**
    - **Cause**: Using `formControlName` without wrapping in a `[formGroup]`.
    - **Fix**: Ensure the parent form group is initialized and bound.

---

### **Miscellaneous**

14. **`Maximum call stack size exceeded`**
    - **Cause**: Recursive functions or circular dependencies.
    - **Fix**: Refactor code to eliminate recursion/circular references.

15. **`Zone.js Promise rejection`**
    - **Cause**: Unhandled promise rejections.
    - **Fix**: Add `.catch()` or use `try/catch` with `async/await`.

16. **AOT Compilation Errors**
    - **Cause**: Template syntax incompatible with Ahead-of-Time compilation.
    - **Fix**: Avoid complex expressions in templates or use Angular-compatible syntax.

---

### **Best Practices to Avoid Errors**

- Use the `async` pipe for observables to auto-unsubscribe.
- Enable strict TypeScript checks (`strict: true` in `tsconfig.json`).
- Run `ng lint` to catch code quality issues.
- Test with `--prod` flag to simulate AOT builds.

By addressing these common issues methodically, you can streamline Angular development and reduce debugging time.
