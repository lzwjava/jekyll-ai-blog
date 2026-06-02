---
audio: false
generated: false
image: false
lang: en
layout: post
title: Companies Should Provide AI Context to Facilitate Integration
translated: false
type: post
---

I have a friend who works at Greptime DB, and I’ve been thinking about how to quickly integrate their product into existing systems.

## Context

One potential approach is to provide more AI context. Greptime DB could organize its documentation in a way that is compatible with AI tools like ChatGPT, streamlining the integration process.

Greptime DB offers documentation at [https://greptime.com](https://greptime.com), but I wonder if tools like ChatGPT or DeepSeek can efficiently process all the pages in their documentation. Additionally, a wealth of information is spread across GitHub repositories, issues, internal documents, public documents, and other pieces of hidden knowledge that aren’t explicitly documented.

To address this, Greptime DB might need to create several specialized GPTs. For example, they could create prompts like this:

```

### Greptime Docs:
Official documentation is available at: [https://docs.greptime.com](https://docs.greptime.com)

* [Quickstart Guide](https://docs.greptime.com/getting-started/quick-start)
* [User Guide](https://docs.greptime.com/user-guide/overview)
* [Demos](https://github.com/GreptimeTeam/demo-scene)
* [FAQ](https://docs.greptime.com/faq-and-others/faq)

### Repository URLs:
Here are the key directories and files from the root of the GreptimeDB repository:

1. [benches](https://github.com/GreptimeTeam/greptimedb/tree/main/benches)
2. [docs](https://github.com/GreptimeTeam/greptimedb/tree/main/docs)
3. [src](https://github.com/GreptimeTeam/greptimedb/tree/main/src)
4. [test](https://github.com/GreptimeTeam/greptimedb/tree/main/test)
5. [third_party](https://github.com/GreptimeTeam/greptimedb/tree/main/third_party)
6. [tools](https://github.com/GreptimeTeam/greptimedb/tree/main/tools)

Additional key files:

7. [Cargo.lock](https://github.com/GreptimeTeam/greptimedb/tree/main/Cargo.lock)
8. [Cargo.toml](https://github.com/GreptimeTeam/greptimedb/tree/main/Cargo.toml)
9. [LICENSE](https://github.com/GreptimeTeam/greptimedb/tree/main/LICENSE)
10. [Makefile](https://github.com/GreptimeTeam/greptimedb/tree/main/Makefile)
11. [README.md](https://github.com/GreptimeTeam/greptimedb/tree/main/README.md)
12. [NOTICE](https://github.com/GreptimeTeam/greptimedb/tree/main/NOTICE)

Please search these resources before responding to any user queries.

```

This would allow users to interact with a GPT-based chatbot that answers questions based on the documentation, ensuring more accurate responses.

Let's create this GPT:  [https://chatgpt.com/g/g-677e87121d448191b0813ca28425ce38-greptimedb-integration](https://chatgpt.com/g/g-677e87121d448191b0813ca28425ce38-greptimedb-integration)

Couldn't answer this question,

```
what is `greptimedb/src/query/src/query_engine/context.rs` about?
```




## Agent

I envision a tool called `greptimedb-agent` to simplify the integration process.

Imagine running a simple command like:

```bash
pip install greptimedb-agent
greptimedb-agent
```

`greptimedb-agent` would intelligently gather information about the current system, such as the machine details and the existing code, in order to understand the context and decide how best to integrate Greptime DB.

This command would automatically update your code to integrate Greptime DB, seamlessly replacing your current database with Greptime DB in just a few steps.
