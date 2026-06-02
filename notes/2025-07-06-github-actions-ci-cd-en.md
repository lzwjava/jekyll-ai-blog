---
audio: false
generated: true
lang: en
layout: post
title: 'GitHub Actions: CI/CD Evolution'
translated: false
type: note
---

GitHub Actions is a powerful **continuous integration and continuous delivery (CI/CD) platform** directly integrated into GitHub. It allows developers to automate various stages of their software development workflow, from building and testing code to deploying applications.

### How it Developed and When it Was Released

GitHub itself was founded in **2007**, with its website launching in **April 2008**. The development of the GitHub platform began in **October 2005**, and it was officially launched by Tom Preston-Werner, Chris Wanstrath, P. J. Hyett, and Scott Chacon.

GitHub Actions, as a specific CI/CD platform, was first announced in **October 2018** and officially released for general availability in **November 2019**. It evolved from GitHub's core mission to provide tools that streamline collaboration and automation for developers.

### How Many Users Does It Have?

While it's difficult to get an exact, real-time number of GitHub Actions *users* specifically, it's worth noting that **GitHub itself has over 100 million developers** as of early 2023. Given GitHub Actions' deep integration and the increasing demand for CI/CD, a significant portion of these users leverage GitHub Actions for their projects. Many development teams across various industries, from small startups to large enterprises, utilize it.

### Which Repos Have a Lot of Actions?

GitHub Actions are defined within individual repositories, typically in the `.github/workflows` directory. Repositories that extensively use GitHub Actions often include:

* **Official GitHub Actions repositories:** The `github/actions` organization on GitHub contains many of the core and commonly used actions like `actions/checkout`, `actions/setup-python`, `actions/setup-node`, `actions/upload-artifact`, and `actions/download-artifact`. These are foundational for many workflows.
* **Large open-source projects:** Major open-source projects across various programming languages (e.g., those for Python, JavaScript, Go, C++) heavily utilize GitHub Actions for their build, test, and release pipelines. Examples often include projects from the likes of Google, Microsoft, and other tech giants, as well as popular frameworks and libraries.
* **Projects focused on automation and DevOps:** Repositories demonstrating DevOps practices, automating various aspects of infrastructure, testing, or deployment, will naturally have a rich set of GitHub Actions workflows.
* **Trending repositories:** Many trending repositories on GitHub today (which can be found on GitHub's trending page) often showcase innovative uses of GitHub Actions for things like generating content, running security scans, or automating releases.

In essence, any repository that benefits from automated processes for code quality, testing, deployment, or general repository management is a candidate for having a robust set of GitHub Actions.
