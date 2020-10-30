# This module handles the operation of translating hack machine language to hack machine code

# Goal:
#   - assembler.py in cmd is executed with name of the original/input file as argument
#   - new file with hack machine code is generated,
#     it has the same name but different extension .hack #todo check the extension

# Procedure:
#   - load the input file
#   - create the empty output file
#   - parse the input file
#   - handle the variables and labels
#   - translate the commands into binary
#   - append the output file with the correct binary code
#   - handle the files - i.e. save/close

import sys
from my_modules.asm_parser import command_parse
from my_modules.asm_translator import asm_translator

input_file = open(sys.argv[1], "r")

file_name = sys.argv[1].rpartition(".")[0]
output_file_extension = ".hack"

output_file = open(file_name+output_file_extension, "a")

parsed_input = command_parse(input_file)
parsed_commands = parsed_input[0]
labels_dict = parsed_input[1]

output_lines = asm_translator(parsed_commands, labels_dict)

for line in output_lines:
    output_file.write(line)


output_file.close()
input_file.close()
