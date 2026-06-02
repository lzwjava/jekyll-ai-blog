---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Spring Boot Overtook Liberty
translated: false
type: note
---

IBM WebSphere Application Server Liberty Profile (often abbreviated as WLP or simply Liberty) was IBM's attempt to modernize its heavyweight traditional WebSphere Application Server (WAS) by creating a lightweight, composable, cloud-friendly Jakarta EE (formerly Java EE) runtime starting around 2012–2013. Despite being technically solid and even superior in some areas (fast startup, low memory footprint, excellent MicroProfile support via Open Liberty), **Liberty largely "lost" the popularity battle to Spring Boot** for new Java web/microservices development from the mid-2010s onward.

### Key Reasons Spring Boot Dominated Over Liberty

| Reason | Spring Boot Advantage | Liberty / Traditional App Server Drawback |
|--------|-----------------------|-------------------------------------------|
| **Developer Productivity & Ease of Use** | Convention-over-configuration, auto-configuration, embedded server (Tomcat/Jetty/Undertow by default), `spring-boot-starter-*` eliminate boilerplate. Zero-config production-ready apps in minutes. | Still requires server.xml configuration, feature activation, and more manual setup even though lighter than full WAS. Feels "old-school" to many devs. |
| **Standalone Executable Model** | Fat JAR / uber-JAR with embedded server → run anywhere with `java -jar`, perfect for Docker/Kubernetes and DevOps. No external server management. | Primarily a separate server you deploy WAR/EAR into (though Liberty later added runnable JAR support, it felt bolted-on and never became the default workflow). |
| **Ecosystem & Community** | Massive open-source community (Pivotal/VMware), huge number of third-party starters, excellent documentation, Stack Overflow answers, tutorials. | Smaller community; mostly IBM documentation and paid support. Fewer ready-made integrations. |
| **Timing & Mindshare** | Spring Boot 1.0 released in 2014 — exactly when microservices, Docker, and cloud-native exploded. It became the de facto standard for new Java services. | Liberty launched earlier (2012–2013) but was still perceived as "IBM's app server" at a time when developers were fleeing heavyweight commercial servers (WebSphere, WebLogic). |
| **Vendor Neutrality & Cost** | Completely free and open-source, no vendor lock-in fears. | IBM product → perception of expensive licensing (even though Liberty Core had a free tier and Open Liberty is fully open-source, the brand carried baggage from traditional WAS). |
| **Microservices & Cloud Fit** | Designed from day one for microservices; actuators, health checks, externalized config, easy 12-factor apps. | Very cloud-friendly (especially Open Liberty), but most developers already chose Spring Boot before discovering Liberty's strengths. |
| **Market Momentum** | By ~2018–2020, surveys showed Tomcat (embedded in Spring Boot) had ~60% share of Java runtimes, dwarfing all full app servers combined. In 2025, Spring Boot is used by >18,000 known companies; traditional app servers are niche. | Liberty/Open Liberty remains popular in IBM-heavy enterprises and for Jakarta EE/MicroProfile, but far behind in greenfield adoption. |

### Where Liberty Still Wins (Niche Cases)

- Pure Jakarta EE / MicroProfile apps without Spring dependencies.
- Enterprises already locked into IBM stack (Red Hat OpenShift with WebSphere licenses, IBM Cloud Pak).
- Optimized Spring Boot deployments (Liberty can run Spring Boot apps with smaller Docker images and higher throughput than embedded Tomcat in some benchmarks).
- Regulated industries needing commercial support/certifications.

In short: **Liberty didn't lose because it was technically inferior — it lost because Spring Boot delivered dramatically higher developer productivity, arrived at the perfect cultural moment, and built unstoppable ecosystem momentum.** Most new Java backend projects in 2025 start with Spring Boot (or Quarkus/Helidon/Micronaut), not a separate application server.

[Spring Boot vs Websphere Liberty | What are the differences?](https://stackshare.io/stackups/spring-boot-vs-websphere-liberty)
[2020 Java Technology Report | JRebel](https://www.jrebel.com/blog/2020-java-technology-report)
[How does Open Liberty’s performance compare to other cloud-native Java runtimes](https://openliberty.io/blog/2022/10/17/memory-footprint-throughput-update.html)
[Spring Boot market share data (6sense)](https://6sense.com/tech/programming-framework/spring-boot-market-share)
