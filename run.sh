#!/bin/bash

# Define the puzzle number
puzzle_number="$1"

# Define the number for the video step fps per second
f_number="$2"

# Define the video start and end seconds
d_number="$3"

# Define the path to DIRNAME (fast downward folder)
dirname_path="$4"

# Define command line options
step_option=false
problem_option=false
video_option=false
pic_option=false

# Check command line options
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -step)
        step_option=true
        ;;
        -problem)
        problem_option=true
        ;;
        -sound)
        video_option=true
        ;;
        -pic)
        pic_option=true
        ;;
        
        *)
        # Ignore unrecognized options
        ;;
    esac
    shift
done

# Generate PDDL problem file
python3 PDDL_generator.py "puzzles/${puzzle_number}.txt"

# Run fast downward
${dirname_path}/fast-downward.py ./domain.pddl ./Progress_files/${puzzle_number}.pddl --search "astar(lmcut())" > ./Progress_files/${puzzle_number}.txt

# Pick steps from fast downward generated file
python3 Pic_Action.py "Progress_files/${puzzle_number}.txt"

# Pick layout of puzzles from the orginal input file
python3 Pic_Layout.py "puzzles/${puzzle_number}.txt"

# Combine the previous picked information together as input file for carton generator
python3 combine.py "Progress_files/${puzzle_number}.txt" "${puzzle_number}.txt"

# Carton generator
python3 main.py "carton/${puzzle_number}.txt" -f ${f_number} -d ${d_number}

# Delete layout
python3 delete.py "${puzzle_number}.txt"


# Delete step if -step option is not present
if [[ "$step_option" = false ]]; then
    python3 delete.py "Progress_files/${puzzle_number}.txt"
fi

if [[ "$step_option" = true ]]; then
    python3 move_around.py "Progress_files/${puzzle_number}.txt" "output"
    python3 delete.py "Progress_files/${puzzle_number}.txt"
fi

# Delete PDDL problem file
if [[ "$problem_option" = false ]]; then
    python3 delete.py "Progress_files/${puzzle_number}.pddl"
fi

if [[ "$problem_option" = true ]]; then
    python3 move_around.py "Progress_files/${puzzle_number}.pddl" "output"
    python3 delete.py "Progress_files/${puzzle_number}.pddl"
fi

# Choose output video
if [[ "$video_option" = false ]]; then
    python3 move_around.py "pictures/${puzzle_number}/output_video_${puzzle_number}.mp4" "output"
    python3 delete.py "pictures/${puzzle_number}/output_video_with_audio_${puzzle_number}.mp4"
    python3 delete.py "pictures/${puzzle_number}/output_video_${puzzle_number}.mp4"
fi

if [[ "$video_option" = true ]]; then
    python3 move_around.py "pictures/${puzzle_number}/output_video_with_audio_${puzzle_number}.mp4" "output"
    python3 delete.py "pictures/${puzzle_number}/output_video_${puzzle_number}.mp4"
    python3 delete.py "pictures/${puzzle_number}/output_video_with_audio_${puzzle_number}.mp4"
fi

# Delete picture set
if [[ "$pic_option" = false ]]; then
    python3 delete_folder.py "pictures/${puzzle_number}"
fi

if [[ "$pic_option" = true ]]; then
    python3 folder_moving.py "pictures/${puzzle_number}" "./output"
fi

python3 delete.py "carton/${puzzle_number}.txt"
