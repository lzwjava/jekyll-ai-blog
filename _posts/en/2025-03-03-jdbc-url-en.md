---
audio: false
generated: true
lang: en
layout: post
title: Construct a JDBC URL
translated: false
type: note
---

To construct a JDBC URL for connecting to a DB2 database based on the `properties.db2.jcc` element in the `server.xml` file of a WebSphere Liberty Profile, you need to use the values provided for certain key attributes, such as `databaseName`, `serverName`, and `portNumber`. Here’s how to do it:

### Basic JDBC URL Format for DB2

The standard format for a JDBC URL using the DB2 JDBC Type 4 driver (which is commonly used in Liberty Profile setups) is:

```
jdbc:db2://<serverName>:<portNumber>/<databaseName>
```

- **`jdbc:db2://`** - This is the protocol identifier for a DB2 database using the Type 4 driver, indicating a direct network connection.
- **`<serverName>`** - The hostname or IP address of the DB2 server, specified by the `serverName` attribute in `properties.db2.jcc`.
- **`<portNumber>`** - The port on which the DB2 instance is listening, specified by the `portNumber` attribute (default is typically `50000` if not specified).
- **`<databaseName>`** - The name of the database to connect to, specified by the `databaseName` attribute.

### Steps to Construct the URL

1. **Identify the Required Properties**: From the `properties.db2.jcc` element in `server.xml`, extract the values for `serverName`, `portNumber`, and `databaseName`. These are the essential components needed for the URL.
2. **Assemble the URL**: Combine these values into the format above, ensuring proper separators (`:` between server and port, `/` before the database name).
3. **Handle Additional Properties (if present)**: If `properties.db2.jcc` includes other attributes (e.g., `currentSchema`, `sslConnection`), they can sometimes be appended to the URL, but this depends on their nature. Typically, properties like `user` and `password` are passed separately when establishing the connection, not in the URL, for security reasons.

### Example

Suppose your `server.xml` contains the following `properties.db2.jcc` configuration:

```xml
<properties.db2.jcc databaseName="SAMPLE" serverName="localhost" portNumber="50000" user="dbuser" password="dbpass"/>
```

- `serverName="localhost"`
- `portNumber="50000"`
- `databaseName="SAMPLE"`

The JDBC URL would be:

```
jdbc:db2://localhost:50000/SAMPLE
```

- The `user` and `password` are not included in the URL; they are typically provided separately when obtaining a connection via the JDBC driver (e.g., through a `DataSource` or `DriverManager`).

### Including Additional Properties (Optional)

If additional properties are specified in `properties.db2.jcc`, such as `currentSchema` or `sslConnection`, and you want to include them in the URL (though some may be better set in connection properties), append them after the database name with a colon (`:`) followed by semicolon-separated `property=value` pairs. For instance:

```xml
<properties.db2.jcc databaseName="SAMPLE" serverName="localhost" portNumber="50000" currentSchema="MYSCHEMA" sslConnection="true"/>
```

The URL could become:

```
jdbc:db2://localhost:50000/SAMPLE:currentSchema=MYSCHEMA;sslConnection=true;
```

However:

- Properties like `sslConnection=true` are often set in a `Properties` object or data source configuration rather than the URL.
- Check the DB2 JDBC driver documentation to confirm which properties are valid in the URL versus those requiring separate configuration.

### Final Answer

In the context of your query, assuming `properties.db2.jcc` provides at least `databaseName`, `serverName`, and `portNumber`, the JDBC URL is constructed as:

```
jdbc:db2://<serverName>:<portNumber>/<databaseName>
```

Replace `<serverName>`, `<portNumber>`, and `<databaseName>` with the actual values from your `properties.db2.jcc` configuration. If additional properties are present and intended for the URL, append them as `:property1=value1;property2=value2;`, but typically, properties like `user`, `password`, and `sslConnection` are handled separately in the connection setup.
