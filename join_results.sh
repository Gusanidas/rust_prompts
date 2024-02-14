#!/bin/bash

# Check if the correct number of arguments is passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 dir1 dir2 dir3"
    exit 1
fi

dir1=$1
dir2=$2
dir3=$3

# Create dir3 if it doesn't exist
mkdir -p "$dir3"

# Process each file in dir1
for file in "$dir1"/*.jsonl; do
    basename=$(basename "$file")
    target="$dir3/$basename"

    if [ -f "$dir2/$basename" ]; then
        # If the file also exists in dir2, concatenate them into dir3
        cat "$file" "$dir2/$basename" > "$target"
    else
        # If the file is unique to dir1, copy it to dir3
        cp "$file" "$target"
    fi
done

# Process files unique to dir2
for file in "$dir2"/*.jsonl; do
    basename=$(basename "$file")
    target="$dir3/$basename"

    if [ ! -f "$dir1/$basename" ]; then
        # If the file does not exist in dir1, copy it to dir3
        cp "$file" "$target"
    fi
    # Files that exist in both directories are already processed in the previous loop
done

echo "Processing complete."
