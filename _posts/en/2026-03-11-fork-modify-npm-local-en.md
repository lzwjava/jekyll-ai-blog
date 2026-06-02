---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fork and Modify NPM Packages Locally
translated: false
type: note
---

I'll search for the best practices on forking and modifying npm packages.Now let me search for more specific information about npm link and path overrides.---

**Question:** How do I fork an NPM package like form-data, manually edit its code to debug or add functionality, or fix bugs? Can I use path overrides to do this?

**Answer:**

There are several methods to fork and modify an NPM package locally. Here are the main approaches:

## Method 1: Using npm link (Symlink Approach)

The npm link command creates a symbolic link between your local package and a project that depends on it. This is the quickest way to test changes during development.

**Steps:**

1. **Clone the repository**: Clone the repository of the package you want to modify by forking it first and then cloning the fork.

   ```bash
   git clone https://github.com/your-username/form-data.git
   cd form-data
   ```

2. **Install dependencies and build**:
   ```bash
   npm install
   npm run build  # Check package.json for the build script
   ```

3. **Create the global link** in the package directory:
   ```bash
   npm link
   ```

4. **Link to your project**: In your main project directory:
   ```bash
   npm link form-data
   ```

5. **Make changes**: Edit the code in the forked package and test immediately.

6. **Clean up when done**:
   ```bash
   npm unlink form-data      # in your main project
   npm unlink                 # in the package directory
   ```

## Method 2: Direct Path Override in package.json

You can point to a local folder directly using relative paths:

```json
{
  "dependencies": {
    "form-data": "file:../path-to-local-form-data"
  }
}
```

Then run:
```bash
npm install
```

This creates a link to the actual folder inside node_modules and saves you additional steps of packaging and installing after every change.

## Method 3: GitHub URL with Branch Pointer

Instead of using the github url of the fork of the library, include the branch you were working on, for example: yarn upgrade form-data@https://github.com/yourname/form-data.git#your-branch-name.

In package.json:
```json
{
  "dependencies": {
    "form-data": "yourname/form-data#feature-branch"
  }
}
```

## Method 4: GitHub Tarball URL

You can point your package.json to the download url of your fork on GitHub by using a tarball link with a specific commit hash:

```json
{
  "dependencies": {
    "form-data": "https://github.com/yourname/form-data/tarball/abc123def456"
  }
}
```

## Method 5: npm pack (Best for Pre-publication Testing)

You can use npm pack as an alternative to symlinks, which creates a .tgz file and provides a great approach to testing local components because it mimics the actual process of publishing to npm.

```bash
cd form-data
npm run build
npm pack
cd ../your-project
npm install ../form-data/form-data-1.0.0.tgz
```

## Method 6: Build Files in Git

To ensure the package works correctly, all build files within the forked repo must not be hidden from source control after building. Usually an npm run build command is sufficient, and you will need to remove the build output directory from .gitignore.

## Important Considerations

- Make sure to check the license of the library you would like to modify and familiarize yourself with building the library by checking the readme or package.json scripts.

- When you link a package, it doesn't automatically link its dependencies. If your package depends on something that's not installed in your project, you might need to run npm install in your linked package directory.

- When running npm link commands, the current node version used is taken into account. If you want to test the library in different node environments, you need to repeat the process for each node version.

---

**References:**

- https://schalkneethling.com/posts/using-npm-link-for-local-package-development/
- https://medium.com/@ruben.alapont/npm-link-developing-and-testing-local-npm-packages-b50a32b50c4a
- https://teambrookvale.com.au/articles/modifying-npm-packages-the-right-way
- https://www.pluralsight.com/resources/blog/guides/how-to-use-forked-npm-dependencies
- https://medium.com/@chrisdmasters/how-to-fork-a-dependency-and-use-it-locally-in-a-project-707c80d3449c
- https://dev.to/one-beyond/different-approaches-to-testing-your-own-packages-locally-npm-link-4hoj
- https://maecapozzi.com/blog/how-to-locally-test-an-npm-package
- https://dev.to/azophy/how-to-edit-replace-npm-package-dependency-1b5e
- https://nickconfrey.medium.com/how-to-edit-a-node-module-locally-1cb8d3530d78
- http://debuggable.com/posts/how-to-fork-patch-npm-modules:4e2eb9f3-e584-44be-b1a9-3db7cbdd56cb
