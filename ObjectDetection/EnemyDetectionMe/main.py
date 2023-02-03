
import numpy as np
from Layers import Layers
from keras.datasets import mnist
import pickle   
from keras.utils import np_utils
from NeuralNetwork import NeuralNetwork

def main():

    nn = NeuralNetwork([["Convolutional", 16, 3],["Normalization","relu"],["MaxPooling",2,1],["Flattner"],["Dense", 13*13*16, "relu"], ["Dense", 10, "sigmoid"]], 0.1)

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    #x_train = x_train.reshape(x_train.shape[0], 1, 28*28)
    x_train = x_train.astype('float32')
    x_train /= 255.0
    #x_train = np.where(x_train>0,1,0)


    images = x_train

    labels = np_utils.to_categorical(y_train)

    #x_test = x_test.reshape(x_test.shape[0], 1, 28*28)
    x_test = x_test.astype('float32')
    x_test /= 255.0
    #x_test = np.where(x_test>0,1,0)
    
    test_images = x_test
    test_labels = y_test

    print("training")
    nn.train(images, labels)
    right = 0
    tries= 0

    for index,d in enumerate(test_images):
        pred_index = np.argmax(nn.test(d))
        if True:
            print(f"Predicted : {pred_index} || Actual : {test_labels[index]}")
        if pred_index == test_labels[index]:
            right +=1
        tries+=1
    print(f"Right on {right/tries} percent ! ")

        
if __name__ == "__main__":
    main()