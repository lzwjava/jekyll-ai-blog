---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Jenkins 安全访问 NPM 私有包
translated: true
type: note
---

是的，完全可以！这在 Jenkins 构建中访问私有 npm packages 非常有用。以下是常用的方法：

## 1. 使用 Jenkins Credentials（推荐）

将你的 token 存储为 Jenkins credential，然后在 pipeline 中使用它：

```groovy
pipeline {
    agent any
    
    environment {
        NPM_TOKEN = credentials('npm-registry-token') // 你的 Jenkins credential ID
    }
    
    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    npm config set //registry.npmjs.org/:_authToken ${NPM_TOKEN}
                    npm install
                '''
            }
        }
    }
}
```

## 2. 使用包含 Token 替换变量的 .npmrc 文件

在仓库中创建一个 `.npmrc.template`：

```
//registry.npmjs.org/:_authToken=${NPM_TOKEN}
```

然后在 Jenkins 中：

```groovy
steps {
    sh '''
        envsubst < .npmrc.template > .npmrc
        npm install
    '''
}
```

## 3. 针对 Private Registries (例如 Nexus, Artifactory)

```groovy
environment {
    REGISTRY_TOKEN = credentials('private-registry-token')
}

steps {
    sh '''
        npm config set //your-registry.com/:_authToken ${REGISTRY_TOKEN}
        npm config set registry https://your-registry.com/
        npm install
    '''
}
```

## Security Best Practices

- **切勿**将包含 tokens 的 `.npmrc` 提交到 git
- 将 `.npmrc` 添加到 `.gitignore`
- 使用 Jenkins credentials store (类型选 Secret text)
- 如果需要，在构建后清理配置：`npm config delete //registry.org/:_authToken`

这种方法可以确保你的 tokens 安全，并使你的构建在不同环境之间具有可复现性。