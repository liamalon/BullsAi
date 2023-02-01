import numpy as np
from Layer import Layer

from ActiovationFuncs import ActivationFuncs


class FlattnerLayer(Layer):
    def __init__(self):
        self.original_shape = None
    
    def forward_prop(self, input):
        self.original_shape = input.shape
        input_shape = input.shape

        input_height = input_shape[0]
        input_width = input_shape[1]
        num_inputs = input_shape[2]

        input_reshaped = input.reshape((input_height*input_width, num_inputs))
        sliced_input = np.hsplit(input_reshaped, num_inputs)
        flatten_input = np.array(sliced_input).flatten()
        return flatten_input

    def back_prop(self, _, deriv):
        return np.reshape(deriv, self.original_shape)