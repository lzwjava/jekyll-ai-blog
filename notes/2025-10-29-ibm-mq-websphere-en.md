---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring IBM MQ in WebSphere
translated: false
type: note
---

### Configuring Message Queues in IBM WebSphere Application Server (Using IBM MQ as the Provider)

IBM WebSphere Application Server (WAS) supports message queuing through Java Message Service (JMS) integration with IBM MQ (formerly WebSphere MQ). Configuration is typically done via the **WebSphere Integrated Solutions Console** (the administrative interface), accessible at `https://your-server:9043/ibm/console` (default secure port; adjust as needed). This guide focuses on the traditional full-profile WAS (e.g., version 9.0+), but steps are similar for WebSphere Liberty with minor adjustments.

#### Prerequisites

- IBM MQ must be installed, running, and accessible (e.g., queue manager started).
- WAS server is started, and you have admin access to the console.
- Download and install the IBM MQ JMS client libraries (e.g., `com.ibm.mq.allclient.jar`) into WAS's shared libraries if not already present (under **Environment > Shared Libraries**).
- Ensure the WebSphere MQ messaging provider is configured (under **Resources > JMS > JMS providers**). If not, create one with details like host, port (default 1414), and queue manager name.

After configuration, save changes (**Save** button at the top) and restart the application server for them to take effect.

#### Step 1: Create a JMS Queue Connection Factory

The connection factory establishes connections to the IBM MQ queue manager.

1. Log in to the WAS Admin Console.
2. In the navigation pane, expand **Resources > JMS > Queue connection factories**.
3. Select the appropriate **Scope** (e.g., Cell, Node, Server) from the dropdown and click **Apply**.
4. Click **New**.
5. Select **WebSphere MQ messaging provider** and click **OK**.
6. On the next screen:
   - **Name**: Enter a descriptive name (e.g., `MyMQQueueConnectionFactory`).
   - **JNDI name**: Enter a JNDI binding (e.g., `jms/MyQueueConnectionFactory`).
   - Click **Next**.
7. Enter connection details:
   - **Queue manager**: Name of your IBM MQ queue manager (e.g., `QM1`).
   - **Host name**: IBM MQ server hostname or IP.
   - **Port**: Listener port (default: 1414).
   - **Transport type**: CHANNEL (for client mode) or BINDINGS (for embedded).
   - **Channel**: Default channel name (e.g., `SYSTEM.DEF.SVRCONN`).
   - **User ID** and **Password**: Credentials for MQ authentication (if required).
   - Click **Next**.
8. Review the summary and click **Finish**.
9. Select the new factory, go to **Additional Properties > Connection pool** (optional), and tune settings like **Maximum connections** (e.g., based on expected load).
10. Click **Test connection** to verify.

#### Step 2: Create a JMS Queue Destination

This defines the actual queue endpoint for sending/receiving messages.

1. In the navigation pane, expand **Resources > JMS > Queues**.
2. Select the appropriate **Scope** (matching the connection factory) and click **Apply**.
3. Click **New**.
4. Select **WebSphere MQ messaging provider** and click **OK**.
5. Specify properties:
   - **Name**: Descriptive name (e.g., `MyRequestQueue`).
   - **JNDI name**: JNDI binding (e.g., `jms/MyRequestQueue`).
   - **Base queue name**: Exact queue name in IBM MQ (e.g., `REQUEST.QUEUE`; must exist or be created in MQ).
   - **Target client**: JMS (for JMS apps) or MQ (for native MQ apps).
   - **Target destination mode**: Once only (default for reliability).
   - Click **OK**.
6. (Optional) Under **Additional Properties**, configure persistence, expiry, or priority settings.
7. Save the configuration.

#### Step 3: (Optional) Create an Activation Specification for Message-Driven Beans (MDBs)

If using MDBs to consume messages asynchronously:

1. In the navigation pane, expand **Resources > JMS > Activation specifications**.
2. Select the **Scope** and click **New**.
3. Select **WebSphere MQ messaging provider** and click **OK**.
4. Enter:
   - **Name**: e.g., `MyQueueActivationSpec`.
   - **JNDI name**: e.g., `jms/MyQueueActivation`.
   - **Destination type**: Queue.
   - **Destination JNDI name**: The JNDI of your queue (e.g., `jms/MyRequestQueue`).
   - **Connection factory JNDI name**: The JNDI of your connection factory (e.g., `jms/MyQueueConnectionFactory`).
   - Message selector (optional): JMS selector for filtering messages.
5. Under **Additional Properties > Message Listener Service > Listener Ports**, create a port if needed:
   - **Name**: e.g., `MyListenerPort`.
   - **Connection factory JNDI**: As above.
   - **Destination JNDI**: As above.
   - **Component**: Your MDB's deployment descriptor.
6. Click **OK** and save.

#### Step 4: Verify and Test

- **Test in Console**: Use the **Test connection** on factories and specs.
- **Deploy an App**: Create a simple JMS client or MDB app, deploy it, and send/test messages via IBM MQ tools (e.g., MQ Explorer).
- **Monitoring**: Under **Monitoring and Tuning > Performance Viewer** or **Troubleshooting > Logs**, check for JMS-related errors.
- Common Issues:
  - Connection failures: Verify firewall, MQ channel status (`DISPLAY CHANNEL`), and credentials.
  - JNDI lookup errors: Ensure bindings are correct and app uses the right scope.
  - Persistence: Align durability settings between WAS and MQ.

For command-line alternatives (wsadmin scripting), refer to IBM docs. Tune based on your version (e.g., WAS 9.0.5+ supports JMS 2.0).

#### References

- [Configuring JMS resources in WebSphere Application Server](https://www.ibm.com/docs/en/ibm-mq/9.2.x?topic=resources-configuring-jms-in-websphere-application-server)
- [WebSphere MQ messaging provider queue settings](https://www.ibm.com/docs/en/was/8.5.5?topic=settings-websphere-mq-messaging-provider-queue)
- [Creating a WebSphere MQ messaging provider queue connection factory](https://help.hcl-software.com/commerce/7.0.0/com.ibm.commerce.integration.doc/tasks/tcvjmsqueuefactory.html)
- [Configure a JMS queue destination for WebSphere MQ](http://www.setgetweb.com/p/i5/portal/WAS60/Configure_JMS_queue_destinationfor_WebSphere_MQ.html)
