## Day 6 - Part 4 Explanation

### day-6: neuron + dense layer from scratch

### Constraint (must follow)

- No NumPy
- No PyTorch

### Why no libraries?

- If you can build this with plain Python by hand, you understand the core math and flow deeply.
- Then when you use PyTorch, you do it intelligently because you know what is happening under the hood.

### What each weight represents

- Each weight represents the importance/impact of one specific input feature.
- If a weight is positive, increasing that input tends to increase the neuron output.
- If a weight is negative, increasing that input tends to decrease the neuron output.
- The absolute value of the weight (for example, `0.9` vs `0.1`) shows how strong that effect is.

Simple example:
- Inputs: `[x1, x2, x3]`
- Weights: `[0.2, 0.7, -0.5]`
- This means `x2` has a strong positive effect, while `x3` pulls the output down.

### What bias does

- Bias is a constant value added to the weighted sum:
  `z = sum(w*x) + bias`
- Bias gives the neuron flexibility, so it can shift output even when inputs are zero.
- Bias helps move the decision boundary left or right.

### ReLU vs Sigmoid - what changes?

- **ReLU**:
  - Formula: `max(0, x)`
  - Negative input becomes `0`; positive input stays unchanged.
  - Fast and commonly used in deep networks.
  - Produces sparse activations (some neurons become 0).

- **Sigmoid**:
  - Formula: `1 / (1 + e^-x)`
  - Output is always between `0` and `1`.
  - Useful for probability-style outputs (especially in output layers).
  - Can saturate for very large positive/negative inputs (very small gradients).

### In this exercise

- In Part 1, we ran the same neuron with both ReLU and Sigmoid to compare behavior.
- In Part 3 tiny network, we used ReLU in the first layer and Sigmoid in the second:
  - ReLU helps extract hidden features
  - Sigmoid gives bounded final outputs

### Forward propagation (in my own words)

- Forward propagation means passing input forward layer by layer.
- Each neuron computes `sum(w*x) + bias`, then applies an activation function.
- The output of one layer becomes input for the next layer.
- At the end, we get final numbers that represent the model's current prediction.
- At this stage, only calculation happens; no learning happens yet.

### What is missing for actual learning?

For the network to actually learn, these parts are missing:
- **Training data with labels** (ground truth targets)
- **Loss function** (measure how wrong predictions are)
- **Backpropagation** (compute gradients for weights/biases)
- **Optimizer / update rule** (for example gradient descent to update parameters)
- **Many training iterations (epochs)** so error can decrease over time

Right now we only implemented the forward pass, so the network can produce outputs but cannot improve by itself.
