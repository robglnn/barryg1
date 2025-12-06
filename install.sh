#!/bin/bash

# Installation script for Unitree G1 EDU development environment
# This script installs Unitree SDK2, MuJoCo, and Cyclone DDS on macOS

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project directories
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_DIR="$PROJECT_ROOT/dependencies"
CYCLONEDDS_DIR="$DEPS_DIR/cyclonedds"
UNITREE_SDK2_DIR="$DEPS_DIR/unitree_sdk2"
MUJOCO_DIR="$DEPS_DIR/mujoco"

echo -e "${GREEN}=== Unitree G1 EDU Development Environment Setup ===${NC}"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${YELLOW}Warning: This script is optimized for macOS. Some commands may need adjustment.${NC}"
fi

# Create dependencies directory
mkdir -p "$DEPS_DIR"
cd "$DEPS_DIR"

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo -e "${RED}Error: Homebrew is not installed.${NC}"
    echo "Please install Homebrew first: https://brew.sh"
    exit 1
fi

echo -e "${GREEN}[1/4] Installing system dependencies...${NC}"
brew install cmake pkg-config eigen boost yaml-cpp spdlog fmt

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}[2/4] Installing Cyclone DDS...${NC}"
if [ ! -d "$CYCLONEDDS_DIR" ]; then
    echo "Cloning Cyclone DDS repository..."
    git clone https://github.com/eclipse-cyclonedds/cyclonedds.git -b releases/0.10.x
    cd cyclonedds
else
    echo "Cyclone DDS directory exists, updating..."
    cd "$CYCLONEDDS_DIR"
    git pull
fi

# Build Cyclone DDS
mkdir -p build install
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_BUILD_TYPE=Release
cmake --build . --parallel $(sysctl -n hw.ncpu)
cmake --build . --target install
cd "$DEPS_DIR"

CYCLONEDDS_HOME="$CYCLONEDDS_DIR/install"
echo -e "${GREEN}Cyclone DDS installed to: $CYCLONEDDS_HOME${NC}"

echo -e "${GREEN}[3/4] Installing MuJoCo...${NC}"
MUJOCO_VERSION="3.3.4"
MUJOCO_ARCHIVE="mujoco-${MUJOCO_VERSION}-macos-universal2.tar.gz"

if [ ! -d "$MUJOCO_DIR" ]; then
    echo "Downloading MuJoCo ${MUJOCO_VERSION}..."
    cd "$DEPS_DIR"
    curl -L -o "$MUJOCO_ARCHIVE" \
        "https://github.com/google-deepmind/mujoco/releases/download/${MUJOCO_VERSION}/${MUJOCO_ARCHIVE}"
    
    echo "Extracting MuJoCo..."
    tar -xzf "$MUJOCO_ARCHIVE"
    mv "mujoco-${MUJOCO_VERSION}" mujoco
    rm "$MUJOCO_ARCHIVE"
else
    echo "MuJoCo directory already exists, skipping download."
fi

MUJOCO_HOME="$MUJOCO_DIR"
echo -e "${GREEN}MuJoCo installed to: $MUJOCO_HOME${NC}"

# Install MuJoCo Python bindings
echo "Installing MuJoCo Python package..."
pip3 install mujoco

echo -e "${GREEN}[4/4] Installing Unitree SDK2...${NC}"
if [ ! -d "$UNITREE_SDK2_DIR" ]; then
    echo "Cloning Unitree SDK2 repository..."
    git clone https://github.com/unitreerobotics/unitree_sdk2.git
    cd unitree_sdk2
else
    echo "Unitree SDK2 directory exists, updating..."
    cd "$UNITREE_SDK2_DIR"
    git pull
fi

# Build Unitree SDK2
mkdir -p build
cd build
export CYCLONEDDS_HOME="$CYCLONEDDS_HOME"
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --parallel $(sysctl -n hw.ncpu)
sudo cmake --build . --target install
cd "$DEPS_DIR"

echo ""
echo -e "${GREEN}=== Installation Complete ===${NC}"
echo ""
echo "Next steps:"
echo "1. Add the following to your ~/.zshrc or ~/.bash_profile:"
echo ""
echo "   export CYCLONEDDS_HOME=\"$CYCLONEDDS_HOME\""
echo "   export MUJOCO_HOME=\"$MUJOCO_HOME\""
echo "   export DYLD_LIBRARY_PATH=\"\$MUJOCO_HOME/bin:\$DYLD_LIBRARY_PATH\""
echo "   export PATH=\"\$MUJOCO_HOME/bin:\$PATH\""
echo ""
echo "2. Reload your shell configuration:"
echo "   source ~/.zshrc  # or source ~/.bash_profile"
echo ""
echo "3. Verify installations by running the examples in each repository."

