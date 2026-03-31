"""
Day 6 - Neural Network Basics (No training)

Rules:
    - No NumPy
    - No PyTorch
    - Sirf basic Python se forward-pass logic samajhna hai.

Run:
    python3 neural_basics.py
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Callable, List


# Type alias: activation function ek float leti hai aur float return karti hai.
ActivationFn = Callable[[float], float]


def sigmoid(x: float) -> float:
    # Sigmoid output ko 0 aur 1 ke darmiyan squeeze karta hai.
    return 1.0 / (1.0 + exp(-x))


def relu(x: float) -> float:
    # ReLU negative values ko 0 bana deta hai, positive ko as-it-is rakhta hai.
    return max(0.0, x)


@dataclass
class Neuron:
    # weights: har input ke liye ek weight hota hai.
    weights: List[float]
    # bias: weighted sum me extra shift add karta hai.
    bias: float
    # activation: sigmoid ya relu function assign hoga.
    activation: ActivationFn

    def forward(self, inputs: List[float]) -> float:
        # Validate: inputs aur weights ka size same hona zaroori hai.
        if len(inputs) != len(self.weights):
            raise ValueError(
                f"Input size {len(inputs)} aur weight size {len(self.weights)} match nahi karte."
            )

        # Weighted sum nikalna: sum(w*x)
        weighted_sum = sum(w * x for w, x in zip(self.weights, inputs))

        # Bias add karna: sum(w*x) + bias
        z = weighted_sum + self.bias

        # Activation apply karna: output = activation(z)
        return self.activation(z)


class DenseLayer:
    def __init__(
        self,
        n_inputs: int,
        n_neurons: int,
        activation: ActivationFn,
        weights: List[List[float]] | None = None,
        biases: List[float] | None = None,
    ) -> None:
        # Layer configuration save kar rahe hain.
        self.n_inputs = n_inputs
        self.n_neurons = n_neurons
        self.activation = activation

        # Agar weights pass nahi kiye to default 0.0 se initialize kar do.
        if weights is None:
            weights = [[0.0] * n_inputs for _ in range(n_neurons)]
        if biases is None:
            biases = [0.0] * n_neurons

        # Safety checks: dimensions sahi honi chahiye.
        if len(weights) != n_neurons:
            raise ValueError("weights rows ki count n_neurons ke barabar honi chahiye.")
        if any(len(row) != n_inputs for row in weights):
            raise ValueError("Har weight row ki length n_inputs ke barabar honi chahiye.")
        if len(biases) != n_neurons:
            raise ValueError("biases ki length n_neurons ke barabar honi chahiye.")

        # Har neuron ko uske weights, bias aur activation ke sath create karna.
        self.neurons = [
            Neuron(weights=weights[i], bias=biases[i], activation=activation)
            for i in range(n_neurons)
        ]

    def forward(self, inputs: List[float]) -> List[float]:
        # Layer output: har neuron ka forward result ek list me.
        return [neuron.forward(inputs) for neuron in self.neurons]


def part_1_demo() -> None:
    print("=== Part 1: Single Neuron ===")

    inputs = [0.5, -0.3, 0.8]
    weights = [0.2, 0.7, -0.5]
    bias = 0.1

    # Ek neuron sigmoid activation ke sath.
    neuron_sigmoid = Neuron(weights=weights, bias=bias, activation=sigmoid)
    output_sigmoid = neuron_sigmoid.forward(inputs)
    print(f"Sigmoid neuron output: {output_sigmoid:.6f}")

    # Wohi same neuron ReLU activation ke sath.
    neuron_relu = Neuron(weights=weights, bias=bias, activation=relu)
    output_relu = neuron_relu.forward(inputs)
    print(f"ReLU neuron output:    {output_relu:.6f}")
    print()


def part_2_demo() -> None:
    print("=== Part 2: Dense Layer ===")

    # 3 inputs aur 3 neurons ka ek sample layer.
    layer = DenseLayer(
        n_inputs=3,
        n_neurons=3,
        activation=relu,
        weights=[
            [0.2, 0.7, -0.5],
            [0.1, -0.4, 0.9],
            [-0.3, 0.8, 0.2],
        ],
        biases=[0.1, -0.2, 0.05],
    )

    inputs = [0.5, -0.3, 0.8]
    outputs = layer.forward(inputs)
    print(f"Layer input:  {inputs}")
    print(f"Layer output: {[round(x, 6) for x in outputs]}")
    print()


def part_3_demo() -> None:
    print("=== Part 3: Tiny Network (3->4->2) ===")

    # Layer 1: 3 inputs -> 4 neurons (ReLU)
    layer1 = DenseLayer(
        n_inputs=3,
        n_neurons=4,
        activation=relu,
        weights=[
            [0.2, -0.1, 0.4],
            [0.7, 0.3, -0.5],
            [-0.3, 0.8, 0.1],
            [0.5, -0.6, 0.2],
        ],
        biases=[0.1, -0.2, 0.05, 0.0],
    )

    # Layer 2: 4 inputs -> 2 neurons (Sigmoid)
    layer2 = DenseLayer(
        n_inputs=4,
        n_neurons=2,
        activation=sigmoid,
        weights=[
            [0.6, -0.2, 0.1, 0.4],
            [-0.5, 0.3, 0.8, -0.1],
        ],
        biases=[0.05, -0.1],
    )

    sample_input = [0.5, -0.3, 0.8]

    # Forward pass step-1: pehle layer1 ka output nikalo.
    hidden_output = layer1.forward(sample_input)

    # Forward pass step-2: hidden_output ko layer2 me pass karo.
    final_output = layer2.forward(hidden_output)

    print(f"Input:         {sample_input}")
    print(f"Hidden output: {[round(x, 6) for x in hidden_output]}")
    print(f"Final output:  {[round(x, 6) for x in final_output]}")
    print()


if __name__ == "__main__":
    # Part 4 short note:
    # - Har weight batata hai ke us specific input feature ka asar kitna hai:
    #   positive weight output ko barhata hai, negative weight output ko kam karta hai.
    # - Bias ek constant shift hai jo decision boundary ko left/right move karta hai.
    # - ReLU vs Sigmoid:
    #   ReLU fast/simple hai aur negative values ko 0 kar deta hai.
    #   Sigmoid output ko 0..1 me squeeze karta hai (probability-style output ke liye useful).
    # Top-to-bottom demo run for all 3 parts.
    part_1_demo()
    part_2_demo()
    part_3_demo()
