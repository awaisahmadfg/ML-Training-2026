## Day 6 - Part 4 Explanation

### day-6: neuron + dense layer from scratch

### Constraint (must follow)

- No NumPy
- No PyTorch

### Why no libraries?

- Kyun ke agar aap is cheez ko hand-written Python me bana lete ho, to aapko actual math + flow deeply samajh aata hai.
- Phir jab aap PyTorch use karte ho, to blind coding nahi hoti; aap intelligent decisions lete ho kyun ke "andar kya ho raha hai" clear hota hai.

### What each weight represents

- Har weight ek specific input feature ki importance/impact ko represent karta hai.
- Agar weight positive ho, to woh input barhne par neuron output barhne ka chance hota hai.
- Agar weight negative ho, to woh input barhne par neuron output kam hone ka chance hota hai.
- Weight ka absolute size (jaise `0.9` vs `0.1`) batata hai kitna strong effect hai.

Simple example:
- Inputs: `[x1, x2, x3]`
- Weights: `[0.2, 0.7, -0.5]`
- Is ka matlab `x2` ka effect strong positive hai, aur `x3` output ko neeche kheench raha hai.

### What bias does

- Bias ek constant value hoti hai jo weighted sum me add hoti hai:
  `z = sum(w*x) + bias`
- Bias neuron ko flexibility deta hai ke input sab zero hon tab bhi output shift ho sake.
- Decision boundary ko shift karne me bias important role play karta hai.

### ReLU vs Sigmoid - what changes?

- **ReLU**:
  - Formula: `max(0, x)`
  - Negative input ka output `0`, positive input same rehta hai.
  - Fast aur deep networks me common use hota hai.
  - Sparse activations deta hai (kuch neurons 0 ho jate hain).

- **Sigmoid**:
  - Formula: `1 / (1 + e^-x)`
  - Output hamesha `0` se `1` ke darmiyan hota hai.
  - Probability-style output ke liye useful (especially output layer me).
  - Large positive/negative inputs par saturate karta hai (gradient very small ho sakta hai).

### In this exercise

- Part 1 me same neuron ko ReLU aur Sigmoid dono se run karke difference dekha.
- Part 3 tiny network me pehla layer ReLU aur doosra Sigmoid rakha:
  - ReLU hidden layer features extract karta hai
  - Sigmoid final layer output ko bounded range me deta hai

### Forward propagation (in my own words)

- Forward propagation ka matlab hai input ko layer-by-layer aage pass karna.
- Har neuron pehle `sum(w*x) + bias` nikalta hai, phir activation function lagata hai.
- Jo output pehli layer se nikalta hai, woh next layer ka input ban jata hai.
- End me final numbers milte hain jo model ka current prediction hote hain.
- Is stage me sirf "calculation" hoti hai, learning abhi nahi hoti.

### What is missing for actual learning?

Network ko learn karne ke liye yeh cheezein missing hain:
- **Training data with labels** (ground truth chahiye hota hai)
- **Loss function** (prediction kitni ghalat hai, yeh measure karna)
- **Backpropagation** (weights/biases ke gradients nikalna)
- **Optimizer / update rule** (jaise gradient descent se parameters update karna)
- **Many training iterations (epochs)** taake error dheere dheere kam ho

Abhi humne sirf forward pass banaya hai; isi liye network predict to karta hai, lekin khud se better hona nahi seekhta.
