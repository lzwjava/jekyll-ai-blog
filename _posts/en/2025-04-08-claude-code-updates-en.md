---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Claude Code Major Updates
translated: false
type: note
---

### Major Updates in Claude Code

Claude Code, Anthropic's AI-powered coding assistant, has seen significant enhancements recently, particularly around autonomy, integration, and user interface features. Based on the latest news (September 29, 2025), the key update focuses on enabling more autonomous operation, including a native VS Code extension, an upgraded terminal interface (version 2.0), and new checkpoint functionality to manage long-running tasks. Additionally, features like toggling "thinking" mode appear to be part of the ongoing refinements, allowing users to turn on and off the display of Claude's reasoning steps for cleaner interactions [1].

#### Autonomy and Agent Capabilities

- **Native VS Code Extension**: Enables seamless integration with the VS Code editor, allowing Claude Code to operate directly within the development environment for more autonomous code editing and debugging.
- **Terminal Interface v2.0**: Upgrades include improved handling of permissions, memory management across tasks, and coordination of subagents. This makes Claude Code better at balancing user control with automated operations during complex workflows [1][2].
- **Checkpoints**: A new feature for saving progress in lengthy tasks, allowing pauses and resumes without losing context. This supports running tasks that span multiple days or sessions.

These changes build on Anthropic's Claude Agent SDK, providing developers with tools to create custom AI agents that mirror Claude Code's internal infrastructure [2].

#### Other Notable Changes

- **Model Upgrade Integration**: Claude Code now uses Claude Sonnet 4.5 by default, offering improved performance in coding tasks without price changes. This model is recommended across all Claude products for its enhanced alignment and reduced hallucinations [2].
- **User Interface Tweaks**: The "Thinking off (tab to toggle)" feature seems to be a toggle for showing or hiding Claude's internal reasoning process, which can streamline the output. This aligns with user feedback on transparency and usability in coding sessions [3].
- **Known Issue Fix Attempts**: Reports of Claude Code appending "2024" to searches due to training data cutoffs are being addressed, though some users note persistent bugs. A workaround involves custom hooks to update date awareness [3][4].

For the full details, install or check the latest version—updates are auto-applied for all users [1]. If you're experiencing issues, ensure your client is up to date. For historical changes, check community changelogs like ClaudeLog, though they may not cover the absolute latest features [5].

Citations:
[1] <https://anthropic.com/news/enabling-claude-code-to-work-more-autonomously>
[2] <https://www.anthropic.com/news/claude-sonnet-4-5>
[3] <https://www.reddit.com/r/ClaudeAI/comments/1mtgjdi/claude_code_thinks_it_is_2024_and_keeps_web/>
[4] <https://medium.com/@dan.avila7/fixed-claude-codes-2024-tunnel-vision-with-a-simple-hook-cb32cfaf9b27>
[5] <https://www.claudelog.com/claude-code-changelog/>
