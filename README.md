# rgbd-pathfinder
A script that takes in an RGB-D image and finds a traversable path &amp; direction using image segmentation.

---

## Running the Script

1. Install the requirements using the given `requirements.txt` file.
Command:
```
pip install -r requirements.txt
```

2. In the `input/` directory, put in the necessary inputs.
3. Run the command `python3 script.py [IMAGE NAME].jpg`.
4. The output will be stored in the `output/` directory.

(Currently only supports a single image. Will be extended in the future to support videos / multiple images.)

---

## What it currently does:

1. Copies the input RGB image in the `input` folder into the `output` folder, and displays it.

---

## What it should do:

1. As input, take in two images (1 RGB image and 1 Depth image) as well as a set of coordinates indicating the direction of the goal (may be arbitrary). The RGB image is mandatory. The depth image is specified with the option `--depth`, and the goal vector coordinates are specified with `--goal`. (Optional arguments not implemented yet)
1.1. Alternatively, take in a single image and use a [Dense Prediction Transformer (DPT)](https://github.com/isl-org/DPT) to produce a Depth image corresponding to the RGB image.
2. Perform Image Segmentation on the RGB image, using the [Mask2Former Segmentation tool](https://github.com/facebookresearch/Mask2Former).
3. Through the Image Segmentation, obtain the areas which are considered traversable. This is dependent on the labels available for the specific Image Segmentation model used.
4. With the "Traversable Area", use a classical vector method, i.e. starting from the goal vector (input) and slowly rotating it, to find a traversable path that most closely aligns with the goal vector.
5. Output the Image Segmentation with the output vector as an overlay on top of it, as well as a set of coordinates for the output vector.

---