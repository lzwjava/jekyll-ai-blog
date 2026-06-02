---
audio: false
generated: true
image: false
lang: en
layout: post
title: Jenkins RBAC Guide With Role Plugin
translated: false
type: note
---

In Jenkins, **role-based access control (RBAC)** is about defining who can do what, and where. By default Jenkins only has a basic user/administrator model, but with the **Role-Based Strategy plugin** (or similar authorization strategies) you can define fine-grained access.

---

### Core Concepts of RBAC in Jenkins

1. **Global Roles**
   These apply to the entire Jenkins instance. Examples:

   * **Admin**: full control.
   * **Read-only**: can view jobs but not run them.
   * **Developer**: can create and configure jobs.

2. **Project/Job Roles**
   You can grant permissions on a per-job or per-folder basis. For example:

   * User A can build *Project X* but not see *Project Y*.
   * Contractors can trigger builds but cannot change configurations.

3. **Build Permissions**
   Permissions can be split:

   * `Job/Read` (see job definition and build history)
   * `Job/Build` (trigger builds)
   * `Job/Configure` (change pipeline or settings)
   * `Job/Delete` (remove jobs or builds)
   * `Job/Cancel` (abort running builds)

---

### How to Manage Job or Build Access Rights

1. **Install the Role-Based Strategy Plugin**

   * Go to **Manage Jenkins → Plugins → Available Plugins → Role-based Authorization Strategy**.
   * After installation, select it in **Manage Jenkins → Configure Global Security → Authorization**.

2. **Define Roles**

   * Go to **Manage Jenkins → Manage and Assign Roles**.
   * Create global roles (like *admin*, *viewer*, *developer*) and project roles (like *projectX-builder*).
   * Assign each role the needed permissions (`Job/Build`, `Job/Configure`, etc.).

3. **Assign Roles to Users/Groups**

   * Still under **Manage and Assign Roles**, map your Jenkins users (or LDAP groups if integrated) to the roles.
   * For example:

     * Map *alice* → `developer`
     * Map *bob* → `viewer`
     * Map *qa-team* → `projectX-builder`

4. **Use Folders for Better Granularity**

   * Organize jobs into **Folders** (via the *Folders Plugin*).
   * Apply role restrictions at the folder level so only the right team can see/build/modify jobs inside.

---

### Example Scenarios

* **Developers**: Can build and configure their team’s jobs, but cannot touch admin settings.
* **QA Team**: Can only trigger builds (not reconfigure pipelines).
* **External Users**: Can see job status but not modify or trigger builds.

---

👉 In practice: you keep **admins few**, give **developers configure + build access** to their own jobs, and grant **read-only or build-only rights** to others. This ensures consistency, reduces mistakes, and keeps sensitive jobs protected.

---

Do you want me to show you a **step-by-step example config** (with roles, permissions, and job mapping) that matches a typical enterprise setup?
