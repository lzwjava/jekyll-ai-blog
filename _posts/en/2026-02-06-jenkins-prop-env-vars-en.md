---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Jenkins Properties as Environment Variables
translated: false
type: note
---

Yes, exactly! In Jenkins, "properties" typically refers to **environment variables** that are available during a job's execution.

There are a few ways properties/environment variables work in Jenkins:

1. **Environment variables** - Jenkins automatically provides built-in variables like `BUILD_NUMBER`, `JOB_NAME`, `WORKSPACE`, etc.

2. **Pipeline properties** - In declarative pipelines, you can set properties using the `environment` directive:

   ```groovy
   pipeline {
       environment {
           MY_VAR = 'some value'
       }
   }
   ```

3. **Properties file** - You can also load properties from a file (like a `.properties` file) and use them as environment variables in your build.

4. **Job parameters** - When you configure parameters for a job, they become available as environment variables during execution.

So yes, when people talk about "Jenkins properties" in the context of a running job, they're generally referring to these environment variables that the job can access and use during its execution.
