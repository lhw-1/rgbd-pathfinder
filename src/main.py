from PIL import Image, ImageDraw
import json
import numpy as np
import random
import sys
import torch
np.set_printoptions(threshold=sys.maxsize)

import register_ade20k_panoptic

RGB_IMAGE_PATH = '../input/'
M2F_PATH = '../data/M2F_output/'
DPT_PATH = '../data/DPT_output/'
RGBDP_PATH = '../data/RGBDP_output/'
TRAVERSABLE = register_ade20k_panoptic.TRAVERSABLE

def generate_mapping(segments_info):
    mapping = {0:-1}
    for obj in segments_info:
        mapping[obj["id"]] = obj["category_id"]
    return mapping

def calculate_traversable_paths(panoptic_seg, segments_info):

    # Convert the Panoptic Segmentation Tensor into NumPy array
    panoptic_seg_arr = panoptic_seg.cpu().clone().detach().numpy()

    # Map the ids to the correct category ids using segments_info
    segments_mapping = generate_mapping(segments_info)
    apply_mapping = lambda id, segments_info : segments_info[id]
    apply_mapping = np.vectorize(apply_mapping)
    panoptic_seg_arr = apply_mapping(panoptic_seg_arr, segments_mapping)

    # TODO: Make this more efficient using np.vectorize or otherwise
    # TODO: There must be a better way to iterate over a NumPy array
    # TODO: Forking roads may require more consideration
    traversable_areas = []
    traversable_paths = []
    row_idx = 0
    for row in panoptic_seg_arr:
        # Filter all non-traversable areas to -1
        # Append all traversable areas to traversable_areas (list of dictionaries)
        # For every traversable area, find the center
        count = 0
        for i in range(len(row)):
            if row[i] not in TRAVERSABLE:
                count = 0
                row[i] = -1
            elif i == len(row) - 1 or row[i+1] not in TRAVERSABLE:
                traversable_areas.append({'row': row_idx, 'id': row[i], 'start': i - count, 'end': i})
                traversable_paths.append({'id': row[i], 'x': int((2 * i - count) / 2), 'y': row_idx})
            else:
                count = count + 1
        row_idx = row_idx + 1
    
    return traversable_areas, traversable_paths

def prune_semantic_paths(semantic_paths, dpt_img):
    return # All remaining paths not pruned by obstacle detection using Binary Dilation and the Depths Image
    # TODO: Set flexibility hyperparameter (E.g. Path with similar ID in the previous / next row within x pixels)

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
    rgb_img = Image.open(rgb_img_file)
    m2f_img = Image.open(m2f_img_file)
    m2f_panoptic_seg = torch.load(m2f_panoptic_seg_file)
    m2f_segments_info = json.load(m2f_segments_info_file)
    dpt_img = np.array(Image.open(dpt_img_file)) # NumPy array to be used for Binary Dilation

    # Read the Panoptic Segmentation data and calculate the traversable areas and traversable paths
    traversable_areas, traversable_paths = calculate_traversable_paths(m2f_panoptic_seg, m2f_segments_info)
    
    # TODO: Prune paths that are blocked by obstacles using the Depths Image
    # traversable_paths = prune_semantic_paths(traversable_paths, dpt_img)

    # Create a copy of the RGB Image
    rgb_img_map = rgb_img.load()
    rgb_img_traversable = Image.new(rgb_img.mode, rgb_img.size)
    rgb_img_traversable_map = rgb_img_traversable.load()
    for i in range(rgb_img.size[0]):
        for j in range(rgb_img.size[1]):
                rgb_img_traversable_map[i,j] = rgb_img_map[i,j]

    # Plot the traversable paths obtained onto the RGB Image
    draw = ImageDraw.Draw(rgb_img_traversable)
    sample_path = -1
    for path in traversable_paths:
        # rgb_img_traversable_map[path['x'], path['y']] = (255,0,0,255)
        draw.ellipse((path['x'] - 2, path['y'] - 2, path['x'] + 2, path['y'] + 2), fill=(255, 0, 0))
        if path['y'] > (5 * rgb_img.size[1] / 8) and path['y'] < (7 * rgb_img.size[1] / 8):
            sample_path = path['x']

    # Print out and Plot the Goal Destination for the agent
    # goal_dest = [int(sys.argv[2]), int(sys.argv[3])]
    if sample_path == -1:
        print("No Path Available.")
        print("Action to be taken: Rotate")
    else:
        # Manual creation of Goal Destination for even testing
        chance = random.randint(1, 30)
        if chance % 3 == 0:
            goal_dest = [random.randint(0, sample_path - 1), int(rgb_img.size[1] / 2)]
            print("Goal Destination given: " + str(goal_dest))
        elif chance % 3 == 1:
            goal_dest = [random.randint(sample_path + 1, rgb_img.size[0]), int(rgb_img.size[1] / 2)]
            print("Goal Destination given: " + str(goal_dest))
        else:
            goal_dest = [sample_path, int(rgb_img.size[1] / 2)]
            print("Goal Destination given: " + str(goal_dest))
    
    draw.ellipse((goal_dest[0] - 5, goal_dest[1] - 5, goal_dest[0] + 5, goal_dest[1] + 5), fill=(0, 0, 0))

    # Save the copy as a separate Image
    rgb_img_traversable.save(RGBDP_PATH + "traversable_" + sys.argv[1], "PNG")

    # Print out the actions to be taken by the agent
    if sample_path < goal_dest[0]:
        print("Action to be taken: Rotate Right")
    elif sample_path > goal_dest[0]:
        print("Action to be taken: Rotate Left")
    else:
        print("Action to be taken: Move Forward")
