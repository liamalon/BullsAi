from Layer import Layer
from ActiovationFuncs import ActivationFuncs
class NormalizationLayer(Layer):
    def __init__(self, activation_func):
        self.actiovation_func = eval("ActivationFuncs._"+activation_func)
        self.actiovation_deriv_func =  eval("ActivationFuncs._"+activation_func+"_"+"deriv")
    
    def forward_prop(self, input):
        return self.actiovation_func(input)

    def back_prop(self, _, input):
        return self.actiovation_deriv_func(input)

    def __str__(self) -> str:
        return "NormalizationLayer Layer ---- \n"
