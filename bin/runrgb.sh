# Move the code over to run.sh once the RGBDP part is finalised
# Filename Variables
FILE="$1"
FILENAME="${FILE%.*}"
GOALX="$2"
GOALY="$3"

# RGBD-Pathfinder
cd src/
python3 main.py $FILE $2 $3
# cp combine.png ../data/RGBDP_output/$FILENAME.png
# rm *.png
# eog ../data/RGBDP_output/$FILENAME.png
