---
audio: false
generated: true
image: false
lang: en
layout: post
title: Principles of Network Congestion Control
translated: false
type: note
---

Question: Organize this transcript from the YouTube video (https://www.youtube.com/watch?v=Fm92xvIp6JY), keeping the original text as much as possible while making it more coherent.

Answer:

**Organized Transcript: 3.6 Principles of Congestion Control**
*(Lecture by Jim Kurose, from Computer Networking: A Top-Down Approach)*

[Music]

In this section we're gonna take a big picture view of congestion control — really looking for a principled understanding of both the causes and the costs of congestion. We'll identify two basic approaches for dealing with congestion.

In the next section we're going to take a look at TCP and how it actually implements these principles, but for now we're going to step back and take the big picture view. So you can put your pens and pencils down and sit back, think, listen — put your thinking caps on, as the saying goes. I think you're going to really enjoy this. And remember, congestion control really is a top five issue in computer networking, so pay attention.

Well, let's start by asking the most basic question: what do we mean by congestion? Well, informally, congestion is all about too many sources sending too many packets too fast for a congested network link somewhere in the network to handle.

Now remember that links have a transmission rate, and when the arrival rate of packets exceeds the transmission rate, queues will start to build up and delays will get larger and larger. And if the link's packet buffers fill up completely, arriving packets will be dropped and lost.

It's important to remember that congestion control is really about multiple senders sending too fast in aggregate, while flow control — which we studied in the last section — is really about speed matching between a single sender and a single receiver.

So with that as background, let's dive into the causes and the costs of congestion. We'll do this by starting with a simple idealized scenario — you know, idealized scenarios are something that professors love to think about — and then we'll start adding increasingly more realistic assumptions.

So let's start with the scenario shown here. We'll look at the case of a single router where congestion will occur. First assume that there's an infinite amount of buffering (that's idealized, of course). The router has input and output links of capacity R bits per second, and there are two flows: the red flow and the blue flow shown here.

Let's take a careful look at the flow rates associated with the red flow. On the sending side there's λ_in — that's the rate at which data is being sent from the application layer down to the transport layer. And at the receiving side there's λ_out, which we'll refer to as the throughput — that's the rate at which data is actually delivered up to the application layer at the receiver.

And we'll want to ask the question: what happens to the throughput as we dial up the arrival rate on the sending side, assuming that we increase the arrival rate for the red and the blue flows similarly?

Well, with the case of infinite buffering, no packets are lost — every packet that is sent is eventually received. And so the throughput at the receiver equals the sender's sending rate, as shown in the plot here. Note though that the x-axis ends at R/2, since if each sender were sending at a rate faster than R/2, the throughput would simply max out at R/2 per flow. That's because the router's input and output links can't carry more than R bits per second of traffic — R/2 for each of the two flows.

Well, this looks pretty good, at least from the throughput standpoint. But remember we learned in Chapter 1 that when the arrival rate to a link comes close to the link's transmission rate, large queuing delays can occur, as shown here. And so we see already that there are costs in this case: the delay costs, even in this idealized scenario.

Let's see now what happens when we drop this unrealistic assumption about infinite buffering. So let's consider the same scenario except that now the amount of buffering is going to be finite.

Recall from our study of reliable data transfer that we learned that senders are going to retransmit in the face of possible packet loss due to buffer overflows or corruption. So we're going to need to look a little bit more carefully now at the sending rate. In particular, we'll want to make a distinction between:

- the rate of original data that's being passed down from the application — we'll denote that λ_in
- and the overall rate at which the transport layer is sending data, including retransmissions — we'll denote this as λ_in' (lambda in prime)

The rate at which packets arrive to the router is λ_in', not λ_in. Make sure you've got this distinction between λ_in and λ_in' — it's really important. And as noted here, λ_in equals λ_out, and λ_in' is going to be greater than or equal to λ_in since it's going to include the retransmissions.

Alright, for this case of finite buffers, let's start with an idealized scenario still and let's imagine that somehow magically the sender knows whether or not there will be free buffer space for a transmitted packet. So in this case no packets are going to be lost. The source sends a packet, it's just buffered at the router, eventually transmitted, and received at the receiver. In this case no packets are lost and the throughput λ_out here on the y-axis equals λ_in. No problems here — well, except for the queuing delays as λ_in approaches R/2, just as in our first scenario.

So let's next relax this assumption that the sender somehow magically knows when there's going to be free buffer space, and consider what happens when packets can be lost at the router when they arrive and there's no free buffer space.

Here we see a packet arriving to find the buffers full — it's lost, and so a copy of the packet is retransmitted by the sender eventually, and in this case finds free buffer space, advances into the buffer, and is eventually transmitted by the router and received at the destination.

In this case, when retransmissions occur because of known loss, the plot showing the overall arrival rate versus throughput looks something like this. At a low arrival rate, buffers will almost always be available and every originally transmitted packet is going to make it through. So in the slow arrival region, the arrival rate including retransmissions (which really don't occur very often) essentially equals the receiver throughput. A unit increase in the overall arrival rate λ_in' equals a unit increase in the throughput λ_out — that is to say that the slope of this red curve here is close to one.

What's much more interesting is the high arrival rate region here. Here the arriving packets increasingly include retransmitted packets, and so the receiver throughput no longer increases one-for-one with an increase in the overall arrival rate. And we see that as the overall arrival rate on the x-axis approaches R/2 (can't go any higher), the maximum throughput at the receiver is actually less than R/2. This gap here — and this is important to note — is because n retransmitted copies of a packet take up n times the transmission capacity of a single packet, but in the end these n packet transmissions contribute only a single packet to the throughput.

Well now let's see what happens if we drop the unrealistic assumption that all of the retransmissions are actually needed. That is to say, let's assume the sender may timeout prematurely, as shown in the example here, and actually deliver two copies of a packet to the receiver.

In this example the first packet is delayed, and so the sender times out eventually and retransmits, and both packets here eventually make it to the receiver. The receiver of course only delivers one segment's worth of data up to the application layer even though...

*(Note: The provided transcript excerpt ends here mid-sentence. The full video continues to discuss further costs of congestion, including "goodput" collapse and additional scenarios.)*

References:

- [Original Video: 3.6 Principles of Congestion Control](https://www.youtube.com/watch?v=Fm92xvIp6JY)
