---
audio: false
generated: true
image: false
lang: en
layout: post
title: Control-M Windows Installation Process
translated: false
type: note
---

Question: What is the Control-M v9.0.21 installation process on Windows, and does it require you to input a web host and port?

Answer:

## Control-M v9.0.21 (v921) Installation on Windows — Full Overview

Control-M v9.0.21 is a BMC workload automation product. On Windows, it can be installed as a **Full Installation** (all components in one), or component-by-component (Enterprise Manager, Server, Agent separately). Here is the comprehensive breakdown:

---

### 1. Installation Options

Control-M v9.0.21 supports a Full Installation that installs all components including Application Plug-ins and add-ons on Windows via an interactive or automatic installation. You can install with the default settings, or choose the custom installation to select the database server, database names, usernames, hostnames, and port settings.

The two installation modes are:

- **Interactive Install** — GUI-guided wizard, step by step on screen
- **Automatic (Silent) Install** — uses a pre-generated XML parameter file for unattended installation

---

### 2. Pre-requisites Before Running Setup.exe

Before starting the installation on Windows, you must:

- Verify that your operating system and database software is compatible with the current version of Control-M (per Control-M Full Installation System Requirements).
- Verify that you have met Java requirements (Control-M External Java Installation).
- Verify that the target computer is clean and does not have any previous Control-M version installed.
- Verify that you have downloaded the correct installation files.
- If installing in a cluster environment, complete the Control-M Cluster Configuration steps first.

---

### 3. Running the Windows Installer (Setup.exe)

To begin installation:

1. Log in to the computer with a user ID that has Administrator permissions.
2. From a command prompt window, run: `<source_path>\Setup.exe`
3. Select the **Control-M 9.0.21.100 - Full Installation** option and continue with the on-screen instructions until installation is complete.

---

### 4. Does It Ask for Web Host and Port? YES — During Custom Installation

Yes, the installer **does** prompt for hostnames and ports when you choose the **Custom** installation path (as opposed to Default).

**Web Server Port:**
During the Self Service and Web component setup, you must verify that either the default web server port **18080** or another configured port you want to use is open. At the end of installation, you can find the URL for accessing the Control-M web component by opening the Control-M Configuration Manager, selecting Web Server under All Components, and viewing the Web Server URLs.

**EM and Server Communication Ports:**
Key ports that are required for firewall rules and bidirectional communication include:

- Control-M/EM TCP/IP Port: **2370**
- Configuration Agent Port: **2369**
- Agent-to-Server Port: **7005**
- High Availability Port: **2368**

**Database Port:**
If you are installing Control-M/Server with a PostgreSQL database on the same computer where Control-M/EM with a PostgreSQL database was already installed, you must use a **different port** for the second database instance.

**Zookeeper/Kafka Ports (if co-located):**
If you are installing Control-M/EM and Control-M/Server on the same computer, you must configure the Zookeeper and Kafka services to use different ports on Control-M/EM and on the additional Control-M/Server instances.

---

### 5. Automatic (Silent) Installation

For the Automatic Install, you proceed through the wizard until the Summary window, click **Generate** to create an XML parameter file, then run:

```
<source_path>\Setup.exe -silent <xml_path>\<filename.xml>
```

To encrypt a password in the installation, run:

```
<source_path>\Setup.exe -encrypt <password>
```

Installation logs are saved at:

```
<installFolder>\BMCINSTALL\log\BMC_Control-M_Install_<date-time>.log
```

Note: The generated XML parameter file is relevant only for computers with the same Agent instance name. A separate file must be created or manually modified for each computer with a different name.

---

### 6. Control-M/Agent on Windows (Separate Component)

To install the Control-M/Agent on Windows:

1. Log in with Administrator permissions.
2. Copy installation files to the home directory.
3. From a command prompt, run `<source_path>\setup.exe`.
4. Follow the on-screen instructions (interactive) or generate an XML file for automatic install.
The agent installation log is at: `<installFolder>\BMCINSTALL\log\BMC_Control-M_AGENT_Install<date-time>.log`

---

### Summary Table

| Parameter | Default Value | Notes |
| --- | --- | --- |
| Web Server Port | 18080 | Configurable during custom install |
| EM TCP/IP Port | 2370 | Required open in firewall |
| Config Agent Port | 2369 | Required open in firewall |
| Agent-to-Server Port | 7005 | Required open in firewall |
| HA Port | 2368 | For high-availability setup |
| PostgreSQL Port | Default (5432) | Must use different port if EM+Server on same host |

---

### Key Takeaway

Yes — when installing Control-M v9.0.21 on Windows, the installer **does require you to confirm or input the web host and port settings** if you choose the Custom installation option. The Default option uses pre-set values (e.g., port 18080 for the web server). The main executable is `Setup.exe`, launched from a command prompt with Administrator rights.

References:

- [Control-M Full Installation on Windows (BMC Documentation)](https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Installing_Control-M_on_Windows.htm)
- [Introduction to Control-M Installation v9.0.21](https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Introduction_to_Control-M_Installation.htm)
- [Control-M/Agent Installation on Windows](https://controlm.wisconsin.gov/help/CTMHelp/en-US/Documentation/Installing_Control-M_Agent_on_Windows.htm)
- [Control-M/Server Installation](https://documents.bmc.com/supportu/9.0.21/en-US/Documentation/Control-M_Server_installation.htm)
- [Control-M System Configuration / Ports](https://controlm.wisconsin.gov/help/CTMHelp/en-US/Documentation/System_Configuration.htm)
- [Control-M Self Service Installation (Web Port)](https://controlm.wisconsin.gov/help/CTMHelp/en-US/Documentation/Control-M_Self_Service_installation.htm)
