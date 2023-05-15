import shutil
import os
import sys

# get the folder path from the command line arguments
folder_path = sys.argv[1]

# check if the folder exists
if os.path.exists(folder_path):
    # delete the folder
    shutil.rmtree(folder_path)
    print(f"The folder {folder_path} has been deleted.")
else:
    print("The specified folder does not exist.")
