---
audio: false
generated: true
lang: en
layout: post
title: Using XML in Java
translated: false
type: note
---

Using XML in Java can be done in several ways depending on what you want to achieve—parsing, creating, or manipulating XML data. Here’s a concise guide to get you started with some common approaches:

### 1. **Parsing XML with DOM (Document Object Model)**
If you want to read and manipulate XML as a tree structure in memory, the DOM API is a good choice.

```java
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

public class XMLParser {
    public static void main(String[] args) {
        try {
            // Load and parse the XML file
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse("example.xml");

            // Normalize the XML structure
            doc.getDocumentElement().normalize();

            // Access elements (e.g., all "item" tags)
            NodeList list = doc.getElementsByTagName("item");
            for (int i = 0; i < list.getLength(); i++) {
                Element element = (Element) list.item(i);
                System.out.println("Element: " + element.getNodeName());
                System.out.println("Value: " + element.getTextContent());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

**Example XML (example.xml):**
```xml
<root>
    <item>Item 1</item>
    <item>Item 2</item>
</root>
```

- **Pros**: Easy to navigate and modify the XML structure.
- **Cons**: Memory-intensive for large files.

---

### 2. **Parsing XML with SAX (Simple API for XML)**
For large XML files where memory efficiency matters, SAX is event-driven and doesn’t load the whole file into memory.

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
                        System.out.println("Item: " + new String(ch, start, length));
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

- **Pros**: Lightweight and fast for large files.
- **Cons**: No random access; you process it sequentially.

---

### 3. **Creating XML with DOM**
To generate XML from scratch:

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

            // Root element
            Element root = doc.createElement("root");
            doc.appendChild(root);

            // Child element
            Element item = doc.createElement("item");
            item.appendChild(doc.createTextNode("Item 1"));
            root.appendChild(item);

            // Save to file
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult("output.xml");
            transformer.transform(source, result);

            System.out.println("XML file created!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

This creates an `output.xml` file with the structure shown earlier.

---

### 4. **Using JAXB (Java Architecture for XML Binding)**
If you’re working with XML that maps to Java objects (e.g., serialization/deserialization), JAXB is a higher-level option. You’ll need to define a class with annotations.

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
            // Marshalling (Java to XML)
            JAXBContext context = JAXBContext.newInstance(Item.class);
            Marshaller marshaller = context.createMarshaller();
            marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);

            Item item = new Item();
            item.setName("Item 1");
            marshaller.marshal(item, new File("item.xml"));

            // Unmarshalling (XML to Java)
            Unmarshaller unmarshaller = context.createUnmarshaller();
            Item loadedItem = (Item) unmarshaller.unmarshal(new File("item.xml"));
            System.out.println("Loaded item: " + loadedItem.getName());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

- **Pros**: Simplifies XML-to-object mapping.
- **Cons**: Requires annotated classes and isn’t ideal for complex, irregular XML.

---

### Getting Started
- **Dependencies**: These examples use Java’s built-in libraries (like `javax.xml.parsers`), so no external dependencies are needed for DOM or SAX. For JAXB, ensure you’re using a Java version that includes it (pre-Java 9) or add it via Maven/Gradle if using a newer version.
- **File**: Replace `"example.xml"` or `"output.xml"` with your actual file paths.

Which approach suits you depends on your needs—DOM for flexibility, SAX for efficiency, or JAXB for object mapping. Want me to dive deeper into any of these?
