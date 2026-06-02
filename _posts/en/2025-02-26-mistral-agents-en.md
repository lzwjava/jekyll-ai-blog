---
audio: false
generated: true
lang: en
layout: post
title: Mistral AI Agents
translated: false
type: note
---

Mistral AI Agents are autonomous systems powered by large language models (LLMs) designed to execute complex tasks based on high-level instructions. Leveraging advanced natural language processing, these agents can understand and carry out specific goals, making them suitable for a wide range of applications such as customer support, data analysis, workflow automation, and coding assistance. They can plan, utilize tools, take actions, and even collaborate to achieve specific objectives, offering a new level of automation and intelligence.

---

## Creating Agents

Mistral AI provides two primary methods for creating agents: the **La Plateforme Agent Builder** and the **Agent API**.

### 1. La Plateforme Agent Builder

The Agent Builder offers a user-friendly interface for creating agents without extensive technical knowledge. To create an agent:

- Navigate to the Agent Builder at [https://console.mistral.ai/build/agents/new](https://console.mistral.ai/build/agents/new).
- Customize the agent by selecting a model, setting the temperature, and providing optional instructions.
- Once configured, the agent can be deployed and accessed via the API or Le Chat.

### 2. Agent API

For developers, the Agent API allows programmatic creation and integration of agents into existing workflows. Below are examples of how to create and use an agent via the API:

#### Python Example

```python
import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

chat_response = client.agents.complete(
    agent_id="your-agent-id",
    messages=[{"role": "user", "content": "What is the best French cheese?"}],
)
print(chat_response.choices[0].message.content)
```

#### JavaScript Example

```javascript
import { Mistral } from '@mistralai/mistralai';

const apiKey = process.env.MISTRAL_API_KEY;
const client = new Mistral({ apiKey: apiKey });

const chatResponse = await client.agents.complete({
    agentId: "your-agent-id",
    messages: [{ role: 'user', content: 'What is the best French cheese?' }],
});
console.log('Chat:', chatResponse.choices[0].message.content);
```

---

## Customizing Agents

Mistral AI agents can be customized to fit specific needs through several options:

- **Model Selection**: Choose the model that powers the agent. Options include:
  - "Mistral Large 2" (default, `mistral-large-2407`)
  - "Mistral Nemo" (`open-mistral-nemo`)
  - "Codestral" (`codestral-2405`)
  - Fine-tuned models

- **Temperature**: Adjust the sampling temperature (between 0.0 and 1.0) to control the randomness of the agent's responses. Higher values make outputs more creative, while lower values make them more focused and deterministic.

- **Instructions**: Provide optional instructions to enforce specific behaviors across all interactions. For example, you can create an agent that only speaks French or generates Python code without explanations.

### Example: Creating a French-Speaking Agent

To create an agent that only responds in French:

- Set the model to "Mistral Large 2".
- Use instructions like: "Always respond in French, regardless of the language of the input."
- Provide few-shot examples to reinforce the behavior.

---

## Use Cases

Mistral AI agents can be applied across various industries and tasks. Some notable use cases include:

- **Customer Support**: Automate responses to common inquiries, handle FAQs, and escalate complex issues to human agents.
- **Data Analysis**: Create agents that analyze datasets, generate reports, or perform calculations based on user inputs.
- **Workflow Automation**: Integrate agents with tools like email, CRM systems, or payment processing to automate repetitive tasks.
- **Coding Assistance**: Design agents to generate code, provide debugging suggestions, or create unit tests.

### Specific Examples

- **French-Speaking Agent**: An agent configured to only respond in French, useful for businesses targeting French-speaking customers.
- **Python Code Generator**: An agent that outputs Python code snippets without explanations, ideal for developers needing quick, clean code.

---

## Deployment

Once an agent is created, it can be deployed and accessed in two ways:

- **API Integration**: Use the Mistral AI API to integrate the agent into your applications. See the code examples in the "Creating Agents" section for details.
- **Le Chat**: Toggle the option to chat with the agent directly on Mistral's Le Chat platform.

Agents can be easily shared within organizations, and with the advanced reasoning capabilities of models like Mistral Large 2, you can build complex workflows involving multiple agents.

---

This documentation provides a comprehensive guide to understanding, creating, customizing, and deploying Mistral AI agents, based on the official documentation at [https://docs.mistral.ai/capabilities/agents/](https://docs.mistral.ai/capabilities/agents/). By leveraging these tools, you can automate tasks, enhance productivity, and unlock new levels of efficiency in your workflows. For further details, explore the [Mistral AI documentation](https://docs.mistral.ai/capabilities/agents/).
