import numpy as np
from Layer import Layer
from ActiovationFuncs import ActivationFuncs
class DenseLayer(Layer):
    """
    Dense layer of the network  
    """

    def __init__(self, num_of_neurons: int, next_layer_len: int, activation_func: str, learning_rate: float = 0.1) -> None:
        """
        Initializing all the parameters of the layer
        """

        ## Sigmoid init
        self.weights = np.multiply(np.subtract(np.random.rand(num_of_neurons, next_layer_len), 0.5), 2)
        self.biases = np.multiply(np.subtract(np.random.rand(num_of_neurons), 0.5), 2)

        ## Relu init
        self.weights = self.weights*np.sqrt(2 / num_of_neurons)
        self.biases = self.biases*np.sqrt(2 / num_of_neurons)

        self.activation_values = np.zeros((num_of_neurons)) 
        self.no_activation_values = np.zeros((num_of_neurons))

        self.activation_func = eval("ActivationFuncs._"+activation_func)
        self.actiovation_deriv_func =  eval("ActivationFuncs._"+activation_func+"_"+"deriv")
        self.learning_rate = learning_rate
    
    
    def _calc_cost(self,  prediction_array):
        """
        Calculates the cost of the layer
        """ 
        return  np.multiply(2, (self.activation_values - prediction_array))
    
    def forward_prop(self, input_array, next_layer):
        """
        Calculates the value of the next layer
        """ 
        val = np.dot(input_array,  self.weights) + next_layer.biases
        return val, self.activation_func(val)

    def back_prop(self,  prev_layer_array,  prediction_array):

        """
        Calculates the derivativ for the layer
        """ 

        output_layer = self.no_activation_values

        actiovation_deriv = self.actiovation_deriv_func(output_layer)

        cost_deriv = self._calc_cost(prediction_array)

        cost_sig_deriv = np.multiply(cost_deriv, actiovation_deriv)  

        cost_sig_deriv = np.multiply(cost_sig_deriv, self.learning_rate)  

        ### Bias calc

        self.biases = np.subtract(self.biases, cost_sig_deriv)

        ### Prev layer actiotions values

        input_deriv = np.dot(np.multiply(cost_deriv, actiovation_deriv), np.swapaxes(prev_layer_array.weights,  0,  1))
                            
        input_deriv = np.divide(input_deriv , len(output_layer)) 

        ### Weights calc

        weights_deriv = np.outer(prev_layer_array.activation_values,  cost_sig_deriv )

        prev_layer_array.weights = np.subtract(prev_layer_array.weights, weights_deriv)

        return np.subtract(prev_layer_array.activation_values ,  input_deriv)