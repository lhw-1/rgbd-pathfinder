# Filename Variables
FILE="$1"
FILENAME="${FILE%.*}"

# Dense Prediction Transformer
cp input/$FILE ../DPT/input/$FILE
cd ../DPT/
python run_monodepth.py
cp output_monodepth/$FILENAME.png ../rgbd-pathfinder/data/DPT_output/$FILENAME.png
rm input/$FILE
rm output_monodepth/$FILENAME.png
rm output_monodepth/$FILENAME.pfm
cd ../
xdg-open rgbd-pathfinder/data/DPT_output/$FILENAME.png

# Mask2Former Segmentation
cp rgbd-pathfinder/input/$FILE Mask2Former/demo/$FILE
cd Mask2Former/demo/
# Change the parameters for --config-file and MODEL.WEIGHTS as needed here
python demo.py --config-file ../configs/ade20k/panoptic-segmentation/maskformer2_R50_bs16_160k.yaml --input $FILE --output ../outputs/ --opts MODEL.WEIGHTS ../models/model_final_5c90d4.pkl
cd ..
cp outputs/$FILE ../rgbd-pathfinder/data/M2F_output/
rm demo/$FILE
rm outputs/$FILE
xdg-open ../rgbd-pathfinder/data/M2F_output/$FILE

# RGBD-Pathfinder
cd ../rgbd-pathfinder/
