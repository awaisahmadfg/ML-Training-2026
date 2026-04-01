"""
Day 6 Extra Basic Practice
Topic: Neuron math step-by-step

Run:
    python3 neuron_math_practice.py
"""

from math import exp


def sigmoid(x: float) -> float:
    # Sigmoid value 0 aur 1 ke darmiyan laata hai.
    return 1.0 / (1.0 + exp(-x))


def relu(x: float) -> float:
    # ReLU negative ko 0 kar deta hai.
    return max(0.0, x)


def main() -> None:
    print("=== Neuron Math Practice (Step by Step) ===")

    # Input features (sample values)
    x1 = 0.5
    x2 = -0.3
    x3 = 0.8

    # In features ke corresponding weights
    w1 = 0.2
    w2 = 0.7
    w3 = -0.5

    # Bias
    b = 0.1

    # Step 1: Har input ko uske weight se multiply karo
    p1 = x1 * w1
    p2 = x2 * w2
    p3 = x3 * w3

    # Step 2: In products ka sum lo (weighted sum)
    weighted_sum = p1 + p2 + p3

    # Step 3: Bias add karo
    z = weighted_sum + b

    # Step 4: Activation functions apply karo
    out_relu = relu(z)
    out_sigmoid = sigmoid(z)

    # Clean print taake flow clear nazar aaye
    print(f"Inputs:  x1={x1}, x2={x2}, x3={x3}")
    print(f"Weights: w1={w1}, w2={w2}, w3={w3}, bias={b}")
    print("-" * 45)
    print(f"x1*w1 = {x1} * {w1} = {p1}")
    print(f"x2*w2 = {x2} * {w2} = {p2}")
    print(f"x3*w3 = {x3} * {w3} = {p3}")
    print(f"weighted_sum = p1 + p2 + p3 = {weighted_sum}")
    print(f"z = weighted_sum + bias = {weighted_sum} + {b} = {z}")
    print("-" * 45)
    print(f"ReLU(z) = {out_relu}")
    print(f"Sigmoid(z) = {out_sigmoid:.6f}")

    print("\nPractice task for you:")
    print("1) x2 ko -0.3 se +0.3 kar ke output dobara nikaalo.")
    print("2) bias ko 0.1 se 0.6 karo aur dekho kya change aata hai.")
    print("3) w3 ko -0.5 se +0.5 karo aur compare karo.")


if __name__ == "__main__":
    main()
