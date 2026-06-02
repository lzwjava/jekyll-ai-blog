---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Role-Based Access Control in Jenkins
translated: false
type: note
---

### Role-Based Access Control (RBAC) in Enterprise Jenkins (CloudBees CI)

Enterprise Jenkins, powered by CloudBees CI, uses the CloudBees Role-Based Access Control (RBAC) plugin to implement fine-grained, role-based permissions. This allows administrators to define custom roles, assign them to users or groups, and control access at global, folder, or job levels. It integrates with the Folders plugin for team-based isolation and supports external identity providers like LDAP or Active Directory for group management. Permissions are aggregated from all roles assigned to a user's groups, and they can propagate to child objects (e.g., subfolders) unless pinned or filtered.

RBAC replaces or enhances Jenkins' built-in matrix-based authorization, enabling delegation of administration without full system access. It's configured under **Manage Jenkins > Manage Security > Authorization**, where you select the "Role-based matrix authorization strategy."

#### Key Permissions and Access Rights

Permissions define atomic actions users can perform on Jenkins objects (e.g., jobs, folders, agents, views). Enterprise Jenkins includes core Jenkins permissions plus plugin-extended ones. Permissions are hierarchical—some imply others (e.g., `Job/Configure` implies `Job/Read`).

Here's a table of common permission categories and examples, focusing on build/read as mentioned:

| Category          | Examples of Permissions                                                                 | Description |
|-------------------|-----------------------------------------------------------------------------------------|-------------|
| **Read/Read-Only** | - `Overall/Read`<br>- `Job/Read`<br>- `View/Read`<br>- `Agent/Read`                     | Grants view access to configurations, builds, logs, and artifacts without modification. Useful for auditors or viewers. Extended Read Permission plugin adds granular read controls (e.g., view workspace without build rights). |
| **Build/Execute** | - `Job/Build`<br>- `Job/Cancel`<br>- `Job/Workspace`<br>- `Job/Read (for artifacts)`   | Allows starting, stopping, or accessing build outputs. Can be scoped to specific jobs/folders. |
| **Configure/Modify** | - `Job/Configure`<br>- `Job/Create`<br>- `Job/Delete`<br>- `Folder/Configure`            | Enables editing job parameters, adding triggers, or managing child items. |
| **Administrative** | - `Overall/Administer`<br>- `Overall/Configure`<br>- `Group/Manage`<br>- `Role/View`     | Full system control or delegated tasks like managing roles/groups. `Overall/Administer` is the super-user permission. |
| **Other**         | - `SCM/Tag`<br>- `Credentials/View`<br>- `Agent/Launch`<br>- `RunScripts`                | SCM operations, credential access, node management, or script execution. Negation (e.g., `-Job/Build`) can restrict inherited rights. |

Access rights are controlled at multiple scopes:

- **Global**: Applies to the entire instance (e.g., via root-level groups).
- **Object-Specific**: Overridden on jobs, folders, or agents (e.g., a team can only build in their folder).
- **Propagation**: Roles auto-inherit to children unless "pinned" (local override) or filtered (e.g., hide a project from a role).
- **Implications**: Certain permissions auto-grant subordinates (configurable in recent versions for security).

Admins can filter roles to prevent propagation (e.g., via **Roles > Filter** on a job) or use non-filterable roles for enforced global access.

#### Managing User Roles

Roles are predefined sets of permissions:

1. Go to **Manage Jenkins > Manage Roles**.
2. Click **Add Role** and name it (e.g., "Developer").
3. Assign permissions by checking boxes (use "Check all" or "Clear all" for bulk). System roles like "anonymous" (for unauthenticated users) and "authenticated" (logged-in users) are pre-built and can't be deleted.
4. Save. Roles can be marked as "non-filterable" to always apply globally.

Users inherit permissions from roles assigned to their groups—no direct user-role assignment; it's group-based for scalability.

#### Assigning Roles to Groups and Users

Groups bundle users and roles, allowing easy delegation:

1. On an object (e.g., root, folder, or job), go to **Groups > New Group**.
2. Enter a group name (e.g., "DevTeam").
3. Assign roles by checking them (propagates to children by default; uncheck to pin locally).
4. Add members (see below).
5. Save.

Groups support nesting (e.g., subgroups) and external integration (e.g., LDAP groups).

#### How Admins Add a User to a Group

Admins with `Group/Manage` permission can edit memberships:

1. Navigate to the group's configuration (e.g., **Groups** on the root or object).
2. In the "Members" section, click **Add user** (or **Add group** for external/nested).
3. Enter the user ID (e.g., username from Jenkins' user database, LDAP DN, or external group name). Use `/whoAmI` to verify IDs.
4. Click **Add** and save. Confirm removal with a prompt if needed.
5. For bulk/automation:
   - Use CLI: `java -jar jenkins-cli.jar group-membership <object-path> <group-name> <user-id>` (lists/sets members).
   - REST API: POST to `/rbac/api/v1/groups/<group>/members` with JSON payload.

Avoid circular group memberships to prevent loops. For external realms (e.g., Active Directory), configure the security realm first under **Manage Security > Security Realm**.

This setup ensures secure, scalable control—e.g., devs get `Job/Build` + `Job/Read` in their folder, while admins handle everything.

[Restrict access and delegate administration with Role-Based Access Control](https://docs.cloudbees.com/docs/cloudbees-ci/latest/secure/rbac)
