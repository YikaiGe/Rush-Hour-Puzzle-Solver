import os
import argparse

# Create an argument parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("file_path", help="The path to the file you want to delete")

# Parse the arguments
args = parser.parse_args()

# Get the file path from the arguments
file_path = args.file_path

# Check if the file exists
if os.path.isfile(file_path):
    # Try to remove the file
    try:
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")
else:
    print(f"The file {file_path} does not exist.")
