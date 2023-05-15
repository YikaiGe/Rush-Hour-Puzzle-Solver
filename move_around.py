import os
import shutil
import argparse

# Create the parser
parser = argparse.ArgumentParser(description="Copy a file from source to target location")

# Add the arguments
parser.add_argument('source_file', type=str, help='The source file')
parser.add_argument('target_dir', type=str, help='The target directory')

# Parse the arguments
args = parser.parse_args()

# Construct the full path of the target file
target_file = os.path.join(args.target_dir, os.path.basename(args.source_file))

# Copy the file to the target directory
shutil.copyfile(args.source_file, target_file)

print("File copied successfully!")


