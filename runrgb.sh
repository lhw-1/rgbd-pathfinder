# Move the code over to run.sh once the RGBDP part is finalised
# Filename Variables
FILE="$1"
FILENAME="${FILE%.*}"

# RGBD-Pathfinder
cd src/
python3 plot.py $FILE
cp combine.png ../data/RGBDP_output/$FILENAME.png
rm *.png
xdg-open ../data/RGBDP_output/$FILENAME.png
