---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 搭建企微员工查询应用
translated: true
type: note
---

**问题：** 如何在企业微信中构建一个支持群组/服务应用，以便员工能用来查询信息？

**回答：**

## 在企业微信中构建内部支持查询应用

在企业微信中，你想构建的被称为**自建应用** —— 类似于面向员工的“服务通道”。这与面向外部用户的微信公众服务号不同。企业微信自建应用存在于企业内部，仅对员工可见，并能自动回复他们的查询。

根据你的技术能力，主要有两种方法：

---

## 方法一：无代码/低代码 —— 使用企业微信内置的“智能机器人”

这是**最快的方法**，尤其是在企业微信5.0之后。企业微信的“智能机器人”功能允许品牌上传内部知识集，并构建针对各部门的专用AI助手，例如门店助手、IT助手或HR助手。这些智能助手可以即时响应员工咨询。

### 步骤

**步骤1：登录企业微信管理后台**

- 前往 [work.weixin.qq.com](https://work.weixin.qq.com) 并以管理员身份登录。
- 导航至**应用管理**。

**步骤2：创建自建应用**

- 点击**创建应用**。
- 上传图标，设置应用名称（例如"HR支持"、"IT帮助台"），填写描述。
- 将**可见范围**设置为相关员工分组或整个组织。
- 点击**创建**。

**步骤3：启用AI机器人/智能机器人**

- 在新创建的应用设置内，找到**AI机器人 / 智能机器人**。
- 上传公司的知识库文档（常见问题、HR政策、IT指南、产品手册等）。
- 配置机器人的欢迎消息和自动回复规则。
- 智能助手可以提供即时响应并生成个性化脚本 —— 知识库可包含部门特定的制度信息，员工可以7x24小时查询。

**步骤4：配置自动回复和FAQ规则**

- 在**消息接收**下，启用基于关键词的自动回复。
- 将常见的员工问题（例如“如何申请休假？”、“IT帮助台电话是多少？”）映射到预先写好的答案。

**步骤5：发布给员工**

- 保存并发布应用。员工将在其企业微信应用中的**工作台**选项卡下看到它。
- 员工只需打开应用并输入问题即可收到即时回复。

---

## 方法二：开发者模式 —— 通过API构建自定义查询机器人

这种方法提供完全的控制权。在企业微信应用管理中，创建应用，设置图标、名称、描述和可见范围。然后在新创建的应用设置页面，复制**AgentId**和**Secret**信息，以备后续在后端系统中使用。点击“接收消息”并选择“设置API接收”，然后生成一个**Token**和**EncodingAESKey**。

### 架构概览

```
员工在企业微信应用中发送消息
        ↓
企业微信将消息转发至你的Webhook URL
        ↓
你的后端服务器接收并处理查询
        ↓
后端查询你的数据库/知识库/LLM
        ↓
后端调用企业微信API发送回复
        ↓
员工在企业微信应用中收到答案
```

### 分步指南

**步骤1：在管理后台注册应用**

- 进入**应用管理 → 创建应用**（同上）。
- 记下：`CorpID`、`AgentId`、`AgentSecret`。

**步骤2：设置消息接收（Webhook）**

- 在应用设置中，进入**接收消息 → 设置API接收**。
- 生成随机的`Token`和`EncodingAESKey`。
- 输入你服务器的回调URL（必须是可通过HTTPS公开访问的）。
- 企业微信将通过发送GET请求来验证URL——你的服务器必须正确响应。

**步骤3：配置可信IP白名单**

- 企业微信应用接收消息需要配置可信IP列表。该列表由你服务所在服务器的出口IP组成。未配置此列表将导致企业微信与你的系统之间通信失败。

**步骤4：构建后端服务器**

示例（Node.js / Python伪代码）：

```python
# Flask 示例 - 接收并回复员工查询
from flask import Flask, request
import xml.etree.ElementTree as ET
import requests

app = Flask(__name__)

@app.route('/wecom/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        # 与企业微信进行URL验证
        return verify_signature(request)

    # 解析传入的XML消息
    xml_data = ET.fromstring(request.data)
    user_query = xml_data.find('Content').text
    from_user = xml_data.find('FromUserName').text

    # 查询你的知识库或LLM
    answer = query_knowledge_base(user_query)

    # 通过企业微信API发送回复
    send_wecom_message(from_user, answer)
    return 'success'

def send_wecom_message(to_user, content):
    access_token = get_access_token()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    payload = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": YOUR_AGENT_ID,
        "text": {"content": content}
    }
    requests.post(url, json=payload)
```

**步骤5：连接到知识库或LLM（可选但功能强大）**

为实现智能回复，将你的后端连接到：

- **FAQ数据库**（例如通过API连接的MySQL、Notion、Google Sheets）
- 通过API连接的**LLM**，如Claude或GPT，用于自然语言理解
- 搜索你内部文档的**RAG（检索增强生成）** 系统

**步骤6：测试与部署**

- 从企业微信内的员工账号发送测试消息。
- 验证机器人是否收到消息并正确回复。
- 监控日志中的错误。

---

## 方法三：第三方无代码平台

如果完全不想编码，有几个第三方平台与企业微信集成：

像SaleSmartly这样的平台与DeepSeek和ChatGPT等AI引擎深度集成。企业可以通过API连接到企业微信，在此类平台上配置自动回复、FAQ回复和订单跟踪，从而显著加快响应时间。

其他选项包括：

- **Hengshi SENSE** —— 用于连接业务数据集的数据问答机器人
- **Omnichat** —— 用于多渠道客户支持管理
- **SaleSmartly** —— 用于CRM + AI聊天机器人自动化

---

## 总结对比

| 方法 | 所需技术能力 | 设置时间 | 灵活性 |
|---|---|---|---|
| 企业微信AI机器人（内置） | 无 | 分钟级 | 中等 |
| 自定义API Webhook | 需要开发者 | 天级 | 完全 |
| 第三方平台 | 低 | 小时级 | 中-高 |

---

## 关键提示

- 员工通过其企业微信应用中的**工作台**选项卡访问支持应用。
- 企业微信的AI驱动聊天机器人可以协助客户服务、自动化常规任务，并对常见查询提供即时响应，从而简化工作流程并提高效率。
- 对于敏感的HR或IT数据，确保你的后端使用HTTPS并遵循企业微信的加密消息格式。
- 在全公司推广前，始终先用小范围用户组测试。

---

**参考资料：**

- [企业微信官方网站](https://work.weixin.qq.com/)
- [企业微信数据问答机器人配置 —— 衡石文档](https://docs.hengshi.com/v6.0/en-us/chatbot-wecom.html)
- [企业微信 + DeepSeek智能机器人 —— IT Consultis](https://it-consultis.com/insights/wechat-wecom-integrating-deepseek/)
- [企业微信功能概览 —— Choose Oxygen](https://www.chooseoxygen.com/en/blog/everything-you-should-know-about-wechat-work)
- [企业微信AI与私域策略 —— SaleSmartly](https://www.salesmartly.com/en/blog/docs/enterprise-wechat)
