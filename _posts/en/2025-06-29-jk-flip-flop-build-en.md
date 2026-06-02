---
audio: false
generated: true
lang: en
layout: post
title: Building and Testing a JK Flip-Flop
translated: false
type: note
---

In a previous video, we explored the JK flip-flop and its operation, noting its similarity to the SR flip-flop but with the added feedback mechanism. This feedback allows the output to toggle when both inputs are high on a rising clock edge, rather than entering an undefined state. In this video, I aim to build and observe its practical functionality.

I've constructed a JK flip-flop following the provided circuit diagram. During the build, I realized a labeling error in the diagram: this is actually the K input, and this is the J input. J corresponds to setting, meaning when it goes high, the Q output should also go high. Conversely, K corresponds to resetting, so when it goes high, the Q output should go low. Aside from this minor labeling correction, the rest of the circuit is accurate.

For the NOR gates, I'm utilizing the 74LS02 chip, specifically the two NOR gates on its top side. The other chip, the 74LS11, is a triple 3-input AND gate. I'm employing two of these three-input AND gates for the circuit.

Upon supplying power, the circuit settles into a state, with the Q output appearing to be "on." I then connected my clock circuit. The two switches you see are pulled low via pull-down resistors; pressing a button makes the input go high. These switches are connected by green wires to the two AND gates, serving as the K and J inputs.

The clock signal also feeds into the AND gates. It passes through an RC circuit, consisting of a 0.0001 microfarad capacitor and a 1000 ohm resistor. The output of this RC circuit, carried by two white wires, goes to another input on both AND gates. The outputs of these AND gates are represented by blue wires, which connect to two of the inputs on the NOR gates. The other inputs of the NOR gates receive feedback from their own outputs via yellow wires. These yellow wires also loop back to the AND gates. Finally, the NOR gate outputs drive two LEDs: one for Q and one for Q complement.

When the K input is driven high, the latch should reset, and the Q output should turn off, which it does. Similarly, driving the J input high should set the latch, turning the Q output on, which it also does. Importantly, observe that the change isn't instantaneous upon pressing the button; it occurs with the next clock signal, as this operation is gated by the clock's rising edge.

Now, as this is a JK flip-flop, if both J and K inputs are set high, we expect the output to toggle with each clock pulse. However, it's not consistently toggling. Sometimes it does, especially if I manipulate the circuit slightly, but it's very inconsistent. To ensure I'm pushing both buttons, I'll insert jumpers across them, effectively providing a continuous high input to both J and K. This *should* cause it to toggle with every rising clock edge. While it's working better now, it's still inconsistent.

This inconsistent behavior has a clear explanation, and the best way to understand it is by using an oscilloscope to examine the signals.

First, let's look at the clock input for reference. The oscilloscope shows the clock signal switching on and off, approximately twice per second. Each division on the scope represents 100 milliseconds, so over 10 divisions, it pulses twice per second.

Next, I want to observe the output, as this is what we expect to toggle with each clock pulse. The clock is indeed pulsing at about two pulses per second. Currently, the output isn't toggling, but with some slight adjustment, it does toggle, though inconsistently. When it *does* toggle, it does so on the clock's rising edges, as desired.

The interesting part emerges when we zoom in on the rising edge of the clock. We see some activity there. Zooming in further, it becomes quite clear: when the clock goes high, the output *does* toggle, but it toggles back and forth multiple times before finally settling into a stable state. This is precisely why the behavior is so inconsistent. The output toggles as desired on the rising clock edge, but then it rapidly toggles again shortly thereafter. The period of these rapid toggles is about 82 nanoseconds.

This phenomenon, known as "racing," makes sense when we re-examine the circuit diagram. The clock pulse, even though we intend to use only its leading edge, remains high for a considerable duration (250 milliseconds in this case). If the output switches *before* this pulse goes back to zero, the feedback loop causes it to switch again, and again, leading to multiple toggles. So, when the clock pulse goes high, the output switches on, but then immediately switches off and on repeatedly. It's purely by chance that it settles into the desired state sometimes.

The root cause of this racing condition lies in the RC circuit used for detecting the rising edge. I mentioned that the capacitor is 0.0001 microfarads and the resistor is 1000 ohms. Multiplying these values gives the time constant of the RC circuit, which indicates the pulse width. This time constant is approximately 100 nanoseconds.

Let's measure the pulse input for the circuit. Initially, it looks great when zoomed out – a quick pulse on the rising edge of the clock, as desired. The problem is that this pulse isn't quick *enough*. It's a 1-microsecond pulse, and during that 1 microsecond, the output toggles on and off repeatedly before finally settling when the pulse drops to a logic zero.

What can be done about this? One option is to make the pulse shorter. Given that the toggling period is around 80 nanoseconds, we need a pulse significantly shorter than 1 microsecond. We can try changing the 1000-ohm resistor to a 100-ohm resistor, which should reduce the time constant to 100 nanoseconds.

After swapping out the resistor, we observe a much smaller pulse. However, it's still not consistently working. At this point, we're encountering the limitations of breadboards. High-speed signals in the tens of nanoseconds range are challenging on breadboards due to stray capacitances, inductances, and other parasitic effects. This explains why simply waving my hand near the circuit can alter its behavior, as my hand changes the capacitance by acting as a grounded object.

You can see that the output is now going high, then low, and staying low. But again, if I adjust my hand, it might start toggling. I'm not changing any connections, just moving my hand, which affects the capacitance.

Even the rising edge of our clock isn't perfectly sharp on this timescale, again due to breadboard limitations. The pulse we're generating isn't as clean as it was with the larger resistor. Ultimately, this all points to the fact that we're pushing the boundaries of what's feasible on a breadboard. This particular method of detecting a rising edge using an RC circuit is inherently problematic in a JK flip-flop due to the racing condition. If the pulse isn't narrow enough (ideally just a few nanoseconds), the output will feed back and toggle more than once per clock rising edge.

So, what's the solution? In the next video, I'll demonstrate a far superior method for building a JK flip-flop that entirely eliminates this racing problem: the master-slave JK flip-flop. It's a much more robust design and should work without any issues on a breadboard.
