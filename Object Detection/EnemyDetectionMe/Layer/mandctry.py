import numpy as np
import tensorflow as tf
import sys
from keras.utils import np_utils
from Convolutional import ConvolutionalLayer
from MaxPooling import MaxPoolingLayer
from Normalization import NormalizationLayer

sys.path.insert(1, 'E:\\Final Project\\Auto Aim Nerf\\Object Detection\\CNN')
from Layers import Layers

def CNN_forward(image, label, layers):
  #output = image/255.
  output = image
  for layer in layers:
    if isinstance(layer, Layers):
      output = flatten(output)
    output = layer.forward_prop(output) # TODO  Check kernel size bug
    print(layer)
  # Compute loss (cross-entropy) and accuracy
  
  loss = np.mean(np.square(np.subtract(output,  np_utils.to_categorical(label,10)))) 
  accuracy = 1 if np.argmax(output) == label else 0
  return output, loss, accuracy
  
def flatten(input):
  input_shape = input.shape

  input_height = input_shape[0]
  input_width = input_shape[1]
  num_inputs = input_shape[2]

  input_reshaped = input.reshape((input_height*input_width, num_inputs))
  sliced_input = np.hsplit(input_reshaped, num_inputs)
  flatten_input = np.array(sliced_input).flatten()
  return flatten_input


def CNN_backprop(gradient, layers, label, alpha=0.05 ):
  grad_back = gradient
  for layer in layers[::-1]:
    if type(layer) in [ConvolutionalLayer]:
        grad_back = layer.back_prop(grad_back, alpha)
    elif type(layer) == MaxPoolingLayer:
        grad_back = layer.back_prop(grad_back)
    else:
      grad_back = layer.back_prop(np_utils.to_categorical(label,10))  
  return grad_back

def CNN_training(image, label, layers, alpha=0.05):
  # Forward step
  output, loss, accuracy = CNN_forward(image, label, layers)

  # Initial gradient
  gradient = np.zeros(10)
  gradient[label] = -1/output[label]

  # Backprop step
  gradient_back = CNN_backprop(gradient, layers, label, alpha)

  return loss, accuracy

def main():
  # Load training data
  (X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()
  X_train = X_train[:5000]
  y_train = y_train[:5000]

  # Define the network
  layers = [
    ConvolutionalLayer(3,3), # layer with 8 3x3 filters, output (26,26,16)
    NormalizationLayer("relu"),
    MaxPoolingLayer(2, 1), # pooling layer 2x2, output (13,13,16)
    Layers([["Dense", 48, "relu"], ["Dense", 16, "relu"], ["Dense", 10, "sigmoid"]] ,0.1)
    ] 

  for epoch in range(4):
    print('Epoch {} ->'.format(epoch+1))
    # Shuffle training data
    permutation = np.random.permutation(len(X_train))
    X_train = X_train[permutation]
    y_train = y_train[permutation]
    # Training the CNN
    loss = 0
    accuracy = 0
    for i, (image, label) in enumerate(zip(X_train, y_train)):
      if i % 100 == 0: # Every 100 examples
        print("Step {}. For the last 100 steps: average loss {}, accuracy {}".format(i+1, loss/100, accuracy))
        loss = 0
        accuracy = 0
      image  =np.array([[-1,]*9]*9)
      image[1][1] = 1
      image[1][7] = 1

      image[2][2] = 1
      image[2][6] = 1
      
      image[3][3] = 1
      image[3][5] = 1

      image[4][4] = 1

      image[5][5] = 1
      image[5][3] = 1

      image[6][6] = 1
      image[6][2] = 1

      image[7][7] = 1
      image[7][1] = 1
      loss_1, accuracy_1 = CNN_training(image, label, layers)
      loss += loss_1
      accuracy += accuracy_1
  
  
if __name__ == '__main__':
  main()