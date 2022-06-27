mkdir input
mkdir data
cd data/
mkdir DPT_output
mkdir M2F_output
mkdir RGBDP_output
cd ../../Mask2Former/
mkdir models/
mkdir outputs/
cd models/
# Change the Download link as needed here
wget https://dl.fbaipublicfiles.com/maskformer/mask2former/ade20k/panoptic/maskformer2_R50_bs16_160k/model_final_5c90d4.pkl
cd ../../rgbd-pathfinder/
