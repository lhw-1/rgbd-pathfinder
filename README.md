# rgbd-pathfinder
A script that takes in an RGB-D image and finds a traversable path &amp; direction using image segmentation.

1. As input, take in two images (1 RGB image and 1 Depth image) as well as a set of coordinates indicating the direction of the goal (may be arbitrary).
1.1. Alternatively, take in a single image and use a [Dense Prediction Transformer (DPT)](https://github.com/isl-org/DPT) to produce a Depth image corresponding to the RGB image.
2. Perform Image Segmentation on the RGB image, using the [Mask2Former Segmentation tool](https://github.com/facebookresearch/Mask2Former).
3. Through the Image Segmentation, obtain the areas which are considered traversable. This is dependent on the labels available for the specific Image Segmentation model used.
4. With the "Traversable Area", use a classical vector method, i.e. starting from the goal vector (input) and slowly rotating it, to find a traversable path that most closely aligns with the goal vector.
5. Output the Image Segmentation with the output vector as an overlay on top of it, as well as a set of coordinates for the output vector.
