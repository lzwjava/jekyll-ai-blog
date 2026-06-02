---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Liberty Vault Integration Options
translated: false
type: note
---

**Question:** How to integrate HashiCorp Vault with WebSphere Liberty Profile? Does WLP have a vault-1.0 feature? In JDBC config, can I use something like ${vault:namespace#db_password}?

**Answer:**

No, **WebSphere Liberty Profile (WLP)** does not have a built-in `vault-1.0` feature or any native `${vault:...}` variable substitution syntax for directly fetching secrets from HashiCorp Vault at configuration time (similar to what some other platforms offer).

Liberty (and Open Liberty) supports variable substitution in `server.xml` (e.g. `${db_password}`), but the values must come from:

- `bootstrap.properties`
- `server.env`
- Environment variables
- JVM system properties
- Files in specific directories (in newer versions, especially when running in containers)

There is **no direct Vault resolver** built into Liberty like `${vault:secret/path#key}`.

### Common Practical Approaches to Integrate HashiCorp Vault

1. **Vault Agent (Sidecar) + File-Based Variables (Recommended for containers/Kubernetes)**
   Use Vault Agent to render secrets as files. Liberty can then read them as config variables from the filesystem.

   - Run Vault Agent in sidecar mode (or as init container) to authenticate (e.g. via Kubernetes auth, AppRole, etc.) and write secrets to files like:

     ```
     /config/variables/db_password
     /config/variables/db_username
     ```

   - Liberty automatically treats files under `/config/variables/` (or similar configured path) as variables.
   - In `server.xml`:

     ```xml
     <dataSource id="DefaultDataSource" jndiName="jdbc/myapp">
         <jdbcDriver libraryRef="DerbyLib"/>
         <properties.derby.embedded databaseName="memory:db" user="${db_username}" password="${db_password}"/>
     </dataSource>
     ```

   - This is explicitly supported/documented in Open Liberty (and works the same in WebSphere Liberty) when using Vault Agent to populate files.

2. **Vault Agent Templating → Environment Variables**
   Vault Agent can template secrets into environment variables using its supervisor mode or `envconsul`-like behavior.

   - Then reference them in Liberty via `${env.VAULT_DB_PASSWORD}` (if using env var substitution) or map them in `bootstrap.properties`.

3. **AppRole + Custom Code in Application**
   - For application-level secrets (not server.xml config), your Java code can authenticate to Vault using AppRole and fetch secrets at runtime (e.g. for JDBC connection pooling callbacks or custom config).
   - This doesn't help with Liberty's built-in `<dataSource>` password fields.

4. **External Secrets Operator (Kubernetes only)**
   If running on Kubernetes, use External Secrets Operator to sync Vault secrets → Kubernetes Secrets → environment variables or mounted files → Liberty variables.

5. **bootstrap.properties + External Script/Init**
   - At container startup, run a script that authenticates to Vault (using AppRole or token) and writes values to `bootstrap.properties` or `server.env`.
   - Liberty reads these at startup.

### Summary Table of Options

| Approach                        | Works in server.xml? | Native Vault syntax? | Best for              | Complexity |
|---------------------------------|----------------------|----------------------|-----------------------|------------|
| Vault Agent → files             | Yes                  | No                   | Containers / K8s      | Medium     |
| Vault Agent → env vars          | Yes (via ${env.})    | No                   | Containers            | Medium     |
| Application code fetches secret | No (config level)    | No                   | App runtime secrets   | Low-Medium |
| Custom user feature             | Possible             | No                   | Very custom needs     | High       |
| Direct ${vault:...}             | No                   | No                   | —                     | —          |

The file-based approach with Vault Agent is the most common and officially mentioned pattern for Liberty/Open Liberty environments.

**References:**

- [Open Liberty blog on Kubernetes secrets + Vault Agent example](https://openliberty.io/blog/2021/10/29/kube-secrets-210011.html)
- [HashiCorp Discuss thread on WebSphere + Vault](https://discuss.hashicorp.com/t/websphere-integration-with-vault/55528)
- [Liberty variable substitution documentation](https://www.ibm.com/docs/en/was-liberty/base?topic=overview-liberty-variables)
