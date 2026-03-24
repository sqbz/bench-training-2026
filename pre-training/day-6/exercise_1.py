import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def relu(x):
    return x if x > 0 else 0.0


class Neuron:
    def __init__(self, weights, bias, activation):
        self.weights = weights
        self.bias = bias
        self.activation = activation

    def forward(self, inputs):
        total = 0.0
        for w, x in zip(self.weights, inputs):
            total += w * x
        total += self.bias
        return self.activation(total)


class DenseLayer:
    def __init__(self, n_inputs, neurons):
        self.n_inputs = n_inputs
        self.neurons = neurons

    def forward(self, inputs):
        if len(inputs) != self.n_inputs:
            raise ValueError(f"Expected {self.n_inputs} inputs, got {len(inputs)}")
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.forward(inputs))
        return outputs


if __name__ == "__main__":
    single = Neuron(weights=[-0.2, 0.5, 0.1], bias=0.2, activation=sigmoid)
    single_out = single.forward([0.5, -0.3, 0.8])
    print("Part 1 - Single Neuron (sigmoid):", round(single_out, 6))

    layer1 = DenseLayer(
        n_inputs=3,
        neurons=[
            Neuron([0.2, -0.1, 0.5], 0.1, relu),
            Neuron([-0.3, 0.7, 0.1], -0.2, relu),
            Neuron([0.5, 0.2, -0.4], 0.0, relu),
            Neuron([0.2, 0.7, 0.3], 0.05, relu),
        ],
    )

    layer2 = DenseLayer(
        n_inputs=4,
        neurons=[
            Neuron([0.4, -0.2, 0.5, 0.1], 0.4, sigmoid),
            Neuron([-0.5, 0.3, 0.6, -0.1], 0.1, sigmoid),
        ],
    )

    sample_input = [0.5, -0.3, 0.8]
    out_layer1 = layer1.forward(sample_input)
    out_layer2 = layer2.forward(out_layer1)

    print("Part 2 - Layer 1 Output:", [round(x, 6) for x in out_layer1])
    print("Part 3 - Tiny Network Output:", [round(x, 6) for x in out_layer2])

