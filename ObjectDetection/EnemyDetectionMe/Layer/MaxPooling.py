import numpy as np
from ActiovationFuncs import ActivationFuncs
from Layer import Layer

class MaxPoolingLayer(Layer):
    """
    MaxPooling layer of the network  
    """
    
    def __init__(self, kernel_size:int, stride:int = 1):
        self.kernel_size = kernel_size
        self.stride = stride
    
    def patches_generator(self, image, output_height, output_width):
        self.image = image

        for height in range(0, output_height, self.stride):
            for width in range(0, output_width, self.stride):
                # Getting image block
                patch = image[(height*self.kernel_size):(height*self.kernel_size+self.kernel_size), (width*self.kernel_size):(width*self.kernel_size+self.kernel_size)]
                yield patch, (height - self.stride + 1 if height>0 else height), (width - self.stride + 1 if width>0 else width) 

    def forward_prop(self, image):
        image_height, image_width, num_kernels = image.shape
        output_height = int(np.ceil(image_height/self.kernel_size))
        output_width = int(np.ceil(image_width/self.kernel_size))
        # Max pooling padding
        max_pooling_output = np.zeros((output_height, output_width , num_kernels))
        for patch, height, width in self.patches_generator(image, output_height, output_width):
            max_pooling_output[height, width] = np.amax(patch, axis=(0,1))
        return max_pooling_output

    def back_prop(self, _, input_deriv):
        kernel_deriv = np.zeros(self.image.shape)
        image_height, image_width, num_kernels = self.image.shape
        for patch, height, width in self.patches_generator(self.image, image_height, image_width):
            image_height, image_width, num_kernels = patch.shape
            max_val = np.amax(patch, axis=(0,1))

            for idx_h in range(image_height):
                for idx_w in range(image_width):
                    for idx_k in range(num_kernels):
                        if patch[idx_h,idx_w,idx_k] == max_val[idx_k]:
                            kernel_deriv[height*self.kernel_size+idx_h, width*self.kernel_size+idx_w, idx_k] = input_deriv[height, width, idx_k]
            return kernel_deriv

        
    def __str__(self) -> str:
        return "MaxPooling Layer ---- \n"