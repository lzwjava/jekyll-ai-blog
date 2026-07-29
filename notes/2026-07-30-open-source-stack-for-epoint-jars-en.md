---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-source Stack for Epoint JARs
translated: false
type: note
---

Question: What open-source Java + frontend stack can replace Epoint internal JAR frameworks?

Answer:

I assume you mean 国泰新点软件股份有限公司 (Epoint / 新点软件), whose ecosystem has internal Java JARs and frontend frameworks for government/business application development. Their docs mention internal frontend frameworks such as M8 and FMUI, with concepts like containers, components, forms, SSO, etc. ([Epoint][1])

Usually these internal JARs are doing several things:

```
Epoint internal platform
        |
        +-- Spring MVC / Servlet wrapper
        +-- ORM + DAO
        +-- Permission / RBAC
        +-- Workflow
        +-- Form engine
        +-- Report
        +-- File upload
        +-- SSO
        +-- Frontend component library
        +-- Code generator
```

You can replace it with an open-source enterprise stack.

## 1. Java backend replacement

### Base framework

| Epoint role          | Open source replacement  |
| -------------------- | ------------------------ |
| Web MVC              | Spring Boot + Spring MVC |
| Dependency injection | Spring Framework         |
| REST API             | Spring Web               |
| Validation           | Hibernate Validator      |
| Config               | Spring Boot Config       |

Typical:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

---

## 2. ORM / database layer

Replace internal DAO JAR:

### Option A: MyBatis (common in China enterprise)

MyBatis

```java
@Mapper
public interface UserMapper {

    @Select("""
       select * from user where id=#{id}
    """)
    User findById(Long id);
}
```

Pros:

* close to SQL
* good for government systems
* easy migration from old JDBC style

---

### Option B: JPA

Hibernate ORM

```java
@Entity
class User {

    @Id
    Long id;

    String name;
}
```

Better for greenfield.

---

## 3. Admin framework replacement

Epoint systems often contain:

* user management
* department tree
* role permission
* menus
* audit logs

Use:

### RuoYi

Very popular in China.

Architecture:

```
Vue3
 |
Spring Boot
 |
MyBatis
 |
MySQL
```

Features:

* RBAC
* code generation
* logging
* file upload
* Excel export

Alternative:

### JHipster

More international:

```
Angular/React/Vue
        |
Spring Boot
        |
PostgreSQL
        |
Docker/K8s
```

---

## 4. Frontend replacement

Epoint M8/FMUI seems similar to an enterprise component framework. ([Epoint][2])

Replace with:

### Vue 3 ecosystem

Most Chinese enterprise apps:

```
Vue3
 |
TypeScript
 |
Vite
 |
Element Plus
 |
Pinia
 |
Axios
```

Components:

Element Plus

Example:

```vue
<el-table :data="users">
  <el-table-column 
       prop="name"
       label="Name"/>
</el-table>
```

---

For more enterprise UI:

Ant Design Vue

Good for:

* complex forms
* tables
* dashboards

---

## 5. Form engine replacement

Epoint-like systems usually have dynamic forms.

Options:

### Low-code form

Formily

Example:

```
JSON schema

{
 type:"input",
 name:"username"
}

        |
        v

Vue form renderer
```

---

### Workflow

If Epoint has approval/workflow:

Replace:

Flowable

Architecture:

```
User submits form

      |
      v

Flowable BPMN Engine

      |
      +-- Manager approve
      |
      +-- Finance approve
      |
      +-- Complete
```

---

## 6. Permission system

Replace internal security JAR:

### Spring Security

```
JWT
 |
Spring Security Filter
 |
RBAC
 |
Database
```

or:

Apache Shiro

---

## 7. File management

Replace:

```
epoint-file.jar
```

with:

* MinIO
* S3 compatible storage

Architecture:

```
Browser

 |
Spring Boot

 |
MinIO

 |
Object Storage
```

---

## 8. Reporting

Government apps usually need reports.

Replace:

JasperReports

or:

ECharts

for dashboards.

---

## A modern replacement stack I would choose

For a 2026 enterprise Java system:

```
Frontend
---------
Vue3
TypeScript
Vite
Element Plus
ECharts


Backend
---------
Spring Boot 3
Java 21
MyBatis Plus
Spring Security
JWT


Business
---------
Flowable
Quartz
EasyExcel


Storage
---------
PostgreSQL/MySQL
Redis
MinIO


Deployment
---------
Docker
Kubernetes
Nginx
```

This covers ~90% of what proprietary enterprise JAR platforms provide.

The biggest thing you lose compared with Epoint is not technology — it is **domain assets**:

* government-specific forms
* procurement workflows
* templates
* customer integrations
* accumulated business components

The code replacement is easy; the accumulated business knowledge is the real moat.

References:

* Epoint frontend framework documentation ([Epoint][2])
* Epoint developer FAQ / framework notes ([Epoint][1])
* FMUI framework documentation ([Epoint][3])

[1]: https://app.epoint.com.cn/faqdoc/?utm_source=chatgpt.com "如何正确的提问？ | 移动前端常见问题库"
[2]: https://app.epoint.com.cn/m8fedoc/index.html?file=014-%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98%2F%E6%A3%80%E6%B5%8B%E5%8F%98%E5%8C%96%E7%9A%84%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9&utm_source=chatgpt.com "M8移动前端框架"
[3]: https://app.epoint.com.cn/faqdoc/F2E/FMUI/?utm_source=chatgpt.com "FMUI框架 | 移动前端常见问题库"