---
audio: true
generated: false
image: false
lang: en
layout: post
title: Smart Charging Solutions
type: post
---

### Table of Contents

1. [Forgetfulness about Charging Power Banks](#forgetfulness-about-charging-power-banks)
   - The Recurring Problem of Dead Power Banks
   - Multiple Device Management Challenges
   - Psychology Behind Charging Forgetfulness
   - Current Power Bank Collection (30,000 mAh Total)
   - Practical Solutions and Workarounds

2. [Smart Universal Charger Box](#smart-universal-charger-box)
   - Concept Design and Visualization
   - Ultrasonic Cleaner-Inspired Solution
   - Wireless Charging Protocol Integration
   - Cloud-Connected Smart Home Vision
   - Universal Device Compatibility
   - MagSafe Technology Applications

## Forgetfulness about Charging Power Banks

The problem of often forgetting to charge power banks has been frustrating me.

I have two small electric lamps that I've been using recently. I had two power banks a week ago and I have three mobile phones. I was frustrated to find that both of my power banks were out of electricity, so I bought a third one.

I was initially happy to have three power banks, but the happiness didn't last long. Today, I found that all three of my power banks were out of electricity, and I needed one to charge my iPhone 14 Pro Max.

Why did this happen?

The reason is that I often forget to charge them after using them. Regardless of how many power banks I buy, if I don't charge one after using it, I will eventually deplete all of them.

The first power bank is a Ugreen MagSafe wireless power bank with a 10,000 mAh capacity. The second and third ones are power banks with built-in cables, both also with 10,000 mAh capacities.

When they are all fully charged, I have 30,000 mAh of portable electricity. If I use some of them, I need to recharge them to maintain a considerable amount of power.

But why do I forget to charge them? It's similar to being lazy about washing dishes after a meal, even though it just means putting the dishes in the dishwasher.

Charging the power bank is very easy. I just need to stand up from my reclining pillow and walk one meter away to plug it in.

It's not about the effort or energy. In many cases, I just don't want anything to interrupt my activities like writing blogs, chatting with AI chatbots, or writing code.

Recently, I bought a power strip to help charge my Mac laptop as I work in bed, since there are no sockets nearby.

So, my solution is to use that power strip to charge my three phones as well. This way, I can use the power banks less frequently if I don't want to charge them. A power strip has sockets in it, so it's like having sockets near the bed.

Another solution is to use the Shortcuts app in iOS to set a notification to remind me to check or charge the power banks at a certain time each day.

By the way, I thought of a new kind of charging method: a [Smart Universal Charger Box](./charger-box-en). I introduced it in another article. Actually, this is a different problem. It is about how to charge, not about solving the issue of forgetting to charge power banks.

---

## Smart Universal Charger Box

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 400">
  <!-- Charger Box -->
  <rect x="50" y="50" width="400" height="300" rx="20" fill="#f0f0f0" stroke="#333" stroke-width="3"/>

  <!-- Wireless charging pad base -->
  <rect x="70" y="320" width="360" height="10" fill="#4a90e2" opacity="0.3"/>

  <!-- Wireless charging waves -->
  <path d="M 70 300 Q 250 280 430 300" stroke="#4a90e2" fill="none" stroke-width="2" opacity="0.5">
    <animate attributeName="d" dur="3s" repeatCount="indefinite"
      values="M 70 300 Q 250 280 430 300;
              M 70 300 Q 250 290 430 300;
              M 70 300 Q 250 280 430 300"/>
  </path>
  <path d="M 70 280 Q 250 260 430 280" stroke="#4a90e2" fill="none" stroke-width="2" opacity="0.3">
    <animate attributeName="d" dur="3s" repeatCount="indefinite"
      values="M 70 280 Q 250 260 430 280;
              M 70 280 Q 250 270 430 280;
              M 70 280 Q 250 260 430 280"/>
  </path>

  <!-- Devices -->
  <!-- Smartphone -->
  <rect x="100" y="150" width="60" height="100" rx="5" fill="#333"/>
  <rect x="105" y="155" width="50" height="85" fill="#666"/>

  <!-- Laptop -->
  <rect x="200" y="150" width="120" height="80" rx="5" fill="#555"/>
  <rect x="200" y="230" width="120" height="10" fill="#444"/>

  <!-- Smartwatch -->
  <rect x="360" y="150" width="40" height="50" rx="5" fill="#777"/>
  <circle cx="380" cy="175" r="15" fill="#999"/>

  <!-- Power Bank -->
  <rect x="100" y="270" width="80" height="30" rx="5" fill="#666"/>

  <!-- Bluetooth Speaker -->
  <rect x="270" y="150" width="70" height="70" rx="10" fill="#888"/>
  <circle cx="305" cy="185" r="25" fill="#999"/>

  <!-- Cloud Connection -->
  <path d="M 250 30 Q 280 10 310 30 Q 330 0 350 30 Q 370 20 360 40 Q 380 50 350 60 Q 340 80 310 60 Q 280 80 270 60 Q 240 70 250 30"
        fill="#4a90e2" opacity="0.6"/>

  <!-- Connection lines to cloud -->
  <line x1="250" y1="60" x2="250" y2="100" stroke="#4a90e2" stroke-width="2" stroke-dasharray="5,5"/>

  <!-- Label -->
  <text x="250" y="380" text-anchor="middle" font-family="Arial" font-size="16" fill="#333">Smart Universal Charger Box</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 400">
  <!-- Box - Isometric View -->
  <!-- Front face -->
  <path d="M 100 150 L 400 150 L 400 350 L 100 350 Z"
        fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <!-- Top face -->
  <path d="M 100 150 L 400 150 L 450 100 L 150 100 Z"
        fill="#e0e0e0" stroke="#333" stroke-width="2"/>
  <!-- Side face -->
  <path d="M 400 150 L 450 100 L 450 300 L 400 350 Z"
        fill="#d0d0d0" stroke="#333" stroke-width="2"/>

  <!-- Charging pad surface (with grid pattern) -->
  <path d="M 120 330 L 380 330 L 420 290 L 160 290 Z"
        fill="#4a90e2" fill-opacity="0.1" stroke="#4a90e2" stroke-width="1"/>
  <path d="M 120 310 L 380 310 L 420 270 L 160 270"
        fill="none" stroke="#4a90e2" stroke-width="0.5" opacity="0.3"/>

  <!-- Devices in isometric view -->
  <!-- Laptop -->
  <path d="M 150 280 L 250 280 L 270 260 L 170 260 Z"
        fill="#555"/>
  <path d="M 150 240 L 250 240 L 250 280 L 150 280 Z"
        fill="#666"/>

  <!-- Smartphone -->
  <path d="M 300 260 L 340 260 L 355 245 L 315 245 Z"
        fill="#333"/>
  <path d="M 340 260 L 340 310 L 300 310 L 300 260"
        fill="#444"/>

  <!-- Smartwatch -->
  <ellipse cx="380" cy="270" rx="20" ry="15" fill="#777"/>
  <path d="M 370 270 L 375 250 L 385 250 L 390 270"
        fill="#888" stroke="#777" stroke-width="1"/>

  <!-- Charging waves animation -->
  <g opacity="0.3">
    <path d="M 120 290 Q 250 270 420 290" stroke="#4a90e2" fill="none" stroke-width="2">
      <animate attributeName="d" dur="3s" repeatCount="indefinite"
        values="M 120 290 Q 250 270 420 290;
                M 120 290 Q 250 280 420 290;
                M 120 290 Q 250 270 420 290"/>
    </path>
    <path d="M 120 270 Q 250 250 420 270" stroke="#4a90e2" fill="none" stroke-width="2">
      <animate attributeName="d" dur="3s" repeatCount="indefinite"
        values="M 120 270 Q 250 250 420 270;
                M 120 270 Q 250 260 420 270;
                M 120 270 Q 250 250 420 270"/>
    </path>
  </g>

  <!-- Cloud connection visualization -->
  <path d="M 250 80 Q 280 60 310 80 Q 330 50 350 80 Q 370 70 360 90 Q 380 100 350 110"
        fill="#4a90e2" opacity="0.6"/>

  <!-- Wireless signals -->
  <g opacity="0.4">
    <circle cx="250" cy="200" r="30" fill="none" stroke="#4a90e2" stroke-width="1">
      <animate attributeName="r" dur="2s" repeatCount="indefinite"
        values="20;30;20"/>
    </circle>
    <circle cx="250" cy="200" r="40" fill="none" stroke="#4a90e2" stroke-width="1">
      <animate attributeName="r" dur="2s" repeatCount="indefinite"
        values="30;40;30"/>
    </circle>
  </g>

  <!-- Label -->
  <text x="250" y="380" text-anchor="middle" font-family="Arial" font-size="16" fill="#333">Smart Universal Charger Box - Side View</text>
</svg>

People can invent a charger box. This box is like ultrasonic cleaner. When I used up a power bank, I just put it in the charger box. Then after few hours, the power bank is fully charged.

This is really interesting. May be the electric portable products in home can all implement some protocal to let them charge wirelessly. And they are all connected to cloud's server. And there is a charger box. You just need to put bluetooth speakers, mobile phones, electric lamps, laptop to the box, smart watches to the big charger box. Then they can be charged up. It is like smart cashier machine in big supermarkets.

Just like wireless power bank can passed the energy to the iPhones, the charger box can pass energy from it to the electric products inside it. It is like Magsafe charger.
