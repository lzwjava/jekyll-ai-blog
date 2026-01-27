---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Professional Developer Exam Questions
translated: false
type: note
---

Question: Provide 50 multiple-choice exam questions for the Google Cloud Professional Cloud Developer certification exam (without showing the answers)

Answer: 

Here are 50 original multiple-choice questions covering key topics from the Google Cloud Professional Cloud Developer certification exam. Each question has four options (A–D). These are designed to reflect the style and scope of the real exam (as of 2025–2026).

1. Which service is best suited for hosting a stateless web application that requires automatic scaling to zero instances and supports custom runtimes?  
   - A. App Engine Standard  
   - B. Cloud Run  
   - C. Compute Engine  
   - D. Cloud Functions (1st gen)

2. You need to store structured data with strong consistency and SQL querying capabilities. Which database should you choose?  
   - A. Cloud Firestore in Datastore mode  
   - B. Cloud SQL  
   - C. Bigtable  
   - D. Cloud Bigtable

3. What is the recommended way to authenticate a service running on Cloud Run to call the Cloud Storage JSON API?  
   - A. Use a service account key file stored in Secret Manager  
   - B. Attach a service account to the Cloud Run service  
   - C. Use Application Default Credentials with no configuration  
   - D. Enable the Compute Engine default service account

4. Which deployment strategy minimizes downtime when updating a Cloud Run service?  
   - A. Blue-green deployment  
   - B. Traffic splitting with revisions  
   - C. Rolling update with managed instance groups  
   - D. Canary deployment using Compute Engine

5. You are designing an application that processes images uploaded to Cloud Storage. Which event source should trigger a Cloud Function?  
   - A. Pub/Sub message  
   - B. Cloud Storage object finalize event  
   - C. Cloud Audit Logs entry  
   - D. HTTP request

6. What is the primary benefit of using Cloud Build with a cloudbuild.yaml file over manual gcloud commands?  
   - A. Faster build times  
   - B. Built-in caching and parallel steps  
   - C. Automatic secret rotation  
   - D. Free unlimited build minutes

7. Which IAM role allows an application to read and write to a specific Cloud Storage bucket without granting broader project permissions?  
   - A. roles/storage.objectAdmin  
   - B. roles/storage.legacyBucketReader  
   - C. roles/storage.objectViewer + roles/storage.objectCreator  
   - D. roles/storage.admin

8. You need to implement distributed tracing for a microservices application running on Cloud Run. Which Google Cloud service should you integrate?  
   - A. Cloud Trace  
   - B. Cloud Profiler  
   - C. Cloud Monitoring  
   - D. Cloud Logging

9. What is the correct way to deploy a new version of an App Engine Standard application without affecting current traffic?  
   - A. Use gcloud app deploy --promote  
   - B. Deploy to a new version and use traffic splitting  
   - C. Update the default version directly  
   - D. Redeploy the same version number

10. Which storage class in Cloud Storage is most appropriate for infrequently accessed backup files that still need millisecond access latency?  
    - A. Standard  
    - B. Nearline  
    - C. Coldline  
    - D. Archive

11. You are migrating a monolithic application to microservices. Which service is best for exposing internal APIs securely between services?  
    - A. Cloud Endpoints  
    - B. Cloud Load Balancing internal HTTP(S)  
    - C. VPC Service Controls  
    - D. BeyondCorp Enterprise

12. How can you ensure that a Cloud Function only processes one message at a time from a Pub/Sub subscription?  
    - A. Set --max-instances=1  
    - B. Set concurrency=1 in the function configuration  
    - C. Use ordered delivery in Pub/Sub  
    - D. Use --trigger-topic with --ack-deadline

13. Which option provides the fastest way to read small configuration values that change infrequently in a Cloud Run application?  
    - A. Cloud Firestore document  
    - B. Secret Manager + environment variable  
    - C. Cloud SQL query on startup  
    - D. Cloud Storage JSON file

14. What should you use to automatically build and deploy container images to Artifact Registry when code is pushed to Cloud Source Repositories?  
    - A. Cloud Scheduler + Cloud Build  
    - B. Cloud Build trigger connected to the repository  
    - C. Artifact Registry webhook  
    - D. gcloud builds submit in CI/CD pipeline

15. Which load balancer type should you use for a global HTTP(S) application running on GKE with multi-region clusters?  
    - A. Internal HTTP(S) Load Balancer  
    - B. External Application Load Balancer  
    - C. Network Load Balancer  
    - D. Classic VPN Gateway

16. You need to run a batch job that processes 1 TB of data daily and then terminates. Which service offers the lowest cost?  
    - A. Compute Engine preemptible VMs  
    - B. Cloud Run jobs  
    - C. Dataflow batch pipeline  
    - D. Dataproc Serverless

17. What is the best practice for managing secrets in a containerized application running on Cloud Run?  
    - A. Bake secrets into the Docker image  
    - B. Mount secrets from Secret Manager as volumes  
    - C. Pass secrets via environment variables from Cloud Build  
    - D. Use Cloud KMS directly in application code

18. Which service automatically handles retries, dead-letter queues, and exactly-once processing semantics for event-driven workloads?  
    - A. Cloud Tasks  
    - B. Eventarc  
    - C. Pub/Sub with ordering keys  
    - D. Workflows

19. You want to monitor custom latency metrics from your application. Which service should you use to create these custom metrics?  
    - A. Cloud Monitoring custom service metrics  
    - B. Cloud Trace spans  
    - C. Cloud Profiler  
    - D. Cloud Logging structured logs

20. What is the recommended way to implement rate limiting for a public Cloud Run API?  
    - A. Use API Gateway with quotas  
    - B. Implement in application code with Redis  
    - C. Use Cloud Armor  
    - D. Enable IAP with OAuth

21. Which database supports multi-region strong consistency for globally distributed applications?  
    - A. Cloud Spanner  
    - B. Firestore multi-region  
    - C. Cloud SQL with cross-region read replicas  
    - D. Bigtable multi-cluster routing

22. How can you grant a third-party service account access to your Cloud Storage bucket without creating a key?  
    - A. Use workload identity federation  
    - B. Generate a signed URL  
    - C. Add the service account to the bucket IAM policy  
    - D. Use gsutil acl ch

23. Which tool helps analyze memory usage and detect leaks in a Go application running on Cloud Run?  
    - A. Cloud Profiler  
    - B. Cloud Debugger  
    - C. pprof via Cloud Trace  
    - D. Memorystore for Redis

24. You are using Terraform to manage GCP resources. Where should you store sensitive values like service account keys?  
    - A. In the Terraform state file  
    - B. In Google Cloud Secret Manager with Terraform provider  
    - C. Hardcoded in .tf files  
    - D. In Git repository with encryption

25. What is the default scaling behavior of Cloud Functions (2nd gen)?  
    - A. Scales to zero automatically  
    - B. Minimum 1 instance always running  
    - C. Fixed instance count  
    - D. Manual scaling only

26. Which option provides the strongest durability for objects stored in Cloud Storage?  
    - A. Dual-region  
    - B. Multi-region  
    - C. Regional with object versioning  
    - D. Turbo replication enabled

27. You need to run containerized background workers that pull messages from Pub/Sub. Which service is most appropriate?  
    - A. Cloud Run services with --cpu-throttling  
    - B. Compute Engine VM with Pub/Sub pull subscriber  
    - C. Cloud Run jobs triggered by Pub/Sub  
    - D. GKE with Deployment and pull subscription

28. What should you use to orchestrate a multi-step serverless workflow that includes conditional branching?  
    - A. Cloud Composer  
    - B. Cloud Workflows  
    - C. Cloud Functions chained via Pub/Sub  
    - D. Dataflow Flex templates

29. Which service integrates natively with Cloud Build to scan container images for vulnerabilities?  
    - A. Artifact Registry vulnerability scanning  
    - B. Container Analysis  
    - C. Security Command Center  
    - D. Binary Authorization

30. You want to implement canary testing for a new Cloud Run revision. How can this be achieved?  
    - A. Use traffic tags and gradual traffic shift  
    - B. Deploy to a separate service  
    - C. Use --no-traffic flag and manual switch  
    - D. Create a new project

31. What is the best way to handle large file uploads (>100 MB) to a Cloud Run service?  
    - A. Direct upload to Cloud Run  
    - B. Upload directly to Cloud Storage signed URL  
    - C. Use multipart/form-data with increased timeout  
    - D. Stream through Pub/Sub

32. Which feature allows you to route traffic to different App Engine versions based on cookie or header value?  
    - A. Traffic splitting  
    - B. Custom domain mapping with routing  
    - C. Dispatch.yaml  
    - D. Versions with tags

33. You need transactional consistency across multiple Firestore documents. Which API should you use?  
    - A. Batch write  
    - B. Transaction  
    - C. Run in transaction  
    - D. Distributed counter pattern

34. What is the recommended way to implement authentication for an internal GKE workload calling Cloud APIs?  
    - A. Workload Identity  
    - B. Service account key JSON  
    - C. Default Compute Engine SA  
    - D. OAuth 2.0 client credentials

35. Which service provides managed Redis compatible caching with automatic scaling?  
    - A. Memorystore for Redis Cluster  
    - B. Cloud Memorystore  
    - C. ElastiCache (AWS)  
    - D. Redis Enterprise on GKE

36. You are debugging a production issue in a Cloud Run service. Which tool allows you to take snapshots of running instances?  
    - A. Cloud Debugger  
    - B. Cloud Logging real-time tail  
    - C. Cloud Trace  
    - D. gcloud beta run services proxy

37. What is the primary purpose of Binary Authorization in a CI/CD pipeline?  
    - A. Sign container images  
    - B. Scan for malware  
    - C. Enforce admission policies  
    - D. Rotate service account keys

38. Which Pub/Sub feature ensures messages are processed in the order they were published for a specific entity?  
    - A. Ordering keys  
    - B. Exactly-once delivery guarantee  
    - C. Flow control  
    - D. Dead-letter topic

39. You need to run machine learning inference with low latency. Which deployment option is best for a TensorFlow model?  
    - A. Cloud Run with GPU  
    - B. Vertex AI Endpoints  
    - C. Compute Engine with attached GPU  
    - D. GKE with GPU nodes

40. What should you use to automatically rotate service account keys used by external CI/CD systems?  
    - A. Workload Identity Federation  
    - B. Short-lived credentials via OAuth  
    - C. Cloud KMS asymmetric keys  
    - D. Service account impersonation

41. Which monitoring metric indicates that a Cloud Run service is scaling up due to high CPU usage?  
    - A. container/cpu/utilization  
    - B. run.googleapis.com/request_count  
    - C. run.googleapis.com/container/startup_latency  
    - D. run.googleapis.com/active_instance_count

42. You are designing a system that must process 1 million events per second. Which messaging service is most appropriate?  
    - A. Pub/Sub  
    - B. Cloud Tasks  
    - C. Eventarc  
    - D. Cloud Pub/Sub Lite

43. What is the best practice for logging in a distributed system on GCP?  
    - A. Use stdout/stderr with structured JSON  
    - B. Write directly to Cloud Logging API  
    - C. Use legacy App Engine logging  
    - D. Store logs in Cloud Storage

44. Which option allows gradual rollout of configuration changes without redeploying code?  
    - A. App Engine config versions  
    - B. Cloud Run environment variables per revision  
    - C. Feature flags stored in Firestore  
    - D. Secret Manager versions

45. You need to grant fine-grained access to BigQuery datasets for different teams. Which approach is recommended?  
    - A. Authorized views  
    - B. Dataset-level IAM roles  
    - C. Column-level security  
    - D. BigQuery Omni

46. What is the correct order of operations in a typical Cloud Build pipeline for containerized apps?  
    - A. Build → Scan → Push → Deploy  
    - B. Push → Build → Deploy → Scan  
    - C. Deploy → Build → Scan → Push  
    - D. Scan → Deploy → Build → Push

47. Which service helps you implement chaos engineering experiments in GKE?  
    - A. Chaos Mesh (open source)  
    - B. Cloud Service Mesh  
    - C. Fault Injection (Cloud Load Testing)  
    - D. No native GCP service exists

48. You want to reduce cold start latency in Cloud Functions (2nd gen). Which option helps the most?  
    - A. Use minimum instances  
    - B. Increase allocated CPU  
    - C. Use Cloud Run instead  
    - D. Pre-warm with Cloud Scheduler

49. What is the recommended way to implement idempotency in an event-driven payment processing system?  
    - A. Use transaction ID as idempotency key  
    - B. Enable Pub/Sub exactly-once  
    - C. Use Cloud Tasks lease duration  
    - D. Store processed IDs in Firestore

50. Which combination provides both authentication and authorization for public APIs with least operational overhead?  
    - A. API Gateway + Identity-Aware Proxy  
    - B. Cloud Endpoints + ESPv2  
    - C. Cloud Run + Firebase Authentication  
    - D. Apigee + Service accounts

References:  

- [Google Cloud Professional Cloud Developer Exam Guide](https://cloud.google.com/learn/certification/cloud-developer)
- [Google Cloud sample questions for Professional Cloud Developer](https://cloud.google.com/learn/certification/cloud-developer#sample-questions)