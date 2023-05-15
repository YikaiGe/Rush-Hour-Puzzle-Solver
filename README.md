# Rush-Hour-Puzzle-Solver
This is a Rush Hour video solver that could solving 6x6 puzzle.

# Rush-Hour-Puzzle-Solver
This is a Rush Hour video solver that could solving Rush Hour puzzle.

This README.md file provides an overview of how to run and use **‘run.sh’** script in this project.

# Prerequisites
Before you run the script, please ensure you have:

* Python 3 and necessary Python packages **os**, **sys**, **argparse**, **shutil**, **re**, **PIL**, **cv2**, **moviepy.editor**  installed
* Access to the fast downward 

# How to Run

The script **‘run.sh’** can be run with the following command:

```shell
./run.sh <puzzle_number> <f_number> <d_number> <dirname_path> [options]
```


where

* **<puzzle_number>**: Number of the puzzle to solve (1-40 is the puzzle in Rush Hour, and 41-29207 is the puzzle from online).
* **<f_number>**: Frame per second for the output video
* **<d_number>**: Start and end seconds for the video
* **<dirname_path>**: Path to the fast downward folder

# Options:

* **-step**: If this option is present, the script will keep the step files, otherwise it will delete them.
* **-problem**: If this option is present, the script will keep the PDDL problem files, otherwise it will delete them.
* **-sound**: If this option is present, the script will generate a video with sound, otherwise it will generate a video without sound.
* **-pic**: If this option is present, the script will keep the picture set, otherwise it will delete them.



# What the script does

1.The script first generates a PDDL problem file based on the puzzle number.
2.It then uses the Fast Downward planner to solve the problem and outputs the result to a text file.
3.Then, it extracts the steps and the layout of the puzzle from the text file and combines this information into an input file for the video generator.
4.The video generator then creates a video based on the input file.
5.Finally, the script cleans up any unnecessary files and moves the final output to the output directory.
