#!/bin/bash

# Define variables
URL="https://github.com/revarbat/BOSL/archive/refs/tags/v1.0.3.tar.gz"
FILE="BOSL-1.0.3.tar.gz"
DIR="BOSL"

echo "Downloading BOSL v1.0.3..."
curl -L "$URL" -o "$FILE"

echo "Uncompressing..."
# Create the directory first to ensure a clean target
mkdir -p "$DIR"

# Extract while stripping the top-level directory from the tarball 
# so the files land directly inside your $DIR
tar -xzf "$FILE" -C "$DIR" --strip-components=1

echo "Cleaning up..."
rm "$FILE"

echo "Done! The library is ready in: $(pwd)/$DIR"
