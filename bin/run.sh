# Filename Variables
FILE="$1"
FILENAME="${FILE%.*}"
GOALX="$2"
GOALY="$3"

# Dense Prediction Transformer
cp input/$FILE ../DPT/input/$FILE
cd ../DPT/
python run_monodepth.py
cp output_monodepth/$FILENAME.png ../rgbd-pathfinder/data/DPT_output/dpt_$FILENAME.png
rm input/$FILE
rm output_monodepth/$FILENAME.png
rm output_monodepth/$FILENAME.pfm
cd ../rgbd-pathfinder/
# eog rgbd-pathfinder/data/DPT_output/$FILENAME.png

# Mask2Former Segmentation
cd ../
cp rgbd-pathfinder/input/$FILE Mask2Former/demo/$FILE
cp -f rgbd-pathfinder/src/m2f_extraction/predictor.py Mask2Former/demo/predictor.py
cd Mask2Former/demo/
# Change the parameters for --config-file and MODEL.WEIGHTS as needed here
python demo.py --config-file ../configs/ade20k/panoptic-segmentation/maskformer2_R50_bs16_160k.yaml --input $FILE --output ../outputs/ --opts MODEL.WEIGHTS ../models/model_final_5c90d4.pkl
cp -f panoptic_seg.pt ../../rgbd-pathfinder/data/M2F_output/panoptic_seg.pt
cp -f segments_info.json ../../rgbd-pathfinder/data/M2F_output/segments_info.json
rm panoptic_seg.pt
rm segments_info.json
cd ..
cp outputs/$FILE ../rgbd-pathfinder/data/M2F_output/m2f_$FILENAME.png
rm demo/$FILE
rm outputs/$FILE
# eog ../rgbd-pathfinder/data/M2F_output/$FILE

# RGBD-Pathfinder
cd ../rgbd-pathfinder/src/
python3 main.py $FILE $2 $3
# eog ../data/RGBDP_output/traversable_$FILENAME.png
