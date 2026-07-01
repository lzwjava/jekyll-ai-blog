---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: Custom Banking Framework on Spring Boot
translated: false
type: note
---

### Benefits of Building a Custom Framework on Top of Spring Boot for Microservices in a Large Banking Project

In a big enterprise project like a bank's system with 20-30 microservices, Spring Boot is already a solid foundation due to its auto-configuration, embedded servers, and production-ready features. However, layering a custom framework on top makes sense for several strategic reasons, especially in regulated industries like banking where consistency, security, and scalability are non-negotiable. Here's why:

- **Standardization Across Teams**: With multiple microservices, you'll have diverse teams working in parallel. A custom framework enforces architectural patterns (e.g., common DTOs, exception handling, validation rules) to avoid "N ways to do the same thing." This reduces bugs, speeds up reviews, and ensures compliance with banking regs like GDPR, PCI-DSS, or internal audit standards.

- **Reusability and Reduced Boilerplate**: Centralize shared components like authentication (OAuth2/JWT integration), logging (SLF4J with structured logs), monitoring (Micrometer/Prometheus), and tracing (Sleuth/ZIPkin). Instead of copying code into each service, teams pull from the framework, cutting development time by 20-30% in large setups.

- **Enhanced Security and Governance**: Banks deal with sensitive data, so embed features like rate limiting, input sanitization, encryption at rest/transit, and audit trails. The framework can integrate with enterprise tools (e.g., Keycloak for auth, Vault for secrets) out-of-the-box, making it easier to pass security audits.

- **Scalability and Observability**: For 20-30 services, add built-in support for service mesh patterns (e.g., via Istio) or circuit breakers. This helps manage inter-service communication without reinventing the wheel in every repo.

- **Faster Onboarding and Maintenance**: New devs can ramp up quicker with pre-baked starters (e.g., via Spring Initializr customized for your framework). Long-term, it lowers tech debt as updates (e.g., Spring Boot upgrades) propagate easily.

Without a framework, you'd risk siloed services leading to integration hell, higher costs, and compliance risks. It's like building a house of cards vs. a reinforced structure—worth the upfront effort for a project this scale.

### Feign Client vs. Other Options for Inter-Service Calls

For service-to-service communication in a microservices setup, **Feign Client (from Spring Cloud OpenFeign)** is often the better choice for synchronous REST calls, especially in a Spring Boot ecosystem. Here's a quick comparison:

| Approach | Pros | Cons | Best For |
| ---------- | ------ | ------ | ---------- |
| **Feign Client** | - Declarative (annotation-based, like `@FeignClient`).<br>- Integrates seamlessly with Spring Cloud (auto-load balancing via Ribbon, circuit breaking via Resilience4j).<br>- Load-balanced calls with service discovery (Eureka/Consul).<br>- Easy to mock for testing. | - Synchronous only (blocks threads).<br>- Slightly heavier than raw HTTP clients. | Traditional, request-response patterns in banking (e.g., account balance checks). Use if your services are mostly sync and you want minimal config. |
| **WebClient (Spring WebFlux)** | - Reactive/non-blocking, great for high-throughput.<br>- Modern, fluent API.<br>- Built into Spring Boot 2+.<br>- Supports backpressure. | - Steeper learning curve if team isn't reactive-savvy.<br>- Overkill for simple calls. | Async-heavy workloads (e.g., real-time fraud detection streams). Prefer if scaling to 100s of req/sec per service. |
| **RestTemplate** | - Simple, familiar.<br>- No extra deps. | - Deprecated in Spring 6+.<br>- No built-in load balancing or retries.<br>- Manual error handling. | Legacy or quick prototypes—avoid for production microservices. |
| **OpenTelemetry/HTTP Clients (e.g., Apache HttpClient)** | - Highly customizable.<br>- Fine-grained tracing. | - More verbose code.<br>- Requires manual integration for discovery/circuit breaking. | When you need ultimate control, but adds complexity. |

**Recommendation**: Stick with Feign for your banking project—it's battle-tested in enterprises, reduces boilerplate for HTTP calls, and pairs perfectly with your custom framework (e.g., add a base Feign config for timeouts/retries). If any services need reactive flows, hybridize with WebClient. Always layer in a gateway (Spring Cloud Gateway) for external entry points to centralize routing/security.

### Popular Frameworks Built on Top of Spring Boot/Spring in Industry

Yes, the industry loves extending Spring Boot for microservices—it's the de facto Java standard. Here's a rundown of popular ones:

- **Spring Cloud**: The official "framework on top of Spring Boot" for microservices. Includes Netflix OSS tools (Eureka for discovery, Config Server for centralized config, Gateway for routing). Used by giants like Netflix, Alibaba, and banks (e.g., HSBC). It's not "custom" but serves as a base for many internals.

- **Internal Enterprise Frameworks**:
  - **Photon Framework (JPMorgan Chase)**: Built on Spring Boot for their "New Banking Architecture." Handles common patterns like event sourcing, security, and cloud-native deployment. Scaled to thousands of services in production.
  - **Axway's Amplify API Management**: Extends Spring Boot for API gateways in financial services, adding monetization and analytics.
  - **Many banks/insurers** (e.g., ING, Allianz) build unnamed "internal platforms" on Spring Boot, often called "Service Frameworks" or "Microservices Starters," focusing on compliance and ops automation.

Other notable extensions (not purely on Spring but compatible/inspired):

- **Spring Boot Actuator + Micrometer**: For observability—often wrapped into custom monitoring frameworks.
- **JHipster**: Open-source generator that scaffolds full-stack apps on Spring Boot + Angular/React, popular for quick enterprise prototypes.

In banking specifically, custom Spring Boot frameworks are common because off-the-shelf ones like Quarkus or Micronaut (great alternatives) might not fit legacy integrations or strict regs as seamlessly.

If you're architecting this, start with Spring Cloud as your base layer, then customize upward. For a 20-30 service setup, it'll pay dividends in velocity and reliability.

**References**:

- [Top 12 Microservices Frameworks - TatvaSoft Blog](https://www.tatvasoft.com/blog/top-12-microservices-frameworks/)
- [Native Cloud Adoption and Microservice Framework | Next at Chase](https://medium.com/next-at-chase/driving-native-cloud-adoption-at-scale-through-a-microservice-framework-a461e87bb8f2)
- [Top 7 Java Microservices Frameworks - foojay](https://foojay.io/today/top-7-java-microservices-frameworks/)
- [Top 10 Microservices Frameworks in 2025 - GeeksforGeeks](https://www.geeksforgeeks.org/blogs/microservices-frameworks/)
