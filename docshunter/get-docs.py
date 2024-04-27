#!/usr/bin/env python3

import os
import shutil
from halo import Halo

# Get the root directory from user input
root_dir = input("Enter the root directory path: ")

# Create the "found-documents" directory if it doesn't exist
output_dir = "found-documents"
os.makedirs(output_dir, exist_ok=True)

# Create and start the spinner
spinner = Halo(text='Searching for README.md files...', spinner='dots')
spinner.start()

# Walk through the directory tree and find README.md files
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "README.md":
            # Construct the source file path
            src_path = os.path.join(dirpath, filename)
            
            # Construct the destination file path
            relative_path = os.path.relpath(dirpath, root_dir)
            dest_name = relative_path.replace("/", "_") + "_" + filename
            dest_path = os.path.join(output_dir, dest_name)
            
            # Copy the file to the destination
            shutil.copy2(src_path, dest_path)
            spinner.text = f"Copied {src_path} to {dest_path}"

# Stop the spinner and print completion message
spinner.stop()
print("Done copying README.md files.")

