import numpy as np
class ActivationFuncs:
    @staticmethod
    def _softmax(x):   
        """
        Soft max activation function
        """     
        m = np.exp(x)
        return m / m.sum()
        
    @staticmethod
    def _tanh(x):
        """
        Tanh activation function
        """    
        return np.tanh(x)

    @staticmethod
    def _tanh_deriv(x):
        """
        Tanh activation function derivativ
        """    
        return 1 - np.power(ActivationFuncs._tanh(x), 2) 

    @staticmethod
    def _relu(x):     
        """
        Relu activation function
        """    
        return np.maximum(0, x)

    @staticmethod
    def _relu_deriv(x):
        """
        Tanh activation function derivativ
        """   
        x[x<=0] = 0
        x[x>0] = 1
        return x
        
    @staticmethod
    def _sigmoid( x):
        """
        Sigmoid activation function
        """    
        return np.divide(1, np.add(1, np.exp(-x)))

    @staticmethod
    def _sigmoid_deriv( x):
        """
        Sigmoid activation function derivativ
        """    
        return  np.multiply(ActivationFuncs._sigmoid(x), (1 - ActivationFuncs._sigmoid(x)))