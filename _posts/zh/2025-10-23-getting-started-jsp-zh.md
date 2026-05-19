---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: JSP入门指南
translated: true
type: note
---

JavaServer Pages (JSP) 是一种服务器端技术，用于在 Java 应用程序中创建动态网页内容。它允许您直接将 Java 代码嵌入 HTML 页面，从而更轻松地基于用户输入或数据生成动态响应。JSP 是 Jakarta EE（原 Java EE）平台的一部分，在 Web 应用程序中与 Servlet 协同工作良好。

以下是从环境搭建到部署的 JSP 入门分步指南，假设您已具备 Java 和 HTML 的基础知识。

## 1. 环境准备
- **Java 开发工具包 (JDK)**：安装 JDK 8 或更高版本（现代应用推荐 JDK 17+）。可从 [Oracle](https://www.oracle.com/java/technologies/downloads/) 下载或使用 OpenJDK。
- **Web 服务器/容器**：推荐使用 Apache Tomcat（免费且适合初学者）。从 [Apache Tomcat](https://tomcat.apache.org/) 下载。
- **集成开发环境（可选但推荐）**：IntelliJ IDEA、Eclipse 或安装 Java 扩展的 VS Code 可简化开发流程。

## 2. 环境配置
1. 安装 Tomcat：
   - 将 Tomcat 压缩包解压到目录（如 Windows 系统为 `C:\tomcat`，Linux 系统为 `/opt/tomcat`）。
   - 运行 `bin/startup.bat`（Windows）或 `bin/startup.sh`（Unix）启动 Tomcat。在浏览器中访问 `http://localhost:8080` 验证是否正常运行。

2. 创建项目结构：
   - 在 Tomcat 的 `webapps` 目录中创建应用文件夹（如 `my-jsp-app`）。
   - 在该文件夹内创建：
     - `WEB-INF/web.xml`（部署描述符，JSP 2.2+ 中为可选但建议用于配置）
     - 用于存放 JSP 文件的根目录（如 `index.jsp`）。

   基础 `web.xml` 示例：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee
            https://jakarta.ee/xml/ns/jakartaee/web-app_5_0.xsd"
            version="5.0">
       <display-name>My JSP App</display-name>
   </web-app>
   ```

## 3. 编写首个 JSP 页面
JSP 文件使用 `.jsp` 扩展名，通过脚本片段 (`<% %>`)、表达式 (`<%= %>`) 和声明 (`<%! %>`) 将 Java 代码与 HTML 结合。现代最佳实践建议使用 JSP 表达式语言 (EL) 和 JSTL 替代原始脚本片段。

示例：在应用根目录创建 `index.jsp`：
{% raw %}
```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>  <!-- 如需使用 JSTL -->

<html>
<head>
    <title>Hello JSP</title>
</head>
<body>
    <h1>Welcome to JSP!</h1>
    
    <!-- 脚本片段：Java 代码 -->
    <% 
        String name = request.getParameter("name") != null ? request.getParameter("name") : "World";
        java.util.Date now = new java.util.Date();
    %>
    
    <!-- 表达式：输出值 -->
    <p>Hello, <%= name %>! The time is <%= now %>.</p>
    
    <!-- 使用 EL 实现更简洁的输出 -->
    <p>Your name via EL: ${param.name}</p>
    
    <!-- JSTL 示例：遍历列表 -->
    <c:set var="fruits" value="${{'Apple', 'Banana', 'Cherry'}}" />
    <ul>
        <c:forEach var="fruit" items="${fruits}">
            <li>${fruit}</li>
        </c:forEach>
    </ul>
</body>
</html>
```
{% endraw %}

- **核心元素**：
  - **指令**：`<%@ page ... %>` 设置页面属性；`<%@ taglib ... %>` 导入标签库。
  - **脚本片段**：嵌入 Java 代码（建议少用，优先使用 EL/JSTL）。
  - **EL 表达式**：通过 `${expression}` 访问数据而无需脚本片段。
  - **JSTL**：从 [Apache Taglibs](https://tomcat.apache.org/taglibs/standard/) 下载并将 JAR 文件放入 `WEB-INF/lib`。

## 4. 部署与运行
1. 将应用文件夹（如 `my-jsp-app`）放入 Tomcat 的 `webapps` 目录。
2. 重启 Tomcat。
3. 在浏览器中访问：`http://localhost:8080/my-jsp-app/index.jsp`。
4. 通过查询参数测试：访问 `http://localhost:8080/my-jsp-app/index.jsp?name=Grok` 查看动态输出效果。

## 5. 常用功能与最佳实践
- **表单与用户输入**：使用 `<form>` 标签和 `request.getParameter()` 或 EL 表达式 (`${param.field}`) 处理提交数据。
- **会话与 JavaBean**：通过 `session.setAttribute()` 管理状态；使用 JavaBean 封装可复用数据。
- **错误处理**：在 `web.xml` 中添加 `<error-page>` 或使用 `<%@ page errorPage="error.jsp" %>`。
- **安全性**：对输入内容进行消毒处理以防 XSS 攻击；生产环境启用 HTTPS。
- **现代替代方案**：JSP 仍被使用，但新项目可考虑更灵活的 Thymeleaf 或 Spring MVC。
- **调试技巧**：查看 Tomcat 日志（`logs/catalina.out`）定位错误。

## 6. 进阶主题
- 与 Servlet 集成：采用 MVC 模式，JSP 负责视图层，Servlet 处理业务逻辑。
- 数据库连接：使用 JDBC 或 JPA（例如搭配 H2 或 MySQL）。
- 构建工具：通过 Maven/Gradle 管理依赖（如 JSTL）。

建议从简单的 "Hello World" 开始实践，逐步添加功能。如需构建完整 Web 应用，可参考 Jakarta EE 官方教程。

## 参考资源
- [Oracle JSP 教程](https://docs.oracle.com/javaee/7/tutorial/jspx.htm)
- [Baeldung: JSP 入门指南](https://www.baeldung.com/jsp-tutorial)
- [Apache Tomcat JSP 示例](https://tomcat.apache.org/tomcat-10.1-doc/jsp-examples/)