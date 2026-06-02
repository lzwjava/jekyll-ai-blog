---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: SOAP Envelope XML Explained
translated: false
type: note
---

### What is an Envelope XML?

I believe "envalop" is a typo for "envelope," referring to the **SOAP Envelope** in XML. SOAP (Simple Object Access Protocol) is a protocol for exchanging structured information in web services using XML. The SOAP Envelope is the root element of a SOAP message, which wraps the entire message to identify it as a SOAP document. It ensures the receiver knows it's a complete message.

A basic SOAP Envelope structure looks like this:

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>
    <!-- Optional: Metadata like authentication -->
  </soap:Header>
  <soap:Body>
    <!-- Mandatory: The actual payload/data -->
    <YourCustomElement>
      <Data>Some value</Data>
    </YourCustomElement>
  </soap:Body>
</soap:Envelope>
```

- **Envelope**: Defines the start/end of the message and namespace.
- **Header** (optional): For non-body info like security or routing.
- **Body** (required): Contains the request/response data.

This format makes SOAP messages self-contained and transport-agnostic (e.g., over HTTP).

### How to Use SOAP Envelope XML in Java

Java has built-in support for SOAP via the **JAX-WS** (Java API for XML Web Services) and **SAAJ** (SOAP with Attachments API for Java) libraries, part of the JDK (no external dependencies needed for basics).

#### Steps to Create and Send a SOAP Message

1. **Create a SOAP Message**: Use `javax.xml.soap` to build the envelope programmatically.
2. **Add Content**: Populate the Body (and Header if needed).
3. **Send via HTTP**: Use `HttpURLConnection` or a client like JAX-WS for full web service calls.

Here's a simple Java example to create a SOAP Envelope and print it (you can extend this to send it over HTTP):

```java
import javax.xml.soap.*;
import java.util.Iterator;

public class SoapEnvelopeExample {
    public static void main(String[] args) throws Exception {
        // Create a SOAP factory
        SOAPFactory soapFactory = SOAPFactory.newInstance();

        // Create the message and envelope
        MessageFactory messageFactory = MessageFactory.newInstance();
        SOAPMessage soapMessage = messageFactory.createMessage();
        SOAPEnvelope envelope = soapMessage.getSOAPEnvelope();

        // Namespace for SOAP (version 1.2)
        envelope.addNamespaceDeclaration("soap", "http://www.w3.org/2003/05/soap-envelope");

        // Create Body element
        SOAPBody body = envelope.getBody();
        SOAPBodyElement bodyElement = body.addBodyElement(soapFactory.createName("GetBalance", "ns", "http://example.com"));
        SOAPElement amount = bodyElement.addChildElement("AccountNumber", "ns", "http://example.com");
        amount.addTextNode("12345");

        // Save and print the message
        soapMessage.saveChanges();
        System.out.println("SOAP Envelope:");
        soapMessage.writeTo(System.out);
    }
}
```

- **Output**: This generates a SOAP XML with the envelope, body, and your custom elements.
- **To Send It**: Wrap in a JAX-WS client. Generate stubs from a WSDL file using `wsimport` tool: `wsimport -keep YourService.wsdl`. Then use the generated client classes to invoke methods, which handle the envelope automatically.
- **Libraries**: For advanced use, add Apache CXF or Axis2 if needed, but stick to JDK for simplicity.

Run this in any Java environment (JDK 8+). For full web services, ensure your project handles exceptions like `SOAPException`.

### Does Finacle Use Envelope (SOAP XML)?

Yes, Finacle (Infosys's core banking software) extensively uses SOAP XML envelopes for integration. It exposes web services via SOAP over HTTP through the **Finacle Integrator** layer, allowing external systems to communicate using standard SOAP protocols. This includes EJB interactions and middleware for services like account queries or transactions. Finacle's APIs often follow SOAP standards for secure, XML-based messaging in banking integrations.

[XML Soap - W3Schools](https://www.w3schools.com/xml/xml_soap.asp)
[The structure of a SOAP message - IBM](https://www.ibm.com/docs/en/integration-bus/9.0.0?topic=soap-structure-message)
[SOAP - Envelope - Tutorials Point](https://www.tutorialspoint.com/soap/soap_envelope.htm)
[java - how to add <soap:Envelope> and <soap:body> in xml request - Stack Overflow](https://stackoverflow.com/questions/44721823/how-to-add-soapenvelope-and-soapbody-in-xml-request)
[SOAPEnvelope (Java Platform SE 8) - Oracle Help Center](https://docs.oracle.com/javase/8/docs/api/javax/xml/soap/SOAPEnvelope.html)
[Implementation of Microservice on Finacle Integrator using Spring Boot](https://medium.com/@einjoku/implementation-of-microservice-on-finacle-integrator-using-spring-boot-docker-with-kubernetes-d8f9c6026a6d)
[Architectural Considerations for Integrating with Finacle](https://www.ijcttjournal.org/2024/Volume-72%20Issue-6/IJCTT-V72I6P108.pdf)
[AS-TFINFRIXM1012-FTX100 Finacle Integration Technical - Scribd](https://www.scribd.com/document/369534444/TFINFRIXM1012-ENU)
