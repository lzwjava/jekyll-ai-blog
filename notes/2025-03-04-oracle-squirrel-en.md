---
audio: false
generated: true
lang: en
layout: post
title: Add the Oracle JDBC Driver to Squirrel SQL Client
translated: false
type: note
---

To add the Oracle JDBC driver to Squirrel SQL Client, follow these detailed steps. This process involves configuring the driver and setting up a connection alias for your Oracle database.

### Step 1: Locate the Required File

You need the Oracle JDBC driver file, specifically `ojdbc.jar`. This file contains the necessary classes to enable Squirrel SQL Client to connect to an Oracle database. Ensure you have downloaded this file (e.g., from the Oracle website or your database administrator) and know its location on your system.

### Step 2: Launch Squirrel SQL Client

Open the Squirrel SQL Client application on your computer.

### Step 3: Access the Drivers Tab

On the left-hand side of the Squirrel SQL Client interface, locate and click on the **Drivers** tab. This section allows you to manage the JDBC drivers available to the application.

### Step 4: Add a New Driver

- In the Drivers tab, click the **"+"** button to open the "Add Driver" dialog box.

### Step 5: Name the Driver

- In the "Name" field of the "Add Driver" dialog, enter **Oracle Thin Driver**. This is a descriptive name to identify the Oracle driver within Squirrel SQL Client.

### Step 6: Add the `ojdbc.jar` File

- Switch to the **Extra Class Path** tab within the "Add Driver" dialog.
- Click the **Add** button.
- Navigate to the location of the `ojdbc.jar` file on your system, select it, and confirm to add it to the driver’s classpath.

### Step 7: Specify the Java Driver Class

- In the "Class Name" field, enter the Java driver class: **oracle.jdbc.OracleDriver**. This tells Squirrel SQL Client which class to use from the `ojdbc.jar` file to handle Oracle database connections.

### Step 8: Provide an Example URL

- Optionally, you can specify an example URL format for connecting to an Oracle database:
  - **For connecting via SID**: `jdbc:oracle:thin:@HOST[:PORT]:DB`
  - **For connecting via service name**: `jdbc:oracle:thin:@//HOST[:PORT]/DB`
- Replace `HOST`, `PORT`, and `DB` with actual values when setting up a connection later (in the alias configuration).

### Step 9: Save the Driver Configuration

- Click **OK** to save the driver settings and close the "Add Driver" dialog. The "Oracle Thin Driver" should now appear in the Drivers tab with a green checkmark, indicating it’s properly configured.

### Step 10: Create an Alias for Your Database

- Switch to the **Aliases** tab on the left-hand side of Squirrel SQL Client.
- Click the **"+"** button to open the "Add Alias" dialog box.

### Step 11: Configure the Alias

- In the "Add Alias" dialog:
  - **Name**: Enter a name for this connection (e.g., "My Oracle DB").
  - **Driver**: Select **Oracle Thin Driver** from the dropdown menu.
  - **URL**: Enter the connection URL for your specific Oracle database:
    - Via SID: `jdbc:oracle:thin:@HOST[:PORT]:DB`
    - Via service name: `jdbc:oracle:thin:@//HOST[:PORT]/DB`
    - Replace `HOST` (e.g., localhost or IP address), `PORT` (default is 1521), and `DB` (SID or service name) with your database’s details.
  - **Username**: Enter the database username.
  - **Password**: Enter the database password.

### Step 12: Test the Connection

- Click the **Test** button in the "Add Alias" dialog to verify that Squirrel SQL Client can connect to your Oracle database using the provided details. If successful, you’ll see a confirmation message.

### Step 13: Save the Alias

- If the test connection succeeds, click **OK** to save the alias. The new alias will now appear in the Aliases tab.

### Step 14: Connect to the Database

- In the Aliases tab, select your newly created alias (e.g., "My Oracle DB").
- Click the **Connect** button to establish a connection to your Oracle database. Once connected, you can start querying your database using Squirrel SQL Client.

### Summary of Key Information

- **Required File**: `ojdbc.jar`
- **Java Driver Class**: `oracle.jdbc.OracleDriver`
- **URL Formats**:
  - SID: `jdbc:oracle:thin:@HOST[:PORT]:DB`
  - Service Name: `jdbc:oracle:thin:@//HOST[:PORT]/DB`

By following these steps, you’ll have successfully added the Oracle JDBC driver to Squirrel SQL Client and configured a connection to your Oracle database. Ensure all details (file path, URL, credentials) are accurate to avoid connection issues.
