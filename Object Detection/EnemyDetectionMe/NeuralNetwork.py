

import numpy as np
from Layers import Layers
import pickle

class NeuralNetwork:
    def __init__(self, layers: int = 0, learning_rate: float = 0.1 , load: bool = False) -> None:
        """
        layers  = [num of nodes] 
        learning_rate deafult to 0.1 
        Load if True loads winner.pickle file of a traind network 
        """
        if load:
            self.network = self.load_moudle()

        else:
            self.network = Layers(layers, learning_rate)
    
    def mse_calc(self, pred) -> float :
        """
        Claculates error using Mean Squerd Error 
        """
        output = self.network.layers[-1].activation_values       
        return np.mean(np.square(np.subtract(output, pred))) 

    def train(self, data, labels) -> None :  
        """
        Train the Neural Network given data and labels 
        Supervised learning  
        Saves the moudle with the best Erorr 
        """
        total_error_rate= 1

        laps = 0

        error_alpha = 1.5

        min_error = 1

        while total_error_rate>0.09:

            total_error_rate=  0
            
            for index, data_piece in enumerate(data):
                label = labels[index]
                self.network.forward_prop(data_piece)
                total_error_rate += self.mse_calc(label)
                self.network.back_prop(label)

            laps +=1
            
            total_error_rate /= 60000

            error_and_alpha  = total_error_rate / error_alpha

            if min_error > error_and_alpha :
                min_error = error_and_alpha 
                self.save_moudle()
                
            #self.cahnge_lerning_rate(error_and_alpha)

            print("Finished Epoch num : " , laps , "Total Erorr : " , total_error_rate , "Learning Rate : " , total_error_rate / error_alpha ) 
            
        self.save_moudle()

    def cahnge_lerning_rate(self, learning_rate: float) -> None :
        """
        Changes learning rate in all layers of the network 
        """
        for layer in self.network.layers:
            layer.learning_rate = learning_rate

    
    def save_moudle(self) -> None :
        """
        Saves traind network 
        """
        with open("winner.pickle", "wb") as f :
            pickle.dump(self.network, f)
    
    def load_moudle(self) -> None :
        """
        Loads already traind network 
        """
        with open("winner.pickle", "rb") as f :
            return pickle.load(f)

        
    def test(self, data) -> int :
        """
        To test network, feeds input to network and returns output 
        """
        data = data.flatten()
        self.network.forward_prop(data)
        return(self.network.layers[-1].activation_values)

    # def show_image(self, data, label) -> None:
    #     """
    #     Shows numpy array as an image in pyplot 
    #     """
    #     data = data.flatten()
    #     self.network.feed_forowrd(data)
    #     arr = self.network.layers[-1].activation_values.reshape(28,28)
    #     plt.imshow(arr*255)
    #     plt.xlabel(str(label))
    #     plt.show()

