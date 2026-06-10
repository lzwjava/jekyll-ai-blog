---
audio: false
generated: true
image: false
lang: en
layout: post
title: JDK Upgrade Test Evidence Guide
translated: false
type: note
---

Question: For a JDK upgrade change request to a production server, how should I provide test evidence for the change request?

Answer:

For a production JDK upgrade, the goal is to prove that:

1. The application works correctly with the new JDK.
2. No critical functionality is broken.
3. Performance is acceptable.
4. The rollback plan is ready if issues occur.

A typical change request (CR) test evidence package includes the following.

## 1. Environment Information

Document the current and target versions.

| Item        | Current      | Target       |
| ----------- | ------------ | ------------ |
| OS          | RHEL 8       | RHEL 8       |
| JDK         | JDK 11.0.20  | JDK 17.0.12  |
| Application | MyApp 3.2.1  | MyApp 3.2.1  |
| Server      | App Server A | App Server A |

Example evidence:

```bash
java -version

openjdk version "17.0.12" 2025-07-15
OpenJDK Runtime Environment
OpenJDK 64-Bit Server VM
```

Include screenshots or console output.

---

## 2. Build Verification

Show that the application builds successfully using the new JDK.

Example:

```bash
mvn clean package
BUILD SUCCESS
```

or

```bash
gradle build
BUILD SUCCESSFUL
```

Evidence:

* Build logs
* CI pipeline screenshots
* Jenkins/GitLab job results

---

## 3. Application Startup Verification

Demonstrate that the application starts successfully.

Evidence:

```bash
systemctl status myapp

Active: active (running)
```

Application log:

```text
Application started successfully
Started MyApp in 23.4 seconds
```

Attach:

* Startup logs
* Service status screenshots

---

## 4. Smoke Testing (Most Important)

Execute key business functions.

Example:

| Test Case           | Result |
| ------------------- | ------ |
| User Login          | Pass   |
| Account Search      | Pass   |
| Payment Processing  | Pass   |
| Report Generation   | Pass   |
| Batch Job Execution | Pass   |

Evidence:

* Screenshots
* API responses
* Test execution report

Example API evidence:

```bash
curl https://api.company.com/health

{
  "status":"UP"
}
```

---

## 5. Regression Test Results

If your organization has automated tests:

```text
Total Tests: 523
Passed: 523
Failed: 0
```

Attach:

* JUnit report
* Selenium report
* TestNG report
* CI pipeline report

---

## 6. Performance Comparison

Compare old and new JDK.

Example:

| Metric            | Before | After  |
| ----------------- | ------ | ------ |
| Startup Time      | 35 sec | 28 sec |
| Heap Usage        | 4.2 GB | 4.0 GB |
| Avg Response Time | 210 ms | 205 ms |

Evidence:

* JMeter results
* Grafana screenshots
* Application monitoring reports

---

## 7. Security Verification

Verify vulnerabilities are addressed.

Example:

```text
JDK 11.0.20 -> Vulnerable
JDK 17.0.12 -> Approved corporate standard
```

Include:

* Security team's approval
* Vulnerability scan results
* Vendor advisory references

---

## 8. Health Check Validation

Verify:

```bash
curl /health
curl /actuator/health
```

Expected:

```json
{
  "status": "UP"
}
```

Check:

* Database connectivity
* MQ connectivity
* External API connectivity
* Cache connectivity

---

## 9. Rollback Test

Provide rollback procedure.

Example:

```bash
1. Stop application
2. Switch JAVA_HOME back to JDK 11
3. Restart application
4. Verify health endpoint
```

Evidence:

```text
Rollback tested successfully in UAT.
Estimated duration: 10 minutes.
```

---

## 10. Sample Change Request Test Evidence Summary

A concise summary often accepted by CAB/Change Management:

JDK Upgrade Test Evidence

Change:
Upgrade JDK from 11.0.20 to 17.0.12 on Production Application Servers.

Testing Performed:

1. Application compiled successfully using JDK 17.
2. Application startup completed successfully with no errors.
3. Smoke testing executed:

   * User Login: PASS
   * Account Search: PASS
   * Payment Processing: PASS
   * Report Generation: PASS
4. Regression test suite executed:

   * Total Tests: 523
   * Passed: 523
   * Failed: 0
5. Health checks verified:

   * Database connectivity: PASS
   * MQ connectivity: PASS
   * External API connectivity: PASS
6. Performance comparison showed no degradation.
7. Rollback procedure validated in UAT.

Conclusion:
The application is fully compatible with JDK 17. No functional or performance issues were identified. Production implementation is recommended.

In large enterprises such as banks, the minimum evidence normally expected by the Change Advisory Board (CAB) is:

* Successful startup logs
* Smoke test results for critical business functions
* Health-check results
* Rollback plan
* UAT or non-production testing sign-off

Since you work in a banking environment, attaching Jenkins build results, application startup logs, smoke-test screenshots, and UAT sign-off is usually sufficient for a standard JDK upgrade change request.
