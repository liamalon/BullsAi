from Layer import Dense, MaxPooling, Convolutional, Normalization, Flattner

class Layers:
    def __init__(self, layers, learning_rate: float = 0.1) -> None:
        """
        layers  = [[num of nodes actiovtion]]
        learning_rate set to defult of 0.1
        """

        self.layers = []

        for index, layer in enumerate(layers):
            layer_type = eval(layer[0]+"."+layer[0]+"Layer")
            if layer_type == Convolutional.ConvolutionalLayer:
                self.layers.append(layer_type(layer[1], layer[2]))
            elif layer_type ==  Normalization.NormalizationLayer:
                self.layers.append(layer_type(layer[1]))
            elif layer_type == MaxPooling.MaxPoolingLayer:
                self.layers.append(layer_type(layer[1], layer[2]))
            elif layer_type == Flattner.FlattnerLayer:
                self.layers.append(layer_type())
            elif layer_type ==  Dense.DenseLayer:
                if index +1 != len(layers):
                    self.layers.append(layer_type(layer[1], layers[index+1][1], layer[2], learning_rate))
                else:
                    self.layers.append(layer_type(layer[1], 0, layer[2], learning_rate))
    
    def forward_prop(self, input_array) -> None:
        """
        Feeds input to all of the next layers
        """
        for index, layer in enumerate(self.layers):           
            if isinstance(layer, Dense.DenseLayer):
                self.layers[0].activation_values = input_array
                if index+1 != len(self.layers):
                    self.layers[index+1].no_activation_values , self.layers[index+1].activation_values = layer.forward_prop(input_array, self.layers[index+1])
                    input_array = self.layers[index+1].activation_values
            else:
                input_array = layer.forward_prop(input_array)
        return self.layers[-1].activation_values
    
    def back_prop(self, prediction_array) -> None:
        """
        Does back propagetion for all the layers 
        """
        for layer in reversed(range(1,  len(self.layers))):
            try:
                prediction_array = self.layers[layer].back_prop(self.layers[layer-1], prediction_array)
            except:
                pass
        return prediction_array
        