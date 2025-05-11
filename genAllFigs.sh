cd cache-model
bash fetch-all-figs.sh
cd ..
mv cache-model/*.pdf ./
cd CacheFX-SassCache/CacheFX/CacheFX
python3 get-figs.py 1 15
python3 get-figs.py 1 16
cd ../../..
mv CacheFX-SassCache/CacheFX/CacheFX/*.pdf ./
