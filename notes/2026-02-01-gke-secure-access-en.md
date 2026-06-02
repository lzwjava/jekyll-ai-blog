---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Secure GKE Access Without Service Keys
translated: false
type: note
---

Workload Identity is Google Cloud's recommended way to allow applications running in Google Kubernetes Engine (GKE) to securely access Google Cloud services without needing to manage service account keys.

Here's how it works: instead of downloading and storing JSON service account keys in your pods (which is a security risk), Workload Identity creates a relationship between a Kubernetes service account in your GKE cluster and a Google Cloud service account. When your application needs to call a Google Cloud API, GKE automatically handles the authentication behind the scenes.

The setup involves binding your Kubernetes service account to a Google Cloud service account, then configuring your pods to use that Kubernetes service account. When your application makes API calls, the GKE metadata server intercepts the request and exchanges the Kubernetes identity for short-lived Google Cloud credentials.

This approach has several benefits: you eliminate the need to manage and rotate static credentials, you reduce the risk of credential leakage since there are no keys to accidentally commit to source control, and you get more granular control since each application can have its own identity with specific permissions.

For example, if you have a pod that needs to read from Cloud Storage, you'd create a Google Cloud service account with Storage Object Viewer permissions, bind it to your pod's Kubernetes service account, and your application can then authenticate to Cloud Storage automatically without any credentials in your code or configuration.

It's essentially Google Cloud's implementation of the broader concept of workload identity federation, making it much easier to follow security best practices in containerized environments.
