---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Getting Started with AWS Lambda
translated: false
type: note
---

### Getting Started with AWS Lambda

AWS Lambda is a serverless compute service that runs your code in response to events without managing servers. Here's a beginner-friendly step-by-step guide to creating, deploying, and using your first Lambda function. This is based on the official AWS documentation.

#### Prerequisites
- An active AWS account. Sign up at [aws.amazon.com](https://aws.amazon.com/) if you don't have one.
- Basic familiarity with a programming language like Node.js or Python (Lambda supports many runtimes).

#### Step 1: Create a Lambda Function
1. Log in to the AWS Management Console and navigate to the Lambda service (search for "Lambda" in the services menu).
2. On the Functions page, click **Create function**.
3. Choose **Author from scratch**.
4. Enter a **Function name** (e.g., `my-first-function`).
5. Select a **Runtime** (e.g., Node.js 22.x or Python 3.13).
6. Leave the default architecture (x86_64) and click **Create function**.

This automatically creates an execution role (an IAM role) with basic permissions, like writing logs to Amazon CloudWatch.

#### Step 2: Write Your Code
In the Lambda console's code editor (under the **Code** tab), replace the default "Hello World" code with something simple. Here's an example that calculates the area of a rectangle based on input JSON with `length` and `width` keys.

- **Node.js example**:
  ```javascript
  exports.handler = async (event) => {
    const length = event.length;
    const width = event.width;
    const area = length * width;
    console.log(`The area is ${area}`);
    console.log('Log group: /aws/lambda/' + process.env.AWS_LAMBDA_FUNCTION_NAME);
    return { area: area };
  };
  ```

- **Python example**:
  ```python
  import json

  def lambda_handler(event, context):
    length = event['length']
    width = event['width']
    area = length * width
    print(f"The area is {area}")
    print(f"Log group: /aws/lambda/{context.function_name}")
    return {
        'statusCode': 200,
        'body': json.dumps({'area': area})
    }
  ```

Save the changes—deployment happens automatically for interpreted languages.

For compiled languages (e.g., Java), create a deployment package locally and upload it via the console or AWS CLI.

#### Step 3: Test Your Function
1. In the **Test** tab, click **Create new test event**.
2. Name it (e.g., `test-area-calc`).
3. Paste sample JSON input:
   ```json
   {
     "length": 6,
     "width": 7
   }
   ```
4. Save and click **Test**.

View results in the **Execution results** section (e.g., `{"area": 42}`). Check logs in CloudWatch for details like duration and memory usage.

#### Step 4: Invoke and Monitor
- **Manual invocation**: Use the console's Test button or AWS CLI: `aws lambda invoke --function-name my-first-function output.json`.
- **Event-driven invocation**: Connect triggers like API Gateway, S3 buckets, or DynamoDB streams. Go to the **Configuration** > **Triggers** tab to add them.
- **Logs**: Automatically sent to CloudWatch Logs. View at [console.aws.amazon.com/cloudwatch/home#logsV2:log-groups](https://console.aws.amazon.com/cloudwatch/home#logsV2:log-groups) under `/aws/lambda/your-function-name`.

Key concepts:
- **Event sources/triggers**: Services (e.g., S3 upload) that invoke your function with event data (JSON payload).
- **Handler**: The entry point (e.g., `index.handler` for Node.js) that processes the event.

#### Step 5: Clean Up (Optional)
Delete the function via the console: Actions > Delete. Also remove associated logs and IAM roles to avoid charges.

#### Tips
- Start with the free tier (1M requests/month).
- Use AWS SAM or Serverless Framework for advanced deployments.
- For production, configure environment variables, layers, and VPC settings in the **Configuration** tab.

[Create your first Lambda function](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)
