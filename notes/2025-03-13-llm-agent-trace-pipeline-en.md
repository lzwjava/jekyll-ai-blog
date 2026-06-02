---
audio: false
generated: true
image: false
lang: en
layout: post
title: End-to-End Trace to LLM Agent Pipeline
translated: false
type: note
---

You’re on a solid track: AOP (AspectJ), servlet filters, and Log4j2 each shine at different layers. Here’s a compact, end-to-end way to use them together—first to **harvest execution traces and HTTP I/O** (so you can auto-mint Python tests), then to **feed rich context to an LLM “agent” endpoint in Spring**.

---

## 1) Capture what you need (AOP + Filter + Log4j2)

**a) Method interception with AOP (timings, args, return/throwables).**

Use `@Around` advice to wrap service methods; store a `traceId` in MDC so logs from all layers join up.

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

(“Around advice” is the right tool when you need pre/post logic and control of the call. ([Home][1], [DigitalOcean][2]))

**b) HTTP logging with a Filter (request/response body + status).**

Wrap the request/response once per call; attach the same `traceId` (from header or generate). Spring’s `OncePerRequestFilter` pattern is standard. Good guides show how to buffer body safely and avoid double-consumption. ([Baeldung on Kotlin][3], [SigNoz][4])

**c) Route logs per user/tenant/test using Log4j2 RoutingAppender.**

This lets you send matched logs (e.g., by `traceId` or `tenantId` in MDC) into **separate files** you’ll later convert into tests.

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

(Log4j2’s RoutingAppender + MDC pattern is the canonical way to split logs by key. ([Apache Logging][5], [Roy Tutorials][6], [Stack Overflow][7]))

---

## 2) Turn those logs into **Python tests** (pytest + requests)

Once logs are JSON-ish or parseable lines, a tiny generator can emit deterministic tests:

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
      "    # optionally assert on structured fields from response JSON",
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

Tips:

* Prefer **JSON logs** for requests/responses; it makes test generation trivial.
* Keep sensitive headers out (e.g., Authorization).
* If bodies are large, store a hash in logs and assert hash equality rather than full string.

---

## 3) Use Spring to **provide context** to LLM “agents”

If you’re on Spring Boot today, the shortest path is **Spring AI**:

**a) Set up a `ChatClient` and prompt templates.**
Spring AI gives you `ChatClient`/`PromptTemplate` abstractions and tool-calling so the model can ask your app to fetch data. ([Home][8], [Home][9])

```java
@Configuration
public class AiConfig {
  @Bean ChatClient chatClient(org.springframework.ai.chat.ChatModel model) {
    return ChatClient.builder(model).defaultSystem("You are a helpful banking agent.").build();
  }
}
```

**b) Provide context via Spring beans (services) and “tools.”**
Expose domain lookups as **tools** so the model can call them during a chat turn. (Spring AI supports tool calling—model decides when to invoke; result flows back as extra context.) ([Home][9])

```java
@Component
public class AccountTools {
  @org.springframework.ai.tool.annotation.Tool
  public String fetchBalance(String userId){
    // query DB or downstream service
    return "{\"balance\": 1234.56, \"currency\": \"HKD\"}";
  }
}
```

**c) Add retrieval (RAG) for documents/code.**
Wire a `VectorStore` (PGVector, etc.) and stuff it with embeddings of your knowledge. At runtime, retrieve top-k chunks and attach them to the prompt. There’s a current, practical tutorial building a full RAG stack with Spring Boot + PGVector. ([sohamkamani.com][10])

**d) Thread user/session context through Interceptors.**
Use a `HandlerInterceptor` (or your Filter) to resolve `userId`, `tenantId`, roles, locale, last-N actions—put them into:

* request attributes,
* a scoped bean, or
* the **system** and **user** parts of your prompt.

**e) One HTTP endpoint to rule them all.**

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
    var userCtx = ctx.fromPrincipal(principal);          // ids, roles, preferences
    var docs   = retriever.findRelevant((String)req.get("message")); // RAG
    return chat.prompt()
      .system("Use tools if needed. Respect tenant="+userCtx.tenant()+" and role="+userCtx.role()+".")
      .user("Context:\n"+docs+"\n\nUser says: "+req.get("message"))
      .call().content();                                  // tool calls happen implicitly
  }
}
```

**f) Optional: Deploy “skills” with Spring Cloud Function.**
If you want each agent skill as a single function (great for serverless and routing by headers), **Spring Cloud Function** lets you write pure `Function<T,R>` and route dynamically—nice for plugging into AWS Lambda/Azure and for internal “agent tool” endpoints. ([cloud.spring.io][11], [Home][12], [Baeldung on Kotlin][13])

---

## 4) Putting it all together (flow)

1. **Filter** adds `traceId`, logs HTTP I/O.
2. **AOP** wraps service methods and emits structured events.
3. **Log4j2 RoutingAppender** writes per-trace files.
4. **Python generator** reads those files → emits **pytest** that replays real calls.
5. **Spring AI** endpoint uses:

   * request/tenant/user context from Interceptor/Filter,
   * domain “tools” for live data,
   * vector store (RAG) for doc/code context,
   * `ChatClient` for chat orchestration.

That gives you reproducible tests and a robust, contextual agent interface—both driven by the same telemetry.

If you want, I can sketch a minimal repo structure with the Spring Boot pieces, a Log4j2 config, and the Python generator script wired into a `make testgen && pytest` workflow.

[1]: https://docs.spring.io/spring-framework/reference/core/aop/ataspectj/advice.html?utm_source=chatgpt.com "Declaring Advice :: Spring Framework"
[2]: https://www.digitalocean.com/community/tutorials/spring-aop-example-tutorial-aspect-advice-pointcut-joinpoint-annotations?utm_source=chatgpt.com "Spring AOP Example Tutorial - Aspect, Advice, Pointcut, ..."
[3]: https://www.baeldung.com/spring-http-logging?utm_source=chatgpt.com "Log Incoming Requests - Spring"
[4]: https://signoz.io/guides/spring-boot-how-to-log-all-requests-and-responses-with-exceptions-in-single-place/?utm_source=chatgpt.com "How to Log All Spring Boot Requests and Responses"
[5]: https://logging.apache.org/log4j/2.12.x/manual/configuration.html?utm_source=chatgpt.com "Configuring Log4j 2 - Apache Logging Services"
[6]: https://roytuts.com/how-to-create-separate-log-file-for-each-module-using-routingappender-and-mdc-mapped-diagnostic-context-in-log4j2-slf4j/?utm_source=chatgpt.com "How to create separate log file for each module using ..."
[7]: https://stackoverflow.com/questions/18279656/wildcard-pattern-for-routingappender-of-log4j2?utm_source=chatgpt.com "Wildcard pattern for RoutingAppender of Log4j2 - java"
[8]: https://spring.io/projects/spring-ai?utm_source=chatgpt.com "Spring AI"
[9]: https://docs.spring.io/spring-ai/reference/api/tools.html?utm_source=chatgpt.com "Tool Calling :: Spring AI Reference"
[10]: https://sohamkamani.com/java/spring-ai-rag-application?utm_source=chatgpt.com "Build a RAG-Powered Chat App with Spring AI and PGVector"
[11]: https://cloud.spring.io/spring-cloud-function/reference/html/spring-cloud-function.html?utm_source=chatgpt.com "Spring Cloud Function"
[12]: https://docs.spring.io/spring-cloud-function/docs/current/reference/html/spring-cloud-function.html?utm_source=chatgpt.com "Spring Cloud Function"
[13]: https://www.baeldung.com/spring-cloud-function-microsoft-azure?utm_source=chatgpt.com "Spring Cloud Function for Azure Function"
