---
audio: false
generated: true
image: false
lang: en
layout: post
title: Optimizing Cloud Choice for Fun Live
translated: false
type: note
---

**My answer: Alibaba Cloud Hong Kong is a reasonable candidate, but I would not commit to the architecture you pasted without validating several assumptions.** The strongest choice depends on where your users are, how you deliver live video, and whether you need China-specific integrations.

For your situation, I would optimize for three things:

1. **Minimize fixed costs.** You're rebuilding a product while developing AI consultancy revenue, so you should avoid paying for infrastructure before you have users.
2. **Preserve the ability to serve Chinese and international users.** Fun Live previously reached around 30,000 users, and your new product could target users in mainland China, Hong Kong, Singapore, and the US.
3. **Avoid unnecessary infrastructure complexity.** You can operate a lean application first and introduce managed video, specialized networking, and multiple regions when actual demand justifies them.

The key distinction is that **Alibaba Cloud Hong Kong may be a good deployment choice, but it does not automatically solve mainland connectivity, regulatory compliance, or global distribution.**

## 1. First, correct three important claims

I checked Alibaba Cloud's current documentation. Three points in the proposed design need qualification.

### A. Hong Kong hosting does not require ICP filing

This part is correct.

Alibaba Cloud states that servers in Hong Kong and other overseas regions do not require an MIIT ICP filing, unlike servers in mainland China. [Alibaba Cloud Help Center](https://help.aliyun.com/en/icp-filing/basic-icp-service/user-guide/icp-filing-application-overview?utm_source=chatgpt.com)

However, this doesn't mean every service targeting mainland users is exempt from every applicable Chinese regulatory requirement.

### B. Global Accelerator is not automatically a solution without ICP

This is the biggest technical qualification.

Alibaba Cloud explicitly states that if your Global Accelerator configuration includes mainland China acceleration for HTTP/HTTPS traffic, your domain needs a valid ICP filing. Without one, acceleration fails. [AlibabaCloud](https://www.alibabacloud.com/help/en/ga/support/faq-about-global-accelerator?utm_source=chatgpt.com)

Therefore, I would **not include mainland Global Accelerator in your initial architecture**.

Start with a Hong Kong origin and test real connectivity from mainland China. Add networking services only after you establish that ordinary connectivity is inadequate and verify the applicable requirements.

### C. Managed live streaming can become more expensive than the application servers

ApsaraVideo Live is attractive because you don't have to operate your own streaming infrastructure. However, bandwidth and processing costs matter.

Alibaba's published pricing lists standard live-streaming traffic at approximately $0.07/GB for North America and $0.081/GB for its first Asia-Pacific tier, which includes Hong Kong and several other markets. Actual billing depends on the applicable region, pricing tier, and service configuration. [AlibabaCloud](https://www.alibabacloud.com/en/product/apsaravideo-for-live/pricing?_p_lc=1\&utm_source=chatgpt.com)

For illustration:

| Monthly video delivery | North America | Asia-Pacific tier 1 |
| --- | ---: | ---: |
| 100 GB | $7 | $8.10 |
| 1 TB (1,000 GB) | $70 | $81 |
| 10 TB | $700 | $810 |

These are illustrative traffic charges, not complete bills. They exclude transcoding, recording, storage, and other applicable fees.

**The implication:** Don't migrate to managed video merely because it's managed. First estimate your actual video consumption.

---

## 2. How I would choose between Alibaba Cloud, GCP, and AWS

For Fun Live, I would evaluate the options like this:

| Requirement | Alibaba Cloud Hong Kong | GCP | AWS |
| --- | --- | --- | --- |
| Hong Kong application hosting | Good fit | Good fit | Good fit |
| Mainland China access without ICP | Possible, but must be tested | Possible, but must be tested | Possible, but must be tested |
| Mainland-specific cloud integrations | Strong ecosystem | Less China-centric | Less China-centric |
| Managed live video | ApsaraVideo Live | Generally requires a third-party service or self-hosting | Amazon IVS is an option |
| Global infrastructure and tooling | Good | Strong | Strong |
| Existing workloads using Docker | Straightforward to migrate | Straightforward to migrate | Straightforward to migrate |
| Best reason to choose it | China-oriented product | Google Cloud ecosystem or existing GCP workloads | AWS ecosystem or existing AWS workloads |

This is a practical comparison, not a claim that one provider always delivers better mainland latency. Routing varies by ISP, location, time, and network configuration.

The most important factor is whether your existing product depends on particular integrations, not which cloud has the most impressive product catalog.

## 3. My recommendation: start with Alibaba Cloud Hong Kong, but keep the architecture simple

Assuming you want to restore Fun Live, preserve its live-video capabilities, and serve international users, this is the architecture I would start with.

```text
                   Users
          ┌──────────┼──────────┐
          │          │          │
       Mainland   HK / SG      US / EU
          │          │          │
          └──────────┼──────────┘
                     │
                DNS / HTTPS
                     │
          Alibaba Cloud Hong Kong
                     │
          ┌──────────┴──────────┐
          │                     │
       Web/API               MySQL
       Docker                Managed DB
          │
      ┌───┴────────┐
      │            │
   Redis       Live Video
                   │
             ┌─────┴─────┐
             │           │
         Existing SRS   Managed
         (self-hosted)  Apsara Live

          Object Storage
          Replays / Images
```

You don't need every component on day one.

### Phase 1: Get the application running

Use:

- **ECS:** Run your existing Docker Compose stack.
- **MySQL:** Keep your existing database temporarily if migration risk is significant.
- **Redis:** Keep it only if the application actually requires it.
- **SRS:** Retain your current streaming server.
- **OSS:** Introduce it for uploads and recordings when useful.
- **Cloudflare:** Consider it for DNS, TLS, and suitable caching.

Deploy in Hong Kong and verify that your API, database, authentication, and video flows work.

I would initially avoid Kubernetes, a load balancer, Global Accelerator, and multiple regions. They add operational cost and complexity without necessarily improving the experience for your current traffic.

### Phase 2: Measure performance from real users

Test from at least four locations:

| Location | What to measure |
| --- | --- |
| Guangzhou or Shenzhen | API latency, connection failures, playback startup |
| Hong Kong | API latency and video playback |
| Singapore | API latency and video playback |
| US West Coast | API latency and video playback |

Measure:

- API p50 and p95 latency.
- TCP connection success rate.
- Video startup time.
- Video rebuffering rate.
- Playback failures.
- Monthly bandwidth per active user.

For example, a simple API probe:

```bash
URL="https://api.example.com/health"

for i in $(seq 1 100); do
  curl -sS -o /dev/null \
    -w '%{time_connect} %{time_starttransfer} %{time_total}\n' \
    "$URL" || echo "request_failed"
done
```

Replace the example URL with your real endpoint.

Run this from machines in each target market. This measures real network behavior rather than relying on a cloud provider's marketing claims.

For production, also collect failures, timeouts, and percentile distributions; don't base decisions on averages alone.

**Important:** If mainland users experience poor connectivity, first identify whether the bottleneck is DNS, TCP/TLS establishment, API processing, or video delivery. Each requires a different solution.

### Phase 3: Decide whether managed video is worth it

Keep SRS if:

- Your traffic is small.
- You already know how to operate it.
- You can tolerate managing streaming infrastructure.
- Your current video requirements are straightforward.

Evaluate ApsaraVideo Live if:

- You need adaptive bitrate transcoding.
- You expect unpredictable viewer spikes.
- You want managed ingest and distribution.
- Operating SRS is consuming too much engineering time.

Alibaba supports both standard streaming and its lower-latency RTS service, with different protocols and pricing. RTS is not simply a cheaper replacement for standard streaming. [AlibabaCloud](https://www.alibabacloud.com/help/en/live/product-overview/billing-overview?utm_source=chatgpt.com)

For Fun Live, I'd start with SRS and compare the actual operating cost against managed video after estimating viewer-hours and bandwidth.

---

## 4. What about payments, SMS, and compliance?

These are important, but I would treat them as separate decisions from your cloud provider.

### Payments

Choose the payment integration based on your actual customers and legal business entity.

- Mainland Chinese customers: investigate Alipay and WeChat Pay eligibility.
- International customers: investigate an international payment provider.
- Mixed market: design a payment abstraction so you can support multiple providers.

Alibaba Cloud doesn't automatically grant you access to every domestic payment integration simply because you host on its infrastructure.

### SMS

Use a provider that supports your target countries, sender requirements, and authentication workflow.

You may need different routes for mainland Chinese phone numbers and international numbers. Test delivery rates and total costs before migrating your existing authentication system.

### Data compliance

Don't assume that storing all mainland customer information in Hong Kong automatically satisfies Chinese data protection requirements.

Your obligations depend on the data involved, your business, the applicable rules, and whether cross-border transfer requirements apply.

For a paid livestreaming product, separately assess the regulatory requirements for the content, platform operation, payments, and user data. An overseas server does not eliminate those questions.

---

## 5. The decision rule I'd actually use

Here is my practical recommendation for your situation:

| Your situation | My choice |
| --- | --- |
| Rebuilding Fun Live with limited initial traffic | Alibaba Cloud HK, existing Docker stack |
| Primarily international users and existing GCP infrastructure | GCP HK |
| Primarily international users with existing AWS infrastructure | AWS |
| Need managed live-video delivery | Compare ApsaraVideo Live and Amazon IVS against actual usage |
| Need reliably optimized mainland access | Benchmark first; investigate compliant network acceleration |
| Need mainland hosting and domestic distribution | Evaluate mainland infrastructure and its filing and licensing requirements |

Google Cloud has a Hong Kong region (`asia-east2`), so you aren't choosing between a Hong Kong deployment and a deployment elsewhere. [Google Cloud Documentation](https://docs.cloud.google.com/compute/docs/regions-zones?utm_source=chatgpt.com)

### One additional consideration: avoid a premature migration

If your current application already runs in Docker, most of your application code should not care whether the VM runs on Alibaba Cloud, GCP, or AWS.

Keep the deployment portable:

```text
Application
  ├── Docker Compose
  ├── Environment-based configuration
  ├── Database migrations
  ├── Object-storage interface
  ├── Payment-provider interface
  └── Streaming-provider interface
```

You can then move infrastructure without rewriting the product.

The main sources of cloud lock-in are usually managed services, networking assumptions, IAM, storage APIs, and observability—not Docker itself.

## References

- [Alibaba Cloud: ICP filing requirements](https://www.alibabacloud.com/help/en/icp-filing/basic-icp-service/user-guide/icp-filing-application-overview)
- [Alibaba Cloud: Global Accelerator FAQ](https://www.alibabacloud.com/help/en/ga/support/faq-about-global-accelerator)
- [Alibaba Cloud: ApsaraVideo Live pricing](https://www.alibabacloud.com/en/product/apsaravideo-for-live/pricing)
- [Google Cloud: Compute Engine regions and zones](https://docs.cloud.google.com/compute/docs/regions-zones)
- [Amazon IVS: Pricing](https://aws.amazon.com/ivs/pricing/)

**My next step would be to build a cost model for Fun Live using your real architecture:** ECS, database, storage, live-video traffic, and expected monthly viewer-hours. That would tell us whether Alibaba HK is genuinely cheaper than GCP, rather than choosing based on assumptions about either provider.
