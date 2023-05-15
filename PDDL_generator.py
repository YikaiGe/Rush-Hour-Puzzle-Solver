import os
import sys

# Get the file to be processed from the command-line argument
input_file_path = sys.argv[1]

output_directory = "./Progress_files"

input_file_name = os.path.basename(input_file_path)
input_file_base_name = os.path.splitext(input_file_name)[0]
output_file_name = f"{input_file_base_name}.pddl"

output_file_path = os.path.join(output_directory, output_file_name)


    # Check if the current file is a regular file (not a folder)
if os.path.isfile(input_file_path):
	with open(input_file_path, 'r') as f:
            read_file = []

            for lines in f:
                ls = lines.strip('\n').replace(' ', '').replace('、', '/').replace('?', '').split('/')
                for i in ls:
                    read_file.append(i)
            f.close()

            # length two cars
            letterx = 0
            lettera = 0
            letterb = 0
            letterc = 0
            letterd = 0
            lettere = 0
            letterf = 0
            letterg = 0
            letterh = 0
            letteri = 0
            letterj = 0
            letterk = 0
            # length three cars
            lettero = 0
            letterp = 0
            letterq = 0
            letterr = 0

            totalrows = 0

            blank = 0

            text = ''
            # how many rows
            lines = 6
            # how many cols
            cols = 6
            # T(op) vs B(ottom) vs R(ight) vs L(eft)
            Exit_direction = read_file[2][0]
            # row or column number/name
            Exit_row_column = read_file[3][0]

            # Using (6, 6+read_file[1][0])
            for i in range(4, 4 + lines):
                text += read_file[i] + '\n'

            posRow = 0

            print(text)
            for i in text:
                if i.isalpha():  # 判断是否是字母
                    if i == "X":
                        letterx += 1
                    if i == "A":
                        lettera += 1
                    if i == "B":
                        letterb += 1
                    if i == "C":
                        letterc += 1
                    if i == "D":
                        letterd += 1
                    if i == "E":
                        lettere += 1
                    if i == "F":
                        letterf += 1
                    if i == "G":
                        letterg += 1
                    if i == "H":
                        letterh += 1
                    if i == "I":
                        letteri += 1
                    if i == "J":
                        letterj += 1
                    if i == "K":
                        letterk += 1

                    # length three
                    if i == "O":
                        lettero += 1
                    if i == "P":
                        letterp += 1
                    if i == "Q":
                        letterq += 1
                    if i == "R":
                        letterr += 1

                elif i.isspace():  # 判断是否是空格
                    totalrows += 1
                else:
                    blank += 1

            car_len = [letterx, lettera, letterb, letterc, letterd, lettere, letterf, letterg, letterh, letteri,
                       letterj, letterk,
                       lettero, letterp, letterq, letterr]

            name = list('XABCDEFGHIJKOPQR')

            colname = list('123456789')

            rowname = list('abcdefghijklmnopqrstuvwxyz')

            print \
                ('Xcarsize:{},Acarsize:{},Bcarsize:{},Ccarsize:{},Dcarsize:{},Ecarsize:{},Fcarsize:{},Gcarsize:{},Hcarsize:{},'
                 'Icarsize:{},Jcarsize:{},Kcarsize:{},Ocarsize:{},Pcarsize:{},Qcarsize:{},Rcarsize:{},Totalrows:{},Blank:{}'.format
                 (letterx, lettera, letterb, letterc, letterd, lettere, letterf, letterg, letterh, letteri, letterj,
                  letterk,
                  lettero, letterp, letterq, letterr, totalrows, blank))

            # Calculate length of each car and separate into different group
            print(car_len)
            two_list = []
            three_list = []
            other_list = []

            i = 0
            for i in range(len(car_len)):
                if car_len[i] == 2:
                    two_list += [name[i]]
                if car_len[i] == 3:
                    three_list += [name[i]]
                else:
                    other_list += [name[i]]

            pddl_trantwo = ''

            for i in range(len(two_list)):
                pddl_trantwo += "    (vehicleSizeTwo {}".format(two_list[i])
                for j in range(len(text)):
                    if text[j] == two_list[i]:
                        poscol = colname[j % (cols + 1)]
                        posrow = rowname[j // (cols + 1)]
                        pddl_trantwo += " {}{}".format(posrow, poscol)
                pddl_trantwo += ") ;A vehicle with two blocks and its initial position\n"

            pddl_tranthree = ''

            for i in range(len(three_list)):
                pddl_tranthree += "    (vehicleSizeThree {}".format(three_list[i])
                for j in range(len(text)):
                    if text[j] == three_list[i]:
                        poscol = colname[j % (cols + 1)]
                        posrow = rowname[j // (cols + 1)]
                        pddl_tranthree += " {}{}".format(posrow, poscol)
                pddl_tranthree += ") ;A vehicle with three blocks and its initial position\n"

            pddl_tranthree += '\n'
            pddl_empty = "    ; Defining initial configuration of the cell:\n"
            times = 0
            for t in range(len(text)):
                if text[t] == '0':
                    times += 1
                    poscol = colname[t % (cols + 1)]
                    posrow = rowname[t // (cols + 1)]
                    pddl_empty += "    (empty {}{})".format(posrow, poscol)
                    if times == lines:
                        pddl_empty += '\n'
                        times = 0

            pddl_empty += '\n'

            all_output = '(define (problem rush-hour-puzzle)\n'
            all_output += '  (:domain rush-hour)\n'

            list_of_strings = two_list + three_list
            separator = " "
            output_string = separator.join(list_of_strings)

            all_output += '  (:objects {} - vehicle '.format(output_string)

            block_num = lines * cols
            output_row = ''
            for i in range(lines):
                for k in range(cols):
                    output_row += ' '
                    output_row += rowname[i]
                    output_row += colname[k]

            all_output += '{} - cell )\n'.format(output_row)

            # output_col = ''
            # for i in range(cols):
            #     output_col += ' '
            #     output_col += colname[i]
            #
            # all_output += '{} - column)\n'.format(output_col)

            output_exrow = ''
            output_exrow_nextto = ''
            output_excol = ''
            output_excol_nextto = ''
            #
            # for i in range(len(rowname)):
            #     if i == Exit_row:
            #         output_exrow = rowname[i]
            #     if i == Exit_row_nextto:
            #         output_exrow_nextto = rowname[i]
            #
            # for i in range(len(colname)):
            #     if i == Exit_col:
            #         output_excol = colname[i]
            #     if i == Exit_col_nextto:
            #         output_excol_nextto = colname[i]

            if Exit_direction == 'R':
                output_excol = colname[cols - 2]
                output_excol_nextto = colname[cols - 1]
                output_exrow = Exit_row_column
                output_exrow_nextto = Exit_row_column

            if Exit_direction == 'L':
                output_excol = colname[0]
                output_excol_nextto = output_excol + 1
                output_exrow = Exit_row_column
                output_exrow_nextto = Exit_row_column

            if Exit_direction == 'U':
                output_exrow = rowname[0]
                output_exrow_nextto = rowname[1]
                output_excol = Exit_row_column
                output_exrow_nextto = Exit_row_column

            if Exit_direction == 'D':
                output_exrow = rowname[lines - 1]
                output_exrow_nextto = rowname[lines - 2]
                output_excol = Exit_row_column
                output_excol_nextto = Exit_row_column

            pddl_direction = '\n' + '    ; Defining vehicle moving direction:\n'

            not_zero = '0'
            vertical_cars = []
            for i in range(len(text) - 1):
                if (text[i] == text[i + 1]) and (text[i] != not_zero[0]):
                    vertical_cars += text[i]

            vertical_cars = list(set(vertical_cars))

            not_blank = ' '
            no_output = ''
            horizontal_cars = []
            horizontal_cars_output = []
            for i in range(len(output_string)):
                if output_string[i] not in vertical_cars and output_string[i] != not_blank:
                    horizontal_cars += output_string[i]
                else:
                    no_output += output_string[i]

            print(set(horizontal_cars))

            for i in range(len(vertical_cars)):
                pddl_direction += "    (horizontalDirection {})\n".format(vertical_cars[i])

            for i in range(len(horizontal_cars)):
                pddl_direction += '    (verticalDirection {})\n'.format(horizontal_cars[i])

            print(pddl_direction)

            next_to_output = '\n' + '    ; defining the grid:\n'
            next_to_output += "    ;horizontal relationships, what's on the right?\n"

            # hR
            for i in range(lines):
                for k in range(cols - 1):
                    next_to_output += "    (horizontalRight {}".format(rowname[i])
                    next_to_output += "{}".format(colname[k])
                    next_to_output += " {}".format(rowname[i])
                    next_to_output += "{})\n".format(colname[k + 1])

            next_to_output += '\n' + "    ; defining the grid:\n"
            next_to_output += "    ; horizontal relationships, what's on the left?\n"

            # hL
            for i in range(lines):
                for k in range(cols - 1):
                    next_to_output += "    (horizontalLeft {}".format(rowname[i])
                    next_to_output += "{}".format(colname[k + 1])
                    next_to_output += " {}".format(rowname[i])
                    next_to_output += "{})\n".format(colname[k])

            next_to_output += '\n' + "    ; defining the grid:\n"
            next_to_output += "    ; vertical relationships, what's on the up?\n"

            # vU
            for i in range(lines - 1):
                for k in range(cols):
                    next_to_output += "    (verticalAbove {}".format(rowname[i + 1])
                    next_to_output += "{}".format(colname[k])
                    next_to_output += " {}".format(rowname[i])
                    next_to_output += "{})\n".format(colname[k])

            next_to_output += '\n' + "    ; defining the cell:\n"
            next_to_output += "    ; vertical relationships, what's on the down?\n"

            # vD
            for i in range(lines - 1):
                for k in range(cols):
                    next_to_output += "    (verticalBelow {}".format(rowname[i])
                    next_to_output += "{}".format(colname[k])
                    next_to_output += " {}".format(rowname[i + 1])
                    next_to_output += "{})\n".format(colname[k])

            next_to_output += "    )\n"

            all_output += "  (:init \n" + '\n' +'    ; Vehicles size and initial occupied cells. \n'
            all_output += pddl_trantwo
            all_output += pddl_tranthree
            all_output += pddl_empty
            all_output += pddl_direction
            all_output += next_to_output
            all_output += '\n' + "  (:goal (and (solved X {}{} {}{}))))".format(output_exrow, output_excol,
                                                                                output_exrow_nextto,
                                                                                output_excol_nextto)

with open(output_file_path, 'w') as fp:
    print(all_output, file=fp)






