---
audio: false
generated: true
lang: en
layout: post
title: Exponential Formulas
translated: false
type: note
---

In science, several formulas describe transient or exponential growth/decay processes similar to the RL circuit current equation, where the behavior starts at a specific value (often zero) at \\( t = 0 \\) and approaches a steady-state value (like \\( V_0 \\) or \\( I_0 \\)) as time progresses, often involving the exponential term \\( e \\). Below is a list of such formulas from various domains of physics and engineering, each exhibiting similar exponential behavior.

### 1. **RC Circuit Charging (Capacitor Voltage)**

- **Context**: In an RC circuit (resistor and capacitor in series), when a voltage is applied, the capacitor charges over time.
- **Formula**:
     \\[
     V_C(t) = V_0 \left( 1 - e^{-\frac{t}{RC}} \right)
     \\]
- **Variables**:
  - \\( V_C(t) \\): Voltage across the capacitor at time \\( t \\).
  - \\( V_0 \\): Maximum voltage (source voltage).
  - \\( R \\): Resistance (ohms).
  - \\( C \\): Capacitance (farads).
  - \\( RC \\): Time constant (\\( \tau \\)).
- **Behavior**: At \\( t = 0 \\), \\( V_C = 0 \\). As \\( t \to \infty \\), \\( V_C \to V_0 \\).
- **Similarity**: Like the RL circuit, it starts at 0 and approaches a maximum value exponentially.

### 2. **RC Circuit Discharging (Capacitor Voltage)**

- **Context**: When a charged capacitor in an RC circuit is allowed to discharge through a resistor.
- **Formula**:
     \\[
     V_C(t) = V_0 e^{-\frac{t}{RC}}
     \\]
- **Variables**:
  - \\( V_0 \\): Initial voltage across the capacitor.
  - Others same as above.
- **Behavior**: At \\( t = 0 \\), \\( V_C = V_0 \\). As \\( t \to \infty \\), \\( V_C \to 0 \\).
- **Similarity**: Involves \\( e \\), but decays from a maximum to zero, complementary to the RL charging case.

### 3. **Radioactive Decay**

- **Context**: In nuclear physics, the number of radioactive atoms decreases over time.
- **Formula**:
     \\[
     N(t) = N_0 e^{-\lambda t}
     \\]
- **Variables**:
  - \\( N(t) \\): Number of radioactive atoms at time \\( t \\).
  - \\( N_0 \\): Initial number of atoms.
  - \\( \lambda \\): Decay constant (s⁻¹).
  - \\( \tau = \frac{1}{\lambda} \\): Mean lifetime.
- **Behavior**: At \\( t = 0 \\), \\( N = N_0 \\). As \\( t \to \infty \\), \\( N \to 0 \\).
- **Similarity**: Uses \\( e \\) for exponential decay, analogous to RC discharging or RL circuit current decay when the voltage is removed.

### 4. **Newton’s Law of Cooling**

- **Context**: Describes the cooling of an object in a cooler environment.
- **Formula**:
     \\[
     T(t) = T_{\text{env}} + (T_0 - T_{\text{env}}) e^{-kt}
     \\]
- **Variables**:
  - \\( T(t) \\): Temperature of the object at time \\( t \\).
  - \\( T_0 \\): Initial temperature of the object.
  - \\( T_{\text{env}} \\): Ambient temperature.
  - \\( k \\): Cooling constant (s⁻¹).
- **Behavior**: At \\( t = 0 \\), \\( T = T_0 \\). As \\( t \to \infty \\), \\( T \to T_{\text{env}} \\).
- **Similarity**: Exponential approach from an initial value to a steady-state value, using \\( e \\).

### 5. **Population Growth (Exponential Model)**

- **Context**: In biology, models unrestricted population growth.
- **Formula**:
     \\[
     P(t) = P_0 e^{rt}
     \\]
- **Variables**:
  - \\( P(t) \\): Population at time \\( t \\).
  - \\( P_0 \\): Initial population.
  - \\( r \\): Growth rate (s⁻¹ or other time units).
- **Behavior**: At \\( t = 0 \\), \\( P = P_0 \\). As \\( t \to \infty \\), \\( P \to \infty \\) (unbounded growth).
- **Similarity**: Uses \\( e \\), but grows exponentially rather than approaching a finite limit (unlike RL/RC circuits).

### 6. **RL Circuit Current Decay (After Voltage Removal)**

- **Context**: When the voltage source is removed from an RL circuit, the current decays.
- **Formula**:
     \\[
     I(t) = I_0 e^{-\frac{R}{L}t}
     \\]
- **Variables**:
  - Same as in the RL circuit charging formula.
- **Behavior**: At \\( t = 0 \\), \\( I = I_0 \\). As \\( t \to \infty \\), \\( I \to 0 \\).
- **Similarity**: Complementary to the RL charging case, showing exponential decay with \\( e \\).

### 7. **Damped Harmonic Oscillator (Under-Damped)**

- **Context**: In mechanics, describes a system (e.g., spring-mass with friction) with damping.
- **Formula**:
     \\[
     x(t) = A e^{-\gamma t} \cos(\omega t + \phi)
     \\]
- **Variables**:
  - \\( x(t) \\): Displacement at time \\( t \\).
  - \\( A \\): Initial amplitude.
  - \\( \gamma \\): Damping constant.
  - \\( \omega \\): Angular frequency of oscillation.
  - \\( \phi \\): Phase angle.
- **Behavior**: At \\( t = 0 \\), oscillation starts with amplitude \\( A \\). As \\( t \to \infty \\), \\( x \to 0 \\).
- **Similarity**: The amplitude decays exponentially with \\( e^{-\gamma t} \\), similar to RL/RC decay.

### Common Characteristics

- **Exponential Term**: All formulas use \\( e \\) to describe growth or decay.
- **Initial and Final States**: They start at an initial value (often 0 or a maximum) and approach a steady-state value (0, \\( V_0 \\), or another constant).
- **Time Constant**: Most involve a time constant (e.g., \\( L/R \\), \\( RC \\), \\( 1/\lambda \\)) that governs the rate of change.
- **Applications**: These appear in electrical circuits, thermodynamics, nuclear physics, biology, and mechanics.

If you’d like, I can provide a chart comparing the behavior of a few of these (e.g., RL charging, RC charging, and Newton’s cooling) over time to visualize their exponential nature. Would you like me to generate such a chart? Alternatively, I can dive deeper into any of these formulas or explore others in specific fields!
