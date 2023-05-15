import os
import sys
import shutil

def move_around_folder(original_dir, target_dir):
    # Get the absolute path to the target directory
    target_dir_abs = os.path.join(os.getcwd(), target_dir)

    # Get the name of the folder to be moved
    folder_name = os.path.basename(original_dir)

    # Create the new path for the folder
    new_path = os.path.join(target_dir_abs, folder_name)

    # Move the folder
    shutil.move(original_dir, new_path)

    print(f"Moved folder to: {new_path}")

# get command-line arguments
if len(sys.argv) != 3:
    print("Usage: python3 move.py <original_dir> <target_dir>")
else:
    original_dir = sys.argv[1]
    target_dir = sys.argv[2]
    move_around_folder(original_dir, target_dir)


