#!/bin/bash

# Define the directory where files will be searched and deleted
DIRECTORY="root/cotfs"

# Check if the directory exists
if [ -d "$DIRECTORY" ]; then
    # Use find to search for files ending in .jonl and delete them
    find "$DIRECTORY" -type f -name "*.jsonl" -exec rm {} \;
    echo "All .jonl files in $DIRECTORY have been deleted."
else
    echo "Directory $DIRECTORY does not exist."
fi
