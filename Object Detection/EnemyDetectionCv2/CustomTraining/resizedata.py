# import required modules
from PIL import Image
import os
import numpy as np

WIDTHS = []
HEIGHTS = []

def get_average_size(path: str):
    """
    Gets average size of each image in the custome dataset
    Args:
        path (str): the path to the images
    """
    global WIDTHS, HEIGHTS
    for  root, dirs, files in os.walk(path):
        for file in files:
            img = Image.open(os.path.join(root, file))
            
            # get width and height
            width = img.width
            height = img.height
            WIDTHS.append(width)
            HEIGHTS.append(height)


def resize_all_to_average_size(path: str):
    """
    Resizes all of the images to same size by average
    Args:
        path (str): the path to the images
    """
    avg_width = round(int(np.average(WIDTHS)), -1)
    avg_height = round(int(np.average(HEIGHTS)), -1)

    for  root, dirs, files in os.walk(path):
        for file in files:
            img = Image.open(os.path.join(root, file))
            
            new_image = img.resize((avg_width, avg_height))
            new_image.save(os.path.join(root, file))

if __name__ == "__main__":
    get_average_size(r"G:\Final Project\Auto Aim Nerf\Object Detection\EnemyDetectionCv2\CustomTraining\MyData\Images")
    resize_all_to_average_size(r"G:\Final Project\Auto Aim Nerf\Object Detection\EnemyDetectionCv2\CustomTraining\MyData\Images")