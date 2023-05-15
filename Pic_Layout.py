import os
import sys

def read_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return data

def parse_data(data):
    rows = int(data[0].split()[0].strip())
    cols = int(data[1].split()[0].strip())
    data = data[4:]

    grid = []
    for i in range(rows):
        grid.append(data[i].strip())

    return grid

def save_grid_to_file(grid, output_file):
    with open(output_file, 'w') as file:
        for row in grid:
            file.write(row + '\n')

def process_file(input_file_path, output_folder):
    data = read_file(input_file_path)
    grid = parse_data(data)

    output_file = os.path.basename(input_file_path)
    output_file_path = os.path.join(output_folder, output_file)
    save_grid_to_file(grid, output_file_path)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 Pic_Action.py [input_file_path]")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_folder = os.path.dirname(os.path.realpath(__file__))  # Current script directory

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_file(input_file_path, output_folder)


if __name__ == '__main__':
    main()

