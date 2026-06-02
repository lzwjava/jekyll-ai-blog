---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Introduction to Google Cloud Run
translated: false
type: note
---

Cloud Run is a fully managed, serverless compute platform in GCP that lets you run stateless containers directly on Google's scalable infrastructure. It's designed for developers who want to deploy applications without worrying about underlying servers, provisioning, or scaling. Whether you're building web apps, APIs, microservices, or event-driven workloads, Cloud Run handles the infrastructure so you can focus on code.

### Key Features
- **Serverless Execution**: Deploy containerized code (supporting any language or runtime) that scales automatically from zero to thousands of instances based on incoming requests or traffic.
- **Pay-Per-Use Pricing**: Billed only for the resources you consume—per request or per instance duration—making it cost-effective for variable workloads.
- **Built-in Integrations**: Works seamlessly with other GCP services like Cloud SQL for databases, Cloud Storage for files, Pub/Sub for messaging, and more. It also supports VPC for private networking.
- **Deployment Options**:
  - Push a pre-built container image from Artifact Registry or Docker Hub.
  - Deploy directly from source code using Cloud Build (supports languages like Node.js, Python, Java, Go, .NET, and Ruby).
  - Use Cloud Run Functions for simpler, function-as-a-service style deployments.
- **Security and Networking**: Services can be public or private (requiring authentication), with support for HTTPS endpoints and custom domains.
- **Additional Modes**: Beyond request-driven services, it offers Jobs for batch tasks (e.g., scheduled scripts or data processing) and Worker Pools for long-running, non-HTTP workloads.

To get started, you can deploy via the GCP Console, gcloud CLI, or CI/CD pipelines. For example, build and deploy a simple "Hello World" container in minutes.

### The Cloud Run Admin Console
The Cloud Run section in the GCP Console provides an intuitive dashboard for managing your deployments. Here's a breakdown based on the Services view you shared:

- **Overview**: The main "Cloud Run > Services" page lists all your deployed services in a table format. It starts with a helpful recommendation banner like "Run your app on a fully managed platform" to encourage quick starts if you're new.

- **Table Columns** (as shown in your snippet):
  - **Name**: The unique identifier for each service (e.g., "my-api").
  - **Deployment Type**: Indicates how it was deployed—e.g., "Container" for images or "Source" for code-based deploys.
  - **Req/sec**: Real-time requests per second metric to monitor traffic load.
  - **Region**: The GCP region where the service runs (e.g., us-central1), affecting latency and compliance.
  - **Authentication**: Shows if the service is public (allow unauthenticated) or requires IAM authentication.
  - **Ingress**: Controls traffic routing—e.g., "All" for internal/external, or restricted to internal only.
  - **Last Deployed**: Timestamp of the most recent update.
  - **Deployed By**: The user or service account that performed the deployment.

- **Filters and Actions**: Above the table, you can filter by any of these columns to narrow down your list. Use the "Create Service" button to deploy new ones, or click on a service name to edit settings like CPU/memory limits, environment variables, scaling configs, or revisions for traffic splitting.

This console makes it easy to monitor performance, view logs, and iterate on deployments without leaving the browser. For hands-on exploration, navigate to [console.cloud.google.com/run](https://console.cloud.google.com/run) after enabling the API.

[What is Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run)
[Cloud Run Documentation](https://cloud.google.com/run/docs)
