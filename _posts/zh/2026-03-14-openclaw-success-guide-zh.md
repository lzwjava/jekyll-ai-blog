---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 项目成功指南
translated: true
type: note
---

## 有效使用 OpenClaw (Claude Code)

### OpenClaw 是什么？
OpenClaw 是 **Claude Code** 的封装/接口——Anthropic 的代理式编码 CLI。它允许 Claude 在你的机器上自主编写、编辑和运行代码。

---

### ✅ 你的直觉是正确的——先创建一个 PRD

是的，**一个好的 PRD (Product Requirements Document) 是 #1 要务**，它将优秀的 Claude Code 结果与平庸的结果区分开来。

**为什么 PRD 重要：**
- Claude Code 在拥有**清晰、结构化的规范**时，效果最佳
- 没有 PRD，它会自行假设并偏离你的愿景
- PRD 作为“真相来源”，它可以随时参考

**你的 PRD 中应包含什么：**
```
## Project: Todo App
### Core Features
- Task creation, editing, deletion
- Projects / folders
- Subtasks
- Priority levels (P1-P4)
- Due dates
- Tags/labels

### Tech Stack
- React + TypeScript
- Tailwind CSS
- localStorage / IndexedDB

### UI Reference
- Inspired by: Google Tasks, Linear, Todoist

### Out of Scope (v1)
- Backend sync
- Mobile app
```

---

### 🪜 正确的流程

```
1. Write PRD  →  2. Small first task  →  3. Review  →  4. Iterate
```

| 步骤 | 操作内容 |
|------|-----------|
| **1. PRD** | 在编写代码前清晰定义范围 |
| **2. Start small** | 先让它搭建项目框架，而不是构建一切 |
| **3. Check output** | 每个主要步骤后审查 |
| **4. Iterate** | 一次添加一个模块的功能 |

---

### ⚠️ 要避免的常见错误

- **不要一次性要求所有功能**——“build a full todo app” 会导致代码混乱
- **不要跳过审查**——Claude Code 可能悄无声息地走偏
- **不要给出模糊规范**——“make it sophisticated” 难以执行，而“implement drag-and-drop reordering with keyboard shortcuts” 则具体可行
- **不要让它无人看管运行太久**——复杂任务每 10-15 分钟检查一次

---

### 💡 OpenClaw 的更好提示策略

不要使用一个巨大的提示，而是分解成阶段：

```
Phase 1: "Scaffold the React project with folder structure and routing"
Phase 2: "Build the Task model and CRUD operations"  
Phase 3: "Build the sidebar with project navigation"
Phase 4: "Add keyboard shortcuts and search"
Phase 5: "Polish UI and add animations"
```

每个阶段 = 一个 Claude Code 会话。**在进入下一阶段前审查。**

---

### 📋 推荐的第一个 OpenClaw 提示

```
Read this PRD carefully before writing any code.
[paste PRD]

Step 1 only: Scaffold the project structure, install dependencies, 
and create empty component files with comments describing what 
each will do. Do not implement logic yet. Show me the file tree when done.
```

这会迫使它**在编码前规划**。

---

### 总结

| 问题 | 答案 |
|----------|--------|
| 你的方法正确吗？ | 基本正确——但要分解成更小的步骤 |
| 先 PRD？ | **绝对是的** |
| 过一段时间检查？ | 是的，对于大任务每 10-15 分钟检查一次 |
| 一个大提示？ | 否——分阶段进行 |