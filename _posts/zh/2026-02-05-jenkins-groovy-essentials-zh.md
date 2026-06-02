---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Jenkins Groovy 脚本编程核心指南
translated: true
type: note
---

Jenkins 广泛地将 Groovy 用于 Pipeline 定义、Shared Libraries 以及系统管理。以下是一份帮助你入门的全面指南。

## Jenkins 中的 Groovy 脚本类型

**1. Declarative Pipeline** - 更简单、结构化的语法
**2. Scripted Pipeline** - 更灵活、拥有完整的 Groovy 能力
**3. Jenkins Script Console** - 用于管理任务
**4. Shared Libraries** - 在不同 Pipeline 之间复用的代码

## 基础 Scripted Pipeline

```groovy
node('linux') {
    stage('Checkout') {
        git branch: 'main', url: 'https://github.com/user/repo.git'
    }

    stage('Build') {
        sh 'mvn clean package'
    }

    stage('Test') {
        sh 'mvn test'
    }
}
```

## 基础 Declarative Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'make build'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'make test'
            }
        }
    }
}
```

## Jenkins 必备 Groovy 语法

### 变量 (Variables)

```groovy
// String 变量
def projectName = 'my-project'
String version = '1.0.0'

// Environment 变量
env.BUILD_VERSION = '1.2.3'
echo "Version: ${env.BUILD_VERSION}"

// Parameters
properties([
    parameters([
        string(name: 'BRANCH', defaultValue: 'main'),
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'])
    ])
])
```

### 条件语句 (Conditionals)

```groovy
if (env.BRANCH_NAME == 'main') {
    echo 'Building main branch'
} else if (env.BRANCH_NAME.startsWith('feature/')) {
    echo 'Feature branch'
} else {
    echo 'Other branch'
}

// 三元运算符
def env = (params.DEPLOY_ENV == 'prod') ? 'production' : 'development'
```

### 循环 (Loops)

```groovy
// For 循环
def servers = ['server1', 'server2', 'server3']
for (server in servers) {
    echo "Deploying to ${server}"
}

// Each 循环
servers.each { server ->
    echo "Processing ${server}"
}
```

### 错误处理的 Try-Catch

```groovy
stage('Deploy') {
    try {
        sh 'deploy.sh'
        currentBuild.result = 'SUCCESS'
    } catch (Exception e) {
        currentBuild.result = 'FAILURE'
        echo "Deployment failed: ${e.message}"
        throw e
    } finally {
        echo 'Cleaning up...'
    }
}
```

## 文件操作

```groovy
// 读取文件
def content = readFile('config.txt')

// 写入文件
writeFile file: 'output.txt', text: 'Hello Jenkins'

// 检查文件是否存在
if (fileExists('settings.xml')) {
    echo 'File exists'
}

// 归档制品 (Archive artifacts)
archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
```

## 常用的 Jenkins Steps

```groovy
// 执行 Shell 命令
sh 'echo "Hello from shell"'
sh returnStdout: true, script: 'pwd'

// Windows Batch
bat 'dir'

// Git 操作
git branch: 'develop', url: 'https://github.com/user/repo.git'

// 使用 Credentials 进行 Checkout
checkout([
    $class: 'GitSCM',
    branches: [[name: '*/main']],
    userRemoteConfigs: [[
        credentialsId: 'github-creds',
        url: 'https://github.com/user/repo.git'
    ]]
])

// 邮件通知
emailext(
    subject: "Build ${currentBuild.result}: ${env.JOB_NAME}",
    body: "Build URL: ${env.BUILD_URL}",
    to: 'team@example.com'
)
```

## 使用 Credentials

```groovy
withCredentials([
    usernamePassword(
        credentialsId: 'docker-hub',
        usernameVariable: 'DOCKER_USER',
        passwordVariable: 'DOCKER_PASS'
    )
]) {
    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
}

// SSH Key
withCredentials([sshUserPrivateKey(
    credentialsId: 'ssh-key',
    keyFileVariable: 'SSH_KEY'
)]) {
    sh 'ssh -i $SSH_KEY user@server'
}
```

## 并行执行 (Parallel Execution)

```groovy
stage('Parallel Tests') {
    parallel(
        'Unit Tests': {
            sh 'mvn test'
        },
        'Integration Tests': {
            sh 'mvn integration-test'
        },
        'Security Scan': {
            sh 'dependency-check.sh'
        }
    )
}
```

## 处理 JSON/XML

```groovy
// 解析 JSON
@Grab('org.codehaus.groovy:groovy-json:3.0.9')
import groovy.json.JsonSlurper

def jsonText = '{"name": "Jenkins", "version": "2.0"}'
def json = new JsonSlurper().parseText(jsonText)
echo "Name: ${json.name}"

// 从文件读取 JSON
def config = readJSON file: 'config.json'

// 写入 JSON
writeJSON file: 'output.json', json: [status: 'success', build: env.BUILD_NUMBER]
```

## 环境特定配置

```groovy
def environments = [
    dev: [url: 'https://dev.example.com', replicas: 1],
    prod: [url: 'https://prod.example.com', replicas: 3]
]

def targetEnv = environments[params.ENVIRONMENT]
echo "Deploying to ${targetEnv.url} with ${targetEnv.replicas} replicas"
```

## 高级 Pipeline 示例

```groovy
pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        APP_NAME = 'my-app'
    }

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'prod'])
        booleanParam(name: 'RUN_TESTS', defaultValue: true)
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                script {
                    def version = sh(returnStdout: true, script: 'git describe --tags').trim()
                    env.VERSION = version
                    echo "Building version ${version}"
                }
                sh "docker build -t ${DOCKER_REGISTRY}/${APP_NAME}:${env.VERSION} ."
            }
        }

        stage('Test') {
            when {
                expression { params.RUN_TESTS == true }
            }
            steps {
                sh 'npm test'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'k8s-token', variable: 'TOKEN')]) {
                        sh """
                            kubectl set image deployment/${APP_NAME} \
                            ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${env.VERSION} \
                            --namespace=${params.DEPLOY_ENV}
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            cleanWs()
        }
    }
}
```

## 最佳实践

1. **尽可能使用 Declarative Pipeline** - 更易于阅读和维护
2. **将脚本纳入版本控制** - 在你的仓库中使用 Jenkinsfile
3. **使用 Shared Libraries** 处理跨项目的通用功能
4. **通过 try-catch 块优雅地处理错误**
5. **使用 Parameters** 而不是硬编码数值
6. **使用 Jenkins Credential Store 保护凭据安全**
7. **构建后清理 Workspace** 以节省磁盘空间
8. **使用 Stages** 逻辑化地组织你的 Pipeline

你是否需要我在某个特定方面进行详细说明，例如 Shared Libraries、特定工具的使用或更高级的 Groovy 技术？
