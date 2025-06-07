# Install cmake
sudo apt-get install cmake

sudo python3 -m pip install numpy
sudo python3 -m pip install scipy
sudo apt install -m python-six

# Build binaries for AES
cd aes/
cd aes_profiled_key/C/

cmake .
make

cd ../../
cd aes_victim_key/C/

cmake .
make

cd ../../

mkdir -p analysis/skew-2-ass64/
cp analysis/ceaser/analysis.py analysis/skew-2-ass64/
cp analysis/ceaser/guessing_entropy.py analysis/skew-2-ass64/
cp analysis/ceaser/run.sh analysis/skew-2-ass64/

mkdir -p analysis/skew-2-ass128/
cp analysis/ceaser/analysis.py analysis/skew-2-ass128/
cp analysis/ceaser/guessing_entropy.py analysis/skew-2-ass128/
cp analysis/ceaser/run.sh analysis/skew-2-ass128/