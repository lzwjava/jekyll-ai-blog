---
audio: false
generated: true
lang: en
layout: post
title: Using Webpack as Module Bundler
translated: false
type: note
---

### Key Points
- It seems likely that to use webpack version 1.13.2 and webpack-dev-server version 1.14.0, you need to set up a Node.js project with specific configurations.
- Research suggests installing these versions via npm, creating a configuration file, and running a development server for live updates.
- The evidence leans toward ensuring an index.html file is in place and the setup includes proper file paths for bundling.

### Installation and Setup
To get started, ensure Node.js is installed from [nodejs.org](https://nodejs.org). Create a project directory, initialize it with npm, and install the specified versions:

- Run `npm init -y` to set up a package.json file.
- Install with `npm install webpack@1.13.2` and `npm install webpack-dev-server@1.14.0`.

### Configuration
Create a `webpack.config.js` file to define how your files are bundled. A basic setup includes:
- Entry point (e.g., `./src/index.js`).
- Output path (e.g., `dist` directory with `bundle.js`).
- Dev server settings, such as `contentBase` for static files.

### Running the Development Server
Start the server with `npx webpack-dev-server` or `./node_modules/.bin/webpack-dev-server` if npx isn't available. Access it at [http://localhost:8080](http://localhost:8080) to see your application, which will auto-update on changes.

### Unexpected Detail
An unexpected aspect is that these older versions require specific configurations like `contentBase` instead of modern `static`, and the setup might need manual adjustments for file serving, unlike newer versions with more automation.

---

### Survey Note: Detailed Guide on Using Webpack 1.13.2 and Webpack-Dev-Server 1.14.0

This comprehensive guide provides a detailed walkthrough for setting up and using webpack version 1.13.2 alongside webpack-dev-server version 1.14.0, focusing on a development environment suitable for JavaScript projects. Given the age of these versions, certain configurations and behaviors differ from modern standards, and this note aims to cover all necessary steps for a layman to follow, ensuring clarity and completeness.

#### Background and Context
Webpack is a module bundler for JavaScript, historically used to compile and bundle files for web applications, managing dependencies and optimizing for production. Webpack-dev-server, a companion tool, provides a development server with live reload capabilities, ideal for iterative development. The versions specified, 1.13.2 for webpack and 1.14.0 for webpack-dev-server, are from 2016, indicating older but still functional setups, possibly for legacy project compatibility.

#### Step-by-Step Installation and Setup
To begin, ensure Node.js is installed, as it's required for npm, the package manager we'll use. You can download it from [nodejs.org](https://nodejs.org). The current time, 09:45 AM PST on Monday, March 03, 2025, is irrelevant to the setup but noted for context.

1. **Create a Project Directory**: Open your terminal and create a new directory, for example, "myproject":
   - Command: `mkdir myproject && cd myproject`

2. **Initialize npm Project**: Run `npm init -y` to create a `package.json` file with default settings, setting up your project for npm dependencies.

3. **Install Specific Versions**: Install the required versions using npm:
   - Command: `npm install webpack@1.13.2`
   - Command: `npm install webpack-dev-server@1.14.0`
   - These commands add the specified versions to your `node_modules` and update `package.json` under `dependencies`.

#### Directory Structure and File Creation
For the development server to function, you'll need a basic directory structure:
- Create a `public` directory for static files: `mkdir public`
- Create a `src` directory for your application code: `mkdir src`

Within `public`, create an `index.html` file, essential for serving your application:
```html
<html>
<body>
<script src="/bundle.js"></script>
</body>
</html>
```
This file references `bundle.js`, which webpack will generate and serve.

In `src`, create an `index.js` file with basic content:
```javascript
console.log('Hello, World!');
```
This is your entry point, which webpack will bundle.

#### Configuration File Setup
Create a `webpack.config.js` file in the root directory to configure webpack:
```javascript
const path = require('path');
module.exports = {
    entry: './src/index.js',
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    devServer: {
        contentBase: path.join(__dirname, 'public')
    }
};
```
- `entry`: Specifies the starting point (`src/index.js`).
- `output`: Defines where the bundled file goes (`dist/bundle.js`).
- `devServer.contentBase`: Points to the `public` directory for serving static files like `index.html`.

Note that in version 1.14.0, `contentBase` is used instead of the modern `static`, reflecting the older API.

#### Running the Development Server
To start the development server, use:
- Preferred: `npx webpack-dev-server`
- Alternative (if npx isn't available): `./node_modules/.bin/webpack-dev-server`

This command launches a server, typically accessible at [http://localhost:8080](http://localhost:8080). The server runs in-memory, meaning files aren't written to disk but served dynamically, with live reload enabled for development convenience.

#### Operational Details and Considerations
- **Accessing the Application**: Open your browser to [http://localhost:8080](http://localhost:8080). You should see your `index.html`, which loads `bundle.js` and executes your JavaScript, logging "Hello, World!" to the console.
- **Live Updates**: Edit files in `src`, and the server will recompile and reload the browser automatically, a key feature of webpack-dev-server for iterative development.
- **Port Conflicts**: If port 8080 is in use, the server might fail. You can specify a different port in `webpack.config.js` under `devServer.port`, e.g., `port: 9000`.

#### File Serving and Path Considerations
Given the versions, `devServer.contentBase` serves files from the specified directory (defaulting to the current directory if not set). Ensure `index.html` is in `public` for it to be served at the root. The script tag `<script src="/bundle.js"></script>` works because `output.publicPath` defaults to '/', and `output.filename` is 'bundle.js', making it accessible at `/bundle.js`.

An important detail is that webpack-dev-server 1.14.0 requires an HTML file for serving, and it doesn't inject scripts automatically, so manual inclusion in `index.html` is necessary. This contrasts with modern setups where plugins like `html-webpack-plugin` might automate this.

#### Compatibility and Limitations
These versions are from 2016, and while functional, they lack modern features and security patches. Compatibility with current Node.js versions (as of March 2025) should be checked, as older versions might require Node.js 6 or 8, which are no longer supported. Testing on a current Node.js version (e.g., 20.x) is recommended, but be prepared for potential deprecation warnings.

#### Table: Version Details and Usage
Below is a table summarizing key version information and usage notes:

| Component               | Version | Release Year | Key Usage Notes                                      |
|-------------------------|---------|--------------|-----------------------------------------------------|
| Webpack                 | 1.13.2  | 2016         | Module bundler, requires configuration for entry/output |
| Webpack-Dev-Server      | 1.14.0  | 2016         | Development server, uses `contentBase` for static files |

#### Advanced Configuration Options
For users needing more, consider enabling hot module replacement by adding `hot: true` to `devServer`:
```javascript
devServer: {
    contentBase: path.join(__dirname, 'public'),
    hot: true
}
```
This allows module updates without full page reloads, enhancing development speed.

#### Conclusion
This setup provides a basic but functional development environment using webpack 1.13.2 and webpack-dev-server 1.14.0. Given their age, expect differences from modern workflows, such as manual file serving and potential compatibility issues with current tools. For production, these versions are not recommended due to lack of updates, but for legacy project maintenance, this guide should suffice.

#### Key Citations
- [Webpack documentation detailed setup guide](https://webpack.js.org/)
- [Webpack-dev-server configuration options](https://webpack.js.org configuration/dev-server/)
