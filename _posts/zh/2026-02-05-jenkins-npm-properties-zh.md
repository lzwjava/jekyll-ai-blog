---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: npm 命令的 Jenkins 属性
translated: true
type: note
---

我将帮助解释 Jenkins properties 的工作原理以及如何将它们与 npm 命令结合使用。

## Jenkins Properties 概述

Jenkins properties 是可以通过多种方式定义的 environment variables：

1. **Build parameters** - 在配置 job 时定义
2. **Environment variables** - 在 Jenkins 配置或 pipeline 中设置
3. **Properties files** - 使用 `readProperties` 或类似方法加载
4. **Credentials** - 存储在 Jenkins 中的安全值

## 在 npm 命令中使用 Properties

是的，你完全可以为 npm 命令使用 Jenkins properties！方法如下：

### 在 Pipeline 中：

```groovy
pipeline {
    agent any
    
    environment {
        NPM_AUTH_URL = 'https://registry.npmjs.org/'
        NPM_TOKEN = credentials('npm-token-id')
    }
    
    stages {
        stage('Install') {
            steps {
                sh '''
                    echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc
                    npm install --registry=${NPM_AUTH_URL}
                '''
            }
        }
    }
}
```

### 在 Freestyle Job 中：

1. 在 job 配置中定义 environment variables
2. 在 build steps 中使用 `${VARIABLE_NAME}` (Linux) 或 `%VARIABLE_NAME%` (Windows) 引用它们

### 常见模式：

**使用 .npmrc 配置：**

```groovy
sh '''
    npm config set registry ${NPM_AUTH_URL}
    npm config set //registry.npmjs.org/:_authToken ${NPM_TOKEN}
    npm install
'''
```

**作为命令参数传递：**

```groovy
sh "npm install --registry=${NPM_AUTH_URL}"
```

**使用 withEnv 代码块：**

```groovy
withEnv(["NPM_AUTH_URL=https://registry.npmjs.org/"]) {
    sh 'npm install --registry=$NPM_AUTH_URL'
}
```

关键点在于 Jenkins properties 会转换为可以在 shell 命令中访问的 environment variables。对于像 tokens 这样的敏感数据，请始终使用 Jenkins credentials 而不是纯文本 properties。