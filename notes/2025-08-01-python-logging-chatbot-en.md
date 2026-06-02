---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python Script for Logging Chatbot Interactions
translated: false
type: note
---

### Clever Python Script for Logging Chatbot Interactions

Ever wanted an easy way to document your conversations with AI chatbots? This nifty Python script uses the clipboard to capture your queries and the bot's responses, then saves them neatly to a Markdown file. It's like a personal logger for AI chats!

It pretends to be GitHub Copilot but actually helps you interact with any chatbot by handling the copy-paste workflow. Requires `pyperclip` (install via pip if needed).

Here's the full code:

```python
import pyperclip
import os

def save_to_file(content, filename="answer.md"):
    with open(filename, "a") as f:
        f.write(content + "\n\n")

def main():
    print("Hello! I'm GitHub Copilot. What can I help you with?")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Copy user input to clipboard
        pyperclip.copy(user_input)
        print("I've copied your input to the clipboard. Please ask the chatbot and copy their answer. When ready, just press Enter.")

        # Wait for user to press Enter after copying the chatbot's answer
        input("Press Enter when you have the answer copied...")

        # Get the answer from clipboard
        answer = pyperclip.paste()
        print("Answer received. Saving to answer.md...")

        # Save the interaction to file
        interaction = f"**User Input:**\n{user_input}\n\n**Chatbot Answer:**\n{answer}\n{'-'*50}"
        save_to_file(interaction)
        print("Saved to answer.md. Anything else I can help with?")

if __name__ == "__main__":
    main()
```

Run it in your terminal, and it'll guide you through the process. Great for researchers, developers, or anyone archiving AI outputs. What do you think—useful hack or what? 🚀

# Python #AI #Chatbots #CodingTips
