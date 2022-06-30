# RGBD-Pathfinder

RGBD-Pathfinder is a script that takes in an RGB / RGB-D Image, as well as a Goal Destination (represented by a single set of pixel co-ordinates), and finds a traversable path and direction using image segmentation and obstacle detection.

This project is currently in progress and has not been fully implemented.

---

## Installation

Before the installation, it is recommended to set up a new conda environment (though not mandatory). The code should work with Python >= 3.6.

```
conda create --name my_env python=3.6
conda activate my_env
```

Additionally, install the following essential libraries:

```
conda install pytorch==1.9.0 torchvision==0.10.0 cudatoolkit=10.2 -c pytorch -c nvidia
pip install -U opencv-python
```

Make sure that you are installing the correct CUDA versions for your system GPU. The versions for `pytorch` and `torchvision` that needs to be installed may also differ depending on your CUDA version.

RGBD-Pathfinder also relies on two separate tools that need to be installed alongside the main repository.

1. The [Dense Prediction Transformer (DPT)](https://github.com/isl-org/DPT) predicts the Depth image from the given RGB Image. **If you have access to the Depth Image, you may skip this step.**
2. The [Mask2Former Segmentation tool](https://github.com/facebookresearch/Mask2Former) is used to perform Image Segmentation on the given RGB Image.

### Installation: Dense Prediction Transformer (DPT)

Install the Dense Prediction Transformer using the following commands. Note that we are currently using the monocular depth estimation model (by default). **Note: Do NOT install the dependencies of the `requirements.txt` for DPT, as they are outdated. The updated dependencies are covered by the `requirements.txt` of RGBD-Pathfinder instead.**

As mentioned above, this step may be skipped if you already have access to the Depth Image.

```
git clone https://github.com/isl-org/DPT.git
cd DPT/weights/
wget https://github.com/intel-isl/DPT/releases/download/1_0/dpt_hybrid-midas-501f0c75.pt
cd ../
```

### Installation: Mask2Former Segmentation Tool

Install the Mask2Former Segmentation Tool using the following commands. 

We first need to install the base Object Detection module, `detectron2`:

```
cd ../
git clone https://github.com/facebookresearch/detectron2.git
cd detectron2/
pip install -e .
pip install git+https://github.com/cocodataset/panopticapi.git
pip install git+https://github.com/mcordts/cityscapesScripts.git
```

You may check [here](https://detectron2.readthedocs.io/en/latest/tutorials/install.html) for more information regarding `detectron2` installation.

Next, we install the Mask2Former tool itself:

```
cd ../
git clone https://github.com/facebookresearch/Mask2Former.git
cd Mask2Former/
pip install -r requirements.txt
cd mask2former/modeling/pixel_decoder/ops/
sh make.sh
```

### Installation: RGBD-Pathfinder

Finally, we install the remaining dependencies for the RGBD-Pathfinder and initialise the directories:

```
cd ../
git clone https://github.com/lhw-1/rgbd-pathfinder.git
cd rgbd-pathfinder/
pip install -r requirements.txt
sh bin/init.sh
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

1. Copy the inputs into the `input/` directory. Currently, only images (.jpg / .png) ~~and ROS bag files (.bag)~~ are supported.
2. Run the command `sh bin/run.sh [IMAGE NAME WITH FILE EXTENSION]`.
- E.g. `sh bin/run.sh test.jpg`
- Yet to be implemented: `sh bin/run.sh [IMAGE NAME WITH FILE EXTENSION] [Goal x-coordinate] [Goal y-coordinate]`
3. The results will be stored in the `data/` directory once the script finishes running. The Depths Image can be found in the `data/DPT_output` directory, the Segmentation Image can be found in the `data/M2F_output` directory, and the Traversable Paths Image can be found in the `data/RGBDP_output` directory.

Currently, the Goal Destination coordinates are randomly generated for testing purposes. Once the testing phase is over, the script will be modified to accommodate custom Goal Destinations.

### Using different Mask2Former Models

To use different Mask2Former models, make changes in `bin/init.sh` to the corresponding download link of your preferred model, and make changes in `bin/run.sh` to the model and configuration file to be used instead. Refer to [this guide](https://github.com/facebookresearch/Mask2Former/blob/main/GETTING_STARTED.md) for more information on the available models and corresponding configuration files. 

---

## What it currently does:

The current script handles the following:
- Conversion from RGB Image to Depth Image using DPT.
- Conversion from RGB Image to Image Segmentation using the ADE20K model of the Mask2Former Segmentation Tool.
- Calculation of Traversable Paths inferred from the Image Segmentation, and Plotting the Paths accordingly onto the original RGB Image.
- Instructions for the agent to follow according to the Traversable Paths, depending on the location of the Goal Destination relative to current position.

Currently, pruning paths based on Depths / Obstacle Detection has not been implemented.

---
