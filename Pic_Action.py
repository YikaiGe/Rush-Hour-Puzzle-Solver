import os
import sys

def filter_data(content):
    lines = content.splitlines()
    filtered_lines = []
    for line in lines:
        if line.startswith("move") or line.startswith("get-out"):
            filtered_line = line.replace(" (1)", "")
            filtered_line = f"({filtered_line})"
            filtered_lines.append(filtered_line)
    return "\n".join(filtered_lines)

def read_and_write_files(input_file_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if input_file_path.endswith(".txt"):
        filename = os.path.basename(input_file_path)
        output_file_path = os.path.join(output_folder, filename)

        with open(input_file_path, 'r') as input_file:
            content = input_file.read()
            filtered_content = filter_data(content)

        with open(output_file_path, 'w') as output_file:
            output_file.write(filtered_content)
        print(f"Processed {input_file_path} -> {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 Pic_Action.py [input_file_path]")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_folder = "./Progress_files"
    read_and_write_files(input_file_path, output_folder)


