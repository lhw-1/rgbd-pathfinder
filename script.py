import os
import sys
from PIL import Image

def convert_image(rgb_img_path):
    rgb_img = Image.open("input/" + rgb_img_path)
    rgb_img.show()
    rgb_img = rgb_img.save("output/" + rgb_img_path)

if __name__ == "__main__": 
    # RGB image filename given as mandatory input to the script
    rgb_img_path = sys.argv[1]
    convert_image(rgb_img_path)
