import numpy as np
import random
import time
from typing import Optional

from carbon.maths import tanh, sigmoid
from carbon.utils import printer


class NeuralNetwork:
    """
    optimized for raw grayscale image processing: where the inputs mostly 0 (inactive cells), and (0, 1] for the drawn cells.

    **
    using normalized Xavier weight initialization.
    using tanh for neurons at hidden layers.
    using sigmoid for neurons at output layer.
    using cross-entropy loss function.
    """

    def __init__(self, sizes, weights = None, biases = None, metadata = None):

        self.sizes = sizes

        if weights is None:
            self.weights = [
                -np.sqrt(6/(x+y)) + np.random.rand(y, x)*2*np.sqrt(6/(x+y))
                for x, y in zip(self.sizes[:-1], self.sizes[1:])
            ]
            printer('New weights created.')
        else:
            self.weights = weights

        if biases is None:
            self.biases = [
                np.random.randn(y, 1)
                for y in self.sizes[1:]
            ]
            printer('New biases created.')
        else:
            self.biases = biases

        if metadata is None:
            self.metadata = {
                'n_learn': 0,
                't_acc': [],
                't_cost': [],
                'v_acc': [],
                'v_cost': []
            }
        else:
            self.metadata = metadata

        self.n_layer = len(sizes)
        self.n_input = sizes[0]
        self.hidden_layers = sizes[1:-1]
        self.n_hidden_layer = len(self.hidden_layers)
        self.n_output = sizes[-1]

        ## values of these list are from the last feedforwarding
        self.z_values = []
        self.a_values = []
        self.decision = None  # the index of the output neuron with highest value

    def feedforward(self, a):
        """
        a: np.array([ [i1], [i2], [i3], ... ]).

        or (for optimization purposes: just feed forward, and backprob is not needed)
        a: [ [i1], [i2], [i3], ... ].
        """

        ## reset
        self.z_values = []
        self.a_values = [a]

        ## if `self.n_layer` is 4 -> the variable `i` below will be: 0, 1, 2
        for i, (w, b) in enumerate(zip(self.weights, self.biases)):

            z = np.dot(w, a) + b

            if i == (self.n_layer - 2):
                a = sigmoid(z)
            else:
                a = tanh(z)

            self.z_values.append(z)
            self.a_values.append(a)

        self.decision = a.argmax()

    def backprop(self, inputs, target):
        """
        target: desired output.

        inputs: np.array([ [i1], [i2], [i3], ... ]).
        target: [ [o1], [o2], [o3], ... ] or np.array([ [o1], [o2], [o3], ... ]).
        """

        self.feedforward(inputs)

        ## gradient delta
        dgw = [np.zeros(w.shape) for w in self.weights]
        dgb = [np.zeros(b.shape) for b in self.biases]

        ## output layer
        delta = self.a_values[-1] - target  # using cross-entropy loss function
        dgw[-1] = np.dot(delta, self.a_values[-2].transpose())
        dgb[-1] = delta

        ## hidden layers
        for l in range(2, self.n_layer):

            delta = np.dot(self.weights[-l + 1].transpose(), delta)*tanh(self.z_values[-l], derivative=True)
            dgw[-l] = np.dot(delta, self.a_values[-l - 1].transpose())
            dgb[-l] = delta

        return (dgw, dgb)

    def tuning(self, samples, k1, k2):
        """
        for optimization purposes, these values are precalculated.
        k1: `learning_rate*(regularization/n_training_data)`
        k2: `learning_rate/len(samples)`
        """

        ## gradient
        gw = [np.zeros(w.shape) for w in self.weights]
        gb = [np.zeros(b.shape) for b in self.biases]

        for inputs, target in samples:

            inputs_vectorized = np.zeros((self.n_input, 1))
            for i, v in inputs:
                inputs_vectorized[i] = v

            target_vectorized = np.zeros((self.n_output, 1))
            target_vectorized[target] = 1

            dgw, dgb = self.backprop(inputs_vectorized, target_vectorized)

            gw = [_gw + _dgw for _gw, _dgw in zip(gw, dgw)]
            gb = [_gb + _dgb for _gb, _dgb in zip(gb, dgb)]

        self.weights = [
            (1 - k1)*w - k2*_gw
            for w, _gw in zip(self.weights, gw)
        ]
        self.biases = [
            b - k2*_gb
            for b, _gb in zip(self.biases, gb)
        ]

    def train(
        self,
        training_data: list[tuple[list[tuple[int, float]], int]],  # actually `list[tuple[list[list[int, float]], int]]` (because json encodes tuple into list)
        n_epoch,
        sample_size,
        learning_rate,
        regularization,
        validation_data: list[tuple[list[tuple[int, float]], int]],
        early_stop_after: Optional[int],
        fn  # function to execute at each epoch
    ) -> None:
        """
        sample_size = 1                   -> stochastic gradient descent
        1 < sample_size < n_training_data -> mini batch gradient descent
        sample_size = n_training_data     -> batch gradient descent
        """

        printer('Training started.')

        n_training_data = len(training_data)
        n_validation_data = len(validation_data)

        k1 = learning_rate*(regularization/n_training_data)
        # k2 = learning_rate/len(samples)  # this cannot be used because `len(samples)` may not be constant

        for epoch in range(1, n_epoch+1):

            printer(f'Epoch-{epoch} started...')
            t0 = time.time()

            random.shuffle(training_data)
            list_of_samples = [
                training_data[i : i + sample_size]
                for i in range(0, n_training_data, sample_size)
            ]

            for samples in list_of_samples:
                self.tuning(samples, k1, learning_rate/len(samples))

            t_acc, t_cost = self.get_report(training_data, n_training_data)
            v_acc, v_cost = self.get_report(validation_data, n_validation_data)

            self.metadata['n_learn'] += n_training_data
            self.metadata['t_acc'].append(t_acc)
            self.metadata['t_cost'].append(t_cost)
            self.metadata['v_acc'].append(v_acc)
            self.metadata['v_cost'].append(v_cost)

            fn(epoch)
            printer(f'Epoch-{epoch} done in {round(time.time() - t0)} secs: {(round(t_acc, 3), round(t_cost, 3), round(v_acc, 3), round(v_cost, 3))}')

            if early_stop_after is not None:
                if epoch > early_stop_after:

                    decreasing = []
                    for i in range(1, early_stop_after+1):
                        decreasing.append(self.metadata['v_acc'][-i] <= self.metadata['v_acc'][-i-1])

                    if all(decreasing):
                        printer(f'Early stop at epoch-{epoch}.')
                        break

    def get_report(self, data, n_data):

        n = 0
        cost = 0

        for inputs, target in data:

            inputs_vectorized = np.zeros((self.n_input, 1))
            for i, v in inputs:
                inputs_vectorized[i] = v

            target_vectorized = np.zeros((self.n_output, 1))
            target_vectorized[target] = 1

            self.feedforward(inputs_vectorized)
            output = self.a_values[-1]

            if output.argmax() == target:
                n += 1

            ## using cross-entropy loss function
            cost += np.sum(np.nan_to_num(-target_vectorized*np.log(output) - (1 - target_vectorized)*np.log(1 - output)))

        accuracy = n/n_data
        cost = cost/n_data

        return accuracy, cost