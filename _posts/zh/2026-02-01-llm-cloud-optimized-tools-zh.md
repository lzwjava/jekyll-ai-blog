---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 大模型优化的云基础设施工具
translated: true
type: note
---

我将搜索对 LLM 友好、强调文本配置和 infrastructure-as-code 方法的云平台。根据我的调研，以下是使用文本配置的**最佳 LLM 友好型云基础设施平台**：

## 顶级推荐

### **1. Pulumi** (对 LLM 最友好)
Pulumi 允许你使用通用编程语言（如 TypeScript, Python, Go, C#, Java 或 YAML）来定义基础设施。这对 LLM 来说非常理想，因为：

- **使用熟悉的语言** - LLM 已经在 Python, TypeScript 等语言上进行了广泛训练。
- **真实的编程结构** - 支持 loops, conditions, functions, classes。
- **多云支持** - 支持 AWS, Azure, GCP 以及 100 多个 provider。
- 与领域特定语言（DSL）相比，LLM 在使用标准编程语言时，能更有效地将自然语言提示词（prompts）翻译成基础设施代码。

### **2. AWS CDK (Cloud Development Kit)**
- 支持使用 TypeScript, Python, Java, C# 和 Go 来定义 AWS 基础设施。
- 将代码转换为 CloudFormation templates。
- 最适合仅限 AWS 的环境。
- 提供具有 autocomplete 功能的深度 IDE 集成。

### **3. CDK for Terraform (CDKTF)**
- 允许使用 TypeScript, Python, Go, C# 和 Java 定义基础设施，然后将其转译为 Terraform JSON。
- 结合了 Terraform 的生态系统与编程语言的优势。
- 支持多云。

### **4. 传统的基于 YAML 的工具**
对于更简单的需求：
- **Kubernetes** - YAML manifests
- **AWS CloudFormation** - YAML/JSON templates
- **Ansible** - YAML playbooks
- YAML 提供了一种声明式的、人类可读的格式，能够减少错误并增强 scalability。

## 为什么这些工具与 LLM 配合良好

最近的研究表明，像 DeepSeek-R1 和 GPT-4 这样的 LLM 可以有效地生成 infrastructure-as-code 配置，其中 DeepSeek 的成本比 GPT-4 便宜约 30 倍。核心优势包括：

1. **全文本化** - 易于复制、编辑和 version control。
2. **LLM 训练数据** - 模型处理过来自 GitHub 和其他渠道的数百万个 YAML 文件和基础设施代码。
3. **迭代优化** - LLM 可以从部署错误中学习，并通过反馈循环优化基础设施代码。

## 实际工作流

```python
# 示例：要求 LLM 生成 Pulumi 代码
"使用 Python 创建带有 API Gateway 的 AWS Lambda 函数"

# LLM 生成 Pulumi Python 代码：
import pulumi
import pulumi_aws as aws

lambda_role = aws.iam.Role("lambdaRole", ...)
lambda_function = aws.lambda_.Function("myFunction", ...)
api_gateway = aws.apigatewayv2.Api("httpApi", ...)
```

**我的建议**：如果你希望获得最大的 LLM 辅助，请从 **Pulumi** 开始。它结合了真实编程语言（LLM 理解得很好）的优点，以及易于生成、复制和修改的文本配置。
