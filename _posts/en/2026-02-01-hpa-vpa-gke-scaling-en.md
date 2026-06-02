---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: HPA vs VPA in GKE Scaling
translated: false
type: note
---

In Google Cloud (specifically Google Kubernetes Engine/GKE), both Vertical Pod Autoscaler (VPA) and Horizontal Pod Autoscaler (HPA) are mechanisms for automatically scaling your Kubernetes workloads, but they work in fundamentally different ways.

**Horizontal Pod Autoscaler (HPA)** scales by adjusting the *number* of pod replicas. When your application needs more resources, HPA creates additional copies of your pods to distribute the load. For example, if CPU usage spikes, HPA might scale from 3 pods to 10 pods. It's ideal for stateless applications that can handle requests in parallel. HPA typically monitors metrics like CPU utilization, memory usage, or custom metrics, and scales out (adds pods) or scales in (removes pods) based on thresholds you define.

**Vertical Pod Autoscaler (VPA)** scales by adjusting the *resource requests and limits* of individual pods. Instead of adding more pods, VPA modifies how much CPU and memory each pod can use. If a pod consistently uses more resources than requested, VPA can increase its resource allocation and restart the pod with the new settings. This is useful when you're not sure what resource requests to set initially, or when your application's resource needs change over time but doesn't benefit from horizontal scaling.

The key difference: HPA adds more instances of your application, while VPA makes each instance bigger or smaller. You can actually use both together, though you need to configure them carefully to avoid conflicts (typically HPA on CPU, VPA on memory). In GKE, these are available as built-in features that integrate with the Kubernetes autoscaling ecosystem.
