---
audio: false
generated: true
lang: zh
layout: post
title: Java中的XML使用
translated: true
type: note
---

在 Java 中使用 XML 可通过多种方式实现，具体取决于你的需求——解析、创建或操作 XML 数据。以下是一份简明指南，介绍几种常见方法：

### 1. **使用 DOM（文档对象模型）解析 XML**
若需将 XML 作为内存中的树结构进行读取和操作，DOM API 是不错的选择。

```java
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

public class XMLParser {
    public static void main(String[] args) {
        try {
            // 加载并解析 XML 文件
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse("example.xml");

            // 标准化 XML 结构
            doc.getDocumentElement().normalize();

            // 访问元素（例如所有 "item" 标签）
            NodeList list = doc.getElementsByTagName("item");
            for (int i = 0; i < list.getLength(); i++) {
                Element element = (Element) list.item(i);
                System.out.println("元素: " + element.getNodeName());
                System.out.println("值: " + element.getTextContent());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

**示例 XML (example.xml):**
```xml
<root>
    <item>项目 1</item>
    <item>项目 2</item>
</root>
```

- **优点**：便于导航和修改 XML 结构
- **缺点**：处理大文件时内存消耗高

---

### 2. **使用 SAX（XML 简单 API）解析 XML**
对于需要内存效率的大型 XML 文件，SAX 采用事件驱动模式，不会将整个文件加载到内存。

```java
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

public class SAXExample {
    public static void main(String[] args) {
        try {
            SAXParserFactory factory = SAXParserFactory.newInstance();
            SAXParser saxParser = factory.newSAXParser();

            DefaultHandler handler = new DefaultHandler() {
                boolean inItem = false;

                @Override
                public void startElement(String uri, String localName, String qName, Attributes attributes) {
                    if (qName.equalsIgnoreCase("item")) {
                        inItem = true;
                    }
                }

                @Override
                public void characters(char[] ch, int start, int length) {
                    if (inItem) {
                        System.out.println("项目: " + new String(ch, start, length));
                        inItem = false;
                    }
                }
            };

            saxParser.parse("example.xml", handler);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

- **优点**：轻量级，处理大文件速度快
- **缺点**：无法随机访问，只能顺序处理

---

### 3. **使用 DOM 创建 XML**
从头生成 XML：

```java
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

public class XMLCreator {
    public static void main(String[] args) {
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.newDocument();

            // 根元素
            Element root = doc.createElement("root");
            doc.appendChild(root);

            // 子元素
            Element item = doc.createElement("item");
            item.appendChild(doc.createTextNode("项目 1"));
            root.appendChild(item);

            // 保存到文件
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult("output.xml");
            transformer.transform(source, result);

            System.out.println("XML 文件已创建！");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

这将创建具有前述结构的 `output.xml` 文件。

---

### 4. **使用 JAXB（Java XML 绑定架构）**
若需处理与 Java 对象映射的 XML（如序列化/反序列化），JAXB 是更高级的选择。需要使用注解定义类。

```java
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
class Item {
    private String name;

    @XmlElement
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}

import javax.xml.bind.JAXBContext;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;
import java.io.File;

public class JAXBExample {
    public static void main(String[] args) {
        try {
            // 编组（Java 转 XML）
            JAXBContext context = JAXBContext.newInstance(Item.class);
            Marshaller marshaller = context.createMarshaller();
            marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);

            Item item = new Item();
            item.setName("项目 1");
            marshaller.marshal(item, new File("item.xml"));

            // 解组（XML 转 Java）
            Unmarshaller unmarshaller = context.createUnmarshaller();
            Item loadedItem = (Item) unmarshaller.unmarshal(new File("item.xml"));
            System.out.println("已加载项目: " + loadedItem.getName());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

- **优点**：简化 XML 与对象的映射
- **缺点**：需要注解类，不适用于复杂非常规 XML

---

### 快速开始
- **依赖项**：这些示例使用 Java 内置库（如 `javax.xml.parsers`），因此 DOM 或 SAX 无需外部依赖。对于 JAXB，请确保使用的 Java 版本包含该模块（Java 9 之前版本），或在使用新版本时通过 Maven/Gradle 添加
- **文件**：将 `"example.xml"` 或 `"output.xml"` 替换为实际文件路径

选择哪种方法取决于具体需求——DOM 适合灵活性要求高的场景，SAX 适合注重效率的场景，JAXB 适合对象映射场景。需要深入了解其中任何方法吗？
