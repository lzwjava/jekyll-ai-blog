---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Configuring Microservice Communication in AKS
translated: false
type: note
---

### Configuring Communication Between Microservices in Azure Kubernetes Service (AKS)

In Azure Kubernetes Service (AKS), microservices are typically deployed as **Pods** managed by **Deployments**. To enable them to communicate with each other (e.g., Service A calling Service B), you use **Kubernetes Services** to abstract the Pods' dynamic IPs and provide stable endpoints. This is done via internal networking, leveraging Kubernetes' built-in DNS resolution. Here's a step-by-step guide to configure and implement this.

#### 1. **Deploy Your Microservices as Deployments**
   Each microservice runs in a Pod (or set of Pods for scaling). Use a Deployment to manage them.

   Example YAML for a simple microservice Deployment (`service-a-deployment.yaml`):
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: service-a
     namespace: default  # Or your custom namespace
   spec:
     replicas: 3  # Scale as needed
     selector:
       matchLabels:
         app: service-a
     template:
       metadata:
         labels:
           app: service-a
       spec:
         containers:
         - name: service-a
           image: your-registry/service-a:latest  # e.g., ACR or Docker Hub image
           ports:
           - containerPort: 8080  # Port your app listens on
   ```

   Apply it:
   ```
   kubectl apply -f service-a-deployment.yaml
   ```

   Repeat for other services (e.g., `service-b`).

#### 2. **Expose Microservices with Services**
   Create a **ClusterIP Service** for each microservice. This type is for internal communication only (not exposed outside the cluster). It load-balances traffic to the Pods and provides a DNS name.

   Example YAML for Service A (`service-a-service.yaml`):
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: service-a
     namespace: default
   spec:
     selector:
       app: service-a  # Matches the Deployment labels
     ports:
     - protocol: TCP
       port: 80  # Service port (what callers use)
       targetPort: 8080  # Pod's container port
     type: ClusterIP  # Internal only
   ```

   Apply it:
   ```
   kubectl apply -f service-a-service.yaml
   ```

   Do the same for Service B. Now, Pods can reach each other via the Service's DNS name.

#### 3. **How Microservices Call Each Other**
   - **DNS-Based Discovery**: Kubernetes DNS resolves Service names automatically. From a Pod in Service A, call Service B using:
     - `<service-name>.<namespace>.svc.cluster.local` (fully qualified, e.g., `service-b.default.svc.cluster.local`).
     - Or just `<service-name>` if in the same namespace (e.g., `service-b`).
   - **HTTP/gRPC Calls**: In your app code, make requests to `http://service-b:80/endpoint`. Kubernetes handles load balancing and failover.
     - Example in Python (using requests):
       ```python
       import requests
       response = requests.get("http://service-b:80/api/data")
       ```
     - For gRPC, use the same hostname with the gRPC port.
   - **Port Mapping**: The Service port (e.g., 80) maps to the Pod's target port (e.g., 8080). No need to hardcode Pod IPs—they change on restarts.

   Test connectivity from a Pod:
   ```
   kubectl exec -it <pod-name-in-service-a> -- curl http://service-b:80/health
   ```

#### 4. **Advanced Configuration Options**
   - **Namespaces**: Deploy services in different namespaces for isolation. Use full DNS (e.g., `service-b.other-ns.svc.cluster.local`).
   - **Network Policies**: Secure communication with Calico or Azure CNI policies to allow/deny traffic between services.
     Example policy allowing Service A to call Service B:
     ```yaml
     apiVersion: networking.k8s.io/v1
     kind: NetworkPolicy
     metadata:
       name: allow-service-a-to-b
     spec:
       podSelector:
         matchLabels:
           app: service-b
       policyTypes:
       - Ingress
       ingress:
       - from:
         - podSelector:
             matchLabels:
               app: service-a
         ports:
         - protocol: TCP
           port: 80
     ```
   - **Service Mesh (e.g., Istio or Linkerd)**: For production, add a mesh for observability, mTLS, and traffic management. Install via Helm on AKS, then inject sidecar proxies into Pods.
   - **External Access (if needed)**: Use **LoadBalancer** or **Ingress** Services for outbound calls, but stick to ClusterIP for internal.

#### 5. **Best Practices**
   - Use **environment variables** or **ConfigMaps** to inject Service DNS names into apps dynamically.
   - Monitor with Azure Monitor for AKS to track inter-service traffic.
   - Scale horizontally with Horizontal Pod Autoscaler (HPA) based on CPU/memory.
   - For Azure-specific integrations, use Azure Container Registry (ACR) for images and Azure AD for auth.

This setup ensures reliable, scalable communication without tight coupling. Start with basic Services, then layer on security/mesh as needed.

[AKS Networking Overview](https://learn.microsoft.com/en-us/azure/aks/concepts-network)
[Kubernetes Services Documentation](https://kubernetes.io/docs/concepts/services-networking/service/)
[AKS Microservices Tutorial](https://learn.microsoft.com/en-us/azure/aks/tutorial-kubernetes-deploy-cluster)
