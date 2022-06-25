# rgbd-pathfinder

RGBD-Pathfinder is a script that uses an RGB / RGB-D Image and finds a traversable path and direction using image segmentation.

---

## Installation

Before the installation, it's a good idea to start a new conda environment, though not necessary.

```
conda create --name my_env python=3.8
conda activate my_env
```

RGBD-Pathfinder currently relies on two separate tools that need to be installed:

1. The [Dense Prediction Transformer (DPT)](https://github.com/isl-org/DPT) predicts the Depth image from the given RGB Image. **If you have access to the Depth Image, you may skip this step.**
2. The [Mask2Former Segmentation tool](https://github.com/facebookresearch/Mask2Former) is used to perform Image Segmentation on the given RGB Image.

Using the following commands, install the Dense Prediction Transformer. Note that we use the monocular depth estimation model (default) for the DPT.

```
git clone https://github.com/isl-org/DPT.git
cd DPT/weights/
wget https://github.com/intel-isl/DPT/releases/download/1_0/dpt_hybrid-midas-501f0c75.pt
cd ..
pip install -r requirements.txt
```

Next, install the Mask2Former Segmentation tool. To do this, we first install some essential libraries:

```
conda install pytorch==1.9.0 torchvision==0.10.0 cudatoolkit=11.1 -c pytorch -c nvidia
pip install -U opencv-python
```

Make sure that you are installing the correct CUDA versions for your system GPU. The version for `pytorch` and `torchvision` may also differ depending on your CUDA version.

We then install the Object Detection tool, `detectron2`:

```
git clone git@github.com:facebookresearch/detectron2.git
cd detectron2
pip install -e .
pip install git+https://github.com/cocodataset/panopticapi.git
pip install git+https://github.com/mcordts/cityscapesScripts.git
```

You may check [here](https://detectron2.readthedocs.io/en/latest/tutorials/install.html) for more information.

Next, we install the Mask2Former tool itself:

```
cd ..
git clone git@github.com:facebookresearch/Mask2Former.git
cd Mask2Former
pip install -r requirements.txt
cd mask2former/modeling/pixel_decoder/ops
sh make.sh
```

Finally, we install the dependencies for the RGBD-Pathfinder:

```
cd ..
git clone https://github.com/lhw-1/rgbd-pathfinder.git
cd rgbd-pathfinder
pip install -r requirements.txt
```

---

## Running the RGBD-Pathfinder

1. In the `input/` directory, put in the necessary inputs.
2. Run the command `python3 script.py [IMAGE NAME].jpg`.
3. The output will be stored in the `output/` directory.

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
