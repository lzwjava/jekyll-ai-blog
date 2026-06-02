---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 端到端追踪至LLM智能体流水线
translated: true
type: note
---

你的方向很明确：AOP（AspectJ）、Servlet过滤器和Log4j2各自在不同层级发挥着作用。以下是一个简洁的全链路方案——首先用于**采集执行轨迹和HTTP输入输出**（以便自动生成Python测试），随后将**丰富上下文信息提供给Spring中的LLM“智能体”接口**。

---

## 1) 捕获所需信息（AOP + 过滤器 + Log4j2）

**a) 使用AOP进行方法拦截（记录耗时、参数、返回结果/异常）。**

通过`@Around`增强切面包装服务方法，将`traceId`存入MDC实现全链路日志关联。

```java
@Aspect
@Component
public class TraceAspect {
  @Around("execution(* com.example.service..*(..))")
  public Object around(ProceedingJoinPoint pjp) throws Throwable {
    String traceId = java.util.UUID.randomUUID().toString();
    org.apache.logging.log4j.ThreadContext.put("traceId", traceId);
    long t0 = System.nanoTime();
    try {
      Object out = pjp.proceed();
      org.apache.logging.log4j.LogManager.getLogger(pjp.getTarget().getClass())
        .info("AOP", "method={},args={},ret={},ms={},traceId={}",
              pjp.getSignature().toShortString(),
              java.util.Arrays.toString(pjp.getArgs()), out,
              (System.nanoTime()-t0)/1_000_000.0, traceId);
      return out;
    } catch (Throwable e) {
      org.apache.logging.log4j.LogManager.getLogger(pjp.getTarget().getClass())
        .error("AOP_ERR", "method={},args={},err={},traceId={}",
               pjp.getSignature().toShortString(),
               java.util.Arrays.toString(pjp.getArgs()),
               e.toString(), traceId);
      throw e;
    } finally {
      org.apache.logging.log4j.ThreadContext.remove("traceId");
    }
  }
}
```

（当需要控制方法调用并实现前后增强逻辑时，"环绕增强"是最佳选择。（[Spring官方文档][1], [DigitalOcean教程][2]））

**b) 使用过滤器记录HTTP日志（请求/响应体及状态码）。**

通过`OncePerRequestFilter`模式包装请求/响应，关联相同`traceId`（从请求头获取或自动生成）。优质教程会展示如何安全缓存请求体并避免重复消费。（[Baeldung Kotlin教程][3], [SigNoz指南][4]）

**c) 使用Log4j2路由附加器按用户/租户/测试分流日志。**

通过该功能可将匹配的日志（如根据MDC中的`traceId`或`tenantId`）写入**独立文件**，后续用于生成测试用例。

```xml
<Appenders>
  <Routing name="ByTrace">
    <Routes pattern="${ctx:traceId}">
      <Route ref="RollingTemplate" key="${ctx:traceId}"/>
    </Routes>
  </Routing>

  <RollingFile name="RollingTemplate"
               fileName="logs/${ctx:traceId}.log"
               filePattern="logs/${ctx:traceId}-%d{yyyy-MM-dd}.gz">
    <PatternLayout pattern="%d %p %c %X{traceId} - %m%n"/>
    <Policies><TimeBasedTriggeringPolicy/></Policies>
  </RollingFile>
</Appenders>
<Loggers>
  <Root level="info">
    <AppenderRef ref="ByTrace"/>
  </Root>
</Loggers>
```

（Log4j2路由附加器配合MDC是实现日志按关键字分流的标准方案。（[Apache日志文档][5], [Roy教程][6], [Stack Overflow解答][7]））

---

## 2) 将日志转化为**Python测试**（pytest + requests）

当日志转为JSON格式或可解析文本后，可通过轻量生成器输出确定性测试：

```python
# gen_tests_from_logs.py
import json, re, pathlib

def extract_calls(log_text):
    calls = []
    for line in log_text.splitlines():
        if '"HTTP_IN"' in line or 'HTTP_IN' in line:
            d = json.loads(re.search(r'({.*})', line).group(1))
            calls.append({
              "method": d["method"],
              "url": d["path"],
              "headers": d.get("headers", {}),
              "body": d.get("body", None),
              "expect_status": d.get("status", 200)
            })
    return calls

def emit_pytest(calls):
    lines = [
      "import requests",
      "import pytest",
      "",
      "@pytest.mark.parametrize('call', ["
    ]
    for c in calls:
      lines.append(f"  {json.dumps(c)},")
    lines += ["])",
      "def test_replay(call):",
      "    resp = requests.request(call['method'], 'http://localhost:8080'+call['url'],",
      "                             headers=call.get('headers'),",
      "                             json=call.get('body'))",
      "    assert resp.status_code == call['expect_status']",
      "    # 可选：对响应JSON中的结构化字段进行断言",
    ]
    return "\n".join(lines)

def main():
    all_calls = []
    for p in pathlib.Path('logs').glob('*.log'):
      all_calls += extract_calls(p.read_text(encoding='utf-8'))
    pathlib.Path('tests/test_replay_generated.py').write_text(emit_pytest(all_calls), encoding='utf-8')

if __name__ == "__main__":
    main()
```

注意事项：

* 推荐使用**JSON格式日志**记录请求/响应，可大幅简化测试生成
* 过滤敏感请求头（如Authorization）
* 若请求体过大，可在日志中存储哈希值并进行哈希断言

---

## 3) 通过Spring为LLM“智能体”**提供上下文**

若已使用Spring Boot，最快捷的方案是**Spring AI**：

**a) 配置`ChatClient`和提示词模板。**
Spring AI提供`ChatClient`/`PromptTemplate`抽象和工具调用能力，使模型能请求应用获取数据。（[官网][8], [工具调用文档][9]）

```java
@Configuration
public class AiConfig {
  @Bean ChatClient chatClient(org.springframework.ai.chat.ChatModel model) {
    return ChatClient.builder(model).defaultSystem("You are a helpful banking agent.").build();
  }
}
```

**b) 通过Spring Bean（服务）和“工具”提供上下文。**
将领域查询暴露为**工具**，使模型在对话过程中可动态调用。（Spring AI支持工具调用——由模型决定调用时机，结果将作为附加上下文返回。）（[工具调用文档][9]）

```java
@Component
public class AccountTools {
  @org.springframework.ai.tool.annotation.Tool
  public String fetchBalance(String userId){
    // 查询数据库或下游服务
    return "{\"balance\": 1234.56, \"currency\": \"HKD\"}";
  }
}
```

**c) 为文档/代码添加检索功能（RAG）。**
配置`VectorStore`（如PGVector）并注入知识嵌入向量。运行时检索最相关的文本块并附加到提示词中。现有实用教程详细演示了基于Spring Boot + PGVector构建完整RAG方案。（[sohamkamani.com][10]）

**d) 通过拦截器传递用户/会话上下文。**
使用`HandlerInterceptor`（或自定义过滤器）解析`userId`、`tenantId`、角色、区域设置、近期操作等——将其注入：

* 请求属性
* 作用域Bean
* 提示词中的**系统**和**用户**部分

**e) 统一接入的HTTP端点。**

```java
@RestController
@RequestMapping("/agent")
public class AgentController {
  private final ChatClient chat;
  private final UserContextProvider ctx;
  private final Retriever retriever;

  public AgentController(ChatClient chat, UserContextProvider ctx, Retriever retriever) {
    this.chat = chat; this.ctx = ctx; this.retriever = retriever;
  }

  @PostMapping
  public String chat(@RequestBody Map<String,Object> req, Principal principal) {
    var userCtx = ctx.fromPrincipal(principal);          // 身份信息、角色、偏好设置
    var docs   = retriever.findRelevant((String)req.get("message")); // RAG检索
    return chat.prompt()
      .system("Use tools if needed. Respect tenant="+userCtx.tenant()+" and role="+userCtx.role()+".")
      .user("Context:\n"+docs+"\n\nUser says: "+req.get("message"))
      .call().content();                                  // 工具调用自动执行
  }
}
```

**f) 可选：通过Spring Cloud Function部署“技能”。**
若需将每个智能体技能作为独立函数部署（适用于无服务器架构和按请求头路由），**Spring Cloud Function**支持编写纯函数`Function<T,R>`并动态路由——便于接入AWS Lambda/Azure，也可作为内部“智能体工具”端点。（[云平台文档][11], [官方文档][12], [Baeldung Kotlin教程][13]）

---

## 4) 全链路整合（流程）

1. **过滤器**添加`traceId`，记录HTTP输入输出
2. **AOP**包装服务方法并输出结构化事件
3. **Log4j2路由附加器**按跟踪标识写入独立文件
4. **Python生成器**读取日志文件 → 输出可回放真实调用的**pytest**
5. **Spring AI**接口使用：

   * 来自拦截器/过滤器的请求/租户/用户上下文
   * 领域“工具”获取实时数据
   * 向量存储（RAG）提供文档/代码上下文
   * `ChatClient`处理对话编排

该方案既可生成可复现的测试用例，又能提供具备丰富上下文的智能体接口——两者均由同一套遥测数据驱动。

如需实现，我可以提供包含Spring Boot组件、Log4j2配置和Python生成器脚本的最小化仓库结构，并集成到`make testgen && pytest`工作流中。

[1]: https://docs.spring.io/spring-framework/reference/core/aop/ataspectj/advice.html?utm_source=chatgpt.com "声明增强 :: Spring框架"
[2]: https://www.digitalocean.com/community/tutorials/spring-aop-example-tutorial-aspect-advice-pointcut-joinpoint-annotations?utm_source=chatgpt.com "Spring AOP实例教程 - 切面、增强、切点..."
[3]: https://www.baeldung.com/spring-http-logging?utm_source=chatgpt.com "记录传入请求 - Spring"
[4]: https://signoz.io/guides/spring-boot-how-to-log-all-requests-and-responses-with-exceptions-in-single-place/?utm_source=chatgpt.com "如何统一记录Spring Boot请求和响应"
[5]: https://logging.apache.org/log4j/2.12.x/manual/configuration.html?utm_source=chatgpt.com "配置Log4j 2 - Apache日志服务"
[6]: https://roytuts.com/how-to-create-separate-log-file-for-each-module-using-routingappender-and-mdc-mapped-diagnostic-context-in-log4j2-slf4j/?utm_source=chatgpt.com "如何使用路由附加器和MDC创建分模块日志"
[7]: https://stackoverflow.com/questions/18279656/wildcard-pattern-for-routingappender-of-log4j2?utm_source=chatgpt.com "Log4j2路由附加器的通配符模式 - Java"
[8]: https://spring.io/projects/spring-ai?utm_source=chatgpt.com "Spring AI"
[9]: https://docs.spring.io/spring-ai/reference/api/tools.html?utm_source=chatgpt.com "工具调用 :: Spring AI参考文档"
[10]: https://sohamkamani.com/java/spring-ai-rag-application?utm_source=chatgpt.com "使用Spring AI和PGVector构建RAG对话应用"
[11]: https://cloud.spring.io/spring-cloud-function/reference/html/spring-cloud-function.html?utm_source=chatgpt.com "Spring Cloud Function"
[12]: https://docs.spring.io/spring-cloud-function/docs/current/reference/html/spring-cloud-function.html?utm_source=chatgpt.com "Spring Cloud Function"
[13]: https://www.baeldung.com/spring-cloud-function-microsoft-azure?utm_source=chatgpt.com "面向Azure Function的Spring Cloud Function"
