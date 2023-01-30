import argparse
import cv2
import glob
import multiprocessing as mp
import numpy as np
import os
import time
import tqdm
import warnings

# fmt: off
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# fmt: on

from detectron2.config import get_cfg
from detectron2.data.detection_utils import read_image
from detectron2.projects.deeplab import add_deeplab_config
from detectron2.utils.logger import setup_logger
from PIL import Image, ImageDraw

from Mask2Former.mask2former import add_maskformer2_config
from predictor import VisualizationDemo
import traversable

WINDOW_NAME = "mask2former demo"
RGB_PATH = '../data/inputs/'
M2F_PATH = '../data/m2f_outputs/'
RGBDP_PATH = '../data/rgbdp_outputs/'
TRAVERSABLE = traversable.TRAVERSABLE

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

def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    add_deeplab_config(cfg)
    add_maskformer2_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()
    return cfg

def panoptic_segmentation(rgb_img_file):
    # Perform Image Segmentation on the RGB Image    
    mp.set_start_method("spawn", force=True)
    args = argparse.Namespace(confidence_threshold=0.5, config_file='../data/configs/maskformer2_R50_bs16_160k.yaml', input=[rgb_img_file], opts=['MODEL.WEIGHTS', '../data/models/model_final_5c90d4.pkl'], output='../data/m2f_outputs/', video_input=None, webcam=False)
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(args))
    cfg = setup_cfg(args)

    demo = VisualizationDemo(cfg)

    if args.input:
        if len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"
        for path in tqdm.tqdm(args.input, disable=not args.output):
            # use PIL, to be consistent with evaluation
            img = read_image(path, format="BGR")
            start_time = time.time()
            predictions, visualized_output, panoptic_seg, segments_info = demo.run_on_image(img)
            logger.info(
                "{}: {} in {:.2f}s".format(
                    path,
                    "detected {} instances".format(len(predictions["instances"]))
                    if "instances" in predictions
                    else "finished",
                    time.time() - start_time,
                )
            )

            if args.output:
                if os.path.isdir(args.output):
                    assert os.path.isdir(args.output), args.output
                    out_filename = os.path.join(args.output, os.path.basename(path))
                else:
                    assert len(args.input) == 1, "Please specify a directory with args.output"
                    out_filename = args.output
                visualized_output.save(out_filename)
            else:
                cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
                if cv2.waitKey(0) == 27:
                    break  # esc to quit
        
        return panoptic_seg, segments_info

if __name__ == "__main__":

    # Initialise filenames
    rgb_img_file = RGB_PATH + sys.argv[1]

    # Read the necessary images and files from the data/ directory
    rgb_img = Image.open(rgb_img_file)
    IM_WIDTH, IM_HEIGHT = rgb_img.size

    # For the case where the input image is 3 images-in-one
    if IM_WIDTH > 1200 and IM_HEIGHT < 600:

        # Suppose top left of image is (0, 0)
        # We want to crop from (IM_WIDTH / 3, 0) to (2 * IM_WIDTH / 3, IM_HEIGHT-1)
        img = cv2.imread(rgb_img_file)
        crop_img = img[0:IM_HEIGHT-1, IM_WIDTH / 3:2 * IM_WIDTH / 3]
        rgb_img_file = RGB_PATH + "cropped_" + sys.argv[1]
        cv2.imwrite(rgb_img_file, crop_img)
        rgb_img = Image.open(rgb_img_file)

    m2f_panoptic_seg, m2f_segments_info = panoptic_segmentation(rgb_img_file)
    STEER_THRESHOLD = IM_WIDTH // 8

    # Read the Panoptic Segmentation data and calculate the traversable areas and traversable paths
    traversable_areas, traversable_paths = calculate_traversable_paths(m2f_panoptic_seg, m2f_segments_info)
    
    # Prune paths that are blocked by obstacles using the Depths Image
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
    traversable_x = -1
    traversable_y = -1
    for path in traversable_paths:
        # rgb_img_traversable_map[path['x'], path['y']] = (255,0,0,255)
        draw.ellipse((path['x'] - 2, path['y'] - 2, path['x'] + 2, path['y'] + 2), fill=(255, 0, 0))
        if path['y'] > (5 * rgb_img.size[1] / 8) and path['y'] < (7 * rgb_img.size[1] / 8):
            traversable_x = path['x']
            traversable_y = path['y']

    # Print out and Plot the Goal Destination for the agent
    print("\n################################")
    print("Instructions to the Agent:")
    print("################################\n")
    results = open('results.txt', 'a')
    results.write(str(sys.argv[1]) + '\n')
    if traversable_x == -1:
        print("No Path Available.")
        print("Action to be taken: Rotate Right.")
        results.write("No Path Available." + '\n')
        results.write("Action to be taken: Rotate Right." + '\n')
    else:
        print("Path found!")
        print("Path found at X: " + str(traversable_x) + ", Y: " + str(traversable_y) + ".")
        dx = (traversable_x - (IM_WIDTH // 2))
        if dx > STEER_THRESHOLD:
            results.write("Action to be taken: Rotate Right." + '\n')
            print("Action to be taken: Rotate Right.")
        elif dx < -STEER_THRESHOLD:
            results.write("Action to be taken: Rotate Left." + '\n')
            print("Action to be taken: Rotate Left.")
        else:
            results.write("Action to be taken: Move Forward." + '\n')
            print("Action to be taken: Move Forward.")
    
    # Save the copy as a separate Image
    rgb_img_traversable.save(RGBDP_PATH + "traversable_" + sys.argv[1], "PNG")
    results.write('\n')
    results.close()
