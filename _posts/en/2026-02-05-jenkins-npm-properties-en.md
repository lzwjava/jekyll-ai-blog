---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Jenkins Properties for npm Commands
translated: false
type: note
---

I'll help explain how Jenkins properties work and how they can be used with npm commands.

## Jenkins Properties Overview

Jenkins properties are environment variables that can be defined in several ways:

1. **Build parameters** - defined when configuring a job
2. **Environment variables** - set in Jenkins configuration or pipeline
3. **Properties files** - loaded using `readProperties` or similar
4. **Credentials** - secure values stored in Jenkins

## Using Properties with npm Commands

Yes, you can definitely use Jenkins properties for npm commands! Here's how:

### In a Pipeline:

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

### In a Freestyle Job:

1. Define environment variables in the job configuration
2. Reference them in your build steps using `${VARIABLE_NAME}` (Linux) or `%VARIABLE_NAME%` (Windows)

### Common Patterns:

**Using .npmrc configuration:**
```groovy
sh '''
    npm config set registry ${NPM_AUTH_URL}
    npm config set //registry.npmjs.org/:_authToken ${NPM_TOKEN}
    npm install
'''
```

**Passing as command arguments:**
```groovy
sh "npm install --registry=${NPM_AUTH_URL}"
```

**Using withEnv block:**
```groovy
withEnv(["NPM_AUTH_URL=https://registry.npmjs.org/"]) {
    sh 'npm install --registry=$NPM_AUTH_URL'
}
```

The key is that Jenkins properties become environment variables that are accessible in your shell commands. For sensitive data like tokens, always use Jenkins credentials rather than plain text properties.
