import numpy as np
from Layer import Layer
from ActiovationFuncs import ActivationFuncs

class ConvolutionalLayer(Layer):
    """
    Convolutional layer of the network  
    """
    
    def __init__(self, kernel_num:int , kernel_size:int, padding:tuple=(0,0), stride:tuple=(1,1)):
        self.kernel_num = kernel_num
        self.kernel_size = kernel_size        
        self.kernels = np.random.randn(kernel_num, kernel_size, kernel_size) / (kernel_size**2)
        self.padding = padding
        self.stride = stride
    
    def pad(self):
        self.image

    def patches_generator(self, image, image_h, image_w):
        self.image = image
        self.pad()
        for h in range(0, image_h-self.kernel_size+1, self.stride[1]):
            for w in range(0, image_w-self.kernel_size+1, self.stride[0]):
                # Getting image block 
                patch = image[h:(h+self.kernel_size), w:(w+self.kernel_size)]
                yield patch, h, w
    
    def forward_prop(self, image):
        if len(image.shape) == 2:
            image_h, image_w = image.shape
        else:
            image_h, image_w, self.kernel_num = image.shape
        
        convolution_output = np.zeros((image_h-self.kernel_size+1, image_w-self.kernel_size+1, self.kernel_num))
        for patch, h, w in self.patches_generator(image, image_h, image_w):
            # Building the new image
            convolution_output[h,w] = np.divide(np.sum(np.multiply(patch, self.kernels), axis=(1,2)),self.kernel_num**2)
        return convolution_output
    
    def back_prop(self, _, dE_dY):
        dE_dk = np.zeros(self.kernels.shape)
        for patch, h, w in self.patches_generator(self.image):
            for f in range(self.kernel_num):
                dE_dk[f] += patch * dE_dY[h, w, f]
        self.kernels -= 0.05*dE_dk
        return dE_dk
    
    def __str__(self) -> str:
        return "Conv Layer ---- \n"

