import sys
from vm_parser import command_parse
from vm_code_writer import vm_translate


file_name = sys.argv[1].rpartition(".")[0]
input_file = open(sys.argv[1], "r")

output_file_extension = ".asm"
output_file = open(file_name+output_file_extension, "w")

parsed_input = command_parse(input_file)
asm_commands = vm_translate(parsed_input, file_name)

for command in asm_commands:
    output_file.write(command + "\n")

output_file.close()
input_file.close()

