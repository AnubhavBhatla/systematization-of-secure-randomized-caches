#!/bin/bash

MAKE="make"

show_usage() {
  echo "Usage: $0 [command]"
  echo ""
  echo "Commands:"
  echo "  build   - Builds the project (calls 'make all')"
  echo "  clean   - Cleans the project (calls 'make clean')"
  echo "  help    - Displays this help message"
  echo ""
  echo "Example:"
  echo "  bash buildAll.sh build"
  echo "  bash buildAll.sh clean"
}

if [ -z "$1" ]; then
  echo "Error: No command provided."
  show_usage
  exit 1
fi

case "$1" in
  build)
    echo "============================================================"
    echo "Building cache-model..."
    echo "============================================================"

    cd cache-model/
    "$MAKE" all
    "$MAKE" datagen/librandomgen.a
    echo "============================================================"

    if [ $? -eq 0 ]; then
      echo "cache-model built successfully!"
    else
      echo "Build failed! Check the output above."
      exit 1
    fi

    echo "============================================================"
    echo "Building cachefx..."
    echo "============================================================"
    
    cd ../cachefx/
    "$MAKE" all
    echo "============================================================"

    if [ $? -eq 0 ]; then
      echo "cachefx built successfully!"
    else
      echo "Build failed! Check the output above."
      exit 1
    fi

    echo "============================================================"
    echo "Building low-occupancy..."
    echo "============================================================"

    cd ../low-occupancy/
    git clone https://github.com/SEAL-IIT-KGP/randomized_caches.git
    echo "============================================================"
    
    cd randomized_caches/docker/
    sudo docker build -t randomized-caches .
    cd ../

    sudo cp ../scripts/buildAES.sh buildAES.sh
    sudo cp ../scripts/genNumbers.sh genNumbers.sh
    sudo cp ../scripts/getGE.sh getGE.sh
    mkdir -p aes/analysis/skew-2-ass64
    mkdir -p aes/analysis/skew-2-ass128
    sudo cp ../scripts/run_key1_ass64.sh aes/analysis/skew-2-ass64/run_key1_ass64.sh
    sudo cp ../scripts/run_key2_ass64.sh aes/analysis/skew-2-ass64/run_key2_ass64.sh
    sudo cp ../scripts/run_key1_ass128.sh aes/analysis/skew-2-ass128/run_key1_ass128.sh
    sudo cp ../scripts/run_key2_ass128.sh aes/analysis/skew-2-ass128/run_key2_ass128.sh

    sudo cp ../configs/spec06_config_multiprogram_key1.py ceaser-s/perf_analysis/gem5/configs/example/spec06_config_multiprogram_key1.py
    sudo cp ../configs/spec06_config_multiprogram_key2.py ceaser-s/perf_analysis/gem5/configs/example/spec06_config_multiprogram_key2.py

    FILE="randomized_cache_hello_world/setup.sh"
    OLD_LINE="THREADS=1"
    NEW_LINE="THREADS=60"
    sed -i "s%$OLD_LINE%$NEW_LINE%g" "$FILE"

    echo "============================================================"
    echo "All projects built successfully!"
    echo "============================================================"

    ;;
  clean)
    echo "Cleaning cache-model..."
    echo "============================================================"

    cd cache-model/
    "$MAKE" clean
    echo "============================================================"

    if [ $? -eq 0 ]; then
      echo "cache-model cleaned successfully!"
    else
      echo "Clean failed! Check the output above."
      exit 1
    fi

    echo "============================================================"
    echo "Cleaning cachefx..."
    echo "============================================================"
    
    cd ../cachefx/
    "$MAKE" clean
    echo "============================================================"

    if [ $? -eq 0 ]; then
      echo "cachefx cleaned successfully!"
    else
      echo "Clean failed! Check the output above."
      exit 1
    fi

    cd ../low-occupancy/
    rm -r randomized_caches/
    echo "============================================================"
    echo "low-occupancy cleaned successfully!"

    echo "============================================================"
    echo "All projects cleaned successfully!"
    echo "============================================================"

    ;;
  help)
    echo "============================================================"
    show_usage
    echo "============================================================"

    ;;
  *)
    # Handle unknown commands
    echo "Error: Unknown command '$1'."
    show_usage
    echo "============================================================"

    exit 1
    ;;
esac

exit 0
