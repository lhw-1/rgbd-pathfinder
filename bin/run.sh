# Filename Variables
FILE="$1"
FILENAME="${FILE%.*}"
GOALX="$2"
GOALY="$3"

# Mask2Former Segmentation
cd src/mask2former/
# Change the parameters for --config-file and MODEL.WEIGHTS as needed here
python3 demo.py --config-file ../../data/configs/maskformer2_R50_bs16_160k.yaml --input ../../data/inputs/$FILE --output ../../data/m2f_outputs/ --opts MODEL.WEIGHTS ../../data/models/model_final_5c90d4.pkl
# RGBD-Pathfinder
cd ..
python3 main.py $FILE $2 $3
