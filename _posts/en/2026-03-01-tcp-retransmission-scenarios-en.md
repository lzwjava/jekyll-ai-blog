---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Retransmission Scenarios Explained
translated: false
type: note
---

Question: Go on (continue organizing the transcript from the YouTube video "3.5-1 TCP Reliability, Flow Control, and Connection Management" Part 1).

Answer: 

Here is the next continuation of the organized transcript from Jim Kurose’s lecture. As before, the original spoken wording is kept as faithfully as possible (including natural phrasing, repetitions for emphasis, and lecture-style delivery), while being structured into clear sections with paragraph breaks and light punctuation for coherence. This section picks up right after the introduction of Fast Retransmit and moves into retransmission examples and scenarios, which form the core of the second half of Part 1.

**Retransmission Scenarios — Illustrating TCP in Action**

Now let’s look at some specific scenarios to see how the TCP sender and receiver behave together when things go wrong — when segments are lost, ACKs are lost, or timeouts occur prematurely.

**Scenario 1: Simple Timeout and Retransmission**

Suppose the sender sends segment 1 (sequence number 1000, 500 bytes of data). The timer starts.  
The segment is lost — never reaches the receiver.  
After the timeout interval expires, the sender retransmits segment 1 (same sequence number 1000).  
This time the segment arrives, the receiver sends back an ACK saying “next expected byte is 1500” (cumulative ACK).  
The sender receives that ACK, removes the data from the send buffer, and everything continues normally.

This is the basic Go-Back-N style recovery we already know.

**Scenario 2: ACK is Lost**

Sender sends segment 1 (seq=1000, 500 bytes).  
Receiver gets it, sends ACK 1500.  
But that ACK is lost on the way back.  
The sender’s timer eventually expires → sender retransmits segment 1.  
Receiver gets the duplicate segment 1. Because it has already delivered bytes 1000–1499 to the application and is expecting 1500 next, it simply discards the data (but still sends another cumulative ACK 1500).  
Sender receives the (second) ACK 1500 and moves forward.

Key point: duplicate segments are handled safely thanks to cumulative ACKs and sequence numbers.

**Scenario 3: Premature Timeout (Unnecessary Retransmission)**

Sender sends segment 1 (seq=1000, 500 bytes) and segment 2 (seq=1500, 500 bytes) in the same flight (pipelined).  
Both arrive at the receiver.  
Receiver sends cumulative ACK 2000 (acknowledging both).  
But suppose that ACK is delayed (due to congestion or queuing).  
Sender’s timer for segment 1 expires before the delayed ACK arrives → sender retransmits segment 1.  
Shortly afterward the delayed ACK 2000 arrives.  
Sender sees that ACK 2000 covers the retransmitted segment 1 (and more), so it removes both segments from the buffer and continues.

This is an example of an unnecessary retransmission — wasteful, but correct. TCP prefers to retransmit rather than risk leaving data undelivered.

**Scenario 4: Multiple Segments Lost — Cumulative ACK Helps Later**

Sender sends segments 1, 2, 3, 4 (each 500 bytes, seq 1000, 1500, 2000, 2500).  
Segment 2 is lost; 1, 3, and 4 arrive.  
Receiver delivers segment 1 to application (in-order), buffers 3 and 4, sends duplicate ACK 1500 (next expected = 1500).  
When segment 3 arrives again (duplicate), still duplicate ACK 1500.  
Same for segment 4.  
Sender eventually times out on segment 2, retransmits it.  
Receiver gets segment 2, now has 2,3,4 in buffer → delivers all of them to application, sends new cumulative ACK 3000.

This shows how cumulative ACKs allow the receiver to “catch up” once the missing segment arrives.

**Fast Retransmit in Action**

Now let’s see why Fast Retransmit is so valuable.

Same setup: segments 1,2,3,4 sent. Segment 2 lost.  
Receiver receives 1 → ACK 1500  
Receives 3 → duplicate ACK 1500  
Receives 4 → duplicate ACK 1500 (third duplicate)  
Sender sees three duplicate ACKs for 1500 → immediately retransmits segment 2 (seq=1500) without waiting for timeout.  
Receiver gets segment 2, delivers 2,3,4 to application, sends ACK 3000.  
Sender receives ACK 3000 and continues.

Fast Retransmit typically detects loss much earlier than the full timeout — often cutting recovery time significantly.

**Why Three Duplicate ACKs?**

Why three, not two or four?  
If only one duplicate ACK, it could be caused by normal reordering (segment arrives out of order temporarily).  
Two duplicates still possible with mild reordering.  
Three duplicates is a strong signal that a segment is missing — reordering of three or more segments is very rare in the Internet.  
So three is a good engineering compromise: fast detection without too many false positives.

(Note: This concludes the main retransmission scenarios and Fast Retransmit discussion usually covered in Part 1 of this lecture. The video typically ends here or shortly after a quick preview of flow control and connection management, which are covered in more depth in Part 2 or the next lecture segment.)

References:  

- [YouTube Video: 3.5-1 TCP Reliability, Flow Control, and Connection Management](https://www.youtube.com/watch?v=UYJP-6mhF6E)
- [Playlist: Computer Networking: A Top-Down Approach - All Chapters](https://www.youtube.com/playlist?list=PLByK_3hwzY3Tysh-SY9MKZhMm9wIfNOas)