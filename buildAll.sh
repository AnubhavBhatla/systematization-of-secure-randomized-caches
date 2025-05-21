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
