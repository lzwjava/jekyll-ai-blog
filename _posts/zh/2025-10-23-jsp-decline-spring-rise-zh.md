---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: JSP的衰落与Spring Boot的崛起
translated: true
type: note
---

JavaServer Pages (JSP) 曾是构建 Java 动态 Web 应用的主要技术，允许开发者直接将 Java 代码嵌入 HTML。然而多年来其使用率显著下降，尤其在新项目中。基于 Spring 生态构建的 Spring Boot 框架已成为 Java Web 开发的首选。需要注意的是，JSP 与 Spring Boot 并非直接竞争关系——JSP 是视图技术（用于页面渲染），而 Spring Boot 是用于创建 Web 应用、API 和微服务的完整框架。这种转变通常意味着用 Spring Boot 搭配现代模板引擎或前端框架来取代传统的 JSP/Servlet 技术栈。

这种迁移并非要"完全弃用 JSP"（旧系统仍在使用的场景），而是采用更高效、更易维护的方案。下面我将根据开发者讨论、调查数据和专家分析阐述关键原因。

## JSP 失宠的核心原因
诞生于 1999 年的 JSP 在 2025 年的快节奏开发环境中已显过时，以下是其很少被新项目选用的原因：

- **代码混乱难以维护**：JSP 允许将 Java 脚本片段（如 `<% %>`）与 HTML 混合，导致代码难以阅读、测试和调试。JSP 生成的 Servlet 代码在大型项目中容易变成"一团乱麻"，这违背了现代关注点分离原则。

- **原型设计与开发流程低效**：由于自定义标签的存在，JSP 文件无法在浏览器中作为静态 HTML 打开——必须通过运行中的服务器（如 Tomcat）才能正常渲染。修改 UI 需要经历部署、重启和页面跳转流程，严重拖慢迭代速度。设计人员也会因无效的 HTML 标签而难以协作。

- **易出错且过度灵活**：该技术允许在模板中编写过多 Java 逻辑，易诱使开发者将业务逻辑混入视图层，导致应用难以扩展并存在安全风险（例如未过滤输出引发的 XSS 漏洞）。

- **缺乏现代特性支持**：早期版本对 HTML5 支持不完善（直到 Spring 3.1 才原生支持 `type="email"` 绑定）。基础功能如 Java Time API 日期格式化都需要第三方库。此外它不适合构建交互式 UI，依赖整页刷新机制。

- **调查数据认可度低**：近期 JVM 生态调查显示仅约 8% 的应用使用 JSP 相关技术（如 JSF），而 Spring Boot 占比达 58%。JSP 被视为"遗留技术"或"失败的技术"，过去十余年的架构讨论中已鲜少被提及。

## Spring Boot 崛起的原因
Spring Boot 通过基于 Spring 框架但减少样板代码的方式简化了 Java Web 开发。它并非直接替代 JSP，而是通过更优的抽象和集成使其失去必要性。开发者青睐 Spring Boot 源于：

- **快速启动与自动配置**：无需手动编写 XML 配置或搭建服务器——Spring Boot 通过"启动器"（如 `spring-boot-starter-web`）管理依赖，内嵌 Tomcat/Jetty 并提供合理默认配置。"Hello World" 应用仅需数分钟即可完成。

- **约定优于配置且灵活**：框架强制实施最佳实践（如 MVC 模式）同时支持自定义。内置的 REST API、安全防护、测试监控等功能使其成为微服务和云原生应用的理想选择。

- **更易维护与扩展**：抽象了 Servlet 等底层细节（Spring Boot 底层仍通过 DispatcherServlet 使用 Servlet），让开发者专注于业务逻辑。执行器端点与结构化日志等特性加速生产运维。

- **活跃的生态系统**：与数据库（JPA/Hibernate）、缓存（Redis）及现代视图技术无缝集成。开箱即用的生产级特性支持单 JAR 部署——不再需要费力处理 WAR 文件。

- **社区与就业市场**：Spring Boot 在招聘需求和教程资源中占据主导地位。直接学习该框架可提升就业竞争力，无需先掌握 JSP 基础（但了解基础有助于调试）。

简而言之，Spring Boot 隐藏了原始 JSP/Servlet 应用中的复杂细节，让团队在保持功能强大的同时提升开发效率。

## Spring Boot 中替代 JSP 的现代方案
虽然通过 `spring-boot-starter-web` 和 WAR 打包仍可支持 JSP，但官方明确不推荐——Spring Boot 的"设计主张"认为 JSP 存在前述缺陷。替代方案包括：

- **Thymeleaf（最流行）**：能生成合规 HTML 的天然模板引擎。优势包括静态原型设计（无需服务器即可在浏览器中预览）、原生 HTML5 支持、易读语法（如 `th:field` 属性）和便捷的国际化支持。对设计人员友好且与 Spring MVC 完美集成。示例：Thymeleaf 表单看起来像纯 HTML，不像 JSP 那样标签冗杂。

- **其他模板引擎**：轻逻辑场景可选 Freemarker 或 Velocity；追求简洁可选用 Mustache/Handlebars。

- **前端优先方案**：许多 Spring Boot 应用提供 JSON API 供 React、Vue 或 Angular 单页应用消费。这种方式将后端与视图完全解耦，无需服务端渲染即可实现丰富交互。

对于简单应用，甚至仅需静态 HTML/CSS/JS 配合 Spring Boot 的资源处理机制即可满足需求，无需模板引擎。

## 总结
从 JSP 到 Spring Boot 的转变反映了向更简洁、更高效率工具演进的大趋势。若需维护遗留 JSP 代码，建议逐步迁移（例如转向 Thymeleaf）。新项目应直接采用 Spring Boot——这已是 2025 年的行业标准。了解 JSP 基础仍有助理解 Web 开发原理，但已非必要前提。

[JSP 和 Servlet 是否仍有价值？(Reddit)](https://www.reddit.com/r/java/comments/197jl86/are_jsp_and_servlets_still_relevant/)
[学习 Spring 前是否需要掌握 JSP 和 Servlet？(Medium)](https://medium.com/@abhishekmalagi2002/before-spring-learn-jsp-servlets-24fc5596cbc4)
[JSP 是否已被替代？若是，如何替代？(Stack Overflow)](https://stackoverflow.com/questions/41309564/is-jsp-superseeded-and-if-so-how)
[Spring MVC 视图层：Thymeleaf 与 JSP 对比 (Thymeleaf.org)](https://www.thymeleaf.org/doc/articles/thvsjsp.html)
[Spring 与 Spring Boot 对比分析 (Baeldung)](https://www.baeldung.com/spring-vs-spring-boot)
