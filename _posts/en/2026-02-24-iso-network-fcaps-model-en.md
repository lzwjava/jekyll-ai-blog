---
audio: false
generated: true
image: false
lang: en
layout: post
title: ISO Network Management FCAPS Model
translated: false
type: note
---

Question: According to the ISO definition of network management functions, what are the main aspects included?

Answer:

According to the International Organization for Standardization (ISO), specifically within the **ISO/IEC 7498-4** standard (which is part of the Open Systems Interconnection or OSI model framework), network management is defined by five functional areas. These are commonly referred to as the **FCAPS** model.

The five main aspects are:

1.  **Fault Management (故障管理)**
    *   **Purpose:** To detect, log, notify users of, and (to the extent possible) automatically fix network problems to keep the network running effectively.
    *   **Key Activities:** Error detection, isolation, correction, and maintaining an error log. It often involves monitoring for alarms and ensuring high availability.

2.  **Configuration Management (配置管理)**
    *   **Purpose:** To monitor and manage the configuration of network devices and software to maintain a desired state.
    *   **Key Activities:** Identifying managed objects, initializing the network, setting parameters, collecting configuration data, and modifying configurations (e.g., adding new devices or updating firmware).

3.  **Accounting Management (计费管理)**
    *   **Purpose:** To track network usage by individuals or groups so that usage fees can be determined and billed appropriately. It also helps in managing resource quotas.
    *   **Key Activities:** Measuring network utilization, establishing billing rates, generating invoices, and enforcing usage limits. In non-billing environments, this is sometimes referred to as "Administration" or "Usage Management."

4.  **Performance Management (性能管理)**
    *   **Purpose:** To measure and make available various aspects of network performance to ensure the network runs efficiently.
    *   **Key Activities:** Gathering statistical data (such as throughput, latency, packet loss, and utilization), analyzing trends, and tuning network parameters to optimize performance.

5.  **Security Management (安全管理)**
    *   **Purpose:** To control access to network resources according to local guidelines so that the network cannot be sabotaged (intentionally or unintentionally) and sensitive information cannot be accessed by unauthorized users.
    *   **Key Activities:** Authentication, authorization, encryption key management, security logging, and detecting security breaches (such as virus infections or intrusion attempts).

**Summary Mnemonic:**
These five functions are often remembered by the acronym **FCAPS**:
*   **F**ault
*   **C**onfiguration
*   **A**ccounting
*   **P**erformance
*   **S**ecurity
