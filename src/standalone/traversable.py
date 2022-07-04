'''
Every model has a list of categories with corresponding IDs.

For example, the ADE20K model's categories can be found at:
https://github.com/facebookresearch/Mask2Former/blob/main/mask2former/data/datasets/register_ade20k_panoptic.py

The list below contains the id for all categories deemed as traversable.
To use a model different from ADE20K, find the list of categories for your model of choice and modify the list to only contain ids for categories that you would deem as traversable.
It is advisable to try out the Mask2Former Segmentation separately beforehand, with your model of choice, to judge which categories are useful to you.

''' 

# Modify this if you want to change the definition of "traversable". These ids correspond to ADE20K categories.
# 3: Floor
# 11: Sidewalk, Pavement
# 52: Path
# 53: Stairs
# 59: Stairway, Staircase
# 91: Dirt Track
# 96: Escalator, Moving Staircase, Moving Stairway
# 121: Step, Stair
TRAVERSABLE = [3,11,52,53,59,91,96,121]