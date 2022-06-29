from PIL import Image
import json
import numpy as np
import sys
import torch

RGB_IMAGE_PATH = '../input/'
M2F_PATH = '../data/M2F_output/'
DPT_PATH = '../data/DPT_output/'

def calculate_semantic_paths(panoptic_seg, segments_info, img_w, img_h):
    return # an nparray of nparray of pixels that are central traversable paths, each subarray is one path

def prune_semantic_paths(semantic_paths, dpt_img):
    return # an nparray of nparray of pixels only of paths that are NOT pruned by depths

def plot_semantic_paths(semantic_paths, rgb_img):
    return # join the path pixels (traced in black?) to the original rgb image

if __name__ == "__main__": 
    
    # Initialise filenames
    rgb_img_file = RGB_IMAGE_PATH + sys.argv[1]
    rgb_img_name = sys.argv[1].split(".")
    m2f_img_file = M2F_PATH + sys.argv[1]
    m2f_panoptic_seg_file = M2F_PATH + 'panoptic_seg.pt'
    m2f_segments_info_file = open(M2F_PATH + 'segments_info.json')
    dpt_img_file = DPT_PATH + rgb_img_name[0] + '.png'

    # Read the necessary images and files from the data/ directory
    rgb_img = np.array(Image.open(rgb_img_file)) # Image.fromarray() to save nparray to img
    m2f_img = np.array(Image.open(m2f_img_file))
    m2f_panoptic_seg = torch.load(m2f_panoptic_seg_file)
    m2f_segments_info = json.load(m2f_segments_info_file)
    dpt_img = np.array(Image.open(dpt_img_file))

    # Dimensions of the RGB Image
    img_dim = rgb_img.shape
    img_w = img_dim[1]
    img_h = img_dim[0]
    
    # Read the Panoptic Segmentation data and calculate the traversable paths
    semantic_paths = calculate_semantic_paths(m2f_panoptic_seg, m2f_segments_info, img_w, img_h)
    
    # Prune paths that are blocked by obstacles using the Depths Image
    semantic_paths = prune_semantic_paths(semantic_paths, dpt_img)

    # Plot the traversable paths obtained onto the RGB Image and save as a separate Image
    # Closest path to goal is outlined as Black, and the rest as Dark Grey
    plot_semantic_paths(semantic_paths, rgb_img)

    # TODO: Print out the actions to be taken
    # Goal Destination given to the script as input
    # goal_dest = np.array([int(sys.argv[2]), int(sys.argv[3])])
    # predict_action(semantic_paths, goal_dest, node_height)
