---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Jenkins Secure NPM Private Package Access
translated: false
type: note
---

Yes, absolutely! This is very useful in Jenkins builds for accessing private npm packages. Here are the common approaches:

## 1. Using Jenkins Credentials (Recommended)

Store your token as a Jenkins credential, then use it in your pipeline:

```groovy
pipeline {
    agent any

    environment {
        NPM_TOKEN = credentials('npm-registry-token') // ID of your Jenkins credential
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

## 2. Using .npmrc File with Token Substitution

Create an `.npmrc.template` in your repo:

```
//registry.npmjs.org/:_authToken=${NPM_TOKEN}
```

Then in Jenkins:

```groovy
steps {
    sh '''
        envsubst < .npmrc.template > .npmrc
        npm install
    '''
}
```

## 3. For Private Registries (e.g., Nexus, Artifactory)

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

- **Never** commit `.npmrc` with tokens to git
- Add `.npmrc` to `.gitignore`
- Use Jenkins credentials store (Secret text type)
- Clean up config after build if needed: `npm config delete //registry.org/:_authToken`

This approach keeps your tokens secure and makes your builds reproducible across different environments.
