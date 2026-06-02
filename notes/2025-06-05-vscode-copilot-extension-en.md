---
audio: false
generated: true
lang: en
layout: post
title: How to Call GitHub Copilot from a VSCode Extension
translated: false
type: note
---

GitHub Copilot is a powerful AI-powered coding assistant integrated into Visual Studio Code (VSCode) and IntelliJ IDEA through their respective plugins. While there’s no public REST API for directly calling Copilot, developers can interact with its capabilities programmatically within a VSCode extension using the VSCode Chat API, Language Model API, or command-based interactions. This blog post walks through creating a VSCode extension that triggers Copilot’s chat functionality with a custom prompt, effectively simulating an “API call” to Copilot, and explains how to leverage Copilot itself to streamline development.

## Understanding Copilot’s Integration in VSCode

GitHub Copilot doesn’t expose a traditional API (e.g., REST endpoints) for direct programmatic access. Instead, its functionality is available through:
- **VSCode Chat API**: Enables extensions to create custom chat participants that interact with Copilot’s chat system for natural language queries.
- **VSCode Language Model API**: Allows extensions to access Copilot’s large language models (LLMs) for tasks like code generation or analysis.
- **VSCode Commands**: Permits triggering Copilot’s built-in features, such as opening the chat window with a predefined prompt.

This guide focuses on using the `workbench.action.chat.open` command to trigger Copilot’s chat interface, as it’s the simplest way to integrate Copilot’s capabilities into an extension.

## Step-by-Step: Building a VSCode Extension to Trigger Copilot Chat

Below is a step-by-step guide to creating a VSCode extension that opens Copilot’s chat window with a custom prompt, effectively “calling” Copilot to process a user-defined query.

### 1. Set Up the VSCode Extension

1. **Scaffold the Project**:
   - Install the Yeoman VSCode extension generator: `npm install -g yo generator-code`.
   - Run `yo code` and select “New Extension (TypeScript)” to create a TypeScript-based extension.
   - Name the extension, e.g., `copilot-api-caller`.

2. **Configure `package.json`**:
   - Define a command to trigger Copilot’s chat.
   - Example `package.json`:

```json
{
  "name": "copilot-api-caller",
  "displayName": "Copilot API Caller",
  "description": "Triggers GitHub Copilot Chat with a custom prompt",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Other"],
  "activationEvents": [
    "onCommand:copilot-api-caller.triggerCopilotChat"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "copilot-api-caller.triggerCopilotChat",
        "title": "Trigger Copilot Chat"
      }
    ]
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0",
    "@types/node": "^20.2.5",
    "typescript": "^5.1.3"
  }
}
```

   - **Using Copilot**: While editing `package.json`, Copilot may suggest fields like `contributes.commands` or `activationEvents` as you type. Accept these with `Tab` to speed up setup.

### 2. Write the Extension Code

Create the extension logic to register a command that opens Copilot’s chat with a user-provided prompt.

- **File**: `src/extension.ts`
- **Code**:

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  // Register the command to trigger Copilot Chat
  let disposable = vscode.commands.registerCommand('copilot-api-caller.triggerCopilotChat', async () => {
    // Get user input for the prompt
    const prompt = await vscode.window.showInputBox({
      prompt: 'Enter your query for GitHub Copilot',
      placeHolder: 'e.g., Write a JavaScript function to sort an array'
    });

    if (prompt) {
      try {
        // Execute the command to open Copilot Chat with the prompt
        await vscode.commands.executeCommand('workbench.action.chat.open', prompt);
        vscode.window.showInformationMessage('Sent prompt to Copilot Chat!');
      } catch (error) {
        vscode.window.showErrorMessage(`Failed to trigger Copilot Chat: ${error}`);
      }
    }
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
```

- **How It Works**:
  - Registers a command `copilot-api-caller.triggerCopilotChat`.
  - Prompts the user for a query (e.g., “Write a Python function to reverse a string”).
  - Uses `vscode.commands.executeCommand('workbench.action.chat.open', prompt)` to open Copilot’s chat window with the prompt.
- **Using Copilot**: In VSCode, type `import * as vscode` and Copilot will suggest the full import. Add a comment like `// Register a command to open Copilot Chat`, and Copilot may propose the `vscode.commands.registerCommand` structure. For the command execution, type `// Open Copilot Chat with a prompt`, and Copilot might suggest the `executeCommand` call.

### 3. Enhance with Context (Optional)

To make the extension more powerful, include context from the editor, such as selected code, to provide Copilot with additional information.

- **Modified Code** (`src/extension.ts`):

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand('copilot-api-caller.triggerCopilotChat', async () => {
    // Get selected text from the active editor
    const editor = vscode.window.activeTextEditor;
    let context = '';
    if (editor) {
      const selection = editor.selection;
      context = editor.document.getText(selection);
    }

    // Prompt for user input
    const prompt = await vscode.window.showInputBox({
      prompt: 'Enter your query for GitHub Copilot',
      placeHolder: 'e.g., Explain this code',
      value: context ? `Regarding this code: \n\`\`\`\n${context}\n\`\`\`\n` : ''
    });

    if (prompt) {
      try {
        await vscode.commands.executeCommand('workbench.action.chat.open', prompt);
        vscode.window.showInformationMessage('Sent prompt to Copilot Chat!');
      } catch (error) {
        vscode.window.showErrorMessage(`Failed to trigger Copilot Chat: ${error}`);
      }
    }
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
```

- **How It Works**:
  - Retrieves selected text from the active editor and includes it as context in the prompt.
  - Pre-fills the input box with the selected code, formatted as a Markdown code block.
  - Sends the combined prompt to Copilot’s chat interface.
- **Using Copilot**: Comment `// Get selected text from editor`, and Copilot may suggest `vscode.window.activeTextEditor`. For formatting, type `// Format code as markdown`, and Copilot might propose the triple-backtick syntax.

### 4. Test the Extension

1. Press `F5` in VSCode to launch the Extension Development Host.
2. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and run `Trigger Copilot Chat`.
3. Enter a prompt (e.g., “Generate a REST API client in TypeScript”) or select code and run the command.
4. Verify that Copilot’s chat window opens with your prompt and provides a response.
5. **Using Copilot**: If errors occur, add a comment like `// Handle errors for command execution`, and Copilot may suggest try-catch blocks or error messages.

### 5. Advanced: Using the VSCode Chat API

For more control, use the VSCode Chat API to create a custom chat participant that integrates with Copilot’s language models, allowing natural language processing within your extension.

- **Example Code** (`src/extension.ts`):

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  // Register a chat participant
  const participant = vscode.chat.createChatParticipant('copilot-api-caller.myParticipant', async (request, context, stream, token) => {
    stream.markdown('Processing your query...\n');
    // Use the Language Model API to generate a response
    const model = await vscode.lm.selectChatModels({ family: 'gpt-4' })[0];
    if (model) {
      const response = await model.sendRequest([{ text: request.prompt }], {}, token);
      for await (const chunk of response.stream) {
        stream.markdown(chunk);
      }
    } else {
      stream.markdown('No suitable model available.');
    }
  });

  participant.iconPath = new vscode.ThemeIcon('sparkle');
  context.subscriptions.push(participant);
}

export function deactivate() {}
```

- **How It Works**:
  - Creates a chat participant (`@copilot-api-caller.myParticipant`) invocable in the Copilot Chat view.
  - Uses the Language Model API to access Copilot’s `gpt-4` model (or another available model) to process the prompt.
  - Streams the response back to the chat view.
- **Using Copilot**: Comment `// Create a chat participant for Copilot`, and Copilot may suggest the `vscode.chat.createChatParticipant` structure. For the Language Model API, comment `// Access Copilot’s LLM`, and Copilot might propose `vscode.lm.selectChatModels`.

### 6. Package and Deploy

1. Install `vsce`: `npm install -g @vscode/vsce`.
2. Run `vsce package` to create a `.vsix` file.
3. Install the extension in VSCode via the Extensions view or share the `.vsix` file with others.
4. **Using Copilot**: Add a comment like `// Add script to package extension` in `package.json`, and Copilot may suggest the `vscode:prepublish` script.

## Leveraging Copilot During Development

GitHub Copilot can significantly speed up extension development:
- **Code Suggestions**: As you type in `src/extension.ts`, Copilot suggests imports, command registrations, and error handling. For example, typing `vscode.commands.` prompts suggestions like `registerCommand`.
- **Prompt Engineering**: Use clear comments like `// Trigger Copilot Chat with a user prompt` to guide Copilot’s suggestions. Refine comments if suggestions are inaccurate.
- **Debugging**: If the extension fails, add comments like `// Log error details`, and Copilot may suggest `console.log` or `vscode.window.showErrorMessage`.

## Limitations

- **No Direct API Access**: Copilot doesn’t expose a public REST API. The VSCode Chat and Language Model APIs are the primary programmatic interfaces.
- **Authentication**: Users must have an active Copilot subscription (free or paid) and be signed into VSCode with a GitHub account.
- **Chat API Scope**: The Chat API is limited to the chat interface; direct access to Copilot’s code completion engine is not available programmatically.
- **Environment**: Ensure the extension complies with any organizational policies regarding custom VSCode extensions.

## Conclusion

By using VSCode’s command system or Chat API, developers can effectively “call” GitHub Copilot from a custom extension, enabling programmatic interaction with its AI capabilities. The example above demonstrates triggering Copilot’s chat with a custom prompt, enhanced with editor context, and provides a foundation for more advanced integrations using the Language Model API. With Copilot’s assistance during development, creating such extensions becomes faster and more intuitive.

For further exploration, consider experimenting with the Chat API for custom participants or integrating additional editor context for richer prompts. Happy coding!
