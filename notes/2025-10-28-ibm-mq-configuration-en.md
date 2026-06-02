---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: IBM MQ WebSphere Application Server Configuration
translated: false
type: note
---

### Prerequisites

Before configuring IBM MQ (formerly WebSphere MQ) in IBM WebSphere Application Server (WAS), ensure the following:

- IBM MQ is installed on a dedicated server (or the same as WAS for local bindings mode).
- A queue manager is created in IBM MQ (e.g., using `crtmqm QMNAME`).
- Required queues are created in the queue manager (e.g., using MQ Explorer or `runmqsc`).
- IBM MQ client libraries (JAR files like `com.ibm.mq.allclient.jar`, `com.ibm.mqjms.jar`) are available. If WAS is remote from MQ, install the IBM MQ client on the WAS machine.
- Add the WAS process user to the `mqm` group for permissions.
- For non-root users on Unix-like systems, use `setmqaut` to grant permissions.

### Step-by-Step Configuration

The configuration involves setting up the JMS provider, connection factories, and destinations in the WAS Administrative Console. This assumes a distributed (client) mode connection over TCP/IP; adjust for bindings mode if local.

1. **Access the WAS Administrative Console**:
   - Start the WAS server.
   - Open a browser and navigate to `https://localhost:9043/ibm/console` (replace with your host/port).
   - Log in with admin credentials.

2. **Configure the IBM MQ JMS Provider**:
   - Go to **Resources > JMS > Providers**.
   - Click **New**.
   - Select **WebSphere MQ messaging provider**.
   - Fill in the details:
     - **Name**: e.g., `MQProvider`.
     - **Description**: Optional.
     - **Class path**: Path to MQ JAR files (e.g., `/opt/mqm/java/lib/*` or copy to `<WAS_HOME>/lib/ext`).
     - **Native library path**: Required for bindings mode (path to MQ libraries, e.g., `/opt/mqm/lib64`).
     - **External initial context factory name**: `com.ibm.mq.jms.context.WMQInitialContextFactory` (for client mode).
     - **External context provider URL**: e.g., `host:1414/CHANNEL` (host = MQ server IP, 1414 = default port, CHANNEL = e.g., `SYSTEM.DEF.SVRCONN`).
   - Save the configuration.

3. **Create a Queue Connection Factory**:
   - Go to **Resources > JMS > Queue connection factories** (scope to your server or cell).
   - Click **New**.
   - Select the provider created in Step 2.
   - Fill in:
     - **Name**: e.g., `MQQueueCF`.
     - **JNDI name**: e.g., `jms/MQQueueCF`.
     - **Queue manager**: Your MQ queue manager name (e.g., `QM1`).
     - **Host**: MQ server hostname or IP.
     - **Port**: 1414 (default).
     - **Channel**: e.g., `SYSTEM.DEF.SVRCONN`.
     - **Transport type**: `CLIENT` (for TCP/IP) or `BINDINGS` (local).
     - **Security credentials**: User ID and password if required.
   - Optional advanced properties: Set connection pool sizes (e.g., max connections based on your load).
   - Save.

4. **Create Queue Destinations**:
   - Go to **Resources > JMS > Queues**.
   - Click **New**.
   - Select the provider.
   - For each queue:
     - **Name**: e.g., `MyQueue`.
     - **JNDI name**: e.g., `jms/MyQueue`.
     - **Queue name**: Exact queue name in MQ (e.g., `MY.LOCAL.QUEUE`).
     - **Queue manager**: Same as above.
     - **Target client type**: `MQ` or `JMS`.
   - Save. Repeat for topics if using pub/sub.

5. **(Optional) Configure WebSphere MQ Server for Bindings Mode**:
   - If using local bindings, go to **Servers > Server Types > WebSphere MQ servers**.
   - Click **New**.
   - Set **Name**, **Queue manager name**.
   - Specify **MQ installations** (path to MQ install).
   - Save and restart the server.

6. **Configure JCA Resource Adapter (for MDBs)**:
   - Go to **Resources > Resource Adapters > J2C connection factories**.
   - If using the built-in MQ RA, ensure it's deployed (WAS includes `wmq.jmsra.rar`).
   - Set properties like max connections (e.g., 10-50 based on load).

7. **Test the Configuration**:
   - Deploy a sample JMS application or use the WAS JMS sample.
   - Check logs for errors (e.g., connection refused on port 1414).
   - Verify in MQ: Use MQ Explorer to monitor queue depths and channels.

8. **Security and Advanced Setup**:
   - Enable SSL: Configure keystores in WAS and MQ (channel with `SSLCIPH`).
   - Set authentication: Use MQ user groups or alternate user IDs.
   - For clusters: Synchronize configurations across nodes.

### Troubleshooting Tips

- **ClassNotFoundException**: Ensure MQ JARs are in the classpath.
- **Connection failures**: Check firewall on port 1414, channel status (`DISPLAY CHSTATUS(*)` in runmqsc).
- **Bindings mode issues**: Verify native libs and user in `mqm` group.
- Restart WAS after changes.

For version-specific details (e.g., WAS 9.x with MQ 9.x), refer to official IBM docs.

[Using WebSphere Application Server with IBM MQ](https://www.ibm.com/docs/en/ibm-mq/9.2.x?topic=together-using-websphere-application-server-mq)
[Configuring WebSphere Application Server for use with IBM MQ](https://help.hcl-software.com/commerce/9.0.0/integration/tasks/tcvconfigure_was_for_mq.html)
[Creating a WebSphere MQ server definition](https://www.ibm.com/docs/SSAW57_8.5.5/com.ibm.websphere.nd.multiplatform.doc/ae/tjfp0004_.html)
