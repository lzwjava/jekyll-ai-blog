---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: IBM WebSphere请求路由详解
translated: true
type: note
---

让我解释一下 IBM WebSphere Application Server (WAS) 如何处理传入请求和路由：

## IBM WAS 中的请求流程

当请求到达 IBM WAS 时，典型的流程如下：

**1. Web 服务器层（可选）**

- 请求首先到达 IBM HTTP Server (IHS) 或其他 Web 服务器
- Web 服务器插件将请求路由到相应的 WAS 实例

**2. Web 容器入口点**
请求通过 **Web 容器** 进入 WAS，这是主 servlet 引擎的一部分。关键的包结构是：

```
com.ibm.ws.webcontainer.*
```

**3. 请求处理链**

路由通过以下几个组件实现：

**传输通道框架**

- `com.ibm.ws.channel.*` - 处理网络通信
- HTTP 传输通道接收请求

**Web 容器处理**

```
com.ibm.ws.webcontainer.servlet.ServletWrapper
com.ibm.ws.webcontainer.filter.WebAppFilterManager
```

**4. 过滤器链执行**

过滤器的工作方式与标准 Java Servlet 过滤器完全相同，但由 WAS 管理：

- **在应用程序的 web.xml 中定义**
- 过滤器按照指定顺序链接
- 每个过滤器都可以检查/修改请求和响应
- 使用标准的 `javax.servlet.Filter` 接口

```xml
<filter>
    <filter-name>MyFilter</filter-name>
    <filter-class>com.example.MyFilter</filter-class>
</filter>

<filter-mapping>
    <filter-name>MyFilter</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

**过滤器执行顺序：**

1. WAS 在应用程序启动时加载过滤器配置
2. WebAppFilterManager 创建过滤器链
3. 每个请求：请求 → 过滤器1 → 过滤器2 → ... → Servlet

## IBM WAS 中的主要包

**核心包：**

- `com.ibm.ws.webcontainer.*` - Web 容器实现
- `com.ibm.ws.runtime.*` - 运行时服务
- `com.ibm.websphere.servlet.*` - WAS 特定的 servlet 扩展
- `com.ibm.ws.channel.*` - 传输层
- `com.ibm.ejs.*` - EJB 容器服务
- `com.ibm.ws.naming.*` - JNDI 实现

## 路由机制

**虚拟主机路由：**

- 在 WAS 管理控制台中配置
- 将 `主机名:端口` 组合映射到应用程序
- 配置路径：`虚拟主机 → 主机别名 → 应用程序`

**上下文根路由：**

- 每个应用程序都有一个上下文根（例如 `/myapp`）
- WAS 维护已部署应用程序的注册表
- URI 映射：`http://服务器:端口/上下文根/servlet路径`

**Servlet 映射：**

- 在 web.xml 或注解中定义
- 模式匹配（精确匹配、路径匹配、扩展名匹配、默认匹配）

## 应用程序启动顺序

当应用程序启动时：

1. **类加载器初始化** - 应用程序获得自己的类加载器
2. **web.xml 解析** - 加载过滤器、servlet、监听器
3. **ServletContextListener 触发** - `contextInitialized()`
4. **过滤器实例化** - 调用 `init()` 方法
5. **启动时加载的 servlet** - 初始化急切加载的 servlet
6. **应用程序标记为已启动** - 准备接受请求

路由注册表被更新，应用程序现在可以通过其上下文根访问。

这澄清了 WAS 如何处理请求路由和过滤了吗？
