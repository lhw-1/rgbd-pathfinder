# RGBD-Pathfinder

RGBD-Pathfinder is a script that takes in an RGB / RGB-D Image, as well as a Goal Destination (represented by vector co-ordinates), and finds a traversable path and direction using obstacle detection and image segmentation.

This project is currently in progress and has not been fully implemented.

---

## Installation

Before the installation, it is recommended to set up a new conda environment (though not mandatory). 

```
conda create --name my_env python=3.8
conda activate my_env
```

Additionally, install the following essential libraries:

```
conda install pytorch==1.9.0 torchvision==0.10.0 cudatoolkit=11.1 -c pytorch -c nvidia
```

Make sure that you are installing the correct CUDA versions for your system GPU. The versions for `pytorch` and `torchvision` that needs to be installed may also differ depending on your CUDA version.

RGBD-Pathfinder relies on two separate tools that need to be installed together. 

1. The [Dense Prediction Transformer (DPT)](https://github.com/isl-org/DPT) predicts the Depth image from the given RGB Image. **If you have access to the Depth Image, you may skip this step.**
2. The [Mask2Former Segmentation tool](https://github.com/facebookresearch/Mask2Former) is used to perform Image Segmentation on the given RGB Image.

### Installation: Dense Prediction Transformer (DPT)

Install the Dense Prediction Transformer using the following commands. Note that we are currently using the monocular depth estimation model (by default). **Note: Do NOT install the dependencies of the `requirements.txt` for DPT, as they are outdated. The updated dependencies are covered by the `requirements.txt` of RGBD-Pathfinder instead.**

As mentioned above, this step may be skipped if you already have access to the Depth Image.

```
git clone https://github.com/isl-org/DPT.git
cd DPT/weights/
wget https://github.com/intel-isl/DPT/releases/download/1_0/dpt_hybrid-midas-501f0c75.pt
```

### Installation: Mask2Former Segmentation Tool

Install the Mask2Former Segmentation Tool using the following commands. 

We first need to install the base Object Detection module, `detectron2`:

```
cd ../../
git clone https://github.com/facebookresearch/detectron2.git
cd detectron2
pip install -e .
pip install git+https://github.com/cocodataset/panopticapi.git
pip install git+https://github.com/mcordts/cityscapesScripts.git
```

You may check [here](https://detectron2.readthedocs.io/en/latest/tutorials/install.html) for more information regarding `detectron2` installation.

Next, we install the Mask2Former tool itself:

```
cd ..
git clone https://github.com/facebookresearch/Mask2Former.git
cd Mask2Former
pip install -r requirements.txt
sh mask2former/modeling/pixel_decoder/ops/make.sh
```

### Installation: RGBD-Pathfinder

Finally, we install the remaining dependencies for the RGBD-Pathfinder and initialise the directories:

```
cd ..
git clone https://github.com/lhw-1/rgbd-pathfinder.git
cd rgbd-pathfinder
pip install -r requirements.txt
pip install -U opencv-python
sh init.sh
```

### Known Problems

In some cases, `detectron2` may need to be rebuilt if PyTorch was re-installed during the installation process.

To rebuild `detectron2` from your working directory:

```
cd detectron2/
rm -rf build/ **/*.so
python -m pip install -e .
```

---

## Running the RGBD-Pathfinder

1. Copy the RGB Image into the `input/` directory.
2. Run the command `sh run.sh [IMAGE NAME WITH FILE EXTENSION]` if on Linux, or `Bash run.sh [IMAGE NAME WITH FILE EXTENSION]` if on Windows. This currently displays the Depth and Segmentation Images of the original RGB Image given.
3. Run the command `sh runrgb.sh [IMAGE NAME WITH FILE EXTENSION]` if on Linux, or `Bash runrgb.sh [IMAGE NAME WITH FILE EXTENSION]` if on Windows. This currently displays all possible Nodes inferred from the Goal Vector given, plotted on the original RGB Image given.
3. The results will be displayed once the process has finished.

(Currently only supports a single image. Will be extended in the future to support videos / multiple images.)

### Using different Mask2Former Models

To use different Mask2Former models, change Line 12 of `init.sh` to the corresponding download link of your preferred model, and change the model and configuration file used in Line 19 of `run.sh`. Refer to [this guide](https://github.com/facebookresearch/Mask2Former/blob/main/GETTING_STARTED.md) for more information. 

---

## What it currently does:

The current script only handles the following:
- Conversion from RGB Image to Depth Image using DPT.
- Conversion from RGB Image to Image Segmentation using the ADE20K model of the Mask2Former Segmentation Tool.
- Calculation and Plotting of all available Nodes, inferred through the given Goal Vector, onto the RGB Image.

The next step is to integrate the Depth Image and the Segmentation Image, and prune Nodes using them.
Another issue is to modify the current Origin from the Bottom to Eye-Level.

---

## What it should do:

1. As input, take in two images (1 RGB image and 1 Depth image) as well as a set of coordinates indicating the direction of the goal (may be arbitrary). The RGB image is mandatory. The depth image is specified with the option `--depth`, and the goal vector coordinates are specified with `--goal`. (Optional arguments not implemented yet)
1.1. Alternatively, take in a single image and use a [Dense Prediction Transformer (DPT)](https://github.com/isl-org/DPT) to produce a Depth image corresponding to the RGB image.
2. Perform Image Segmentation on the RGB image, using the [Mask2Former Segmentation tool](https://github.com/facebookresearch/Mask2Former).
3. Through the Depths Image and the Image Segmentation, obtain the areas which are considered traversable. This is also dependent on the labels available for the specific Image Segmentation model used.
4. With the "Traversable Area", use a classical vector method, i.e. starting from the goal vector (input) and slowly rotating it, to find a traversable path that most closely aligns with the goal vector.
5. Output the Image Segmentation with the output vector as an overlay on top of it, as well as a set of coordinates for the output vector.

---
