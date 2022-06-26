# Dense Prediction Transformer
cp input/$1.* ../DPT/input/$1.*
cd ..
cd DPT/
python run_monodepth.py
cp output_monodepth/$1.png ../rgbd-pathfinder/data/DPT_output/
cd ..
xdg-open rgbd-pathfinder/data/DPT_output/$1.png

# Mask2Former Segmentation

# python3 script.py $1