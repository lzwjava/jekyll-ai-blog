---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 无需服务密钥安全访问 GKE
translated: true
type: note
---

Workload Identity 是 Google Cloud 推荐的一种方式，允许运行在 Google Kubernetes Engine (GKE) 中的应用程序安全地访问 Google Cloud services，而无需管理 service account keys。

其工作原理如下：与其在 pods 中下载并存储 JSON service account keys（这存在安全风险），Workload Identity 会在 GKE cluster 中的 Kubernetes service account 与 Google Cloud service account 之间建立关联。当您的应用程序需要调用 Google Cloud API 时，GKE 会在后台自动处理身份验证。

设置过程包括将您的 Kubernetes service account 绑定到 Google Cloud service account，然后配置您的 pods 使用该 Kubernetes service account。当您的应用程序进行 API calls 时，GKE metadata server 会拦截请求，并将 Kubernetes identity 交换为短效的 Google Cloud credentials。

这种方法具有以下优势：您无需管理和定期更换静态 credentials；由于没有可以意外提交到源码控制系统的 keys，从而降低了 credential 泄露的风险；此外，由于每个应用程序都可以拥有具有特定权限的独立 identity，您可以获得更细粒度的控制。

例如，如果您有一个需要从 Cloud Storage 读取数据的 pod，您可以创建一个具有 Storage Object Viewer 权限的 Google Cloud service account，将其绑定到该 pod 的 Kubernetes service account，然后您的应用程序就可以自动通过 Cloud Storage 身份验证，而无需在代码或配置中包含任何 credentials。

它本质上是 Google Cloud 对更广泛的 workload identity federation 概念的实现，使得在容器化环境中遵循安全最佳实践变得更加容易。
