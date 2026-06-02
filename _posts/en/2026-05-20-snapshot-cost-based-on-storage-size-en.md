---
audio: false
generated: true
image: false
lang: en
layout: post
title: Snapshot Cost Based on Storage Size
translated: false
type: note
---

Question: Why does a droplet snapshot of size 132.77 GB in AMD Developer Cloud cost around $6 per month? Is this cost related to its size?

Answer:

Yes, the cost of a droplet snapshot is directly related to its storage size. In cloud services like AMD Developer Cloud, DigitalOcean, or AWS, snapshot pricing is typically calculated based on **the amount of data stored**, not the compute resources used. Here’s the breakdown:

1. **Snapshot Size**

   * Your droplet snapshot is **132.77 GB**.
   * Cloud providers usually charge a fixed rate per GB per month for storage.

2. **Cost Calculation Example**

   * If the snapshot costs **$0.045 per GB per month** (a typical rate in developer clouds), the monthly cost is:
     [
     132.77 , \text{GB} \times 0.045 , \text{USD/GB} \approx 5.97 , \text{USD}
     ]
   * That matches the ~$6 per month you observed.

3. **Other Factors**

   * Pricing may vary slightly depending on region (ATL1 in your case), storage type (SSD vs. HDD), and any additional redundancy or backup options.
   * The snapshot is essentially a point-in-time copy of your droplet, so the more data your droplet has, the larger the snapshot, and the higher the storage cost.

**Conclusion:** The ~$6 monthly fee is primarily due to the **size of the snapshot (132.77 GB)**, and yes, it scales proportionally with storage.

References:

* [DigitalOcean Droplet Snapshot Pricing](https://www.digitalocean.com/pricing/)
* [Understanding Cloud Snapshot Costs](https://www.cloudzero.com/blog/cloud-snapshot-costs)
