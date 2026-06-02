---
audio: false
generated: true
lang: en
layout: post
title: Using GitHub Copilot in Visual Studio Code
translated: false
type: note
---

GitHub Copilot is an AI-powered coding assistant developed by GitHub and OpenAI, designed to enhance developer productivity in Visual Studio Code (VS Code). It provides context-aware code completions, natural language chat, and advanced editing capabilities. This guide walks you through setting up Copilot, exploring its features, and optimizing your workflow with tips and best practices.

## 1. Introduction to GitHub Copilot
GitHub Copilot acts as an AI pair programmer, offering real-time code suggestions, answering coding questions, and automating repetitive tasks. It is powered by large language models trained on vast datasets of public code, enabling it to support numerous programming languages and frameworks, including Python, JavaScript, TypeScript, Ruby, Go, C#, and C++.

Key features include:
- **Code Completions**: Suggests code snippets as you type, from single lines to entire functions.
- **Copilot Chat**: Allows natural language queries to explain code, generate snippets, or debug issues.
- **Agent Mode**: Automates multi-step coding tasks, such as refactoring or creating apps.
- **Custom Instructions**: Tailors suggestions to match your coding style or project requirements.

## 2. Setting Up GitHub Copilot in VS Code

### Prerequisites
- **VS Code**: Download and install Visual Studio Code from the [official website](https://code.visualstudio.com/). Ensure you have a compatible version (any recent version supports Copilot).
- **GitHub Account**: You need a GitHub account with access to Copilot. Options include:
  - **Copilot Free**: Limited completions and chat interactions per month.
  - **Copilot Pro/Pro+**: Paid plans with higher limits and advanced features.
  - **Organization Access**: If provided by your organization, check with your admin for access details.
- **Internet Connection**: Copilot requires an active connection to provide suggestions.

### Installation Steps
1. **Open VS Code**:
   Launch Visual Studio Code on your machine.

2. **Install the GitHub Copilot Extension**:
   - Go to the **Extensions** view (Ctrl+Shift+X or Cmd+Shift+X on macOS).
   - Search for "GitHub Copilot" in the Extensions Marketplace.
   - Click **Install** for the official GitHub Copilot extension. This also installs the Copilot Chat extension automatically.

3. **Sign In to GitHub**:
   - After installation, a prompt may appear in the VS Code Status Bar (bottom-right corner) to set up Copilot.
   - Click the Copilot icon and select **Sign in** to authenticate with your GitHub account.
   - If no prompt appears, open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P) and run the command `GitHub Copilot: Sign in`.
   - Follow the browser-based authentication flow, copying the code provided by VS Code to GitHub.

4. **Verify Activation**:
   - Once signed in, the Copilot icon in the Status Bar should turn green, indicating an active state.
   - If you don’t have a Copilot subscription, you’ll be enrolled in the Copilot Free plan with limited monthly usage.

5. **Optional: Disable Telemetry**:
   - By default, Copilot collects telemetry data. To disable, go to **Settings** (Ctrl+, or Cmd+,), search for `telemetry.telemetryLevel`, and set it to `off`. Alternatively, adjust Copilot-specific settings under `GitHub Copilot Settings`.

> **Note**: If your organization has disabled Copilot Chat or restricted features, contact your admin. For troubleshooting, refer to the [GitHub Copilot Troubleshooting Guide](https://docs.github.com/en/copilot/troubleshooting).[](https://code.visualstudio.com/docs/copilot/setup)

## 3. Core Features of GitHub Copilot in VS Code

### 3.1 Code Completions
Copilot suggests code as you type, from single lines to entire functions or classes, based on the context of your code and file structure.
- **How It Works**:
  - Start typing in a supported language (e.g., JavaScript, Python, C#).
  - Copilot displays suggestions in grayed-out "ghost text."
  - Press **Tab** to accept a suggestion or continue typing to ignore it.
  - Use **Alt+]** (next) or **Alt+[** (previous) to cycle through multiple suggestions.
- **Example**:
  ```javascript
  // Calculate factorial of a number
  function factorial(n) {
  ```
  Copilot might suggest:
  ```javascript
  if (n === 0) return 1;
  return n * factorial(n - 1);
  }
  ```
  Press **Tab** to accept the suggestion.

- **Tips**:
  - Use descriptive function names or comments to guide Copilot (e.g., `// Sort an array in ascending order`).
  - For multiple suggestions, hover over the suggestion to open the Completions Panel (Ctrl+Enter) to view all options.

### 3.2 Copilot Chat
Copilot Chat allows you to interact with Copilot using natural language to ask questions, generate code, or debug issues.
- **Accessing Chat**:
  - Open the **Chat View** from the Activity Bar or use **Ctrl+Alt+I** (Windows/Linux) or **Cmd+Ctrl+I** (macOS).
  - Alternatively, use **Inline Chat** (Ctrl+I or Cmd+I) directly in the editor for context-specific queries.
- **Use Cases**:
  - **Explain Code**: Select a code block, open Inline Chat, and type `explain this code`.
  - **Generate Code**: Type `write a Python function to reverse a string` in the Chat View.
  - **Debugging**: Paste an error message into Chat and ask for a fix.
- **Example**:
  In the Chat View, type:
  ```
  What is recursion?
  ```
  Copilot responds with a detailed explanation, often including code examples in Markdown.

- **Slash Commands**:
  Use commands like `/explain`, `/doc`, `/fix`, `/tests`, or `/optimize` to specify tasks. For example:
  ```
  /explain this function
  ```
  with a selected function will generate a detailed explanation.

### 3.3 Agent Mode (Preview)
Agent Mode enables Copilot to autonomously handle multi-step coding tasks, such as creating apps, refactoring code, or writing tests.
- **How to Use**:
  - Open the **Copilot Edits View** in VS Code Insiders or Stable (if available).
  - Select **Agent** from the mode dropdown.
  - Enter a prompt, e.g., `Create a React form component with name and email fields`.
  - Copilot analyzes your codebase, suggests edits, and can run terminal commands or tests.
- **Capabilities**:
  - Generates code across multiple files.
  - Monitors errors and iterates to fix issues.
  - Integrates new libraries or migrates code to modern frameworks.

> **Note**: Agent Mode is experimental and performs best in smaller repositories. Share feedback via the VS Code GitHub repo.[](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)

### 3.4 Custom Instructions
Customize Copilot to align with your coding style or project requirements.
- **Setup**:
  - Create a `.github/copilot-instructions.md` file in your workspace.
  - Add instructions in Markdown, e.g., `Use snake_case for Python variable names`.
  - Enable custom instructions in **Settings** > **GitHub** > **Copilot** > **Enable custom instructions** (VS Code 17.12 or later).
- **Example**:
  ```markdown
  # Copilot Custom Instructions
  - Use camelCase for JavaScript variables.
  - Prefer async/await over .then() for promises.
  ```
  Copilot will tailor suggestions to these preferences.

### 3.5 Workspace Context with @workspace
Use the `@workspace` command to query your entire codebase.
- **Example**:
  In the Chat View, type:
  ```
  @workspace Where is the database connection string configured?
  ```
  Copilot searches your workspace and references relevant files.

### 3.6 Next Edit Suggestions (Preview)
Copilot predicts and suggests the next logical edit based on your recent changes.
- **How It Works**:
  - As you edit code, Copilot highlights potential next edits.
  - Accept suggestions with **Tab** or modify them via Inline Chat.
- **Use Case**: Ideal for iterative refactoring or completing related code changes.

## 4. Tips and Tricks for Optimizing Copilot Usage

### 4.1 Write Effective Prompts
- Be specific: Instead of `write a function`, try `write a Python function to sort a list of dictionaries by the 'age' key`.
- Provide context: Include framework or library details (e.g., `use React hooks`).
- Use comments: Write `// Generate a REST API endpoint in Express` to guide completions.

### 4.2 Leverage Context
- **Reference Files/Symbols**: Use `#filename`, `#folder`, or `#symbol` in Chat prompts to scope context.
  ```
  /explain #src/utils.js
  ```
- **Drag and Drop**: Drag files or editor tabs into the Chat prompt for context.
- **Attach Images**: In VS Code 17.14 Preview 1 or later, attach screenshots to illustrate issues (e.g., UI bugs).

### 4.3 Use Slash Commands
- `/doc`: Generate documentation for a function.
- `/fix`: Suggest fixes for errors.
- `/tests`: Create unit tests for selected code.
- Example:
  ```
  /tests Generate Jest tests for this function
  ```

### 4.4 Save and Reuse Prompts
- Create a `.prompt.md` file in `.github/prompts/` to store reusable prompts.
- Example:
  ```markdown
  # React Component Prompt
  Generate a React functional component with Tailwind CSS styling. Ask for component name and props if not provided.
  ```
- Attach the prompt in Chat to reuse it across projects.

### 4.5 Choose the Right Model
- Copilot supports multiple language models (e.g., GPT-4o, Claude Sonnet).
- Select models in the Chat View dropdown for faster coding or deeper reasoning.
- For complex tasks, Claude Sonnet may perform better in Agent Mode.[](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)

### 4.6 Index Your Workspace
- Enable workspace indexing for faster, more accurate code searches.
- Use a remote index for GitHub repositories or a local index for large codebases.

## 5. Best Practices
- **Review Suggestions**: Always verify Copilot’s suggestions for accuracy and alignment with your project’s standards.
- **Combine with IntelliCode**: In Visual Studio, Copilot complements IntelliCode for enhanced completions.[](https://devblogs.microsoft.com/visualstudio/github-copilot-in-visual-studio-2022/)
- **Check Security**: Copilot may suggest code with vulnerabilities. Review suggestions, especially in sensitive projects, and check with your organization’s policies.[](https://medium.com/%40codebob75/how-to-use-copilot-in-visual-studio-a-step-by-step-guide-b2a5db3b54ba)
- **Use Meaningful Names**: Descriptive variable and function names improve suggestion quality.
- **Iterate with Chat**: Refine prompts if initial suggestions are off-target.
- **Monitor Usage Limits**: With Copilot Free, track your monthly completions and chat interactions via the GitHub account settings or Copilot badge in VS Code.[](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-free-plan?view=vs-2022)

## 6. Troubleshooting Common Issues
- **Copilot Inactive**: Ensure you’re signed in with a GitHub account that has Copilot access. Refresh credentials via the Copilot Status Bar dropdown.
- **No Suggestions**: Check your internet connection or switch to a supported language. Adjust settings under **Tools** > **Options** > **GitHub Copilot**.
- **Limited Functionality**: If you hit the Copilot Free usage limit, you’ll revert to IntelliCode suggestions. Upgrade to a paid plan or check your status.[](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-free-plan?view=vs-2022)
- **Network Issues**: See the [GitHub Copilot Troubleshooting Guide](https://docs.github.com/en/copilot/troubleshooting).

## 7. Advanced Use Cases
- **Database Queries**: Ask Copilot to generate SQL queries (e.g., `Write a SQL query to join two tables`).
- **API Development**: Request API endpoint code (e.g., `Create a Flask route to handle POST requests`).
- **Unit Testing**: Use `/tests` to generate tests for frameworks like Jest or Pytest.
- **Refactoring**: Use Agent Mode to refactor code across files (e.g., `Migrate this jQuery code to React`).

## 8. Privacy and Security Considerations
- **Data Usage**: Copilot transmits code snippets to GitHub servers in real-time to generate suggestions but does not retain them (Copilot for Business discards snippets immediately).[](https://medium.com/%40codebob75/how-to-use-copilot-in-visual-studio-a-step-by-step-guide-b2a5db3b54ba)
- **Public Code Matching**: Copilot may suggest code matching public GitHub repositories. Enable code referencing to view license details.[](https://learn.microsoft.com/en-us/visualstudio/ide/visual-studio-github-copilot-extension?view=vs-2022)
- **Organizational Policies**: Check if your organization allows Copilot usage, as some disable Chat or restrict suggestions.[](https://docs.github.com/en/copilot/quickstart)
- **Telemetry**: Disable telemetry in VS Code settings if desired.[](https://code.visualstudio.com/docs/copilot/setup)

## 9. Resources for Further Learning
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Copilot Quickstart](https://code.visualstudio.com/docs/copilot/copilot-quickstart)
- [Copilot Chat Tutorial](https://code.visualstudio.com/docs/copilot/copilot-chat)
- [VS Code Copilot Series on YouTube](https://www.youtube.com/playlist?list=PLj6YeMhvp2S6X0vF4TrRkpZ7GIqM3oPWp)
- [GitHub Copilot FAQs](https://docs.github.com/en/copilot/faq)

## 10. Conclusion
GitHub Copilot in VS Code is a powerful tool that streamlines coding by providing intelligent suggestions, answering questions, and automating complex tasks. By setting it up correctly, leveraging its features, and following best practices, you can significantly boost your productivity and focus on creative coding tasks. Experiment with Copilot’s capabilities, customize it to your workflow, and stay mindful of security and usage limits to make the most of this AI pair programmer.
