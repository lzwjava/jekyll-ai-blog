---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: WebSphere应用服务器中的Jython
translated: true
type: note
---

### 在 IBM WebSphere Application Server 中使用 Jython

注："jPython" 指的是 Jython，一种在 Java 虚拟机（JVM）上运行的 Python 实现。它常用于 WebSphere 的管理脚本编写，也可集成到已部署的应用程序中。WebSphere Application Server (WAS) 捆绑了 Jython（通常为 2.1 或更高版本，具体取决于 WAS 版本），位于 `<WAS_HOME>/optionalLibraries/jython` 目录下，因此通常无需单独安装。下面将介绍两种主要使用场景：管理任务和应用程序中的运行时使用。

#### 1. 使用 wsadmin 进行管理脚本编写
在 WebSphere 中使用 Jython 最常见的方式是执行服务器管理任务，如部署应用程序、启动/停止服务器、配置资源和列出已安装的应用。这通过 `wsadmin` 工具实现，该工具支持将 Jython 作为首选脚本语言（取代已弃用的 Jacl）。

**前提条件：**
- 确保 WebSphere 服务器正在运行。
- 在 `<WAS_HOME>/bin/wsadmin.sh`（Linux/Unix）或 `wsadmin.bat`（Windows）中找到 `wsadmin`。
- Jython 已预捆绑；如需新功能（例如 Python 2.5+ 语法），可能需要通过自定义类路径升级（见下文高级说明）。

**运行 Jython 脚本的基本步骤：**
1. 创建 Jython 脚本文件（例如 `example.py`）并编写代码。使用 AdminConfig、AdminControl 和 AdminApp 对象执行 WebSphere 特定操作。

   列出所有已安装应用程序的示例脚本（`listApps.py`）：
   ```
   # 列出所有应用程序
   apps = AdminApp.list()
   print("已安装的应用程序：")
   for app in apps.splitlines():
       if app.strip():
           print(app.strip())
   AdminConfig.save()  # 可选：保存配置更改
   ```

2. 使用 `wsadmin` 运行脚本：
   - 通过 SOAP 连接（远程默认方式）：
     ```
     wsadmin.sh -lang jython -f listApps.py -host <主机名> -port <soap_port> -user <管理员用户> -password <管理员密码>
     ```
   - 本地连接（无需主机/端口）：
     ```
     wsadmin.sh -lang jython -f listApps.py
     ```
   - 示例输出：列出类似 `DefaultApplication` 的应用程序。

3. 交互模式（REPL）：
   ```
   wsadmin.sh -lang jython
   ```
   然后直接输入 Jython 命令，例如 `print AdminApp.list()`。

**常见示例：**
- **部署 EAR/WAR：** 创建 `deployApp.py`：
  ```
  appName = 'MyApp'
  earPath = '/path/to/MyApp.ear'
  AdminApp.install(earPath, '[-appname ' + appName + ' -server server1]')
  AdminConfig.save()
  print('已部署 ' + appName)
  ```
  运行：`wsadmin.sh -lang jython -f deployApp.py`。

- **启动/停止服务器：**
  ```
  server = AdminControl.completeObjectName('type=Server,process=server1,*')
  AdminControl.invoke(server, 'start')  # 或 'stop'
  ```

- **指定 Jython 版本（如需要）：** 显式使用 Jython 2.1：
  `wsadmin.sh -usejython21 true -f script.py`。对于自定义版本，添加到类路径：`-wsadmin_classpath /path/to/jython.jar`。

**提示：**
- 使用 `AdminConfig.help('object_type')` 获取命令帮助。
- 脚本可在 CI/CD（例如 Jenkins）中通过批处理文件调用 `wsadmin` 实现自动化。
- 对于瘦客户端（无完整 WAS 安装）：从 IBM 下载客户端 jar 并设置类路径。

#### 2. 在已部署的应用程序中使用 Jython
要在运行于 WebSphere 上的 Java 应用程序（例如 servlet 或 EJB）中执行 Jython 代码，需将 Jython 运行时（jython.jar）包含在应用程序的类路径中。这允许嵌入 Python 脚本或将 Jython 用作脚本引擎。如果捆绑版本过时，请从官方 Jython 站点下载最新的 jython.jar。

有两种主要方法：**类路径**（服务器范围）或**共享库**（跨应用程序可重用）。

**方法 1：类路径（直接添加到 JVM）**
1. 将 `jython.jar` 保存到 WebSphere 主机上的可访问路径（例如 `/opt/IBM/WebSphere/AppServer/profiles/AppSrv01/mylibs/jython.jar`）。
2. 登录 WebSphere 管理控制台。
3. 导航至 **服务器 > 服务器类型 > WebSphere 应用程序服务器 > [您的服务器]**。
4. 进入 **Java 和进程管理 > 进程定义 > Java 虚拟机 > 类路径**。
5. 添加 `jython.jar` 的完整路径（例如 `/opt/.../jython.jar`）。
6. 在 **通用 JVM 参数** 中添加 Python 路径：
   `-Dpython.path=/opt/.../jython.jar/Lib`（指向 Jython 的标准库）。
7. 点击 **确定**，保存配置并重启服务器。
8. 如果在集群环境中，同步节点（通过 **系统管理 > 节点 > 同步**）。
9. 在 Java 代码中，使用 `org.python.util.PythonInterpreter` 运行 Jython 脚本：
   ```
   import org.python.util.PythonInterpreter;
   PythonInterpreter interpreter = new PythonInterpreter();
   interpreter.exec("print('Hello from Jython in WebSphere!')");
   ```

**方法 2：共享库（推荐用于多个应用程序）**
1. 将 `jython.jar` 放入共享目录（例如 `/shared/libs/jython.jar`）。
2. 在管理控制台中：**环境 > 共享库 > [范围：服务器或单元] > 新建**。
3. 输入名称（例如 `JythonLib`），勾选 **使用本机库目录**，并将 **类路径** 设置为 `/shared/libs/jython.jar`。
4. 保存。
5. 对于特定应用程序：**应用程序 > 应用程序类型 > WebSphere 企业应用程序 > [您的应用程序] > 引用共享库**。
6. 在 **共享库引用** 下，点击 **添加**，选择 `JythonLib`，并设置 **类路径** 以匹配。
7. 保存，更新应用程序（如需要则重启），并同步节点。
8. 在代码中引用，如类路径方法所示。

**应用程序提示：**
- 对于基于 servlet 的 Jython 应用程序，使用 PyServlet（包含在 Jython 中）处理 Python 处理器。
- 在开发环境中测试；监控日志以排查类路径问题。
- 如果使用较新的 Jython（例如 2.7），确保与 Java 8+ 兼容。

#### 高级说明
- **版本兼容性：** WAS 9.x 使用 Jython 2.7+。升级时，替换捆绑的 jar 但需彻底测试。
- **错误处理：** 在脚本中使用 `try: ... except Exception as e: print(e)`。
- **IDE 支持：** 使用 IBM Rational Application Developer (RAD) 或带有 WebSphere 插件的 Eclipse 调试 Jython/wsadmin 脚本。
- **资源：** 完整教程请参阅书籍 *WebSphere Application Server Administration Using Jython* 或 IBM 的 wsadmin 文档。

如果这与您的具体场景不匹配（例如特定的 WAS 版本或使用案例），请提供更多细节以获取定制建议。

**参考资料：**
- [使用 Jython 进行 wsadmin 脚本编写（IBM 文档）](https://www.ibm.com/docs/en/was/9.0.5?topic=scripting-using-wsadmin-jython)
- [在 WebSphere 上部署 Jython（Oracle 指南）](https://docs.oracle.com/en/applications/jd-edwards/cross-product/9.2/eotos/deploying-jython-on-ais-server-on-ibm-websphere-application.html)
- [WebSphere Jython 集成（Stack Overflow）](https://stackoverflow.com/questions/25187577/will-the-ibm-websphere-application-server-run-the-python-jython-script-without-p)
- [WebSphere 上的 Jython Wiki](https://wiki.python.org/jython/WebSphere)
- [使用 Jython 部署应用程序示例](https://jobhunterssite.wordpress.com/2016/05/12/deploy-an-application-in-websphere-using-jython-automation/)
