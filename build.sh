#!/bin/bash

# Build script for Unitree G1 EDU development environment
# This script builds Cyclone DDS and Unitree SDK2

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

echo -e "${GREEN}=== Building Unitree G1 EDU Development Environment ===${NC}"
echo ""

# Check for required tools
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed.${NC}"
        return 1
    fi
    return 0
}

echo -e "${GREEN}Checking prerequisites...${NC}"
check_command cmake || exit 1
check_command git || exit 1
check_command python3 || exit 1

# Check if repositories exist
if [ ! -d "$CYCLONEDDS_DIR" ]; then
    echo -e "${RED}Error: Cyclone DDS repository not found.${NC}"
    echo "Please run: cd dependencies && git clone https://github.com/eclipse-cyclonedds/cyclonedds.git -b releases/0.10.x"
    exit 1
fi

if [ ! -d "$UNITREE_SDK2_DIR" ]; then
    echo -e "${RED}Error: Unitree SDK2 repository not found.${NC}"
    echo "Please run: cd dependencies && git clone https://github.com/unitreerobotics/unitree_sdk2.git"
    exit 1
fi

# Build Cyclone DDS
echo -e "${GREEN}[1/2] Building Cyclone DDS...${NC}"
cd "$CYCLONEDDS_DIR"
mkdir -p build install
cd build

if [ ! -f "CMakeCache.txt" ]; then
    cmake .. -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_BUILD_TYPE=Release
fi

cmake --build . --parallel $(sysctl -n hw.ncpu 2>/dev/null || echo 4)
cmake --build . --target install

CYCLONEDDS_HOME="$CYCLONEDDS_DIR/install"
echo -e "${GREEN}Cyclone DDS built successfully!${NC}"
echo "Installation path: $CYCLONEDDS_HOME"
echo ""

# Build Unitree SDK2
echo -e "${GREEN}[2/2] Building Unitree SDK2...${NC}"
cd "$UNITREE_SDK2_DIR"
mkdir -p build
cd build

export CYCLONEDDS_HOME="$CYCLONEDDS_HOME"

if [ ! -f "CMakeCache.txt" ]; then
    cmake .. -DCMAKE_BUILD_TYPE=Release
fi

cmake --build . --parallel $(sysctl -n hw.ncpu 2>/dev/null || echo 4)

echo ""
echo -e "${GREEN}=== Build Complete ===${NC}"
echo ""
echo "Next steps:"
echo "1. Install Unitree SDK2 system-wide (optional):"
echo "   cd $UNITREE_SDK2_DIR/build"
echo "   sudo cmake --build . --target install"
echo ""
echo "2. Set environment variables in ~/.zshrc:"
echo "   export CYCLONEDDS_HOME=\"$CYCLONEDDS_HOME\""
echo "   export MUJOCO_HOME=\"\$(python3 -c 'import mujoco; import os; print(os.path.dirname(mujoco.__file__))')\""
echo "   export PATH=\"\$MUJOCO_HOME/bin:\$PATH\""
echo ""
echo "3. Reload your shell:"
echo "   source ~/.zshrc"

