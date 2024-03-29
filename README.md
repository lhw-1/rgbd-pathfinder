# RGBD-Pathfinder

RGBD-Pathfinder is a script that takes in an RGB / RGB-D Image, as well as a Goal Destination (represented by a single set of pixel co-ordinates), and finds a traversable path and direction using image segmentation and obstacle detection.

Currently, only image segmentation is used to find a traversable path; obstacle detection has not been implemented.

The script is also available as a ROS Node [here](https://github.com/lhw-1/rgbd-pathfinder-ros). This allows the script to be used in conjunction with ROS to issue appropriate commands to the robot agent.

---

## Installation

Before the installation, it is recommended to set up a new conda environment (though not mandatory). The code should work with Python >= 3.7.

```
conda create --name my_env python=3.7
conda activate my_env
```

Additionally, install essential libraries using the commands below. Make sure that you are installing the correct CUDA versions for your system GPU. The versions for `pytorch` and `torchvision` that needs to be installed may also differ depending on your CUDA version.

```
conda install pytorch==1.9.0 torchvision==0.10.0 cudatoolkit=10.2 -c pytorch -c nvidia
pip install -U opencv-python
```

RGBD-Pathfinder relies on the [Mask2Former Segmentation tool](https://github.com/facebookresearch/Mask2Former), which in turn relies on the [Detectron2](https://github.com/facebookresearch/detectron2) module, to perform Image Segmentation and Visualisation. 

### Installation: Detectron2

Install the `detectron2` module using the following commands from your project root directory.

You may check [here](https://detectron2.readthedocs.io/en/latest/tutorials/install.html) for more information regarding `detectron2` installation. If using Python 3.6 or lower, you may need to install an older version of `detectron2` from source instead.

```
python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu102/torch1.9/index.html
python -m pip install git+https://github.com/cocodataset/panopticapi.git
python -m pip install git+https://github.com/mcordts/cityscapesScripts.git
```

### Installation: RGBD-Pathfinder

Once `detectron2` has been installed, we can install and set up RGBD-Pathfinder.

Use the commands below to clone this repository and set it up:

```
git clone https://github.com/lhw-1/rgbd-pathfinder.git
cd rgbd-pathfinder
git submodule init
git submodule update
pip install -r requirements.txt
```

Next, use the commands below to download the ADE20K Panoptic Segmentation models and configs:

```
sh bin/init.sh
cd data/models/
```

This downloads the model:

```
wget https://dl.fbaipublicfiles.com/maskformer/mask2former/ade20k/panoptic/maskformer2_R50_bs16_160k/model_final_5c90d4.pkl
```

This downloads the configs:

```
cd ../configs/
curl -o maskformer2_R50_bs16_160k.yaml https://raw.githubusercontent.com/facebookresearch/Mask2Former/main/configs/ade20k/panoptic-segmentation/maskformer2_R50_bs16_160k.yaml
curl -o Base-ADE20K-PanopticSegmentation.yaml https://raw.githubusercontent.com/facebookresearch/Mask2Former/main/configs/ade20k/panoptic-segmentation/Base-ADE20K-PanopticSegmentation.yaml

```

Alternatively, you may download your model of choice from the [Mask2Former Model Zoo](https://github.com/facebookresearch/Mask2Former/blob/main/MODEL_ZOO.md), and the corresponding configuration files from the [Mask2Former Configs](https://github.com/facebookresearch/Mask2Former/tree/main/configs). Refer to [this guide](https://github.com/facebookresearch/Mask2Former/blob/main/GETTING_STARTED.md) for more information on the available models and corresponding configuration files. 

If using a model other than ADE20K, you may also need to modify the list of categories that should be classified as traversable. This list can be found [here](https://github.com/lhw-1/rgbd-pathfinder/blob/main/src/standalone/traversable.py), with instructions on how to do so.

Finally, change `bin/run.sh` to run with the correct model and the configuration file if you are using any model other than the default.

### Known Problems

In some cases, `detectron2` may need to be rebuilt if PyTorch was re-installed during the installation process.

To rebuild `detectron2` from your working directory:

```
cd /path/to/detectron2/
rm -rf build/ **/*.so
python -m pip install -e .
```

---

## Running the Standalone RGBD-Pathfinder

1. Copy the inputs into the `data/inputs/` directory. Currently, only images (.jpg / .png) are supported.
2. Run the command `sh bin/run.sh [IMAGE NAME WITH FILE EXTENSION]`.
* E.g. `sh bin/run.sh test.jpg`
3. The results will be stored in the `data/rgbdp_outputs/` directory once the script finishes running. 

---

## What it currently does:

The current script handles the following:
- Conversion from RGB Image to Image Segmentation using the ADE20K model (default) of the Mask2Former Segmentation Tool.
- Calculation of Traversable Paths inferred from the Image Segmentation, and Plotting the Paths accordingly onto the original RGB Image.
- Instructions for the agent to follow according to the Traversable Paths, depending on the location of the Goal Destination relative to current position.

Currently, additional pruning of possible traversable paths based on Depths / Obstacle Detection has not been implemented.

---
