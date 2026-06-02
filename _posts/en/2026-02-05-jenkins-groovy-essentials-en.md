---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Jenkins Groovy Scripting Essentials Guide
translated: false
type: note
---

Jenkins uses Groovy extensively for pipeline definitions, shared libraries, and system administration. Here's a comprehensive guide to get you started.

## Types of Groovy Scripts in Jenkins

**1. Declarative Pipeline** - Simpler, structured syntax
**2. Scripted Pipeline** - More flexible, full Groovy power
**3. Jenkins Script Console** - Administrative tasks
**4. Shared Libraries** - Reusable code across pipelines

## Basic Scripted Pipeline

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

## Basic Declarative Pipeline

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

## Essential Groovy Syntax for Jenkins

### Variables

```groovy
// String variables
def projectName = 'my-project'
String version = '1.0.0'

// Environment variables
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

### Conditionals

```groovy
if (env.BRANCH_NAME == 'main') {
    echo 'Building main branch'
} else if (env.BRANCH_NAME.startsWith('feature/')) {
    echo 'Feature branch'
} else {
    echo 'Other branch'
}

// Ternary operator
def env = (params.DEPLOY_ENV == 'prod') ? 'production' : 'development'
```

### Loops

```groovy
// For loop
def servers = ['server1', 'server2', 'server3']
for (server in servers) {
    echo "Deploying to ${server}"
}

// Each loop
servers.each { server ->
    echo "Processing ${server}"
}
```

### Try-Catch for Error Handling

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

## Working with Files

```groovy
// Read file
def content = readFile('config.txt')

// Write file
writeFile file: 'output.txt', text: 'Hello Jenkins'

// Check if file exists
if (fileExists('settings.xml')) {
    echo 'File exists'
}

// Archive artifacts
archiveArtifacts artifacts: 'target/*.jar', fingerprint: true
```

## Common Jenkins Steps

```groovy
// Execute shell commands
sh 'echo "Hello from shell"'
sh returnStdout: true, script: 'pwd'

// Windows batch
bat 'dir'

// Git operations
git branch: 'develop', url: 'https://github.com/user/repo.git'

// Checkout with credentials
checkout([
    $class: 'GitSCM',
    branches: [[name: '*/main']],
    userRemoteConfigs: [[
        credentialsId: 'github-creds',
        url: 'https://github.com/user/repo.git'
    ]]
])

// Email notification
emailext(
    subject: "Build ${currentBuild.result}: ${env.JOB_NAME}",
    body: "Build URL: ${env.BUILD_URL}",
    to: 'team@example.com'
)
```

## Using Credentials

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

// SSH key
withCredentials([sshUserPrivateKey(
    credentialsId: 'ssh-key',
    keyFileVariable: 'SSH_KEY'
)]) {
    sh 'ssh -i $SSH_KEY user@server'
}
```

## Parallel Execution

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

## Working with JSON/XML

```groovy
// Parse JSON
@Grab('org.codehaus.groovy:groovy-json:3.0.9')
import groovy.json.JsonSlurper

def jsonText = '{"name": "Jenkins", "version": "2.0"}'
def json = new JsonSlurper().parseText(jsonText)
echo "Name: ${json.name}"

// Read JSON from file
def config = readJSON file: 'config.json'

// Write JSON
writeJSON file: 'output.json', json: [status: 'success', build: env.BUILD_NUMBER]
```

## Environment-Specific Configuration

```groovy
def environments = [
    dev: [url: 'https://dev.example.com', replicas: 1],
    prod: [url: 'https://prod.example.com', replicas: 3]
]

def targetEnv = environments[params.ENVIRONMENT]
echo "Deploying to ${targetEnv.url} with ${targetEnv.replicas} replicas"
```

## Advanced Pipeline Example

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

## Best Practices

1. **Use declarative pipelines when possible** - easier to read and maintain
2. **Keep scripts in version control** - use Jenkinsfile in your repository
3. **Use shared libraries** for common functionality across projects
4. **Handle errors gracefully** with try-catch blocks
5. **Use parameters** instead of hardcoding values
6. **Keep credentials secure** using Jenkins credential store
7. **Clean workspace** after builds to save disk space
8. **Use stages** to organize your pipeline logically

Would you like me to elaborate on any specific aspect, such as shared libraries, working with specific tools, or more advanced Groovy techniques?
