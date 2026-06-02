---
audio: false
generated: true
lang: en
layout: post
title: Install and Use Gemini CLI
translated: false
type: note
---

Below is a concise guide to installing, setting up, and using the **Google Gemini CLI**, an open-source AI agent that integrates Gemini’s capabilities into your terminal for coding, task automation, and more. This guide is based on the latest available information as of June 29, 2025.[](https://github.com/google-gemini/gemini-cli)[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)[](https://gemini-cli.click/)

---

## **Google Gemini CLI Guide**

### **What is Gemini CLI?**

Gemini CLI is an open-source command-line tool developed by Google that brings the power of the Gemini 2.5 Pro model (with a 1 million token context window) to your terminal. It supports coding, debugging, content generation, task automation, and multimodal tasks like image and video generation. It’s free to use with a Google account and integrates with tools like Google Search and Model Context Protocol (MCP) servers.[](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)

---

### **Prerequisites**

- **Node.js**: Version 18 or higher. Check with `node -v`. Install from [nodejs.org](https://nodejs.org) if needed.
- **Google Account**: Required for free access to Gemini 2.5 Pro (60 requests/minute, 1,000 requests/day).[](https://medium.com/google-cloud/getting-started-with-gemini-cli-8cc4674a1371)[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)
- (Optional) **API Key**: For higher limits or specific models, generate one from [Google AI Studio](https://aistudio.google.com).[](https://github.com/google-gemini/gemini-cli)
- (Optional) **Docker**: For MCP server integration (e.g., GitHub tools).[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials.md)

---

### **Installation**

There are two ways to get started with Gemini CLI:

1. **Install Globally**:

   ```bash
   npm install -g @google/gemini-cli
   gemini
   ```

   This installs the CLI globally and runs it with the `gemini` command.[](https://gemini-cli.click/)

2. **Run Without Installing**:

   ```bash
   npx https://github.com/google-gemini/gemini-cli
   ```

   This runs the CLI directly without installation, ideal for testing.[](https://www.bleepingcomputer.com/news/artificial-intelligence/google-releases-gemini-cli-with-free-gemini-25-pro/)

---

### **Setup**

1. **Launch the CLI**:
   - Run `gemini` in your terminal.
   - On first run, select a theme (e.g., ASCII, dark, light) and press Enter.[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)

2. **Authenticate**:
   - Choose **Login with Google** for free access (recommended for most users).
   - A browser window will open; sign in with your Google account.
   - Alternatively, use an API key:
     - Generate a key from [Google AI Studio](https://aistudio.google.com).
     - Set it as an environment variable:

       ```bash
       export GEMINI_API_KEY=YOUR_API_KEY
       ```

     - This is useful for higher limits or enterprise use.[](https://github.com/google-gemini/gemini-cli)[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)

3. **Navigate to Your Project**:
   - Run `gemini` in your project’s root directory to provide context for code-related tasks.[](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)

---

### **Basic Usage**

Gemini CLI operates in an interactive Read-Eval-Print Loop (REPL) environment. Type commands or natural language prompts to interact with the Gemini model. Here are some common tasks:

1. **Code Explanation**:
   - Navigate to a project folder and run:

     ```bash
     gemini
     ```

   - Prompt: `Explain the architecture of this project` or `Describe the main function in main.py`.
   - The CLI reads files and provides a structured explanation.[](https://www.datacamp.com/tutorial/gemini-cli)

2. **Code Generation**:
   - Prompt: `Create a simple to-do app in HTML, CSS, and JavaScript`.
   - The CLI generates the code and can save it to files if requested.[](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)

3. **Debugging**:
   - Paste an error message or stack trace and ask: `What’s causing this error?`.
   - The CLI analyzes the error and suggests fixes, potentially using Google Search for additional context.[](https://ts2.tech/en/everything-you-need-to-know-about-google-gemini-cli-features-news-and-expert-insights/)

4. **File Management**:
   - Prompt: `Organize my PDF invoices by month of expenditure`.
   - The CLI can manipulate files or convert formats (e.g., images to PNG).[](https://github.com/google-gemini/gemini-cli)

5. **GitHub Integration**:
   - Use MCP servers for GitHub tasks (e.g., listing issues):
     - Configure a GitHub MCP server in `.gemini/settings.json` with a Personal Access Token (PAT).[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials.md)
     - Prompt: `Get all open issues assigned to me in the foo/bar repo`.
   - Run `/mcp` to list configured MCP servers and tools.[](https://medium.com/google-cloud/getting-started-with-gemini-cli-8cc4674a1371)

6. **Multimodal Tasks**:
   - Generate media with tools like Imagen or Veo:
     - Prompt: `Create a short video of a cat’s adventures in Australia using Veo`.[](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)

---

### **Key Features**

- **Context Files (GEMINI.md)**: Add a `GEMINI.md` file in your project root to define coding styles, project rules, or preferences (e.g., “Use async/await for JavaScript”). The CLI uses this for tailored responses.[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md)[](https://ts2.tech/en/everything-you-need-to-know-about-google-gemini-cli-features-news-and-expert-insights/)
- **Built-in Tools**:
  - `/tools`: List available tools (e.g., Google Search, file operations).[](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)
  - `/compress`: Summarize chat context to save tokens.[](https://www.datacamp.com/tutorial/gemini-cli)
  - `/bug`: File issues directly to the Gemini CLI GitHub repo.[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md)
- **Non-Interactive Mode**: For scripting, pipe commands:

   ```bash
   echo "Write a Python script" | gemini
   ```

  [](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/index.md)
- **Conversation Memory**: Save session history with `/save <tag>` and resume with `/restore <tag>`.[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md)
- **Custom Configuration**:
  - Edit `~/.gemini/settings.json` for global settings or `.gemini/settings.json` in a project for local settings.
  - Example: Set MCP servers or custom themes.[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md)

---

### **Tips and Tricks**

- **Start with Plans**: For complex tasks, ask for a plan first: `Create a detailed implementation plan for a login system`. This ensures structured output.
- **Use Local Context**: Encode project-specific details in `GEMINI.md` instead of relying on MCP servers for faster, reliable responses.
- **Debugging**: Enable verbose logging with `DEBUG=true gemini` for detailed request/response info.[](https://apidog.com/blog/google-gemini-open-code-cli/)
- **Review Changes**: Always review file modifications or commands before approving (type `y` to confirm).[](https://apidog.com/blog/google-gemini-open-code-cli/)
- **Explore Tools**: Run `/tools` to discover built-in capabilities like web search or memory saving.[](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)

---

### **Troubleshooting**

- **Authentication Issues**: Ensure your Google account or API key is valid. Use `/auth` to switch methods.[](https://www.datacamp.com/tutorial/gemini-cli)
- **Rate Limits**: The free tier allows 60 requests/minute and 1,000/day. For higher limits, use an API key or Vertex AI.[](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)
- **Errors**: Check the [Troubleshooting Guide](https://github.com/google-gemini/gemini-cli/docs/troubleshooting.md) on GitHub.[](https://github.com/google-gemini/gemini-cli)
- **Slow Responses**: The CLI is in preview and may be slow with API calls. File feedback on GitHub.[](https://www.datacamp.com/tutorial/gemini-cli)

---

### **Advanced Usage**

- **MCP Server Integration**:
  - Set up a GitHub MCP server for repository interactions:
    - Create a GitHub PAT with necessary scopes.
    - Add to `.gemini/settings.json`:

      ```json
      {
        "mcpServers": [
          {
            "name": "github",
            "url": "http://localhost:8080",
            "type": "github"
          }
        ]
      }
      ```

    - Run a Docker container for the MCP server (see GitHub docs).[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials.md)
- **Scripting**: Automate tasks by integrating Gemini CLI into scripts:

  ```bash
  gemini --non-interactive "Generate a bash script to backup my files"
  ```

  [](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/index.md)
- **Multimodal Prompts**:
  - Example: `Describe this image: path/to/image.jpg` (requires a vision-capable model like `gemini-pro-vision`).[](https://github.com/eliben/gemini-cli)

---

### **Limitations**

- **Preview Stage**: Gemini CLI is in pre-GA, with potential for limited support or bugs.[](https://cloud.google.com/gemini/docs/codeassist/gemini-cli)
- **Not Fully Open-Source**: Only the CLI UI is Apache 2.0 licensed; the Gemini model is proprietary.[](https://www.bleepingcomputer.com/news/artificial-intelligence/google-releases-gemini-cli-with-free-gemini-25-pro/)
- **Quota Sharing**: Limits are shared with Gemini Code Assist if used.[](https://developers.google.com/gemini-code-assist/docs/gemini-cli)
- **Future Pricing**: Post-preview pricing is unclear; advanced features may require payment.[](https://ts2.tech/en/everything-you-need-to-know-about-google-gemini-cli-features-news-and-expert-insights/)

---

### **Resources**

- **Official GitHub**: [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)[](https://github.com/google-gemini/gemini-cli)
- **Documentation**: [gemini-cli.click](https://gemini-cli.click) or GitHub docs[](https://gemini-cli.click/)
- **Blog Announcement**: [blog.google](https://blog.google)[](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)
- **Feedback**: File bugs or suggestions on GitHub.[](https://ts2.tech/en/everything-you-need-to-know-about-google-gemini-cli-features-news-and-expert-insights/)

---

### **Example Workflow**

1. Install: `npm install -g @google/gemini-cli`
2. Run: `cd my-project && gemini`
3. Authenticate: Log in with Google.
4. Prompt: `Write a Python script for a REST API with FastAPI`.
5. Review and save the generated code.
6. Use `/tools` to explore additional features like GitHub integration.

---

Gemini CLI is a powerful tool for developers, offering seamless AI integration in the terminal. Start simple, leverage `GEMINI.md` for context, and explore its multimodal capabilities to boost productivity. For more examples, check the [GitHub tutorials](https://github.com/google-gemini/gemini-cli/docs/cli/tutorials.md).[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials.md)

If you need specific examples or have questions about a particular feature, let me know!
