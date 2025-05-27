#!/bin/bash

OPTION=($1)

if [[ "$OPTION" -eq 0 ]]; then
  echo "Re-running simulations and generating figures..."
  echo "============================================================"
elif [[ "$OPTION" -eq 1 ]]; then
  echo "Using original results and generating figures..."
  echo "============================================================"
else
  echo "Invalid option. Usage: bash genAllFigs.sh <1/0: 1 - Use generated results 0 - Generate new results and use them>"
  exit 1
fi

cd cache-model
echo "============================================================"
echo "Fetching table $i..."
python3 get-table.py "$OPTION" "2"
echo "============================================================"
cd ..
