---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring JMS Resources in WebSphere
translated: false
type: note
---

### Prerequisites
- Ensure you have administrative access to the IBM WebSphere Application Server (WAS) Integrated Solutions Console (admin console).
- The server should be running, and you need to decide on the scope (e.g., cell, node, server) for the resources.
- This guide focuses on the Default Messaging Provider (using Service Integration Bus or SIBus), which is the built-in JMS provider in WAS. If using WebSphere MQ, additional configuration for the MQ provider is required.
- Restart the server after major changes if prompted.

### Step 1: Create a Service Integration Bus
The service integration bus acts as the messaging backbone for JMS resources.

1. Log in to the WebSphere Integrated Solutions Console.
2. Navigate to **Service integration > Buses**.
3. Click **New**.
4. Enter a unique bus name (e.g., `MyJMSBus`).
5. Clear the **Bus security** option unless required.
6. Click **Next**, then **Finish** to create the bus.

### Step 2: Add the Server as a Bus Member
This enables the server to host messaging engines on the bus.

1. Select the bus you created (e.g., `MyJMSBus`).
2. Under **Additional properties**, click **Bus members**.
3. Click **Add**.
4. In the **Add a New Bus Member** wizard:
   - Select **Messaging engine** as the bus member type.
   - Choose your server (e.g., `server1`) from the list.
   - For the message store, select **File store** (default for non-clustered) or **Data store** for database persistence, and configure properties if needed.
5. Click **Next**, then **Finish**.
6. Restart the WebSphere Application Server to activate the bus member.

### Step 3: Create a JMS Connection Factory
A connection factory is required to connect JMS clients to the provider.

1. Navigate to **Resources > JMS > Connection factories**.
2. Select the appropriate scope (e.g., Server scope for `server1`) and click **New**.
3. Select **Default messaging provider** and click **OK**.
4. Enter details:
   - **Name**: e.g., `MyJMSConnectionFactory`.
   - **JNDI name**: e.g., `jms/MyConnectionFactory`.
   - **Bus name**: Select `MyJMSBus` from the drop-down.
   - Leave other defaults (e.g., Provider endpoints as auto-detected).
5. Click **Apply**, then **Save** to the master configuration.

### Step 4: Create a JMS Queue
This defines the queue destination for point-to-point messaging.

1. Navigate to **Resources > JMS > Queues**.
2. Select the appropriate scope and click **New**.
3. Select **Default messaging provider** and click **OK**.
4. Enter details:
   - **Name**: e.g., `MyJMSQueue`.
   - **JNDI name**: e.g., `jms/MyQueue`.
   - **Bus name**: Select `MyJMSBus`.
   - **Queue name**: Select **Create Service Integration Bus Destination**, enter a unique identifier (e.g., `MyQueueDestination`), and select the bus member created earlier.
   - **Base queue name**: e.g., `$MyJMSBus:MyQueueDestination` (auto-generated).
5. Configure additional properties if needed (e.g., delivery mode, expiry).
6. Click **Apply**, then **Save** to the master configuration.

### Step 5: (Optional) Create Activation Specifications for Message-Driven Beans (MDBs)
If using MDBs to consume from the queue, configure activation specs.

1. Navigate to **Resources > JMS > Activation specifications**.
2. Select the appropriate scope and click **New**.
3. Select **Default messaging provider** and click **OK**.
4. Enter details:
   - **Name**: e.g., `MyActivationSpec`.
   - **JNDI name**: e.g., `jms/activation/MyActivationSpec`.
   - **Bus name**: Select `MyJMSBus`.
   - **Destination type**: Queue.
   - **Destination**: Enter the JNDI name of the queue (e.g., `jms/MyQueue`).
5. Click **Apply**, then **Save** to the master configuration.

### Verification and Testing
- After saving, sync nodes if in a clustered environment.
- Restart the server.
- Use a JMS client application to test sending/receiving messages via the JNDI names.
- Monitor via **Service integration > Buses > [Your Bus] > Bus members > [Your Member] > Messaging engines**.

For advanced configurations (e.g., security, clustering), refer to IBM documentation.

[Configuring IBM WebSphere Application Server for Decision Server](https://docs.redhat.com/en/documentation/red_hat_decision_manager/7.4/html/installing_and_configuring_decision_server_on_ibm_websphere_application_server/was-configure-proc)
[Managing messaging with the default messaging provider](https://www.ibm.com/docs/en/was/9.0.5?topic=resources-managing-messaging-default-messaging-provider)
