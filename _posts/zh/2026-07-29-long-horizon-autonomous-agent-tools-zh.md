---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 长周期自主代理工具
translated: true
type: note
---

**问题：有哪些工具可以运行长时间运行的自主代理任务（Kimi Agent Swarm、Manus、Hermes goal command 等）？**

答案：

当前生态系统正在趋向于以下模式：

```
人类给出目标
        |
        v
规划代理
        |
        +----> 研究代理
        |
        +----> 编码代理
        |
        +----> 浏览器代理
        |
        +----> 测试代理
        |
        v
记忆 + 工件 + 检查点
        |
        v
最终结果
```

关键问题不在于"对话"，而在于**长时间执行**：

* 维持状态数小时/数天
* 从失败中恢复
* 生成子代理
* 观察环境
* 验证输出

## 1. Manus 式自主代理

Manus 普及了"给出目标，等待结果"的工作流程。

示例：

```
目标：
"分析 50 个竞争对手并创建市场报告"

代理：
- 搜索网络
- 下载文档
- 撰写笔记
- 总结
- 创建报告
```

架构：

```
任务队列
    |
规划器
    |
工作代理
    |
沙箱
    |
工件存储
```

适用于：

* 研究
* 报告
* 业务工作流

弱点：

* 对于工程工作流的可控性较差。

---

## 2. Kimi Agent / Agent Swarm

Moonshot AI 推广了多专业代理的理念。

典型 swarm：

```
              管理代理

        /          |          \

 研究员       编码员      审阅员

        \          |          /

            共享内存
```

示例：

```
"构建AI初创公司竞争对手分析"

管理代理：
  拆分任务

代理A：
  收集 YC 公司

代理B：
  分析定价

代理C：
  分析技术

代理D：
  验证事实

管理代理：
  合并结果
```

这更接近于一个软件工程团队。

---

## 3. Hermes Agent goal command 风格

这更接近于 CLI 代理哲学。

示例：

```
hermes goal \
  "将此 Spring Boot 项目升级到 Java 21，
   运行测试，
   修复失败，
   创建 PR"
```

内部流程：

```
目标
 |
 v
任务分解
 |
 v
执行循环

while not finished:

    observe()
    plan()
    act()
    verify()
    update_memory()

```

重要部分在于**循环**。

一个简单的实现：

```python
while True:
    state = observe()

    plan = llm("""
    目标：
    {goal}

    当前状态：
    {state}

    下一步应该做什么？
    """)

    result = execute(plan)

    memory.append(result)

    if verify(goal):
        break
```

这基本上就是"代理操作系统"。

---

## 4. 编码代理

针对当前的软件任务：

### Claude Code

[Claude Code](https://www.anthropic.com/claude-code?utm_source=chatgpt.com)

工作流：

```
问题
 |
代理
 |
编辑文件
 |
运行测试
 |
修复
 |
提交
```

非常适合：

* 仓库理解
* 重构
* 调试

---

### OpenAI Codex

[OpenAI Codex](https://openai.com/codex/?utm_source=chatgpt.com)

更偏向云代理方向：

```
任务
 |
隔离环境
 |
代理执行
 |
工件
```

---

### SWE-agent

研究风格：

```
GitHub issue

      |
      v

代理

      |
      v

补丁

      |
      v

测试
```

---

## 5. 开源代理框架

### LangGraph

[LangGraph](https://www.langchain.com/langgraph?utm_source=chatgpt.com)

适用于明确工作流：

```
        开始

          |

       规划器

          |

   +------+------+

   |             |

 研究         编码

   |             |

   +------+------+

          |

       审阅员

          |

        结束
```

你可以控制状态机。

---

### CrewAI

[CrewAI](https://www.crewai.com?utm_source=chatgpt.com)

更像"虚拟公司"：

```python
researcher = Agent(
    role="研究员"
)

coder = Agent(
    role="工程师"
)

manager = Agent(
    role="经理"
)
```

---

### AutoGen

[AutoGen](https://microsoft.github.io/autogen/?utm_source=chatgpt.com)

微软多代理框架。

模式：

```
用户代理

    |
    |

助手代理

    |
    |

执行代理
```

---

## 6. 针对你的设置（多 GPU + AI 实验室）

考虑到你拥有 RTX 4070 和多个机器的想法，我会构建类似这样的东西：

```
                 Hermes 控制器

                        |
        +---------------+---------------+

        |               |               |

   RTX4070 节点    RTX3090 节点    Mac M2 节点

   编码代理          训练           研究代理


        |
        v

    共享 SQLite/Postgres

        |
        v

    向量记忆
```

每台机器运行：

```
agent-worker

命令：

agent start
agent join swarm
agent execute task
```

通信：

```
Redis 队列

任务：
{
 id:123,
 goal:"训练 GPT-2 64M",
 status:"运行中"
}
```

---

## 7. 缺失的一环：代理监督

长时间任务之所以失败，是因为代理幻觉式地认为自己完成了。

一个生产级循环需要：

```
代理说：
"我完成了"

验证器：

列出文件？
运行测试？
比较预期输出？
检查指标？

是 -> 完成
否 -> 重试
```

示例：

```
目标：
训练模型

代理：
已完成

验证器：

检查点存在？        OK
损失下降？           OK
样本生成？           失败

返回：
"继续训练"
```

---

## 我对严肃工程应用的当前排名

| 工具             | 最佳用途                      |
| ---------------- | ----------------------------- |
| Claude Code      | 日常编码                      |
| Codex            | 云端编码代理                  |
| Manus            | 通用自主任务                  |
| Kimi swarm 风格   | 多代理研究                    |
| LangGraph        | 构建你自己的代理操作系统      |
| AutoGen          | 实验                          |
| CrewAI           | 业务工作流                    |
| Hermes 风格 CLI   | 个人代理基础设施              |

对于构建 AI 系统的人来说，有趣的方向不是直接使用 Manus/Kimi，而是构建一个**个人代理运行时**：

```
goal()
  |
planner()
  |
workers()
  |
memory()
  |
verifier()
  |
artifact()
```

基本上就是一个用于代理的"AI Kubernetes"。
