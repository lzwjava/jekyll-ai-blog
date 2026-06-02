---
audio: false
generated: true
lang: en
layout: post
title: Long Short-Term Memory Networks
translated: false
type: note
---

Long Short-Term Memory (LSTM) networks are a type of recurrent neural network architecture specifically designed to address the vanishing gradient problem and enable the learning of long-term dependencies in sequential data. They achieve this through a more sophisticated internal structure called an **LSTM cell**.

Here's a breakdown of how an LSTM cell works:

**Core Idea: The Cell State**

The central concept in an LSTM is the **cell state** (often denoted as 'C<sub>t</sub>'). Think of the cell state as a conveyor belt running through the entire sequence. It carries information relevant to the long-term history of the sequence. Information can be added to or removed from the cell state as it flows through the network via structures called **gates**.

**The Gates**

LSTM cells have three main gates that regulate the flow of information:

1. **Forget Gate:** This gate decides what information from the previous cell state should be discarded.
    * It receives the previous hidden state (h<sub>t-1</sub>) and the current input (x<sub>t</sub>).
    * These are passed through a neural network layer followed by a **sigmoid activation function**.
    * The sigmoid function outputs values between 0 and 1. A value close to 0 means "completely forget this information," while a value close to 1 means "completely keep this information."
    * Mathematically, the forget gate's output (f<sub>t</sub>) is calculated as:

        ```
        f_t = σ(W_f * [h_{t-1}, x_t] + b_f)
        ```

        where:
        * σ is the sigmoid function.
        * W<sub>f</sub> is the weight matrix for the forget gate.
        * [h<sub>t-1</sub>, x_t] is the concatenation of the previous hidden state and the current input.
        * b<sub>f</sub> is the bias vector for the forget gate.

2. **Input Gate:** This gate decides what new information from the current input should be added to the cell state. This process involves two steps:
    * **Input Gate Layer:** A sigmoid layer decides which values we'll update.

        ```
        i_t = σ(W_i * [h_{t-1}, x_t] + b_i)
        ```

        where:
        * σ is the sigmoid function.
        * W<sub>i</sub> is the weight matrix for the input gate.
        * [h<sub>t-1</sub>, x_t] is the concatenation of the previous hidden state and the current input.
        * b<sub>i</sub> is the bias vector for the input gate.
    * **Candidate Values Layer:** A tanh layer creates a vector of new candidate values (candidate cell state, denoted as 'C̃<sub>t</sub>') that could be added to the cell state. The tanh function outputs values between -1 and 1, which helps in regulating the network.

        ```
        C̃_t = tanh(W_C * [h_{t-1}, x_t] + b_C)
        ```

        where:
        * tanh is the hyperbolic tangent function.
        * W<sub>C</sub> is the weight matrix for the candidate cell state.
        * [h<sub>t-1</sub>, x_t] is the concatenation of the previous hidden state and the current input.
        * b<sub>C</sub> is the bias vector for the candidate cell state.

3. **Output Gate:** This gate decides what information from the current cell state should be output as the hidden state for the current time step.
    * It receives the previous hidden state (h<sub>t-1</sub>) and the current input (x<sub>t</sub>).
    * These are passed through a neural network layer followed by a **sigmoid activation function** to determine which parts of the cell state to output.

        ```
        o_t = σ(W_o * [h_{t-1}, x_t] + b_o)
        ```

        where:
        * σ is the sigmoid function.
        * W<sub>o</sub> is the weight matrix for the output gate.
        * [h<sub>t-1</sub>, x_t] is the concatenation of the previous hidden state and the current input.
        * b<sub>o</sub> is the bias vector for the output gate.
    * The cell state is then passed through a **tanh function** to squash the values between -1 and 1.
    * Finally, the output of the sigmoid gate is multiplied element-wise with the output of the tanh function applied to the cell state. This becomes the new hidden state (h<sub>t</sub>) which is passed to the next time step and can also be used for making predictions.

        ```
        h_t = o_t * tanh(C_t)
        ```

**Updating the Cell State**

The cell state is updated based on the decisions made by the forget and input gates:

```
C_t = f_t * C_{t-1} + i_t * C̃_t
```

* The forget gate (f<sub>t</sub>) determines how much of the previous cell state (C<sub>t-1</sub>) to keep. If f<sub>t</sub> is close to 0, the information is mostly forgotten. If it's close to 1, the information is mostly kept.
* The input gate (i<sub>t</sub>) determines how much of the new candidate values (C̃<sub>t</sub>) should be added to the cell state. If i<sub>t</sub> is close to 0, the new information is mostly ignored. If it's close to 1, the new information is mostly added.

**How LSTMs Solve the Vanishing Gradient Problem:**

The key to LSTM's ability to handle long-term dependencies lies in the cell state and the gating mechanisms. The cell state acts as a direct pathway for information to flow across many time steps without being repeatedly multiplied by weights, which is the primary cause of vanishing gradients in traditional RNNs.

The gates allow the LSTM to learn when to store, access, and forget information in the cell state. This selective memory mechanism enables the network to retain relevant information over long sequences and use it when needed, effectively mitigating the vanishing gradient problem and allowing for the learning of long-term dependencies.

In essence, LSTMs provide a way for the network to maintain a "memory" over extended periods, making them highly effective for tasks involving sequential data with long-range dependencies.
