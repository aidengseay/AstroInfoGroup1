#!/bin/bash

# Exit if any command fails
set -e

# Run the Python script
python3 FitLightCurve.py

# Optional: Notify completion
echo "FitLightCurve.py finished successfully."
