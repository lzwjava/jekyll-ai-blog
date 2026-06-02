---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: WAR与EAR打包方式对比
translated: true
type: note
---

### 概述
在 Java EE（现称为 Jakarta EE）中，WAR（Web 归档文件）和 EAR（企业归档文件）是将应用程序部署到应用服务器（如 Tomcat、WildFly 或 GlassFish）的标准打包格式。WAR 专注于 Web 层组件，而 EAR 则为完整的企业应用程序捆绑多个模块。以下是详细对比。

| 对比维度           | WAR（Web 归档文件）                                                                 | EAR（企业归档文件）                                                                 |
|--------------------|-----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| **用途**         | 将 Web 应用程序（如 Servlet、JSP、静态内容）作为单一单元部署，实现 Web 层功能。 | 通过打包多个子模块（如 WAR、EJB JAR）部署企业级应用程序，适用于多层分布式系统。 |
| **内容**         | - Web 应用文件：JSP、HTML/CSS/JS、Servlet<br>- 依赖库：WEB-INF/lib 中的 JAR 包<br>- 部署描述符：web.xml（新版可选） | - 多模块：WAR、EJB JAR、客户端 JAR<br>- 共享依赖库<br>- 部署描述符：application.xml<br>- 资源适配器 RAR（可选） |
| **目录结构**     | - 根目录：静态资源（如 index.html）<br>- WEB-INF/：classes、lib、web.xml | - 根目录：META-INF/application.xml<br>- 子目录存放各模块（如 myapp.war、myejb.jar） |
| **文件扩展名**   | .war                                                                             | .ear                                                                                     |
| **部署环境**     | 单模块；可部署至 Web 容器（如 Tomcat）或完整应用服务器。                         | 多模块；仅支持完整应用服务器（如 JBoss、WebLogic），需依赖企业级功能（如事务管理）。 |
| **体积与复杂度** | 体积小、结构简单；适合独立 Web 应用。                                            | 体积大、复杂度高；支持模块化与跨模块资源共享。                                           |
| **典型场景**     | 门户网站、REST API、轻量级服务（如 Spring Boot 应用打包为 WAR）。                | 复杂企业系统（如含 Web 界面+业务逻辑+数据访问的银行应用）。                              |
| **依赖管理**     | 依赖容器提供 Web 服务；不支持 EJB。                                              | 支持 EJB、JMS 及跨模块依赖；促进松耦合架构。                                             |

### 核心差异总结
- **模块化**：WAR 是面向 Web 层的单体结构；EAR 支持组合多个 WAR/JAR 模块。
- **服务器要求**：WAR 可运行于轻量级 Web 服务器；EAR 需完整 JEE 服务器支持。
- **发展趋势**：随着微服务与云原生技术（如 Spring Boot、Quarkus）普及，WAR 常用于容器化部署（Docker），而 EAR 更多用于遗留企业系统。

实践示例请参考 Jakarta EE 官方文档：[Jakarta EE 教程](https://jakartaee.github.io/tutorial/) 或 Oracle 的 Java EE 归档文档：[Java EE 打包指南](https://docs.oracle.com/javaee/7/tutorial/packaging.htm)。
