import math
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import random
import sys
from PIL import Image

'''
This script (plot.py) handles plotting various vectors / nodes onto the RGB Image.
A few PNG files (notably, "goal.png", "convert.png", and "combine.png") are created and removed as the script runs.
The final result is saved under data/RGBDP_output/ as "

'''

# TODO: Modify Origin to be Eye-level instead of Bottom
# TODO: Integrate Depth and Segmentation

NODE_ANGLES = [-90, -75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75, 90]

def convert_white(img_file):
    '''
    Converts all white pixels to transparent pixels in the Image given (img_file).
    Saves the result as a PNG file named "convert.png".

    Params:
        img_file: The file path for the RGB image to be converted.
    '''

    img = Image.open(img_file)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save("convert.png", "PNG")

def combine_images(bg_img_file, bg_img_w, bg_img_h, fg_img_file):
    '''
    Combines the two images given (rgb_img_file and convert_img_file).
    Saves the result as a PNG file named "combine.png".

    Params:
        bg_img_file: The file path for the Background Image.
        bg_img_w: The width of the Background Image (to resize the Foreground Image).
        bg_img_h: The height of the Background Image (to resize the Foreground Image).
        fg_img_file: The file path for the Foreground Image.
    '''

    bg_img = Image.open(bg_img_file).convert('RGB')
    fg_img = Image.open(fg_img_file).convert('RGBA').resize((bg_img_w, bg_img_h))
    bg_img.paste(fg_img, box = None, mask = fg_img)
    bg_img.save("combine.png")

def calculate_nodes(goal_vector, rgb_img_w, rgb_img_h):
    '''
    Calculates the nodes from the given Goal Vector, with the angles specified by NODE_ANGLES.

    Params:
        goal_vector: The dimensions of the Goal Vector given.
        rgb_img_w: The width of the RGB Image.
        rgb_img_h: The height of the RGB Image.

    Returns:
        nodes: An array of co-ordinates, each co-ordinates corresponding to a single Node.
    '''
    
    # Initialise an array of nodes, n x 2 (where n is the number of nodes)
    nodes = np.empty([len(NODE_ANGLES), 2])
    
    # Calculate the length and angle of the Goal Vector
    goal_vector_length = math.sqrt(goal_vector[0] ** 2 + goal_vector[1] ** 2)
    goal_vector_angle = math.atan(goal_vector[1] / abs(goal_vector[0]))

    # Calculate all possible Nodes
    for i in range(len(NODE_ANGLES)):
        node_x = int(goal_vector_length * math.cos(goal_vector_angle - math.radians(NODE_ANGLES[i])))
        node_y = int(goal_vector_length * math.sin(goal_vector_angle - math.radians(NODE_ANGLES[i])))
        node_x = node_x * -1 if goal_vector[0] < 0 else node_x
        nodes[i] = np.array([node_x, node_y])

    # Rescale the Nodes
    # TODO: Modify to Eye-Level
    nodes = rescale_nodes(nodes, rgb_img_h / 4, goal_vector_length)
    nodes_location = np.array([np.array([int(node[0] + rgb_img_w / 2), node[1]]) for node in nodes])
    print("Nodes Calculated: " + np.array2string(nodes))
    print("Node Co-ordinates (pixels): " + np.array2string(nodes_location))

    # TODO: Prune Nodes according to Depth
    # TODO: Prune Nodes according to Segmentation

    return nodes

def rescale_nodes(nodes, distance, goal_vector_length):
    '''
    Re-scales the distance between the nodes and the Origin.

    Params:
        nodes: An array of co-ordinates, each co-ordinates corresponding to a single Node.
        distance: The desired distance between each Node to the Origin.
        goal_vector_length: The current length of the Goal Vector (in pixels).

    Returns:
        nodes: The re-scaled array of co-ordinates, each co-ordinates corresponding to a single Node.
    '''
    for i in range(len(nodes)):
        node_x = int(distance * (nodes[i][0] / goal_vector_length))
        node_y = int(distance * (nodes[i][1] / goal_vector_length))
        nodes[i] = np.array([node_x, node_y])
    return nodes

def plot_goal_and_nodes(rgb_img_file, rgb_img_w, rgb_img_h, goal_vector):
    '''
    Plots the Goal Vector, and the possible nodes inferred from the given Goal Vector, onto the given RGB Image.

    Params:
        rgb_img_file: The file path for the RGB Image.
        rgb_img_w: The width of the RGB Image.
        rgb_img_h: The height of the RGB Image.
        goal_vector: The dimensions of the Goal Vector given.
    '''

    # Plot the Goal Vector using Matplotlib
    goal_vector_x = np.array([0, goal_vector[0]])
    goal_vector_y = np.array([0, goal_vector[1]])
    goal_vector_location = np.array([int(goal_vector[0] + rgb_img_w / 2), goal_vector[1]])
    print("Goal Vector Given: " + np.array2string(goal_vector))
    print("Goal Vector Co-ordinates (pixels): " + np.array2string(goal_vector_location))
    plt.plot(goal_vector_x, goal_vector_y, color = '#000000')

    # Plot the Nodes inferred from the Goal Vector using Matplotlib
    nodes = calculate_nodes(goal_vector, rgb_img_w, rgb_img_h)
    # Plot it with distance TODO
    for i in range(len(nodes)):
        node_x = np.array([0, nodes[i][0]])
        node_y = np.array([0, nodes[i][1]])
        plt.plot(node_x, node_y, marker = 'o', ms = 5, color = '#404040')

    # Set the width and height of the axes
    plt.xlim([-int(rgb_img_w / 2), int(rgb_img_w / 2)])
    plt.ylim([0, rgb_img_h])
    plt.savefig('goal_axis.png')

    # Remove the axes from view and save it as an image
    plt.axis('off')
    plt.savefig('goal.png', bbox_inches = 'tight', pad_inches = 0)

    # Convert all white pixels to be transparent
    convert_white('goal.png')

    # Combine the RGB Image and the goal & nodes
    combine_images(rgb_img_file, rgb_img_w, rgb_img_h, 'convert.png')

if __name__ == "__main__": 
    
    # RGB Image filename given to the script as input
    rgb_img_file = '../input/' + sys.argv[1]
    rgb_img = img.imread(rgb_img_file)

    # Dimensions of the RGB Image
    rgb_img_dim = rgb_img.shape
    rgb_img_w = rgb_img_dim[1]
    rgb_img_h = rgb_img_dim[0]

    # Goal Vector (Vector in the Direction of the Goal)
    # Currently generated randomly, but will be changed in the future to be input to script
    goal_vector = np.array([random.randint(-int(rgb_img_w/2), int(rgb_img_w/2)), random.randint(0, rgb_img_h)])
    # goal_vector = np.array([random.randint(0, int(rgb_img_w/2)), random.randint(0, rgb_img_h)])
    
    # Plot the Goal Vector onto the RGB Image
    plot_goal_and_nodes(rgb_img_file, rgb_img_w, rgb_img_h, goal_vector)
