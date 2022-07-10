mkdir data
cd data
mkdir inputs
mkdir models
mkdir configs
mkdir m2f_outputs
mkdir rgbdp_outputs
cd ../src/
git submodule init
git submodule update
cd Mask2Former
touch __init__.py
