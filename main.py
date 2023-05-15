import re
import os
from PIL import Image
import cv2
import moviepy.editor as mp
import sys
import argparse

# Create an argument parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("input_file", help="Input file containing the parking lot instructions")
parser.add_argument("-f", "--fps", type=int, default=5, help="Frames per second for the output video")
parser.add_argument("-d", "--duration_frame", type=int, default=5, help="Duration of the first and last frame in seconds")

# Parse the arguments
args = parser.parse_args()


# read data from file
read_file = []
input_file = args.input_file
input_filename = os.path.splitext(os.path.basename(input_file))[0]


with open(input_file, 'r') as f:
    content = f.read()
    for stat in content.split('\n'):
        ls = stat.strip().replace(' ', '').replace('、', '/').replace('?', '').split('/')
        for i in ls:
            read_file.append(i)

layout = ''

for i in range(0, 6):
    layout += read_file[i]

layout_list = list(layout)

first_six_lines = layout[:6]

# Define the regular expression pattern
pattern = r'\((move-left-two-sized-vehicle|move-right-two-sized-vehicle|move-up-two-sized-vehicle|move-down-two-sized-vehicle|move' \
          r'-right-three-sized-vehicle|move-left-three-sized-vehicle|move-up-three-sized-vehicle|move-down-three-sized-vehicle)\s' \
          r'+(\w+)'

# Search for the pattern in the content
matches = re.findall(pattern, content)

layoutset = []

for i in range(len(matches)):
    if matches[i][0] == 'move-left-two-sized-vehicle':
        first_t = layout_list.index(matches[i][1].upper())
        print(layout_list)
        layout_list[first_t - 1] = layout_list[first_t]
        layout_list[first_t + 1] = '0'
        layoutset.append(layout_list.copy())

    if matches[i][0] == 'move-right-two-sized-vehicle':
        first_t = layout_list.index(matches[i][1].upper())
        print(layout_list)
        layout_list[first_t + 2] = layout_list[first_t]
        layout_list[first_t] = '0'
        layoutset.append(layout_list.copy())

    if matches[i][0] == 'move-up-two-sized-vehicle':
        print(layout_list)
        first_t = layout_list.index(matches[i][1].upper())
        print(layout_list)
        layout_list[first_t - 6] = layout_list[first_t]
        layout_list[first_t + 6] = '0'
        layoutset.append(layout_list.copy())

    if matches[i][0] == 'move-down-two-sized-vehicle':
        first_t = layout_list.index(matches[i][1].upper())
        print(layout_list)
        layout_list[first_t + 12] = layout_list[first_t]
        layout_list[first_t] = '0'
        layoutset.append(layout_list.copy())

    if matches[i][0] == 'move-left-three-sized-vehicle':
        first_t = layout_list.index(matches[i][1].upper())
        print(layout_list)
        layout_list[first_t - 1] = layout_list[first_t]
        layout_list[first_t + 2] = '0'
        layoutset.append(layout_list.copy())

    if matches[i][0] == 'move-right-three-sized-vehicle':
        first_t = layout_list.index(matches[i][1].upper())
        print(layout_list)
        layout_list[first_t + 3] = layout_list[first_t]
        layout_list[first_t] = '0'
        layoutset.append(layout_list.copy())

    if matches[i][0] == 'move-up-three-sized-vehicle':
        first_t = layout_list.index(matches[i][1].upper())
        print(layout_list)
        layout_list[first_t - 6] = layout_list[first_t]
        layout_list[first_t + 12] = '0'
        layoutset.append(layout_list.copy())

    if matches[i][0] == 'move-down-three-sized-vehicle':
        first_t = layout_list.index(matches[i][1].upper())
        print(layout_list)
        layout_list[first_t + 18] = layout_list[first_t]
        layout_list[first_t] = '0'
        layoutset.append(layout_list.copy())

grid_size = 6
output_folder = os.path.join("./pictures", input_filename)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_path_template = os.path.join(output_folder, "output_{}.jpg")

image_symbol_map = {
    '0': "./pic/0.png",
    'A': "./pic/A.png",
    'B': "./pic/B.png",
    'C': "./pic/C.png",
    'D': "./pic/D.png",
    'E': "./pic/E.png",
    'F': "./pic/F.png",
    'G': "./pic/G.png",
    'H': "./pic/H.png",
    'I': "./pic/I.png",
    'J': "./pic/J.png",
    'K': "./pic/K.png",
    'O': "./pic/O.png",
    'P': "./pic/P.png",
    'Q': "./pic/Q.png",
    'R': "./pic/R.png",
    'X': "./pic/X.png"
}

output_image_paths = []

for index, symbol_list in enumerate(layoutset):
    # Open the first image to get dimensions
    first_image = Image.open(next(iter(image_symbol_map.values())))
    img_width, img_height = first_image.size

    # Calculate the dimensions of the combined image
    total_width = img_width * grid_size
    total_height = img_height * grid_size

    # Create a blank image with the combined dimensions
    combined_image = Image.new("RGB", (total_width, total_height))

    # Paste the images onto the combined image canvas
    for i, symbol in enumerate(symbol_list):
        image_path = image_symbol_map[symbol]
        image = Image.open(image_path)
        x = img_width * (i % grid_size)
        y = img_height * (i // grid_size)
        combined_image.paste(image, (x, y))

    # Save the combined image
    output_path = output_path_template.format(index)
    combined_image.save(output_path)
    output_image_paths.append(output_path)
    print(f"Images combined successfully for symbol_list {index}!")

# Video settings
video_output_path = os.path.join(output_folder, f"output_video_{input_filename}.mp4")
fps = args.fps  # Use the fps value from the command line arguments
duration_frame = args.duration_frame  # Duration of the first and last frame in seconds

# Get the dimensions of the first image
first_image = cv2.imread(output_image_paths[0])
height, width, layers = first_image.shape
video_size = (width, height)

# Create a VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(video_output_path, fourcc, fps, video_size)

# Add the first image to the video for a longer duration
for _ in range(fps * duration_frame):
    video_writer.write(first_image)

# Add images to the video
for image_path in output_image_paths:
    image = cv2.imread(image_path)
    video_writer.write(image)

# Add the last image to the video for a longer duration
for _ in range(fps * duration_frame - 1):
    video_writer.write(image)

# Release the video writer and close the video file
video_writer.release()
print("Video created successfully!")

# Load the video using MoviePy
video = mp.VideoFileClip(video_output_path)

# Calculate the video duration
video_duration = len(output_image_paths) / fps + duration_frame

# Load the audio file and trim it to the video duration
audio = mp.AudioFileClip("backgroundmusic.mp3").subclip(0, video_duration)

# Set the audio of the video to the trimmed audio file
video_with_audio = video.set_audio(audio)

# Save the new video with the added audio
output_video_with_audio = os.path.join(output_folder, f"output_video_with_audio_{input_filename}.mp4")
video_with_audio.write_videofile(output_video_with_audio, codec='libx264', audio_codec='aac')

