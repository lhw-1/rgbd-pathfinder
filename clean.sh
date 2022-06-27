# Filename Variables
FILE="$1"
FILENAME="${FILE%.*}"

# Remove Output files from the data/ directory
cd data/DPT_output/
rm $FILENAME.*
cd ../M2F_output/
rm $FILENAME.*
cd ../RGBDP_output/
rm $FILENAME.*
