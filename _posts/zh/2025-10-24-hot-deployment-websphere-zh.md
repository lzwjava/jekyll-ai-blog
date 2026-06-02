---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: WebSphere WAS 中的热部署
translated: true
type: note
---

### 理解 WebSphere 应用服务器中的热部署与热交换

热部署（也称为热重载或热交换）是一种开发技术，允许您在不完全重启应用服务器的情况下，更新并部署应用程序的更改——例如代码、配置或资源。这在迭代开发周期中尤其有价值，因为频繁的代码更改（例如修复错误、调整逻辑或更新UI元素）原本会因冗长的服务器启动时间而减慢速度，尤其是在像 IBM WebSphere 应用服务器这样的企业环境中。重启一个 WAS 实例对于大型应用程序可能需要几分钟甚至更长时间，这会中断工作流程和测试。

您提供的片段侧重于在 WAS 中实现更快迭代的实用策略，强调“展开式”WAR 部署和用于增强热交换的工具。我将逐步分解，解释这些概念、它们的工作原理、它们的局限性以及实现技巧。

#### 1. 部署为“展开式”WAR（解包部署）

WAR文件本质上是一个压缩包，包含您的 Web 应用程序的资源：JSP、Servlet、Java 类、静态文件（HTML/CSS/JS）、库（JAR）和配置文件（例如 web.xml）。默认情况下，WAR 以**打包**（压缩）文件的形式部署，WAS 将其视为不可变的——任何更改都需要重新打包和重新部署整个归档文件。

**展开式 WAR** 指的是在部署之前将 WAR 文件解压（解压缩）到一个目录结构中。这允许在服务器的文件系统上直接修改单个文件或子目录，而无需触及整个归档文件。

**为什么它能实现更快的迭代：**

- **文件级更新：** 您可以编辑单个 JSP 或 Java 类文件，WAS 可以检测并仅重新加载该组件。
- **无需重新打包：** 避免了反复压缩/解压缩大型 WAR 文件的开销。
- **与热重载协同：** 使服务器更容易监控和刷新更改的文件。

**如何在 WAS 中部署展开式 WAR：**

- **使用管理控制台：**
  1. 登录到 WAS 集成解决方案控制台（通常在 `http://localhost:9060/ibm/console`）。
  2. 导航到 **应用程序 > 新建应用程序 > 新建企业应用程序**。
  3. 不要选择打包的 WAR 文件，而是指向您解压后的 WAR 的根目录（例如，`/path/to/myapp.war/`——注意尾部斜杠表示它是一个目录）。
  4. 完成部署向导，确保“部署 Web 服务”和其他选项与您的应用程序匹配。
- **使用 wsadmin（脚本工具）：**

  ```bash
  wsadmin.sh -c "AdminApp.install('/path/to/myapp', '[ -MapWebModToVH [[myapp .* default_host.* virtual_host ]]]')"
  ```

  将 `/path/to/myapp` 替换为您的展开目录。
- **开发服务器（例如 Liberty Profile）：** 为了更轻量级的测试，使用 Open Liberty（一个 WAS 变体）和 `server start`，并将您的展开式应用程序放入 `dropins` 文件夹以进行自动部署。

**最佳实践：**

- 使用源代码控制工具（例如 Git）将更改从您的 IDE 同步到展开目录。
- 监控磁盘空间，因为展开式部署会消耗更多存储空间。
- 在生产环境中，坚持使用打包的 WAR 文件以确保安全性和一致性——热部署主要用于开发/测试。

一旦部署为展开式，WAS 的内置机制就可以用于部分热重载。

#### 2. WAS 的内置热重载支持

WAS 原生支持在不完全重启的情况下热重载某些组件，但这是有限的。这依赖于服务器的**文件轮询**机制，WAS 定期扫描展开部署目录以查找更改（可通过 JVM 参数配置，例如 `-DwasStatusCheckInterval=5` 表示 5 秒检查一次）。

**WAS 开箱即用支持的内容：**

- **JSP：**
  - JSP 在首次访问时动态编译为 Servlet。如果您在展开式 WAR 中修改了 JSP 文件，WAS 可以检测到更改，重新编译它，并重新加载该 Servlet。
  - **工作原理：** 在 `ibm-web-ext.xmi`（位于 WEB-INF 下）中将 `reloadInterval` 设置为较低的值（例如 1 秒）以进行频繁检查。或者使用全局设置：**服务器 > 服务器类型 > WebSphere 应用程序服务器 > [您的服务器] > Java 和进程管理 > 进程定义 > Java 虚拟机 > 自定义属性**，添加 `com.ibm.ws.webcontainer.invokefilterscompatibility=true`。
  - **局限性：** 仅适用于未被积极缓存的 JSP。包含复杂包含或标签的 JSP 可能需要模块重启。
- **某些 Java 类（Servlet 和 EJB）：**
  - 对于展开式部署，如果单个类文件位于 WEB-INF/classes 或 lib 目录中，WAS 可以重新加载它们。
  - **工作原理：** 在部署描述符中或通过控制台启用“应用程序重载”：**应用程序 > [您的应用程序] > 管理模块 > [模块] > 重载行为 > 启用重载**。
  - 这会触发**模块级重载**，这比完整的应用程序重启要快，但仍然会卸载/重新加载整个模块（例如，您的 Web 应用程序）。

**内置支持的局限性：**

- **不是真正的热交换：** 对核心应用程序逻辑的更改（例如，修改正在运行的 Servlet 类中的方法）如果不卸载旧的类加载器就不会生效。您可能会看到 `ClassNotFoundException` 或陈旧的代码。
- **状态丢失：** 会话、单例或数据库连接可能会重置。
- **IBM JDK 特性：** WAS 通常使用 IBM 的 JDK，与 OpenJDK/HotSpot 相比，在类重载方面有其特殊性。
- **不支持结构更改：** 添加新类、更改方法签名或更新注解需要重启。
- **性能开销：** 频繁轮询可能会在开发中消耗资源。

对于基本的 UI 调整（JSP 编辑）或简单的类更新，这已经足够并且免费。但对于“完全热交换”——您可以在执行过程中编辑运行中的代码而无需任何重载——您需要第三方工具。

#### 3. 完全热交换解决方案

为了实现无缝的代码更改（例如，在附加了调试器的 IDE 如 Eclipse 或 IntelliJ 中编辑方法体，并立即看到应用效果），请使用能够修补 JVM 类加载和检测机制的插件。

**选项 1：JRebel（付费插件）**

- **它是什么：** 来自 Perforce（前身为 ZeroTurnaround）的商业工具，为 Java 应用程序提供全面的热交换功能。它在启动时检测您的字节码，允许重新加载类、资源，甚至特定于框架的更改（例如 Spring bean、Hibernate 实体）。
- **为什么在 WAS 中使用它：**
  - 与 WAS 深度集成，包括对展开式 WAR、OSGi 捆绑包和 IBM JDK 的支持。
  - 处理复杂场景，如更改方法签名或添加字段（超出标准 JVMTI 热交换限制）。
  - **特性：** 自动检测来自 IDE 的更改；无需手动重新部署；保留应用程序状态。
- **如何设置：**
  1. 从官方网站下载 JRebel 并安装为 Eclipse/IntelliJ 插件。
  2. 为您的项目生成 `rebel.xml` 配置文件（自动生成或手动）。
  3. 将 JVM 参数添加到您的 WAS 服务器：`-javaagent:/path/to/jrebel.jar`（代理 JAR 的完整路径）。
  4. 在调试模式下启动 WAS（`-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8000`）。
  5. 附加您的 IDE 调试器并编辑代码——JRebel 实时同步更改。
- **成本：** 基于订阅（个人用户约 400 美元/年；企业许可不同）。提供免费试用。
- **优点：** 可靠、用户友好、对 WAS 支持出色。
- **缺点：** 付费；需要为每个项目进行设置。

**选项 2：DCEVM + HotSwapAgent（免费替代方案）**

- **它是什么：** 一个用于高级热交换的开源组合。
  - **DCEVM：** 一个经过修改的 JVM，扩展了 HotSpot 的 JVMTI，以允许更激进的类重定义（例如，添加/移除方法、更改层次结构）。
  - **HotSwapAgent：** 一个构建在 DCEVM 之上的代理，为自动类重载提供 IDE 集成。
- **为什么在 WAS 中使用它：**
  - 免费且功能强大，用于开发，模仿 JRebel 的能力。
  - 支持方法体更改、资源更新，甚至某些框架重载（通过插件）。
- **与 WAS 的 IBM JDK 的兼容性说明：**
  - WAS 通常附带 IBM 的 J9 JDK，它**原生不支持 DCEVM**（DCEVM 是 HotSpot 特定的）。
  - **解决方法：** 在开发时切换到 OpenJDK/HotSpot（例如，通过在 `setInitial.sh` 中覆盖 `JAVA_HOME` 或 Liberty 的 `jvm.options`）。彻底测试——IBM JDK 的垃圾回收和安全特性可能有所不同。
  - 在生产环境中，切换回 IBM JDK；这仅用于开发。
- **如何设置：**
  1. **安装 DCEVM：**
     - 从 GitHub 下载 DCEVM 修补程序 JAR（例如，对于 JDK 11+，使用 `dcevm-11.0.0+7-full.jar`）。
     - 运行：`java -jar dcevm.jar /path/to/your/jdk/jre/lib/server/jvm.dll server`（Windows）或 Linux 的等效命令（`libjvm.so`）。
     - 这会修补您的 JDK 的 JVM 二进制文件——请先备份！
  2. **安装 HotSwapAgent：**
     - 从 GitHub 下载 `hotswap-agent.jar`。
     - 添加到 WAS JVM 参数：`-XXaltjvm=dcevm -XX:+TraceClassLoading -javaagent:/path/to/hotswap-agent.jar=DCEVM`（加上任何插件，例如 `=hotswap-spring` 用于 Spring）。
  3. **IDE 集成：**
     - 为 IntelliJ/Eclipse 安装 HotSwapAgent 插件。
     - 使用上述调试参数启动 WAS。
     - 在 IDE 中编辑并保存代码——代理自动重新加载。
  4. **测试兼容性：**
     - 运行冒烟测试：部署一个简单的 Servlet，编辑一个方法（例如，添加一个日志行），访问端点，并验证更改而无需重启。
     - 检查日志中是否有错误，例如 `HotSwap failed: method limit reached`（DCEVM 对每个类的更改次数有限制）。
- **优点：** 免费、可定制（通过 Spring、CDI 等插件）、社区支持。
- **缺点：** 设置繁琐；使用非标准 JVM 时可能不稳定；仅限于 HotSpot（仔细测试 IBM JDK 切换）；不如 JRebel 精致。

#### 何时使用哪种方案

- **展开式 WAR + 内置重载：** 用于早期开发中的快速 JSP/静态文件调整。
- **JRebel：** 如果预算允许，并且您需要企业级的可靠性。
- **DCEVM + HotSwapAgent：** 用于免费的全功能热交换，但需要分配时间进行 JVM 兼容性测试。

总之，这些技术将 WAS 从一个重量级服务器转变为一个更敏捷的开发环境，将迭代时间从几分钟缩短到几秒钟。从展开式 WAR 开始以获得即时收益，然后根据需要叠加工具。如果您遇到特定的错误，请分享更多详细信息以进行故障排除。

**参考资料：**
[JRebel WebSphere 教程](https://www.jrebel.com/products/jrebel/tutorials/deploy-jrebel-websphere)
[DCEVM GitHub 仓库](https://github.com/dcevm/dcevm)
[HotSwapAgent GitHub 仓库](https://github.com/HotswapProjects/HotswapAgent)
[IBM 知识中心：WebSphere 热部署](https://www.ibm.com/docs/en/was/9.0.5?topic=applications-hot-deployment)
