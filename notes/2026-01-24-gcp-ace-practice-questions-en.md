---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: GCP Associate Cloud Engineer Practice Questions
translated: false
type: note
---

Question: Provide 50 multiple-choice exam questions for the Google Associate Cloud Engineer (ACE) certification exam in GCP, without showing the answers.

Answer:

Here are 50 multiple-choice questions covering key topics from the Associate Cloud Engineer exam (including setting up environments, planning/implementing solutions, configuring access, deploying/managing infrastructure, and operations/monitoring). Each question has four options (A–D).

1. Which Google Cloud resource hierarchy level is the root node where billing is attached and Organization Policies are typically enforced?
   A) Folder
   B) Project
   C) Organization
   D) Resource

2. What is the recommended way to grant a user the ability to create Compute Engine instances in a specific project without giving them broader permissions?
   A) roles/compute.instanceAdmin
   B) roles/compute.instanceAdmin.v1
   C) roles/editor
   D) roles/owner

3. Which command creates a new Google Cloud project using gcloud?
   A) gcloud projects create PROJECT_ID
   B) gcloud init project PROJECT_ID
   C) gcloud projects new PROJECT_ID
   D) gcloud create project PROJECT_ID

4. You need to grant a service account the ability to read objects from a Cloud Storage bucket. Which predefined role should you use?
   A) roles/storage.objectViewer
   B) roles/storage.admin
   C) roles/storage.objectCreator
   D) roles/storage.legacyBucketReader

5. Which storage class in Cloud Storage is most suitable for infrequently accessed data that still needs millisecond access latency?
   A) Standard
   B) Nearline
   C) Coldline
   D) Archive

6. What is the default number of days before an object in a Nearline storage class bucket moves to Coldline automatically (if lifecycle rule is not set otherwise)?
   A) 30 days
   B) 90 days
   C) 180 days
   D) Never

7. Which command lists all instances in a specific zone using gcloud?
   A) gcloud compute instances list --zone=ZONE
   B) gcloud instances list --zone=ZONE
   C) gcloud compute list instances --zone=ZONE
   D) gcloud list compute instances --zone=ZONE

8. You want to create a managed instance group with autoscaling based on CPU utilization. Which resource do you configure?
   A) Autoscaler
   B) Load Balancer
   C) Health Check
   D) Firewall rule

9. What type of load balancer should you use for HTTP(S) traffic that requires global distribution and SSL termination?
   A) TCP/SSL Proxy Load Balancer
   B) HTTP(S) Load Balancer
   C) Internal Load Balancer
   D) Network Load Balancer

10. Which service is serverless and best suited for containerized workloads triggered by HTTP requests?
    A) Cloud Functions
    B) Cloud Run
    C) App Engine Standard
    D) Compute Engine

11. In Cloud Run, what is the unit of billing for CPU and memory usage?
    A) Per request
    B) vCPU-second and GiB-second
    C) Per container instance
    D) Per deployment

12. Which IAM member type represents a Google Workspace group?
    A) user:
    B) serviceAccount:
    C) group:
    D) domain:

13. You need to allow an application running on Compute Engine to call Cloud Storage APIs without embedding credentials. What should you use?
    A) Service account attached to the VM
    B) API key
    C) OAuth 2.0 client ID
    D) Access key

14. Which VPC network type allows you to use custom subnets and manual IP ranges?
    A) Auto mode
    B) Custom mode
    C) Legacy mode
    D) Shared VPC

15. What is the purpose of Cloud NAT in Google Cloud?
    A) Translate private IP to public IP for outbound traffic
    B) Load balance internal traffic
    C) Provide inbound connectivity to private VMs
    D) Encrypt traffic between regions

16. Which command deploys a new version of an App Engine application?
    A) gcloud app deploy
    B) gcloud app create version
    C) gcloud deploy app
    D) gcloud app versions deploy

17. In Kubernetes Engine, what component is responsible for scheduling pods onto nodes?
    A) kubelet
    B) kube-scheduler
    C) kube-controller-manager
    D) etcd

18. Which GKE mode provides a fully managed control plane and reduced operational overhead?
    A) Standard mode
    B) Autopilot mode
    C) Enterprise mode
    D) Classic mode

19. You need to store sensitive configuration data that can be mounted as volumes or environment variables in Kubernetes. Which resource should you use?
    A) ConfigMap
    B) Secret
    C) PersistentVolumeClaim
    D) ServiceAccount

20. What is the primary monitoring tool for Google Cloud resources?
    A) Cloud Trace
    B) Cloud Monitoring
    C) Cloud Logging
    D) Cloud Debugger

21. Which service collects, indexes, and stores log data in Google Cloud?
    A) Cloud Monitoring
    B) Cloud Logging
    C) Cloud Trace
    D) Operations Suite

22. What is the purpose of an uptime check in Cloud Monitoring?
    A) Monitor CPU usage
    B) Check availability of public endpoints
    C) Track request latency
    D) Alert on disk space

23. Which command exports logs from Cloud Logging to BigQuery?
    A) Create a log sink with BigQuery destination
    B) gcloud logging export
    C) gcloud logging sinks create
    D) Both A and C

24. You need to grant a developer temporary elevated permissions to troubleshoot a production issue. What is the best practice?
    A) Give them roles/owner temporarily
    B) Use IAM Conditions with time-based access
    C) Share service account keys
    D) Add them to the project as editor

25. Which feature allows multiple projects to share the same VPC network?
    A) VPC Peering
    B) Shared VPC
    C) Cloud Interconnect
    D) Cloud VPN

26. What is the maximum number of custom VPC networks per project by default?
    A) 1
    B) 5
    C) 10
    D) Unlimited

27. Which disk type provides the lowest cost per GB but is not SSD?
    A) Balanced Persistent Disk
    B) Standard Persistent Disk
    C) SSD Persistent Disk
    D) Extreme Persistent Disk

28. You need to back up a Compute Engine disk. Which service should you use?
    A) Cloud Scheduler
    B) Snapshot
    C) Cloud Backup
    D) Persistent Disk clone

29. What is the purpose of a Cloud Storage lifecycle rule?
    A) Automatically delete or transition objects based on conditions
    B) Encrypt objects
    C) Set retention policies
    D) Both A and C

30. Which command copies files from local to a Cloud Storage bucket?
    A) gsutil cp
    B) gcloud storage cp
    C) gsutil rsync
    D) Both A and B

31. In IAM, what does the principle of least privilege recommend?
    A) Grant owner role to all users
    B) Grant only the permissions required to perform a task
    C) Use basic roles only
    D) Avoid custom roles

32. Which service is best for running stateless batch jobs that need to scale to thousands of instances?
    A) Cloud Run jobs
    B) Compute Engine VMs
    C) App Engine Flexible
    D) Cloud Functions

33. What is the default region for resources created without specifying a location?
    A) us-central1
    B) No default – must specify
    C) global
    D) europe-west1

34. Which Google Cloud service provides a managed PostgreSQL-compatible database?
    A) Cloud SQL
    B) Firestore
    C) Bigtable
    D) AlloyDB

35. You need to allow SSH access to a Compute Engine VM without a public IP. What should you use?
    A) Cloud IAP for TCP forwarding
    B) Bastion host
    C) Cloud VPN
    D) All of the above

36. What does gcloud auth application-default login do?
    A) Authenticates for user credentials in local tools
    B) Creates a service account key
    C) Logs in to the gcloud SDK
    D) Enables ADC on a VM

37. Which load balancer preserves source client IP by default?
    A) HTTP(S) Load Balancer
    B) SSL Proxy Load Balancer
    C) Internal TCP/UDP Load Balancer
    D) TCP Proxy Load Balancer

38. In GKE Autopilot, who manages the nodes?
    A) Customer
    B) Google
    C) Both
    D) No nodes exist

39. Which command scales a managed instance group?
    A) gcloud compute instance-groups managed resize
    B) gcloud compute mig scale
    C) gcloud compute instances resize-group
    D) gcloud resize mig

40. What is the recommended way to authenticate Terraform with Google Cloud?
    A) Service account key file
    B) Application Default Credentials
    C) gcloud auth application-default login
    D) Both B and C

41. Which service is ideal for real-time analytics on streaming data?
    A) BigQuery
    B) Dataflow
    C) Pub/Sub + Dataflow
    D) Dataproc

42. What is the purpose of a firewall rule priority?
    A) Lower number = higher priority
    B) Higher number = higher priority
    C) No priority – first match wins
    D) Priority only for egress

43. Which role allows viewing (but not modifying) most resources in a project?
    A) roles/viewer
    B) roles/browser
    C) roles/reader
    D) roles/monitoring.viewer

44. You are migrating an on-premises MySQL database to Google Cloud. Which service offers the easiest lift-and-shift?
    A) Cloud SQL
    B) Bare Metal Solution
    C) Datastream
    D) Database Migration Service

45. What does Cloud Billing export to BigQuery enable?
    A) Detailed cost analysis and reporting
    B) Automatic budget alerts
    C) Real-time billing dashboard
    D) Only A

46. Which option is NOT a valid machine family in Compute Engine?
    A) E2
    B) N2
    C) T2
    D) C2

47. In Cloud Functions, what is the maximum timeout for a 2nd gen function?
    A) 9 minutes
    B) 60 minutes
    C) 540 seconds
    D) 3600 seconds

48. Which service provides managed Redis-compatible in-memory caching?
    A) Memorystore for Redis
    B) Cloud SQL
    C) Firestore in Datastore mode
    D) Bigtable

49. What is required to use customer-managed encryption keys (CMEK) in Cloud Storage?
    A) Cloud KMS key
    B) Default Google-managed key
    C) Both A and B
    D) Only A

50. Which gcloud command shows the current active configuration?
    A) gcloud config list
    B) gcloud config current
    C) gcloud configuration active
    D) gcloud config show

References:

- <https://cloud.google.com/learn/certification/cloud-engineer>
- <https://cloud.google.com/learn/certification/guides/cloud-engineer>
