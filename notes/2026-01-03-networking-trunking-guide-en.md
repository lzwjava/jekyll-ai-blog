---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: What is Trunking in Networking?
translated: false
type: note
---

Question: What is said in the YouTube video at https://www.youtube.com/watch?v=bQ6D77QeMMg?

Answer: 

The video is a short educational explainer titled **What is Trunking in Networking?** from the channel CBT Nuggets, uploaded on May 6, 2024.

It features instructor Jeremy explaining the concept of trunking in computer networking, particularly in relation to VLANs (Virtual Local Area Networks). Here is the full spoken transcript (auto-generated with minor corrections for readability):

"If someone were to ask me, 'Jeremy, what's the most important thing I should know about trunking?' This is exactly what I would say: Trunking allows you to carry multiple VLANs between devices. So to really understand trunking, you need to make sure that you have a foundational understanding of VLANs.

VLANs allow you to separate your network into multiple subnetworks. That is, a VLAN equals a subnet. And a lot of people miss that correlation. VLAN is the Layer 2 concept—meaning down at the switching layer—that we can use to segment our networks into multiple broadcast domains. And any time you do that, essentially you've introduced a router or a routed network in the middle. And that's why VLANs equaling a subnet is a logical concept that we can tie together, where we link the Layer 2 concept with the Layer 3.

Now, if we could only do VLANs on one device, that would be a major problem—it would be a major scalability limit. So what we do is enable trunking, which is actually a Cisco word, on all of these links between switches.

Now, does that mean that our VLANs only go between Cisco switches? No, it does not. That's because trunking is an industry-standard thing, and that's why everybody else in the world calls trunking 'tagging.' And I actually like that a little bit better than the 'trunking' word.

See, Cisco was first to the game when they came out with this ISL (Inter-Switch Link) trunking. This was the ability to run VLANs between Cisco switches. But obviously, the industry is going to catch up—you have HP, you have Force10, you have all of these other switch vendors: Juniper, you know, all the other ones that I can't think of right now, but for good reason. They all caught up, and eventually the industry said, 'We need an industry-standard 802.1Q trunking protocol.' And that has now replaced ISL 100%.

So now with 802.1Q, you have a language where, as traffic moves from your devices—let's just say we have a client down here that joins the wireless access point. He joins the public SSID, right? And you've configured your wireless access points to tag the public. Whenever somebody joins the public, they're going to be tagged with VLAN 10, let's just say.

As soon as that comes into the switch and exits the link to access other devices—if it's public, probably you've limited it just to the internet, right?—it's going to get a little tag right on the front of that packet that says, 'This belongs to VLAN 10.' Now it is right on the front, and that means that all of the devices that do not understand VLANs will not be able to process that packet. They're going to look at it and say, 'Ah, there's bad data in here.'

So all of your switches have to be configured to support that 802.1Q tagging or trunking method, right? So that's what a trunk does: allow you to carry that tagged traffic from device to device.

And if you're using a router-on-a-stick design—which is a router that's configured to process multiple VLANs using subinterfaces, right?—you'll actually have an 802.1Q trunk configured between switch and router as well. And that's a very common design in small and even in a lot of midsize businesses, because routers have continued to get faster and faster connections, and for the internet, it works just fine, right?

So that is—when I say the real trunking protocol, I'm not being dramatic; I'm just trying to say there is one and only one that is supported: 802.1Q by the world today.

Now, mind you, I brought a server into this picture because it's not just switches that support trunking. You can do a trunk to a server, and that means that server is probably doing virtualization—that is, VMware, Hyper-V, those kinds of things—where you can actually create virtual machines and put them on different VLANs even though they're running on the same device.

Same thing here: when you look at an IP phone, the IP phone can actually have a computer daisy-chained from it, and you can run—I'll call it a mini-trunk. Cisco wouldn't agree with me; they'd say, 'No, it's a voice VLAN.' It's a mini-trunk. It's a trunk that's throttled just to allow the voice VLAN to be the tagged VLAN.

So as it comes into the phone, the phone's like, 'Ah, I understand that' because it can read 802.1Q tags—because phones are smart, and that's what they're designed to do. The untagged traffic comes from the computer. So it's kind of like this very little trunk that runs to the phone. That is all done with the industry-standard 802.1Q.

The fake trunking protocol—some of you might remember—is actually called VTP. Cisco created this; they called it, unfortunately, the VLAN Trunking Protocol. How confusing is that? It should have been called the VLAN Replication Protocol, because what it does is replicate VLANs between switches.

So, take a look right here—let me just clear all this off. I'll put VTP. It's the fake trunking protocol, right? As you create VLAN 10, 20, and 30 on whatever VLANs you want to create on those switches—instead of having to add them here and add them here and add them here—VTP can just go and replicate it.

And this is where it gets its name: over trunk links. So if you have this configured as what kind of trunk? An 802.1Q trunk, right? If that is configured as a real trunk, then the fake trunking protocol VTP can actually replicate the VLANs so they automatically show up on the switches down below.

Now, that doesn't mean the ports automatically get assigned to the VLANs—that's still a you-and-I job, right? We have to have some work that we do. So we have to go down to the switch and assign the ports, but we do not have to create the VLANs if we're using the fake trunking protocol called VTP—because it's not a trunking protocol at all; it's a replication protocol that works over trunk links, right?

Last thing: the Dynamic Trunking Protocol—this guy right here, DTP—is another Cisco creation that was designed to make things easy but in the end made things kind of hard, and that is at least for you and I to remember.

DTP allows the switches to negotiate and figure out trunks on their own, right? Switches can recognize switches if you're using DTP, and that allows them to say, 'Hey, I'd like to be a trunk.'

It's because DTP has two major modes: Auto and Desirable, right? I'll just put Auto and Desire. Auto mode sits there and passively waits for somebody to try and be a trunk. So if you had all your switch ports—let's just say all these switch ports were in auto mode—it would just be like, 'Hey, I could be a trunk. It's kind of like if you want to, I'll do it, but I'm not going to push the issue, right? If you're not going to want to be a trunk...'"

(The transcript cuts off slightly at the end, likely due to the video's conclusion.)

In summary, the video teaches that **trunking** (specifically 802.1Q tagging) is the standard way to extend multiple VLANs across switches and other devices, distinguishing it from Cisco-specific features like VTP (VLAN replication) and DTP (automatic trunk negotiation).

References:  

- [YouTube Video: What is Trunking in Networking?](https://www.youtube.com/watch?v=bQ6D77QeMMg)