---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Cloud Foundry 中配置机密信息
translated: true
type: note
---

Question: 如何在 Cloud Foundry 中配置 secrets？

Answer: 

在 **Cloud Foundry** 中，并非每个部署都包含像 Vault、AWS Secrets Manager 或 CredHub 这样的内置专用 "secrets manager"（CredHub 主要存在于 Tanzu Application Service / PAS 等环境中）。然而，有几种常见且官方推荐的方法可以向应用提供 secrets（API keys、passwords、tokens、certificates 等）。

### 推荐方法 (2025–2026 最佳实践)

1. **User-Provided Service Instances (简单 secrets 的最常用且推荐的方法)**  
   这是官方首选的交付 credentials/secrets 的方式，而不是使用纯文本的 environment variables。

   - Secrets 出现在 `VCAP_SERVICES` (JSON 结构) 中  
   - 对于大多数角色和许多日志，Credentials 在 `cf env` 输出中会被 **redacted** (掩码处理)  
   - Apps 使用与 marketplace services 相同的 binding 机制  
   - 适用于每个 Cloud Foundry foundation

   **创建一个带有 secrets 的 user-provided service：**

   ```bash
   # 非交互模式 (最常用)
   cf cups my-secrets-service \
     -p '{"api-key":"sk_live_abc123xyz","db-password":"verySecret2026!","external-token":"ghp_xxxxxxxxxxxxxxxx"}'
   ```

   **交互模式 (会提示输入 keys)：**

   ```bash
   cf cups my-secrets-service -p api-key,db-password,external-token
   ```

   **绑定到你的 app 并 restage：**

   ```bash
   cf bind-service my-app my-secrets-service
   cf restage my-app
   ```

   **你的 app 如何读取 secrets** (大多数语言的示例)：

   ```json
   // VCAP_SERVICES 将包含类似以下内容：
   {
     "user-provided": [
       {
         "name": "my-secrets-service",
         "credentials": {
           "api-key": "sk_live_abc123xyz",
           "db-password": "verySecret2026!",
           "external-token": "ghp_xxxxxxxxxxxxxxxx"
         }
       }
     ]
   }
   ```

   使用诸如 `cfenv` (Node.js)、`cloudfoundry-client` (Java)、`vcap` helpers (Python) 等 libraries。

2. **避免使用：cf set-env (纯文本用户端环境变量)**  
   ```bash
   cf set-env my-app DATABASE_PASSWORD "verySecret2026!"
   cf restage my-app
   ```

   **为什么 secrets 要避免这种方式？**  
   - 在 `cf env` 输出中可见  
   - 在许多情况下会出现在 Cloud Controller logs 中  
   - 对大多数用户角色不会进行掩码处理  
   官方文档明确指出：  
   > "不要将用户提供的环境变量用于凭据等安全敏感信息。请改用用户提供的服务实例。"

3. **高级 / 企业级选项 (当你的平台可用时)**

   - **CredHub + CredHub Service Broker** (在 VMware Tanzu / PAS 中常见)  
     将 secrets 集中存储在 CredHub → 通过 service broker 绑定 → app 获取最新的 credentials。

   - **HashiCorp Vault + Vault Buildpack / Sidecar**  
     在开源 Cloud Foundry 设置中非常流行。

   - **Conjur / CyberArk Conjur Service Broker**  
     基于策略的 secret 检索。

   - **Spring Cloud Vault / Spring Cloud Config + CredHub** (Java/Spring Boot apps)

   请咨询你的平台团队，了解是否集成了 CredHub、Vault、Conjur 或其他 secret store。

### 快速总结表

| Method                        | Security Level | Redacted in `cf env`? | Recommended? | Use case                              |
|-------------------------------|----------------|-----------------------|--------------|---------------------------------------|
| `cf set-env`                  | Low            | No                    | No           | 仅限非敏感配置                          |
| User-Provided Service (`cups`)| Medium         | Yes (大多数角色)       | **Yes**      | 标准 CF 中的大多数 secrets             |
| CredHub / Vault / Conjur      | High           | Yes + rotation        | Yes (如果可用) | 企业级、secret rotation、审计          |

**对于大多数 Cloud Foundry 用户，2026 年的最佳默认选择 →** 使用 **user-provided services** (`cf cups`)。

References:  

- [User-provided service instances](https://docs.cloudfoundry.org/devguide/services/user-provided.html)
- [Cloud Foundry environment variables – security guidance](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html)
- [Delivering service credentials to an app](https://docs.cloudfoundry.org/devguide/services/application-binding.html)
- [Cloud Foundry security concepts](https://docs.cloudfoundry.org/concepts/security.html)