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

input_file = open(sys.argv[1], "r")

file_name = sys.argv[1].rpartition(".")[0]
output_file_extension = ".hack"

output_file = open(file_name+output_file_extension,"a")

commands = []
for line in input_file:
    stripped_line = "".join(line.split())
    command = stripped_line.split("//")[0]
    if command != "":
        commands.append(command)
parsed_commands = []
for command in commands:
    parsed_command = []
    if command.startswith("@"):
        parsed_command.append(command)
    elif "=" in command:
        parsed_command.append(command.split("=")[0])
        parsed_command.append("=")
        parsed_command.append(command.split("=")[1])
    else:
        parsed_command.append(command.split(";")[0])
        parsed_command.append(";")
        parsed_command.append(command.split(";")[1])
    parsed_commands.append(parsed_command)

comp_dict = {
    "0" : "0101010",
    "1" : "0111111",
    "-1" : "0111010",
    "D" : "0001100",
    "A" : "0110000",
    "!D" : "0001101",
    "!A" : "0110001",
    "M" : "1110000",
    "!M" : "1110001",
    "-A" : "0110011",
    "-M" : "1110011",
    "D+1" : "00111111",
    "A+1" : "0110111",
    "M+1" : "1110111",
    "D-1" : "0001110",
    "A-1" : "0110010",
    "M-1" : "1110010",
    "D+A" : "0000010",
    "D+M" : "1000010",
    "D-A" : "0010011",
    "D-M" : "1010011",
    "A-D" : "0000111",
    "M-D": "1000111",
    "D&A" : "0000000",
    "D&M": "1000000",
    "D|A" : "0010101",
    "D|M": "1010101",
}
dest_dict = {
    "" : "000",
    "M" : "001",
    "D" : "010",
    "MD" : "011",
    "A" : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD" : "111"
}
jump_dict = {
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111"
}
for command in parsed_commands:
    if command[0][0] == "@":
        output_file.write("0"+"{0:015b}".format(int(command[0][1:]))+"\n")
    elif command[1] == "=":
        output_file.write("111"+comp_dict[command[2]]+dest_dict[command[0]]+"000\n")
    else:
        output_file.write("111" + comp_dict[command[0]] + "000" + jump_dict[command[2]] + "\n")

print(parsed_commands)

output_file.close()
input_file.close()

