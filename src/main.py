import cv2
import math
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import random
import sys
from PIL import Image

import depth
import plot
import segmentation

if __name__ == "__main__": 
    
    # RGB Image filename given to the script as input
    rgb_img_file = '../input/' + sys.argv[1]
    rgb_img_name = sys.argv[1].split(".")
    m2f_img_file = '../data/M2F_output' + sys.argv[1]
    dpt_img_file = '../data/DPT_output' + rgb_img_name[0] + '.png'

    # Read the necessary images from data/ directory
    rgb_img = img.imread(rgb_img_file)
    m2f_img = img.imread(m2f_img_file)
    dpt_img = img.imread(dpt_img_file)

    # Dimensions of the RGB Image
    img_dim = rgb_img.shape
    img_w = img_dim[1]
    img_h = img_dim[0]
    
    # Goal Destination given to the script as input
    goal_dest = np.array([int(sys.argv[2]), int(sys.argv[3])])

    # TODO: Read the pixel cluster data and calculate horizontal centers
    # semantic_paths = calculate_semantic_paths(pixel_cluster(bettername), img_w, img_h)
    
    # TODO: Prune paths using Depths
    # semantic_paths = prune_semantic_paths(semantic_paths, dpt_img)

    # TODO: Plot the semantic paths onto the RGB Image
    # plot_semantic_paths(semantic_paths, rgb_img)

    # TODO: Print out the actions to be taken
    # predict_action(semantic_paths, goal_dest, node_height)
