```bash
python3 pre-training/day-6/exercise_1.py
```

This script builds:
- Part 1: one neuron with sigmoid/ReLU support
- Part 2: a dense layer of neurons
- Part 3: a tiny 2-layer network with manual weights

## Part 4 explanation

- **What each weight represents:** A weight controls how strongly one input affects a neuron. Positive weight pushes output up, negative weight pushes it down, and larger magnitude means stronger impact.
- **What bias does:** Bias shifts the neuron's total before activation, so the neuron can still output a useful value even when inputs are small or zero.
- **ReLU vs sigmoid:** ReLU outputs `0` for negative totals and grows linearly for positive totals, which keeps values simple and sparse. Sigmoid squeezes values into `0..1`, useful for probability-like outputs but it compresses large inputs.

