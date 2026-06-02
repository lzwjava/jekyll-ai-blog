---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Microsoft Entra ID Access Management Guide
translated: false
type: note
---

Microsoft Entra ID is a cloud-based identity and access management service that helps secure access to resources like applications, data, and devices. It supports authentication (e.g., sign-in methods, MFA), authorization (e.g., role-based access), and integration with Azure services. To get started, you'll need an Azure subscription and appropriate permissions (e.g., Global Administrator role).

## Getting Started

1. **Sign in to the Azure Portal**: Go to [portal.azure.com](https://portal.azure.com) and sign in with your Microsoft account.
2. **Navigate to Microsoft Entra ID**: Search for "Microsoft Entra ID" in the top search bar or find it under "Azure services."
3. **Explore the Dashboard**: Review your tenant overview, including users, groups, and apps. Set up basics like custom domains if needed.
4. **Enable Key Features**:
   - **Authentication**: Configure self-service password reset or multifactor authentication (MFA) under "Authentication methods."
   - **Conditional Access**: Create policies under "Security" > "Conditional Access" to enforce rules based on user, device, or location.

## Managing Users and Groups

- **Add Users**: Go to "Users" > "New user." Enter details like name, username (e.g., <user@yourdomain.com>), and assign roles or licenses.
- **Create Groups**: Under "Groups" > "New group," choose security or Microsoft 365 type, add members, and use for access assignments.
- **Assign Licenses**: In user/group details, go to "Licenses" to assign Entra ID P1/P2 for advanced features like Privileged Identity Management (PIM).
- **Best Practice**: Follow the principle of least privilege—assign minimal permissions and use groups for bulk management.

## Managing Applications

- **Register an App**: Under "App registrations" > "New registration," provide name, redirect URIs, and supported account types (single-tenant, multi-tenant, etc.).
- **Add Enterprise Apps**: For third-party apps, go to "Enterprise applications" > "New application" to browse the gallery or create non-gallery apps.
- **Configure Access**: Assign users/groups to the app under "Users and groups," and set up single sign-on (SSO) via SAML or OAuth.
- **Provision Identities**: Automate user sync to apps under "Provisioning" for just-in-time access.

For hybrid setups (on-premises AD), use Microsoft Entra Connect to sync identities. Monitor usage via logs under "Monitoring" > "Sign-in logs."

# How to Check Access to a Database, Kubernetes (AKS), or Other Resource

Access in Azure is managed via Role-Based Access Control (RBAC), integrated with Entra ID. Users authenticate with Entra credentials, and roles define permissions. To check access, use the Azure portal's IAM (Identity and Access Management) tools. This lists direct assignments, inherited from parent scopes (e.g., subscription), and deny assignments.

## General Steps for Any Azure Resource

1. **Open the Resource**: In the Azure portal, navigate to the resource (e.g., resource group, VM, storage account).
2. **Go to Access Control (IAM)**: Select "Access control (IAM)" from the left menu.
3. **Check Access**:
   - For your own access: Click "Check access" > "View my access" to see assignments at this scope and inherited.
   - For a specific user/group/service principal:
     - Click "Check access" > "Check access."
     - Select "User, group, or service principal."
     - Search by name or email.
     - View the results pane for role assignments (e.g., Owner, Contributor) and effective permissions.
4. **View Eligible Assignments** (if using PIM): Switch to the "Eligible assignments" tab for just-in-time roles.
5. **PowerShell/CLI Alternative**: Use `az role assignment list --assignee <user> --scope <resource-id>` for scripted checks.

Note: This doesn't include child-scope assignments; drill down if needed.

## Checking Access to Azure SQL Database

Azure SQL uses Entra authentication for contained database users (tied to Entra identities, not SQL logins).

1. **Configure Entra Admin (if not set)**: In the SQL server overview > "Microsoft Entra ID" under Settings > "Set admin." Search and select a user/group, then save. This enables Entra auth cluster-wide.
2. **Check Server-Level Access**:
   - In the SQL server pane > "Microsoft Entra ID," view the admin field to see the assigned identity.
   - Query the `master` database: `SELECT name, type_desc FROM sys.database_principals WHERE type IN ('E', 'X');` (E for external users, X for external groups).
3. **Check Database-Level Access**:
   - Connect to the database using SSMS with Entra auth (select "Microsoft Entra - Universal with MFA" in connection dialog).
   - Run `SELECT * FROM sys.database_principals;` or `EXEC sp_helprolemember;` to list users and roles.
4. **Troubleshoot**: If login fails (e.g., error 33134), check Entra Conditional Access policies allow Microsoft Graph API access.

Users get `CONNECT` by default; grant roles like `db_datareader` via T-SQL: `ALTER ROLE db_datareader ADD MEMBER [user@domain.com];`.

## Checking Access to AKS (Kubernetes Cluster)

AKS integrates Entra ID for auth and uses Azure RBAC or Kubernetes RBAC for authorization.

1. **Azure-Level Access (to AKS Resource)**:
   - Follow general steps above on the AKS cluster resource.
   - Common roles: "Azure Kubernetes Service Cluster Admin" for full kubeconfig access; "Reader" for view-only.
2. **Kubernetes API Access**:
   - Authenticate via `az login` (uses Entra token).
   - Get kubeconfig: `az aks get-credentials --resource-group <rg> --name <cluster>`.
   - Check bindings: `kubectl auth can-i <verb> <resource> --as <user@domain.com> -n <namespace>`.
   - List cluster roles: `kubectl get clusterrolebindings | grep <user-or-group>`.
3. **Using Entra Groups**: Assign Kubernetes Roles/Bindings to groups for scalability. Example YAML for a namespace role (apply with `kubectl apply -f file.yaml`):

   ```
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     name: example-binding
     namespace: default
   subjects:
   - kind: Group
     name: finance-group  # Entra group
     apiGroup: rbac.authorization.k8s.io
   roleRef:
     kind: Role
     name: example-role
     apiGroup: rbac.authorization.k8s.io
   ```

4. **Best Practices**: Use least-privilege roles, integrate with PIM for just-in-time elevation, and avoid fixed credentials—use workload identities for pods.

For pods accessing resources (e.g., SQL from AKS), assign managed identities and check via Azure RBAC on those identities.

[Microsoft Entra ID Documentation](https://learn.microsoft.com/en-us/entra/identity/)
[Check Access to a Single Azure Resource](https://learn.microsoft.com/en-us/azure/role-based-access-control/check-access)
[Configure Entra Authentication for Azure SQL](https://learn.microsoft.com/en-us/azure/azure-sql/database/authentication-aad-configure?view=azuresql)
[AKS Identity and Access Best Practices](https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-identity)
