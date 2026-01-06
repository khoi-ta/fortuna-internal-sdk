#!/bin/bash
# Build script for fortuna-archetype-client Python package

set -e

echo "Building fortuna-archetype-client package..."

# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build the wheel
python -m build

# Or use setup.py if build is not available
# python setup.py bdist_wheel

echo "Build complete! Wheel file is in dist/"


