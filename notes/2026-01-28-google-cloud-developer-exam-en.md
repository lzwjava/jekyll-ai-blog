---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5.2
title: Google Cloud Developer Exam Questions
translated: false
type: note
---

Question: Create 50 multiple-choice exam questions about the Google Professional Cloud Developer certification, without showing answers, using “-” or “*” to indicate options.

Answer:

Below are **50 original multiple-choice exam questions** aligned with the **Google Professional Cloud Developer** certification objectives.
Each question has **four options**, marked using `-`. **No answers are shown**, suitable for self-testing or mock exams.

---

### 1

Which Google Cloud service is best suited for running stateless HTTP applications with automatic scaling and no server management?

* Compute Engine
* Cloud Run
* Cloud Functions
* Google Kubernetes Engine

---

### 2

A Cloud Run service needs to access a Cloud SQL instance securely. What is the recommended approach?

* Use a public IP and whitelist all Google IP ranges
* Use Cloud SQL Auth Proxy
* Store database credentials in source code
* Use VPC peering without authentication

---

### 3

Which Google Cloud product is designed for asynchronous event-driven messaging between services?

* Cloud Tasks
* Pub/Sub
* Cloud Scheduler
* Cloud Load Balancing

---

### 4

What is the primary purpose of a Google Cloud service account?

* To represent a human user
* To manage billing accounts
* To authenticate applications and services
* To store application secrets

---

### 5

Which storage option provides strong consistency for object storage in Google Cloud?

* Persistent Disk
* Cloud Storage
* Filestore
* Bigtable

---

### 6

What is the maximum execution time for a single invocation of Cloud Functions (2nd gen)?

* 1 minute
* 9 minutes
* 15 minutes
* 60 minutes

---

### 7

Which tool is recommended for managing infrastructure as code on Google Cloud?

* Cloud Deployment Manager
* Cloud Shell Editor
* Terraform
* Cloud Build

---

### 8

Which HTTP load balancing feature allows routing traffic based on URL paths?

* Network Load Balancer
* Internal TCP Load Balancer
* HTTP(S) Load Balancer
* VPN Gateway

---

### 9

What is the default deployment unit in Google Kubernetes Engine?

* Pod
* Service
* Deployment
* Node

---

### 10

Which command is used to deploy a service to Cloud Run?

* gcloud run deploy
* gcloud app deploy
* gcloud functions deploy
* kubectl apply

---

### 11

Which Google Cloud database is best suited for globally distributed, strongly consistent relational workloads?

* Cloud SQL
* Firestore
* BigQuery
* Spanner

---

### 12

What is the primary purpose of Cloud Build?

* Hosting applications
* Running CI/CD pipelines
* Monitoring logs
* Managing APIs

---

### 13

Which Google Cloud service is optimized for large-scale analytical queries using SQL?

* Cloud SQL
* Bigtable
* BigQuery
* Firestore

---

### 14

How can sensitive configuration data be securely stored and accessed by applications?

* Environment variables in code
* Cloud Storage buckets
* Secret Manager
* Source repositories

---

### 15

Which GKE feature ensures zero-downtime deployments?

* Node auto-repair
* Rolling updates
* Preemptible VMs
* Static IPs

---

### 16

What is the main benefit of using managed instance groups?

* Manual VM scaling
* Automatic scaling and self-healing
* Cheaper storage
* Faster networking

---

### 17

Which service provides centralized logging for Google Cloud resources?

* Cloud Trace
* Cloud Monitoring
* Cloud Logging
* Error Reporting

---

### 18

Which authentication method is recommended for applications running on GKE to access Google Cloud APIs?

* Service account keys stored as files
* OAuth tokens generated manually
* Workload Identity
* API keys embedded in code

---

### 19

What does a readiness probe in Kubernetes indicate?

* Whether the container has started
* Whether the container is ready to receive traffic
* Whether the node is healthy
* Whether the pod can be scheduled

---

### 20

Which Cloud Run feature allows private access from internal services only?

* IAM roles
* Ingress settings
* VPC Service Controls
* Firewall rules

---

### 21

Which Google Cloud service is used to schedule cron jobs?

* Cloud Tasks
* Pub/Sub
* Cloud Scheduler
* Cloud Functions

---

### 22

What is the recommended way to expose a GKE application to the internet?

* NodePort service
* LoadBalancer service
* Ingress with HTTP(S) Load Balancer
* Direct VM IP access

---

### 23

Which tool helps identify performance bottlenecks in distributed applications?

* Cloud Logging
* Cloud Trace
* Cloud Profiler
* Error Reporting

---

### 24

Which Google Cloud service is best for key-value and wide-column NoSQL workloads?

* Firestore
* Bigtable
* Cloud SQL
* Memorystore

---

### 25

What happens when a Cloud Run service scales to zero?

* The container is paused
* The container is deleted
* No instances are running, and requests trigger new instances
* The service becomes unavailable

---

### 26

Which GKE networking mode assigns a VPC IP address to each pod?

* Routes-based
* NAT-based
* VPC-native
* Overlay networking

---

### 27

What is the primary purpose of Cloud Endpoints?

* Database migration
* API management and security
* Load balancing
* Logging and monitoring

---

### 28

Which IAM role is most appropriate for read-only access to Cloud Storage objects?

* Storage Admin
* Storage Object Admin
* Storage Object Viewer
* Storage Viewer

---

### 29

Which Google Cloud service provides in-memory data storage for low-latency access?

* Bigtable
* Firestore
* Memorystore
* Cloud SQL

---

### 30

Which build configuration file is used by Cloud Build?

* Dockerfile
* cloudbuild.yaml
* build.gradle
* app.yaml

---

### 31

Which option allows blue-green deployments in GKE?

* Node pools
* Traffic splitting using Services
* Rolling node upgrades
* Preemptible nodes

---

### 32

What is the primary use case for Cloud Tasks?

* Batch data processing
* Delayed and asynchronous task execution
* Real-time streaming analytics
* Application hosting

---

### 33

Which Google Cloud service automatically collects application error reports?

* Cloud Logging
* Cloud Monitoring
* Error Reporting
* Cloud Trace

---

### 34

Which feature of Cloud Storage helps reduce costs for infrequently accessed data?

* Multi-region buckets
* Object versioning
* Lifecycle management
* Strong consistency

---

### 35

What is the recommended way to connect on-premises systems to Google Cloud securely?

* Public IP with firewall rules
* Cloud VPN or Cloud Interconnect
* NAT Gateway only
* Load Balancer with SSL

---

### 36

Which deployment platform uses `app.yaml` for configuration?

* Cloud Run
* Cloud Functions
* App Engine
* GKE

---

### 37

Which Google Cloud service supports real-time data ingestion and stream processing?

* Dataflow
* Dataproc
* BigQuery
* Composer

---

### 38

Which Kubernetes object provides stable networking for a set of pods?

* Pod
* Deployment
* Service
* ConfigMap

---

### 39

Which monitoring feature allows defining thresholds and sending notifications?

* Logs Explorer
* Metrics Explorer
* Alerting policies
* Trace Viewer

---

### 40

Which Cloud SQL feature improves read scalability?

* Vertical scaling
* Read replicas
* High availability failover
* Automatic backups

---

### 41

What is the recommended way to store Docker images for Cloud Run deployments?

* Docker Hub
* Cloud Storage
* Artifact Registry
* Git repositories

---

### 42

Which Google Cloud service orchestrates workflows between services?

* Cloud Tasks
* Cloud Workflows
* Pub/Sub
* Cloud Scheduler

---

### 43

Which Kubernetes feature limits CPU and memory usage of a container?

* Node selectors
* Resource requests and limits
* Taints and tolerations
* Pod affinity

---

### 44

Which Google Cloud product is best for batch Spark workloads?

* Dataflow
* Dataproc
* Bigtable
* Composer

---

### 45

Which Cloud Run setting controls the maximum number of concurrent requests per container?

* Instance limit
* CPU allocation
* Concurrency
* Timeout

---

### 46

Which Google Cloud service provides distributed configuration storage?

* Secret Manager
* Config Connector
* Firestore
* Cloud Storage

---

### 47

Which approach is recommended for zero-downtime schema migrations?

* Stop traffic during migration
* Backward-compatible schema changes
* Manual database updates
* Disable application writes

---

### 48

Which Google Cloud feature automatically restarts unhealthy VMs?

* Live migration
* Autohealing policies
* Preemptible instances
* Shielded VMs

---

### 49

Which service is best for handling sudden spikes in HTTP traffic?

* Single Compute Engine VM
* Managed instance group with autoscaling
* Cloud Storage
* Filestore

---

### 50

Which Google Cloud tool helps analyze application CPU and memory usage over time?

* Cloud Logging
* Cloud Trace
* Cloud Profiler
* Error Reporting

---

If you want, I can also:

* Generate **answers separately**
* Turn this into a **timed mock exam**
* Create **scenario-based questions**
* Align questions strictly to the **official exam blueprint**
