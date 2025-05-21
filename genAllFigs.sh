#!/bin/bash

OPTION=($1)

if [[ "$OPTION" -eq 0 ]]; then
  echo "Re-running simulations and generating tables..."
  echo "============================================================"
elif [[ "$OPTION" -eq 1 ]]; then
  echo "Using original results and generating tables..."
  echo "============================================================"
else
  echo "Invalid option. Usage: bash genAllTables.sh <1/0: 1 - Use generated results 0 - Generate new results and use them>"
  exit 1
fi

cd cache-model
bash genFigs.sh "$OPTION"
cd ..
mv cache-model/*.pdf ./

cd cachefx
bash genFigs.sh "$OPTION"
cd ..
mv cachefx/*.pdf ./

cd low-occupancy
python3 get-figure.py
cd ..
mv low-occupancy/*.pdf ./
