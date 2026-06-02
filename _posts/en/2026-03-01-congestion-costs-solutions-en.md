---
audio: false
generated: true
image: false
lang: en
layout: post
title: Congestion Control Costs and Solutions
translated: false
type: note
---

Question: Continue the organized transcript from the YouTube video and provide the latter part.

Answer:

**Organized Transcript: 3.6 Principles of Congestion Control (continued)**
*(Lecture by Jim Kurose, from Computer Networking: A Top-Down Approach)*

...even though two copies arrived. So here we have the case of unnecessary retransmissions — sometimes called “spurious retransmissions” or “premature timeouts.”

In this situation the throughput (goodput) — the rate at which useful data is delivered to the application — is actually less than the arrival rate of original data, because some of the bandwidth is being wasted on duplicate packets that the receiver discards.

Now let's put all of these pieces together and look at the overall relationship between the offered load (the aggregate arrival rate of original data from all senders) and the goodput (the aggregate throughput of useful data delivered to the receivers).

When the offered load is small, almost no packets are lost, almost no retransmissions occur, and goodput rises linearly with offered load — slope close to 1. As offered load increases, we start to see occasional buffer overflows, some retransmissions are needed, and the goodput still increases but with a slope less than 1. Eventually, as offered load continues to increase, more and more retransmissions are needed, many of them carrying duplicate data. The router is increasingly spending its transmission capacity sending and re-sending the same packets, and the goodput actually starts to decrease even though offered load keeps increasing.

At very high offered load the vast majority of link capacity is being used to send duplicate copies of packets that were already successfully delivered earlier. In the extreme case, goodput can approach zero — this is sometimes called “congestion collapse.”

This graph is one of the most famous in networking: it shows the knee and then the cliff of congestion collapse. The key point is that as soon as offered load exceeds the capacity that the network can carry without loss (roughly the point where queues start building significantly), goodput stops increasing and eventually falls dramatically. This is the fundamental cost of congestion when there is no effective congestion control.

So we've now seen several costs of congestion:

1. Large queuing delays (even with infinite buffers)
2. Packet loss requiring retransmissions (with finite buffers)
3. Wasted bandwidth on duplicate packets due to premature timeouts
4. Goodput collapse — in the extreme case, network throughput approaching zero while offered load is very high

These observations lead us to two broad approaches to congestion control:

**End-to-end congestion control**
The network provides no explicit feedback to the senders about congestion. The senders must infer congestion from their own observations — typically packet loss and/or increasing delay. TCP follows this approach.

**Network-assisted congestion control**
The network provides explicit feedback to the senders about congestion. This feedback can come in two forms:

- Direct notification from the congested router to the sender (“backwards” explicit congestion notification)
- A router marks or sets a bit in packets going forward to the receiver, and the receiver then feeds this information back to the sender (“forward” explicit congestion notification)

Examples of network-assisted approaches include DECbit (early 1980s), Explicit Congestion Notification (ECN) in IP, and various ATM ABR schemes.

In the next video/section we will see how TCP combines end-to-end approaches with several specific mechanisms (slow start, congestion avoidance, fast retransmit, fast recovery) to implement congestion control in practice — all without any help from the network layer.

That concludes our high-level principles of congestion control. We’ve seen the causes, the costs, and the two fundamental philosophies for dealing with it.

[Music]

*(End of section 3.6)*

References:

- [Original Video: 3.6 Principles of Congestion Control](https://www.youtube.com/watch?v=Fm92xvIp6JY)
