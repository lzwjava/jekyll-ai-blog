---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Cost-Effective Markdown to PDF API
translated: false
type: note
---

### Recommended Cheap Option: Google Cloud Run

For a simple Java-based API that converts Markdown to PDF (e.g., using a library like Flying Saucer or iText), with only ~100 requests per week for personal blog use, **Google Cloud Run** is the most cost-effective choice. It's a serverless platform that runs containerized apps, scales to zero when idle, and only charges for actual usage. No need to manage VMs or worry about always-on costs—perfect for low-traffic scenarios like yours.

#### Why Cloud Run Over Other Options?

- **Vs. Compute Engine (VMs)**: VMs have fixed hourly costs even when idle, which would be overkill and more expensive (~$5–10/month minimum for a tiny instance).
- **Vs. App Engine**: Similar serverless benefits, but Cloud Run is more flexible for Java containers and often cheaper for sporadic use.
- Your workload fits entirely within the free tier, so expect **$0/month** in practice.

#### Estimated Costs

With 100 requests/week (~400/month):

- Assume each request uses 1 vCPU and 0.5 GiB memory for 10 seconds (conservative for a quick Markdown-to-PDF conversion).
- Total usage: ~4,000 vCPU-seconds and ~2,000 GiB-seconds/month.
- **Free tier covers it all**: 180,000 vCPU-seconds, 360,000 GiB-seconds, and 2 million requests per month (in most regions).
- If you exceed (unlikely), paid rates are ~$0.000024/vCPU-second + $0.0000025/GiB-second + $0.40/million requests after free limits—still under $0.10/month.

No egress fees for your use case (internal API calls stay free within the same region).

#### Recommended Region: us-central1 (Iowa)

- This is the cheapest Tier 1 region for Cloud Run, with the lowest rates for compute and no premium for latency in North America.
- Pricing is similar across Tier 1 regions (US/Europe), but us-central1 edges out on average instance costs.
- If you're outside North America (e.g., Europe or Asia), switch to the closest Tier 1 region like europe-west1 (Belgium) for better latency—costs differ by <10%.
- Avoid Tier 2 regions (e.g., asia-southeast1) as they're 20–50% more expensive.

#### Quick Setup Guide for Your Java Server

1. **Build your app**: Use Spring Boot for a simple REST API. Endpoint example: POST `/convert` with Markdown body, return PDF.
   - Add dependency: `implementation 'org.xhtmlrenderer:flying-saucer-pdf:9.1.22'` (or similar).
   - Sample code snippet:

     ```java:disable-run
     @RestController
     public class MarkdownController {
         @PostMapping("/convert")
         public ResponseEntity<byte[]> convert(@RequestBody String markdown) {
             // Convert logic here (e.g., markdown to HTML, then to PDF)
             byte[] pdfBytes = // your conversion result;
             return ResponseEntity.ok()
                 .header("Content-Type", "application/pdf")
                 .body(pdfBytes);
         }
     }
     ```

2. **Containerize**: Create a `Dockerfile`:

   ```
   FROM openjdk:17-jdk-slim
   COPY target/your-app.jar app.jar
   ENTRYPOINT ["java", "-jar", "/app.jar"]
   ```

   Build: `docker build -t gcr.io/your-project/markdown-api .`
3. **Deploy to Cloud Run**:
   - Enable Cloud Run API in GCP Console.
   - `gcloud run deploy markdown-api --image gcr.io/your-project/markdown-api --platform managed --region us-central1 --allow-unauthenticated --memory 512Mi --cpu 1 --max-instances 1`
   - Get the URL: `https://markdown-api-abc.run.app/convert`
4. **Test**: Send a Markdown POST request; it auto-scales.

Sign up for the $300 free trial if new to GCP. Monitor costs in the Billing dashboard.

[Cloud Run Pricing](https://cloud.google.com/run/pricing)
[GCP Regions Guide](https://www.cloudzero.com/blog/gcp-regions/)
[Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts/build-and-deploy)

```
