---
audio: false
generated: true
lang: en
layout: post
title: Nodal Analysis Solves Node Voltages
translated: false
type: note
---

The primary unknown variable solved for in nodal analysis is **Node voltages**.

Here's an analysis of each option:

* **Branch currents:** While branch currents can be determined *after* solving for node voltages, they are not the primary variables directly solved for in nodal analysis. Nodal analysis focuses on applying Kirchhoff's Current Law (KCL) at each node, which is expressed in terms of voltages and resistances, not directly currents.

* **Loop currents:** Loop currents are the primary unknown variables solved for in **mesh analysis** (also known as loop analysis), not nodal analysis. Mesh analysis applies Kirchhoff's Voltage Law (KVL) around independent loops.

* **Node voltages:** This is the correct answer. In nodal analysis, we define a reference node (often called the ground node) and then assign unknown voltage variables to the other independent nodes in the circuit. By applying Kirchhoff's Current Law (KCL) at each independent node, we form a system of linear equations where the unknowns are precisely these node voltages. Once the node voltages are found, all other circuit quantities (like branch currents, power dissipation, etc.) can be easily calculated.

* **Power dissipation:** Power dissipation is a quantity that can be calculated *after* the node voltages (and subsequently branch currents) are known. It is a result of the analysis, not a primary unknown variable used to set up the initial equations in nodal analysis.
