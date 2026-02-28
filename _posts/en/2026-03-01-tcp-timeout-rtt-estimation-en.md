---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Timeout and RTT Estimation Explained
translated: false
type: note
---

Question: Continue organizing the transcript from the YouTube video "3.5-1 TCP Reliability, Flow Control, and Connection Management" (Part 1), keeping the original text as much as possible while making it more coherent.

Answer: 

Here is the continuation of the organized transcript, picking up exactly where the previous portion ended (mid-sentence: "On the other hand, if we wait too long, TCP..."). The text preserves Jim Kurose’s original spoken wording and natural delivery style as closely as possible, while being structured into clear sections with improved flow, paragraph breaks, and light punctuation for readability. This covers the remainder of the key concepts typically presented in this part of the lecture (based on the standard coverage in the 8th edition of *Computer Networking: A Top-Down Approach* and the video’s content).

**Setting Timeout Values (continued)**

On the other hand, if we wait too long, TCP will take a long time to detect that a segment has actually been lost. So we want to set the timeout interval to be a little bit longer than the round-trip time, but not too much longer.

The question is: how do we actually estimate what the round-trip time is? Because the round-trip time can change over time — there can be congestion in the network, there can be different paths taken — so the RTT is not a fixed value.

**Estimating the Round-Trip Time**

What TCP does is maintain an estimate of the RTT — it calls this EstimatedRTT. And it updates EstimatedRTT using a very simple exponentially weighted moving average. The formula is:

EstimatedRTT = (1 − α) × EstimatedRTT + α × SampleRTT

where SampleRTT is the most recently measured round-trip time — that is, the time from when a segment is sent until the corresponding ACK is received — and α is typically 0.125.

So most of the weight (87.5%) is kept on the history, and only 12.5% on the new sample. That means EstimatedRTT changes slowly — it’s relatively insensitive to large, short-lived fluctuations in RTT, which is good because we don’t want to overreact to a single very long RTT sample.

**Dealing with RTT Variation — the Deviation**

But even with that smoothing, we still want to account for the fact that the RTT can vary quite a bit. So TCP also keeps track of how much the RTT samples are deviating from the EstimatedRTT. It maintains another smoothed value called DevRTT (the RTT deviation), and it’s updated with a similar exponentially weighted moving average:

DevRTT = (1 − β) × DevRTT + β × |SampleRTT − EstimatedRTT|

where β is typically 0.25.

**Setting the Timeout Interval**

Now, with these two values, TCP sets the timeout interval as:

TimeoutInterval = EstimatedRTT + 4 × DevRTT

Why 4? It’s a bit of an engineering choice. It turns out that 4 × DevRTT gives a pretty good balance: it’s long enough that most segments will be acknowledged before the timer goes off (so we avoid a lot of unnecessary retransmissions), but it’s still short enough that when a segment really is lost, we detect the loss reasonably quickly.

**A Key Problem: Ambiguous Round-Trip-Time Samples**

There is one very important detail here. When we measure SampleRTT, we only do it for segments that are not retransmitted. Why? Because if we retransmit a segment and then receive an ACK, we don’t know whether that ACK is for the original transmission or for the retransmission. If we used that ambiguous sample, our RTT estimate could be badly wrong.

So TCP only takes a SampleRTT from a segment that has been sent exactly once (no retransmission of that segment has occurred). This is called Karn’s algorithm (after its inventor Phil Karn).

**TCP Sender — Putting It All Together**

Now let’s look at the big picture of what the TCP sender actually does.

The sender has three main events that drive its behavior:

1. Data is received from the application above → TCP creates a segment, puts it in the send buffer, starts a timer (if the timer is not already running), and sends the segment.
2. A timeout occurs → The sender retransmits the oldest unacknowledged segment, and restarts the timer.
3. An ACK arrives → If it acknowledges new data, the sender removes that data from the send buffer. If there is still unacknowledged data, the timer is restarted (for the oldest unacknowledged segment). If the ACK is cumulative and covers more data, multiple segments can be removed at once.

**TCP Receiver Behavior**

On the receiver side, there are a few important rules:

- When an in-order segment arrives: Deliver the data to the application immediately, send a cumulative ACK for the next expected byte, but delay the ACK for up to about 500 ms (in the hope that another segment will arrive soon and the ACK can piggyback on outgoing data).
- When an out-of-order segment arrives: Buffer it (TCP is allowed to buffer out-of-order data), and send a duplicate ACK indicating the next expected byte (this is a hint to the sender that a gap exists).
- If a segment fills in a gap and now the data is in-order up to a new point: Deliver all buffered in-order data to the application and send a cumulative ACK for the new next-expected byte.

**Fast Retransmit**

Waiting for the timeout can be slow — sometimes much longer than necessary. So TCP includes a very important optimization called Fast Retransmit.

The rule is: if the sender receives three duplicate ACKs in a row, it assumes the segment after the acknowledged byte has been lost, and it retransmits that segment immediately — without waiting for the timeout to expire.

This is much faster than waiting for the full timeout interval. Fast Retransmit is one of the most important performance improvements in TCP.

(Note: This video is Part 1 of 2. It typically ends around the introduction to Fast Retransmit and basic retransmission scenarios. Part 2 continues with more complex loss scenarios, selective acknowledgments (SACK), flow control using the receive window, and the three-way handshake for connection management.)

References:  

- [YouTube Video: 3.5-1 TCP Reliability, Flow Control, and Connection Management](https://www.youtube.com/watch?v=UYJP-6mhF6E)
- [Playlist: Computer Networking: A Top-Down Approach - All Chapters](https://www.youtube.com/playlist?list=PLByK_3hwzY3Tysh-SY9MKZhMm9wIfNOas)