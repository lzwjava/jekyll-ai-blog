---
audio: false
generated: true
lang: en
layout: post
title: Installation Source of npm Packages
translated: false
type: note
---

To change the installation source of the `@ngx-formly/bootstrap` package from a local `.tgz` file to the npm registry, follow these steps:

### 1. Uninstall the Locally Installed Package
Since you previously installed `@ngx-formly/bootstrap` from a local `.tgz` file, it’s currently in your project’s `node_modules` directory. To remove it, run the following command in your terminal:

```bash
npm uninstall @ngx-formly/bootstrap
```

This command removes the package from `node_modules`. If the package was manually added to your `package.json` file under `dependencies` or `devDependencies`, this will also remove it from there. If it wasn’t listed in `package.json` (common when installing from a `.tgz` file without saving), it will still be removed from your project.

### 2. Install the Package from the npm Registry
Now, install the package from the npm registry by running:

```bash
npm install @ngx-formly/bootstrap
```

This command fetches the latest version of `@ngx-formly/bootstrap` from the npm registry (typically `https://registry.npmjs.org/` unless you’ve configured a different registry) and installs it into your `node_modules` directory. It will also add the package to your `package.json` file under `dependencies` by default (in recent npm versions), ensuring it’s tracked as part of your project.

### Optional: Verify the Registry (If Needed)
If you’ve previously changed your npm registry and want to ensure it’s set to the default npm registry, you can check it with:

```bash
npm config get registry
```

If the output is `https://registry.npmjs.org/`, you’re using the default registry, and the `npm install` command will work as expected. If it’s set to a different registry and you want to revert to the default, run:

```bash
npm config set registry https://registry.npmjs.org/
```

However, since you mentioned you’ve already configured your registry, this step may not be necessary.

### Notes
- **Version Control**: If you need the same version as the one in your `.tgz` file, check the version number in `node_modules/@ngx-formly/bootstrap/package.json` before uninstalling. Then, install that specific version with:
  ```bash
  npm install @ngx-formly/bootstrap@<version>
  ```
  If you don’t specify a version, the latest version from the registry will be installed.
- **Dependency Type**: If you want the package as a development dependency instead of a regular dependency, use:
  ```bash
  npm install @ngx-formly/bootstrap --save-dev
  ```

By following these steps, you’ll successfully switch `@ngx-formly/bootstrap` from being installed via a local `.tgz` file to being installed from the npm registry.
