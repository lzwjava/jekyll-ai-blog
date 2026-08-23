---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Rasa企业级AI智能体平台
translated: true
type: note
---

## 问题：Rasa平台介绍 ([https://rasa.com](https://rasa.com))

## 答案

Rasa是一个企业级AI代理平台，专注于构建**可靠、可控的对话式AI系统**。它始于2016年，最初是一个开源对话式AI/NLU框架，现已演变为一个将LLM能力与确定性业务逻辑相结合的生产级AI代理平台。([Rasa][1])

### Rasa解决了什么问题？

现代LLM聊天机器人存在一个常见问题：

```
用户
 |
 v
LLM
 |
 v
回答
```

模型虽然灵活，但可能：

* 产生幻觉
* 忽略业务规则
* 无法满足合规要求
* 行为不一致

Rasa的设计理念是：

```
                 +----------------+
用户 ----------> | 语言模型       |
                 +----------------+
                         |
                         v
              +--------------------+
              | 对话管理器         |
              | 业务逻辑           |
              | 工作流引擎         |
              +--------------------+
                         |
                         v
               API / 数据库 / CRM
```

LLM负责语言理解，而Rasa控制执行流程。([Rasa][2])

---

## 核心产品

### 1. Rasa平台

主要的企业级平台。

功能：

* AI代理编排
* 对话记忆
* 工作流管理
* 集成能力
* 测试与分析
* 部署控制

支持两种模式：

* **无代码**：Rasa Studio
* **专业代码**：开发者工作流

([Rasa][3])

---

### 2. CALM（基于语言模型的对话式AI）

这是Rasa的LLM原生架构。

与传统聊天机器人设计不同：

```
意图：
  预订航班

实体：
  目的地 = 东京

规则：
  询问日期()
```

CALM允许：

```
用户：
“我需要改签明天的航班”

          |
          v

LLM理解意图

          |
          v

Rasa流程决定：

1. 验证身份
2. 检查预订
3. 调用航空公司API
4. 确认变更
```

关键点在于：

LLM ≠ 控制器。

LLM提供建议；Rasa负责执行。([Rasa][4])

---

## 典型架构

企业部署方案：

```
                 网页 / 移动端 / 语音
                         |
                         v
                 +---------------+
                 |     Rasa      |
                 | AI代理核心    |
                 +---------------+
                         |
        +----------------+----------------+
        |                |                |
        v                v                v

    CRM系统         知识库        内部API

        |
        v

  Salesforce / SAP / 银行系统
```

常见行业：

* 银行业
* 保险业
* 医疗健康
* 电信业
* 政府部门
* 客户服务

因为这些行业需要可预测的行为和私有化部署。([Rasa][5])

---

## 开发者体验

Rasa基于Python开发。

示例：

```bash
pip install rasa

rasa init

rasa train

rasa run
```

典型项目结构：

```
my-agent/

├── domain.yml
├── flows/
├── actions/
├── config.yml
├── credentials.yml
└── tests/
```

自定义业务动作：

```python
class CheckBalance(Action):

    def run(self, dispatcher, tracker, domain):

        user_id = tracker.get_slot("user_id")

        balance = bank_api.get_balance(user_id)

        dispatcher.utter_message(
            text=f"您的余额为 {balance}"
        )
```

---

## Rasa vs LangChain / AutoGen / CrewAI

| 平台                     | 主要理念                                         |
| ------------------------ | ------------------------------------------------ |
| Rasa                     | 具有可控工作流的企业级对话代理                   |
| LangChain                | LLM应用框架                                      |
| LlamaIndex               | 数据/RAG框架                                     |
| AutoGen                  | 多代理实验平台                                   |
| CrewAI                   | 代理团队                                         |
| OpenAI Assistants/Agents | 托管代理平台                                     |

Rasa更接近于：

```
空中交通控制系统
```

而许多代理框架更接近于：

```
自由探索的自主机器人
```

对于银行、保险、电信等行业，Rasa这种受控方法更具吸引力。

---

## 优势

### 1. 企业级可靠性

适用于：

* “更改我的账户地址”
* “提交保险索赔”
* “重置企业密码”

这些场景中，错误成本高昂。

### 2. 自托管能力

可运行于：

* 私有云
* Kubernetes
* 本地部署

对受监管的企业非常有用。([Rasa][6])

### 3. 开放生态

历史上拥有强大的开源社区。

GitHub：

[Rasa GitHub仓库](https://github.com/RasaHQ/rasa?utm_source=chatgpt.com)

---

## 劣势

与现代化的LLM原生技术栈相比：

* 需要更多工程投入
* 不如纯GPT代理“智能”
* 需要对话设计
* 生态系统比LangChain小

对于简单的：

```
PDF聊天机器人
+
RAG
+
GPT-4/通义千问
```

使用Rasa可能过于复杂。

对于：

```
1000万次客户对话
+
合规要求
+
工作流
+
审计追踪
```

Rasa的价值就会大大体现。

---

## 我对AI咨询公司的看法

对于企业级AI项目，Rasa非常适合作为**代理编排层**：

```
              用户

               |
               v

        Rasa代理层

               |
       +-------+-------+
       |       |       |

      RAG    工具    LLM

       |       |       |

  向量数据库  API  通义千问/GPT/Claude

```

现代技术栈可以是：

* Rasa → 工作流 + 护栏机制
* vLLM → 自托管模型
* 通义千问/DeepSeek → 推理模型
* Milvus/PGVector → RAG
* Kubernetes → 部署

这与企业级“AI应用平台”项目的发展方向一致。

参考资料：

* [Rasa官方网站](https://rasa.com/?utm_source=chatgpt.com)
* [Rasa平台文档](https://rasa.com/docs/learn/platform-introduction/?utm_source=chatgpt.com)
* [Rasa GitHub仓库](https://github.com/RasaHQ/rasa?utm_source=chatgpt.com)

[1]: https://rasa.com/about?utm_source=chatgpt.com "关于Rasa | 构建可信、可扩展的AI代理"
[2]: https://rasa.com/platform?utm_source=chatgpt.com "Rasa平台 | 构建完全可控的可靠AI代理"
[3]: https://rasa.com/docs/learn/platform-introduction/?utm_source=chatgpt.com "Rasa平台介绍 | Rasa文档"
[4]: https://rasa.com/docs/pro/intro/?utm_source=chatgpt.com "欢迎使用Rasa | Rasa文档"
[5]: https://rasa.com/ai-info-page?utm_source=chatgpt.com "AI信息"
[6]: https://info.rasa.com/rasa-conversational-ai-platform-for-customer-experience?utm_source=chatgpt.com "Rasa对话式AI平台，打造卓越客户体验"
