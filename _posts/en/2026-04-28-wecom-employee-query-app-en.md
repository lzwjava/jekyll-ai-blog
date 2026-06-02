---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building a WeCom Employee Query App
translated: false
type: note
---

**Question:** How do you build a support group / service application (服务号) in Enterprise WeChat (WeCom) so that employees can use it to query messages?

**Answer:**

## Building an Internal Support Query App in Enterprise WeChat (WeCom)

In WeCom (Enterprise WeChat), what you want to build is called a **自建应用 (Self-Built Internal Application)** — the equivalent of a "service channel" for employees. This is different from a WeChat public 服务号 (which targets external users). The WeCom self-built app lives inside the enterprise, visible only to your employees, and can respond to their queries automatically.

There are two main approaches depending on your technical capability:

---

## Approach 1: No-Code / Low-Code — Use WeCom's Built-in "Intelligent Robot" (AI Bot)

This is the **fastest approach**, especially after WeCom 5.0. WeCom's "Intelligent Robot" feature allows brands to upload internal knowledge sets and build dedicated AI-powered assistants tailored to various departments — such as a Store Assistant, IT Assistant, or HR Assistant. These intelligent assistants can provide instant responses to employee inquiries.

### Steps:

**Step 1: Log into the WeCom Admin Console**
- Go to [work.weixin.qq.com](https://work.weixin.qq.com) and log in as the admin.
- Navigate to **应用管理 (App Management)**.

**Step 2: Create a Self-Built Application**
- Click **创建应用 (Create Application)**.
- Upload a logo, set the app name (e.g., "HR Support", "IT Helpdesk"), write a description.
- Set **Visibility Scope** to the relevant employee groups or the entire organization.
- Click **创建 (Create)**.

**Step 3: Enable the AI Bot / Intelligent Robot**
- Inside the newly created app settings, find **AI Robot / 智能机器人**.
- Upload your company's knowledge base documents (FAQs, HR policies, IT guides, product manuals, etc.).
- Configure the bot's greeting message and auto-reply rules.
- The intelligent assistant can provide instant responses and generate personalized scripts — knowledge can include department-specific institutional information, and employees can query this 24/7.

**Step 4: Configure Auto-Reply and FAQ Rules**
- Under **消息接收 (Message Reception)**, enable keyword-based auto-replies.
- Map common employee questions (e.g., "How do I apply for leave?", "What is the IT helpdesk number?") to pre-written answers.

**Step 5: Publish to Employees**
- Save and publish the app. Employees will see it in their WeCom app under the **工作台 (Workbench)** tab.
- Employees simply open the app and type their question to receive an instant reply.

---

## Approach 2: Developer Mode — Build a Custom Query Bot via API

This approach gives full control. In the Enterprise WeChat App Management, you create an app, set the logo, name, description, and visibility scope. Then on the settings page of the newly created application, you copy the **AgentId** and **Secret** information for later use in your backend system. Click on "Receive Messages" and select "Set API Reception," then generate a **Token** and **EncodingAESKey**.

### Architecture Overview

```
Employee sends message in WeCom app
        ↓
WeCom forwards message to your webhook URL
        ↓
Your backend server receives & processes query
        ↓
Backend queries your database / knowledge base / LLM
        ↓
Backend calls WeCom API to send reply back
        ↓
Employee receives answer in WeCom app
```

### Step-by-Step:

**Step 1: Register the App in Admin Console**
- Go to **App Management → Create App** (same as above).
- Note down: `CorpID`, `AgentId`, `AgentSecret`.

**Step 2: Set Up Message Receiving (Webhook)**
- In the app settings, go to **接收消息 (Receive Messages) → Set API Reception**.
- Generate a random `Token` and `EncodingAESKey`.
- Enter your server's callback URL (must be publicly accessible via HTTPS).
- WeCom will verify the URL by sending a GET request — your server must respond correctly.

**Step 3: Configure Trusted IP Whitelist**
- The enterprise WeChat application receiving messages needs to configure a list of trusted IPs. This list consists of the outbound IPs of the server where your service is located. Failure to configure this list will result in communication failure between Enterprise WeChat and your system.

**Step 4: Build Your Backend Server**

Example (Node.js / Python pseudocode):

```python
# Flask example - receive and reply to employee queries
from flask import Flask, request
import xml.etree.ElementTree as ET
import requests

app = Flask(__name__)

@app.route('/wecom/callback', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        # Verify URL with WeCom
        return verify_signature(request)

    # Parse incoming XML message
    xml_data = ET.fromstring(request.data)
    user_query = xml_data.find('Content').text
    from_user = xml_data.find('FromUserName').text

    # Query your knowledge base or LLM
    answer = query_knowledge_base(user_query)

    # Send reply via WeCom API
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

**Step 5: Connect to a Knowledge Base or LLM (Optional but Powerful)**

For intelligent responses, connect your backend to:
- A **FAQ database** (e.g., MySQL, Notion, Google Sheets via API)
- An **LLM** like Claude or GPT via API for natural language understanding
- A **RAG (Retrieval-Augmented Generation)** system that searches your internal documents

**Step 6: Test and Deploy**
- Send a test message from an employee account inside WeCom.
- Verify the bot receives the message and replies correctly.
- Monitor logs for errors.

---

## Approach 3: Third-Party No-Code Platforms

If you don't want to code at all, several third-party platforms integrate with WeCom:

Platforms like SaleSmartly deeply integrate with AI engines like DeepSeek and ChatGPT. Businesses can configure automated replies, FAQ responses, and order tracking within such platforms through API connections to WeCom, dramatically accelerating response times.

Other options include:
- **Hengshi SENSE** — for data Q&A bots connected to business datasets
- **Omnichat** — for multi-channel customer support management
- **SaleSmartly** — for CRM + AI chatbot automation

---

## Summary Comparison

| Method | Technical Skill Needed | Setup Time | Flexibility |
|---|---|---|---|
| WeCom AI Bot (Built-in) | None | Minutes | Medium |
| Custom API Webhook | Developer required | Days | Full |
| Third-Party Platform | Low | Hours | Medium–High |

---

## Key Tips

- Employees access the support app via the **工作台 (Workbench)** tab in their WeCom app.
- WeCom's AI-powered chatbots can assist with customer service, automate routine tasks, and provide instant responses to common queries, streamlining workflow and increasing efficiency.
- For sensitive HR or IT data, ensure your backend uses HTTPS and respects WeCom's encrypted message format.
- Always test with a small group before rolling out company-wide.

---

**References:**

- [WeCom Official Site](https://work.weixin.qq.com/)
- [WeCom Data Q&A Bot Configuration — Hengshi Docs](https://docs.hengshi.com/v6.0/en-us/chatbot-wecom.html)
- [WeCom + DeepSeek Intelligent Robot — IT Consultis](https://it-consultis.com/insights/wechat-wecom-integrating-deepseek/)
- [WeCom Features Overview — Choose Oxygen](https://www.chooseoxygen.com/en/blog/everything-you-should-know-about-wechat-work)
- [WeCom AI & Private Domain Strategy — SaleSmartly](https://www.salesmartly.com/en/blog/docs/enterprise-wechat)
