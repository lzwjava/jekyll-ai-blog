---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 记录聊天机器人交互的Python脚本
translated: true
type: note
---

### 记录聊天机器人交互的智能Python脚本

想要一种简单的方法来记录你与AI聊天机器人的对话吗？这个精巧的Python脚本利用剪贴板捕获你的提问和机器人的回复，然后整齐地保存到Markdown文件中。就像是为AI对话量身打造的个人记录器！

它假装是GitHub Copilot，但实际上通过处理复制粘贴流程，帮助你与任何聊天机器人进行交互。需要安装`pyperclip`（如有需要可通过pip安装）。

以下是完整代码：

```python
import pyperclip
import os

def save_to_file(content, filename="answer.md"):
    with open(filename, "a") as f:
        f.write(content + "\n\n")

def main():
    print("你好！我是GitHub Copilot。有什么可以帮你的吗？")

    while True:
        user_input = input("你：")
        if user_input.lower() in ["exit", "quit"]:
            print("再见！")
            break

        # 将用户输入复制到剪贴板
        pyperclip.copy(user_input)
        print("我已将你的输入复制到剪贴板。请向聊天机器人提问并复制其回答。准备就绪后，直接按Enter键。")

        # 等待用户在复制机器人回答后按Enter键
        input("复制回答后按Enter键...")

        # 从剪贴板获取回答
        answer = pyperclip.paste()
        print("回答已接收。正在保存至answer.md...")

        # 将交互内容保存至文件
        interaction = f"**用户输入：**\n{user_input}\n\n**聊天机器人回答：**\n{answer}\n{'-'*50}"
        save_to_file(interaction)
        print("已保存至answer.md。还有其他需要帮助的吗？")

if __name__ == "__main__":
    main()
```

在终端中运行此脚本，它将引导你完成整个流程。非常适合研究人员、开发者或任何需要归档AI输出的人。你觉得这个技巧实用吗？🚀

#Python #AI #聊天机器人 #编程技巧
