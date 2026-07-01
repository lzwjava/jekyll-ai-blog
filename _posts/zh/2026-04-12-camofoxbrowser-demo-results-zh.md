---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 伪装狐狸浏览器演示结果摘要
translated: true
type: note
---

以下是我们刚刚通过CamofoxBrowser演示的内容总结：

## 演示结果

### 工作流已完成

1. 创建标签页：`POST /tabs` 在 `https://example.com` 上返回标签页ID `ab2e2566-...`

2. 通过宏搜索Google：使用 `@google_search` 宏调用 `POST /tabs/:tabId/navigate`，但Google标记了异常流量

3. 搜索DuckDuckGo：直接导航至 `https://duckduckgo.com/?q=today+in+AI+news` —— 成功加载并包含123个交互元素

4. 点击元素：使用 `ref: "e25"`（搜索结果页上的相对链接）调用 `POST /tabs/:tabId/click`

5. 阅读文章：导航至SecurityWeek的文章《我们能信任AI吗？不能——但最终我们必须信任》——可通过快照获取完整文章内容

### 文章核心要点

- 当前LLM缺乏客观事实基础——它们基于词元概率，而非理解
- 幻觉（虚构）是其架构的固有特征
- 迎合性：AI倾向于认同用户观点，这可能存在危险（引用FBI探员Jim Carden的经历，其中AI成了他的“朋友”）
- 模型崩溃：基于AI生成内容训练的模型会随时间退化（依据Ilia Shumailov的研究）
- 新兴AI安全公司：Kamiwaza AI、DeepKeep、AI Sequrity

### 其他可用API（未测试）

| 端点 | 用途 |
| --- | --- |
| `POST /tabs/:tabId/type` | 在表单字段中输入文本 |
| `POST /tabs/:tabId/scroll` | 向上/向下滚动 |
| `POST /tabs/:tabId/back` | 浏览器后退 |
| `GET /tabs/:tabId/links` | 列出所有链接 |
| `DELETE /tabs/:tabId` | 关闭标签页 |
| `POST /sessions/:userId/cookies` | 导入cookies |
| `DELETE /sessions/:userId` | 删除会话 |

是否需要我尝试特定操作——例如填写表单、测试其他端点，或探索更多功能？
