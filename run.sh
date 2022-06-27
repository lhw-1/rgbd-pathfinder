# Filename Variables
FILE="$1"
FILENAME="${FILE%.*}"

# Dense Prediction Transformer
cp input/$FILE ../DPT/input/$FILE
cd ../DPT/
python run_monodepth.py
cp output_monodepth/$FILENAME.png ../rgbd-pathfinder/data/DPT_output/$FILENAME.png
cd ..
xdg-open rgbd-pathfinder/data/DPT_output/$FILENAME.png

# Mask2Former Segmentation
cp rgbd-pathfinder/input/$FILE ../Mask2Former/demo/$FILE
cd Mask2Former/
mkdir models/
mkdir outputs/
cd models/
# Change the Download link as needed here
wget https://dl.fbaipublicfiles.com/maskformer/mask2former/ade20k/panoptic/maskformer2_R50_bs16_160k/model_final_5c90d4.pkl
cd ../demo/
# Change the parameters for --config-file and MODEL.WEIGHTS as needed here
python demo.py --config-file ../configs/ade20k/panoptic-segmentation/maskformer2_R50_bs16_160k.yaml --input $FILE --output ../outputs/ --opts MODEL.WEIGHTS ../models/model_final_5c90d4.pkl
cp ../outputs/$1 ../../rgbd-pathfinder/data/M2F_output/

# RGBD-Pathfinder
cd ../../rgbd-pathfinder/
