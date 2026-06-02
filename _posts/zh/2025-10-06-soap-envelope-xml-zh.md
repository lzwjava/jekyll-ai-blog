---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: SOAP信封XML详解
translated: true
type: note
---

### 什么是信封 XML？

我相信“envalop”是“envelope”的笔误，指的是 XML 中的 **SOAP 信封**。SOAP（简单对象访问协议）是一种使用 XML 在 Web 服务中交换结构化信息的协议。SOAP 信封是 SOAP 消息的根元素，它包装整个消息以标识其为 SOAP 文档。它确保接收方知道这是一个完整的消息。

基本的 SOAP 信封结构如下所示：

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>
    <!-- 可选：元数据，如身份验证信息 -->
  </soap:Header>
  <soap:Body>
    <!-- 必需：实际的有效载荷/数据 -->
    <YourCustomElement>
      <Data>某个值</Data>
    </YourCustomElement>
  </soap:Body>
</soap:Envelope>
```

- **信封**：定义消息的开始/结束和命名空间。
- **头部**（可选）：用于非主体信息，如安全或路由信息。
- **主体**（必需）：包含请求/响应数据。

这种格式使得 SOAP 消息自包含且与传输协议无关（例如，可通过 HTTP 传输）。

### 如何在 Java 中使用 SOAP 信封 XML

Java 通过 **JAX-WS**（Java API for XML Web Services）和 **SAAJ**（SOAP with Attachments API for Java）库内置支持 SOAP，这些库是 JDK 的一部分（基本功能无需外部依赖）。

#### 创建和发送 SOAP 消息的步骤：
1. **创建 SOAP 消息**：使用 `javax.xml.soap` 以编程方式构建信封。
2. **添加内容**：填充主体（以及头部，如果需要）。
3. **通过 HTTP 发送**：使用 `HttpURLConnection` 或像 JAX-WS 这样的客户端进行完整的 Web 服务调用。

以下是一个简单的 Java 示例，用于创建 SOAP 信封并打印它（您可以扩展此示例以通过 HTTP 发送）：

```java
import javax.xml.soap.*;
import java.util.Iterator;

public class SoapEnvelopeExample {
    public static void main(String[] args) throws Exception {
        // 创建 SOAP 工厂
        SOAPFactory soapFactory = SOAPFactory.newInstance();

        // 创建消息和信封
        MessageFactory messageFactory = MessageFactory.newInstance();
        SOAPMessage soapMessage = messageFactory.createMessage();
        SOAPEnvelope envelope = soapMessage.getSOAPEnvelope();

        // 为 SOAP 添加命名空间（版本 1.2）
        envelope.addNamespaceDeclaration("soap", "http://www.w3.org/2003/05/soap-envelope");

        // 创建主体元素
        SOAPBody body = envelope.getBody();
        SOAPBodyElement bodyElement = body.addBodyElement(soapFactory.createName("GetBalance", "ns", "http://example.com"));
        SOAPElement amount = bodyElement.addChildElement("AccountNumber", "ns", "http://example.com");
        amount.addTextNode("12345");

        // 保存并打印消息
        soapMessage.saveChanges();
        System.out.println("SOAP 信封:");
        soapMessage.writeTo(System.out);
    }
}
```

- **输出**：这将生成一个包含信封、主体和您的自定义元素的 SOAP XML。
- **发送消息**：将其包装在 JAX-WS 客户端中。使用 `wsimport` 工具从 WSDL 文件生成存根：`wsimport -keep YourService.wsdl`。然后使用生成的客户端类调用方法，这些类会自动处理信封。
- **库**：对于高级用途，如果需要，可以添加 Apache CXF 或 Axis2，但为了简单起见，请坚持使用 JDK。

在任何 Java 环境（JDK 8+）中运行此代码。对于完整的 Web 服务，请确保您的项目处理像 `SOAPException` 这样的异常。

### Finacle 是否使用信封（SOAP XML）？

是的，Finacle（Infosys 的核心银行软件）在集成中广泛使用 SOAP XML 信封。它通过 **Finacle Integrator** 层通过 HTTP 上的 SOAP 公开 Web 服务，允许外部系统使用标准 SOAP 协议进行通信。这包括 EJB 交互和用于账户查询或交易等服务的中间件。Finacle 的 API 通常遵循 SOAP 标准，用于银行集成中安全的、基于 XML 的消息传递。

[XML Soap - W3Schools](https://www.w3schools.com/xml/xml_soap.asp)
[SOAP 消息的结构 - IBM](https://www.ibm.com/docs/en/integration-bus/9.0.0?topic=soap-structure-message)
[SOAP - 信封 - Tutorials Point](https://www.tutorialspoint.com/soap/soap_envelope.htm)
[java - 如何在 XML 请求中添加 <soap:Envelope> 和 <soap:body> - Stack Overflow](https://stackoverflow.com/questions/44721823/how-to-add-soapenvelope-and-soapbody-in-xml-request)
[SOAPEnvelope (Java Platform SE 8) - Oracle Help Center](https://docs.oracle.com/javase/8/docs/api/javax/xml/soap/SOAPEnvelope.html)
[使用 Spring Boot 在 Finacle Integrator 上实现微服务](https://medium.com/@einjoku/implementation-of-microservice-on-finacle-integrator-using-spring-boot-docker-with-kubernetes-d8f9c6026a6d)
[与 Finacle 集成的架构考虑](https://www.ijcttjournal.org/2024/Volume-72%20Issue-6/IJCTT-V72I6P108.pdf)
[AS-TFINFRIXM1012-FTX100 Finacle 集成技术 - Scribd](https://www.scribd.com/document/369534444/TFINFRIXM1012-ENU)
