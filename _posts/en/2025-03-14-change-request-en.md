---
audio: false
generated: true
lang: en
layout: post
title: How to Use Change Request
translated: false
type: note
---

To add a group to a Change Request in ServiceNow, you need to assign a group to the **Assignment group** field within the Change Request form. Below is a detailed, step-by-step guide to help you through the process.

---

### Step-by-Step Guide

1. **Navigate to the Change Request Module**
   - Log in to your ServiceNow instance.
   - In the left-hand navigation pane, type "Change" in the filter navigator.
   - Select **Change > All** to view the list of all Change Requests.

2. **Open the Change Request**
   - Locate the specific Change Request you want to assign a group to. You can use the search bar or filters (e.g., by Change Request number or short description).
   - Click on the Change Request to open its form.

3. **Locate the Assignment Group Field**
   - On the Change Request form, find the **Assignment group** field. This is typically located in the "Planning" or "Assignment" section of the form, depending on your instance’s configuration.

4. **Select the Group**
   - Click the magnifying glass icon (reference lookup) next to the **Assignment group** field.
   - A pop-up window will display a list of available groups.
   - Type the name of the group in the search box to filter the list, then select the desired group by clicking on it.
   - If you know the exact group name, you can also start typing it directly in the field, and ServiceNow will suggest matching groups.

5. **Save the Changes**
   - After selecting the group, click **Update** or **Save** (usually found at the top or bottom of the form) to save your changes to the Change Request.

---

### Important Considerations

- **Group Type**
   Ensure the group you want to assign is configured with an appropriate group type (e.g., "Change" or "ITIL"). Some ServiceNow instances restrict the groups available in the **Assignment group** field based on their type. To check or update a group’s type:
  - Go to **User Administration > Groups**, find the group, and verify its "Type" field.

- **Permissions**
   You need sufficient permissions to assign groups to a Change Request. Typically, roles like `change_manager` or equivalent are required. If you can’t assign a group, contact your ServiceNow administrator to confirm your access.

- **Reference Qualifiers**
   The **Assignment group** field might have filters (reference qualifiers) that limit which groups appear. If the group you want isn’t listed, it could be due to a configuration in the field’s dictionary settings. An administrator can check this under **System Definition > Dictionary**.

- **Automated Assignment (Optional)**
   While this guide covers manual assignment, note that groups can also be assigned automatically using workflows or assignment rules configured by your organization.

---

### Troubleshooting

- **Group Not Appearing?**
  - Verify the group exists in **User Administration > Groups**.
  - Check its group type and any reference qualifiers on the **Assignment group** field.
- **No Permission to Save?**
  - Ensure you have the necessary role to edit Change Requests.

By following these steps and considering the above points, you should be able to successfully add a group to a Change Request in ServiceNow. If you encounter issues, consult your ServiceNow administrator for assistance tailored to your instance’s setup.

---

To address your issue where your Change Request in ServiceNow appears empty—with sections like related links, planning, affected CIs, approvers, and the change request list all showing no data—you need to populate these areas with the necessary information. It seems that while the Change Request form itself exists, its related lists and fields lack entries. Below is a step-by-step guide to help you fill in the required details and related lists.

---

### Step 1: Verify and Fill in Basic Information

Even though your Change Request exists, it may lack essential details. Start by ensuring the foundational fields are completed:

- **Open the Change Request**: Navigate to the specific Change Request in ServiceNow (e.g., via the Change > All module or by searching its number).
- **Check Required Fields**:
  - **Short Description**: Add a brief summary of the change (e.g., "Upgrade server memory").
  - **Description**: Provide a detailed explanation of what the change entails.
  - **Requester**: Specify who is requesting the change (this might default to you if you created it).
  - **Assignment Group**: Assign the team responsible for the change (e.g., "Server Team").
  - **Assigned To**: Optionally, assign a specific individual within the group.
- **Save the Form**: Click **Save** or **Update** to ensure these details are recorded. Some fields may be mandatory (marked with a red asterisk), and saving might not be possible until they’re filled.

---

### Step 2: Complete Planning Details

The "planning" section you mentioned likely refers to fields that define the scope and schedule of the change. Populate these to provide context:

- **Change Type**: Select the type (e.g., Normal, Emergency, Standard).
- **Category**: Choose an appropriate category (e.g., Hardware, Software, Network).
- **Priority**: Set based on urgency and impact (e.g., Low, Medium, High).
- **Risk and Impact**: Assess and enter the potential risk and impact levels.
- **Planned Start and End Dates**: Specify when the change will begin and end.
- **Save Changes**: Ensure these fields are saved to update the Change Request.

---

### Step 3: Add Affected CIs

The "affected CIs" list is empty because no Configuration Items (CIs) have been linked yet. Here’s how to populate it:

- **Locate the Related List**: Scroll to the **Affected CIs** section at the bottom of the form.
- **Add CIs**:
  - Click **Edit** or **New** (depending on your instance’s setup).
  - A selection window will appear, allowing you to search for and select CIs from the Configuration Management Database (CMDB).
  - Choose the relevant CIs (e.g., servers, applications) impacted by the change.
- **Save**: Click **Save** to link these CIs to the Change Request.

---

### Step 4: Manage Approvers

The "approvers" list is empty because no approval records exist yet. Depending on your organization’s process, approvers may be added automatically or manually:

- **Check Approval Process**:
  - Look for a **Request Approval** button or UI action on the form. Clicking this may trigger an approval workflow based on predefined rules (e.g., change type or risk level).
- **Manually Add Approvers** (if needed):
  - Go to the **Approvals** related list.
  - Click **New** to create an approval record.
  - Select the approver (e.g., a manager or Change Advisory Board member) and save.
- **Monitor Status**: Once added, the approvers will need to approve or reject the change.

---

### Step 5: Populate the Change Request List (Child Changes or Tasks)

You mentioned a "change request" list being empty, which might refer to child Change Requests or **Change Tasks**. Here’s how to address this:

- **Change Tasks** (more likely):
  - Scroll to the **Change Tasks** related list.
  - Click **New** to create a task.
  - Fill in details like task description, assignment group, assigned to, and due date.
  - Save the task. Repeat for all required tasks.
- **Child Change Requests** (if applicable):
  - If your organization uses parent-child Change Requests, look for a related list like **Child Changes**.
  - Click **New** to create a linked Change Request and fill in its details.
- **Save Changes**: Ensure all tasks or child requests are saved.

---

### Step 6: Address "Related Links"

You mentioned "related links" being empty. This might be a miscommunication for related lists (like incidents or problems) rather than the UI "Related Links" section. To populate related records:

- **Link Related Records**:
  - Check for related lists like **Related Incidents**, **Related Problems**, or **Caused by Change**.
  - Click **Edit** or **New** in these lists.
  - Search for and link relevant records (e.g., an incident that triggered this change).
- **Save**: Update the form after adding these links.

---

### Step 7: Progress the Change Request

Once the basic information and related lists are populated, move the Change Request forward:

- **Check the State**: Verify the current state (likely "New").
- **Move to Next State**: Use the **State** dropdown or UI actions (e.g., **Assess**, **Authorize**) to advance it. Some fields or lists may only become relevant in later states (e.g., actual dates in "Implement").
- **Follow Workflow**: Your instance’s workflow will guide the process—complete required fields at each stage.

---

### Important Notes

- **Permissions**: Ensure you have the necessary access (e.g., `change_manager` role) to edit these fields and lists. If not, contact your ServiceNow administrator.
- **Custom Configuration**: Your instance might use templates, change models, or automated workflows that pre-populate some data. Check with your admin if fields don’t behave as expected.
- **Visibility**: Some sections might be hidden or locked based on the state or your permissions—advancing the state may reveal more options.

By following these steps, you’ll transform your empty Change Request into a fully populated record ready for processing. If issues persist, provide your ServiceNow administrator with details (e.g., Change Request number) for further investigation.
