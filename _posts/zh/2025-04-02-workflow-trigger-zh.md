---
audio: false
generated: true
lang: zh
layout: post
title: 触发您的 GitHub 工作流
translated: true
type: note
---

您说得对，在前端代码中直接嵌入 GitHub 令牌确实存在安全风险。任何查看页面源代码的人都可能获取并滥用您的令牌。

以下是几种安全的方法，可以通过前端按钮触发 GitHub 工作流，附有解释和代码示例：

**核心思路：引入安全的后端组件**

最安全的处理方式是引入一个后端组件（一个 API 端点），它将：

1.  **从前端接收触发请求。**
2.  **安全地存储并使用您的 GitHub 令牌。**
3.  **向 GitHub 发起经过身份验证的 API 调用以触发您的工作流。**

这样，您敏感的 GitHub 令牌就永远不会离开您的服务器端环境。

以下是几种可供选择的后端方案：

**1. 无服务器函数（例如，AWS Lambda、Google Cloud Functions、Netlify Functions、Vercel Functions）**

对于像这样的简单 API 端点，这通常是一种轻量级且经济高效的解决方案。

*   **工作原理：** 您编写一个小型函数，并将其部署到无服务器平台。该函数将包含使用您存储的令牌调用 GitHub API 的逻辑。然后，您的前端按钮将向此无服务器函数的 URL 发出 HTTP 请求。

*   **示例（概念性 - 您需要根据所选平台进行调整）：**

    **无服务器函数代码（Python - 适用于 AWS Lambda/API Gateway 的示例）：**

    ```python
    import os
    import requests
    import json

    def handler(event, context):
        github_token = os.environ.get("GITHUB_TOKEN")
        if not github_token:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'GitHub token not configured'})
            }

        owner = "lzwjava"
        repo = "lzwjava.github.io"
        workflow_id = "nytimes.yml"
        ref = "main"
        api_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"

        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {github_token}',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/json'
        }
        payload = {'ref': ref}

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()  # 对于错误的状态码抛出异常
            return {
                'statusCode': 204,
                'body': ''
            }
        except requests.exceptions.RequestException as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Failed to trigger workflow: {e}'})
            }
    ```

    *   **重要提示：** 您需要在无服务器平台中配置一个环境变量（例如 `GITHUB_TOKEN`）来安全地存储您的 GitHub 个人访问令牌。

    **前端代码（修改后的 `nytimes.js`）：**

    ```javascript
    const nytimesDiv = document.querySelector('.nytimes');
    const backendApiUrl = '/.netlify/functions/trigger-nytimes-update'; // Netlify Functions 的示例

    if (nytimesDiv) {
        const updateButton = document.createElement('button');
        updateButton.textContent = '更新 NYTimes 文章';
        nytimesDiv.appendChild(updateButton);

        updateButton.addEventListener('click', () => {
            fetch(backendApiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}) // 对于简单的触发器，您可能不需要请求体
            })
            .then(response => {
                if (response.status === 204) {
                    alert('更新触发成功！请等待几分钟查看结果。');
                } else {
                    return response.json().then(data => {
                        alert(`更新失败。状态码: ${response.status}: ${data.error || '未知错误'}`);
                        console.error('更新失败:', response, data);
                    });
                }
            })
            .catch(error => {
                alert('更新失败。请检查控制台错误信息。');
                console.error('触发更新时出错:', error);
            });
        });
    } else {
        console.error("未找到 nytimes div 元素!");
    }
    ```

*   **部署：** 您需要将此无服务器函数部署
