---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: IBM WebSphere Administrative Console Navigation Guide
translated: false
type: note
---

### IBM WebSphere Application Server (WAS) Administrative Console: Left Navigation Pane

The left view in the IBM WebSphere Application Server (WAS) administrative console (also known as the Integrated Solutions Console) is a hierarchical navigation tree that organizes configuration and management tasks. It provides quick access to key areas for administering the server environment, applications, and resources. The exact structure can vary slightly by WAS version (e.g., 8.5, 9.0) and edition (Base vs. Network Deployment), but the core top-level categories are consistent.

Below is a list of the main top-level sections in the navigation tree, with brief descriptions of their primary purposes. Subsections are expandable (using +/− icons) for more granular tasks.

#### Main Top-Level Sections

- **Applications**
  Used for deploying, installing, updating, starting/stopping, and managing applications (e.g., EAR/WAR files).
  *Key subsections*: Enterprise Applications, WebSphere Enterprise Applications, Web Modules, Shared Libraries.
  *Common tasks*: Install new apps, map modules to servers, configure class loaders.

- **Resources**
  Configures shared resources like databases, messaging, and connection pools that applications can use.
  *Key subsections*: JDBC (data sources/providers), JMS (queues/topics), JavaMail Sessions, URL Providers.
  *Common tasks*: Set up JDBC data sources, create JMS connection factories.

- **Services**
  Manages server-wide services such as security, messaging, and communication protocols.
  *Key subsections*: Security (global security, users/groups, authentication), Mail Providers, Ports, ORB Service, Transaction Service.
  *Common tasks*: Enable SSL, configure user registries, adjust port assignments.

- **Servers**
  Handles server instances, clustering, and web server definitions.
  *Key subsections*: Server Types (WebSphere application servers, WebSphere proxy servers), Clusters, Web Servers.
  *Common tasks*: Start/stop servers, configure JVM settings, create clusters for high availability.

- **System Administration**
  Oversees the overall topology, including nodes, cells, and console settings.
  *Key subsections*: Nodes, Cells, Deployment Manager, Console Preferences.
  *Common tasks*: Synchronize nodes, manage deployment manager, set console themes/scopes.

- **Environment**
  Defines environment-specific variables and aliases.
  *Key subsections*: WebSphere Variables, Hosts Aliases.
  *Common tasks*: Set system variables for paths or properties.

- **Monitor and Tuning**
  Monitors performance and tunes runtime behavior.
  *Key subsections*: Performance Monitoring Infrastructure (PMI), Custom Services, Logging and Tracing.
  *Common tasks*: Enable metrics, adjust thread pools, view request metrics.

- **Troubleshooting**
  Accesses diagnostic tools and logs.
  *Key subsections*: Logs and Trace, First Steps.
  *Common tasks*: Download logs, enable trace specifications.

#### Additional Notes

- **Scope Selection**: At the top of many pages, you can filter by scope (Cell, Node, Server) to limit visibility.
- **Guided Activities**: Sometimes appears as a top-level or contextual section for wizards (e.g., securing the environment).
- To access the console: Typically via `https://<host>:<port>/ibm/console` (default port 9060 for admin, 9043 for secure).
- For version-specific details (e.g., WAS 9.0), refer to official IBM docs, as minor UI changes occur in updates.

[WebSphere Administrative Console - 101](https://www.ibm.com/community/101/websphere/administrative-console/)
[Introduction: Administrative Console (WAS 9.0.5)](https://www.ibm.com/docs/en/was-nd/9.0.5?topic=administration-introduction-administrative-console)
[WebSphere Application Server V7: Administration Consoles (Redpaper)](https://www.redbooks.ibm.com/redpapers/pdfs/redp4573.pdf)
