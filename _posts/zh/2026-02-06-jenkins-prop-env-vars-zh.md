---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 将 Jenkins 属性作为环境变量
translated: true
type: note
---

没错，正是如此！在 Jenkins 中，“properties” 通常是指在 Job 执行期间可用的 **environment variables**。

在 Jenkins 中，properties/environment variables 的工作方式有以下几种：

1. **Environment variables** - Jenkins 会自动提供内置变量，例如 `BUILD_NUMBER`、`JOB_NAME`、`WORKSPACE` 等。

2. **Pipeline properties** - 在 declarative pipelines 中，你可以使用 `environment` 指令来设置属性：

    ```groovy
    pipeline {
        environment {
            MY_VAR = 'some value'
        }
    }
    ```

3. **Properties file** - 你也可以通过一个文件（如 `.properties` 文件）加载属性，并在 build 过程中将其作为 environment variables 使用。

4. **Job parameters** - 当你为 Job 配置参数时，它们在执行期间会变为可用的 environment variables。

所以，没错，当人们在运行 Job 的语境下谈论 “Jenkins properties” 时，他们通常指的就是这些 Job 在执行期间可以访问并使用的 environment variables。
