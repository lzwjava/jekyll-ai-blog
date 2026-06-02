---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Claude Code Multi-Directory Support
translated: false
type: note
---

Claude Code, Anthropic's AI-powered coding assistant, operates primarily within its initialized working directory for security and focus, but it now fully supports cross-project functionality through a multi-directory feature introduced in recent updates (e.g., version 1.0.18 and later). This allows a single session to access and work with files across multiple unrelated projects or directories outside the original one, enabling tasks like referencing shared configurations, integrating frontend/backend code, or handling monorepo setups without context switching.[1][2][3]

### How Cross-Project Functionality Works

- **Core Mechanism**: Claude Code starts in one root directory (your "primary" project) but can expand permissions to read, edit, and execute commands in additional directories. This is done via the `--add-dir` flag or the interactive `/add-dir` command during a session. Added directories are treated as extensions of the workspace, allowing seamless file operations (e.g., you can lint files from Project A while editing in Project B).[3][4]
- **Session Scope**: Each project addition is temporary unless persisted via configuration. Git worktrees can enable simultaneous sessions on parts of a project for deeper collaboration.[5][6]
- **Limitations**: Claude Code restricts file access to added directories only— it won't automatically discover unrelated paths. For persistent multi-project setups (e.g., monorepos), run from a parent directory containing subfolders.[3][7]
- **Use Cases**:
  - **Monorepos**: Add subdirectories for frontend/backend splits.[3][5][7][8]
  - **Shared Resources**: Reference configs or libraries from a separate project.[3][6]
  - **Cross-Project Collaboration**: Integrate code from libraries or tools in different repos.[1][3]

### How to Instruct Claude Code to Involve Another Project

To add a project outside the current directory (e.g., `${another_project_path}`):

1. **Start Claude Code** in your primary project directory (e.g., `cd /path/to/primary/project && claude`).
2. **Add the Additional Directory Interactively**:
   - During the session, type `/add-dir /full/path/to/another/project` or a relative path (e.g., `../another-project`).
   - Claude Code will confirm access—respond with "yes" if prompted.[2][3][4]
3. **At Startup via CLI Flag** (for immediate multi-dir setup):
   - Run: `claude --add-dir /path/to/another/project` (add multiple with repeated flags).[4][5][7]
4. **Instruct Claude Bots/Agents**: Once added, give natural language prompts like "Reference the API files from the added directory in `/path/to/another/project`" or "Integrate this shared config from Project B." Claude's agentic design understands these requests within the expanded context.[3][5][6]

### Best Practices and Tips

- **Path Specification**: Use absolute paths for clarity across environments. Avoid adding too many directories to prevent performance hits.[3][7]
- **Workspace Setup**: For teams, consider configuration files for reusable setups. Combine with tools like Apidog for API testing across directories.[3][8]
- **Troubleshooting**: If path resolution fails, ensure write permissions. Restart sessions for changes. For persistent issues, check logs or run from a higher-level directory.[3][7]
- **Team Workflows**: Use this for microservices or shared libraries; synchronize via Git for versioning.[5][6][8]

This feature transforms workflows for complex setups, reducing friction compared to running separate sessions in each directory.[3][6] If you encounter issues or need examples for specific tools, provide more details!

Citations:
[1] <https://www.reddit.com/r/ClaudeAI/comments/1l896ek/claude_code_v1018_we_can_now_specify_additional/>
[2] <https://www.threads.com/@boris_cherny/post/DMtFLWOzKAS/video-claude-code-can-now-work-across-multiple-directories-in-a-single-sessiontype-add?hl=en>
[3] <https://apidog.com/blog/claude-code-multi-directory-support/>
[4] <https://claudelog.com/faqs/--add-dir/>
[5] <https://www.anthropic.com/engineering/claude-code-best-practices>
[6] <https://www.linkedin.com/posts/valokafor_how-to-set-up-claude-code-the-right-way-for-activity-7353146981034201089-dhdX>
[7] <https://stackoverflow.com/questions/79763754/best-practices-for-multi-project-workspaces-in-claude-code>
[8] <https://www.siddharthbharath.com/claude-code-the-complete-guide/>
