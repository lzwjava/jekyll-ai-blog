---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: AWS Lambda 入门指南
translated: true
type: note
---

### AWS Lambda 入门指南

AWS Lambda 是一项无服务器计算服务，可在事件触发时运行代码而无需管理服务器。以下是为初学者提供的分步指南，介绍如何创建、部署和使用第一个 Lambda 函数。本文基于 AWS 官方文档编写。

#### 准备工作

- 有效的 AWS 账户（若尚未注册，请访问 [aws.amazon.com](https://aws.amazon.com/)）
- 对 Node.js 或 Python 等编程语言有基本了解（Lambda 支持多种运行时环境）

#### 第一步：创建 Lambda 函数

1. 登录 AWS 管理控制台，进入 Lambda 服务（在服务菜单中搜索 "Lambda"）
2. 在函数页面点击 **创建函数**
3. 选择 **从头开始编写**
4. 输入 **函数名称**（例如 `my-first-function`）
5. 选择 **运行时环境**（如 Node.js 22.x 或 Python 3.13）
6. 保持默认架构（x86_64）并点击 **创建函数**

系统将自动创建具有基本权限的执行角色（IAM 角色），例如将日志写入 Amazon CloudWatch 的权限。

#### 第二步：编写代码

在 Lambda 控制台的代码编辑器（位于 **代码** 标签页）中，替换默认的 "Hello World" 代码。以下是一个根据包含 `length` 和 `width` 键的输入 JSON 计算矩形面积的简单示例：

- **Node.js 示例**：

  ```javascript
  exports.handler = async (event) => {
    const length = event.length;
    const width = event.width;
    const area = length * width;
    console.log(`面积为 ${area}`);
    console.log('日志组: /aws/lambda/' + process.env.AWS_LAMBDA_FUNCTION_NAME);
    return { area: area };
  };
  ```

- **Python 示例**：

  ```python
  import json

  def lambda_handler(event, context):
    length = event['length']
    width = event['width']
    area = length * width
    print(f"面积为 {area}")
    print(f"日志组: /aws/lambda/{context.function_name}")
    return {
        'statusCode': 200,
        'body': json.dumps({'area': area})
    }
  ```

保存更改后，解释型语言会自动部署。对于编译型语言（如 Java），需在本地创建部署包并通过控制台或 AWS CLI 上传。

#### 第三步：测试函数

1. 在 **测试** 标签页点击 **创建新测试事件**
2. 命名事件（如 `test-area-calc`）
3. 粘贴示例 JSON 输入：

   ```json
   {
     "length": 6,
     "width": 7
   }
   ```

4. 保存并点击 **测试**

在 **执行结果** 部分查看结果（如 `{"area": 42}`），可通过 CloudWatch 日志查看持续时间、内存使用量等详细信息。

#### 第四步：调用与监控

- **手动调用**：使用控制台测试按钮或 AWS CLI：`aws lambda invoke --function-name my-first-function output.json`
- **事件驱动调用**：配置 API Gateway、S3 存储桶或 DynamoDB 流等触发器（通过 **配置 > 触发器** 标签页添加）
- **日志**：自动发送至 CloudWatch 日志，可通过 [console.aws.amazon.com/cloudwatch/home#logsV2:log-groups](https://console.aws.amazon.com/cloudwatch/home#logsV2:log-groups) 在 `/aws/lambda/函数名称` 路径下查看

核心概念：

- **事件源/触发器**：通过事件数据（JSON 载荷）调用函数的服务（如 S3 文件上传）
- **处理程序**：处理事件的入口点（如 Node.js 的 `index.handler`）

#### 第五步：清理资源（可选）

通过控制台删除函数：操作 > 删除。同时删除关联的日志和 IAM 角色以避免产生费用。

#### 实用技巧

- 从免费套餐开始（每月 100 万次请求）
- 使用 AWS SAM 或 Serverless Framework 进行高级部署
- 生产环境中通过 **配置** 标签页设置环境变量、层和 VPC

[创建您的第一个 Lambda 函数](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)
