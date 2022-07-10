# Filename Variables
FILE="$1"
FILENAME="${FILE%.*}"

# Mask2Former Segmentation
cd src
# Change the parameters for --config-file and MODEL.WEIGHTS as needed here
python3 main.py $FILE
# Configs and Model name change to be implemented... in the meantime, directly update src/main.py on Line 94