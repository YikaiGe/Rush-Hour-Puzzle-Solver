import os
import sys

def combine_files(file_path1, file_path2, output_path):
    with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2, open(output_path, 'w') as output_file:
        file1_contents = file1.read()
        file2_contents = file2.read()

        output_file.write(file2_contents)
        output_file.write(file1_contents)
    print(f"Combined '{file_path2}' and '{file_path1}' into '{output_path}'")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 like.py [input_file1_path] [input_file2_path]")
        sys.exit(1)

    input_file1_path = sys.argv[1]
    input_file2_path = sys.argv[2]

    # output folder
    output_folder = './carton'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # generate output file path
    output_filename = os.path.basename(input_file1_path)
    output_file_path = os.path.join(output_folder, output_filename)

    combine_files(input_file1_path, input_file2_path, output_file_path)




