# class Parser:
#     def __init__(self, input_file):
#         commands = []
#         for line in input_file:
#             stripped_line = "".join(line.split())
#             command = stripped_line.split("//")[0]
#             if command != "":
#                 commands.append(command)
#         parsed_commands = []
#         for command in commands:
#             parsed_command = []
#             if command.startswith("@"):
#                 parsed_command.append(command)
#             else:
#                 parsed_command.append(command.split("=")[0])
#                 parsed_command.append(command.split("=")[1].rsplit(";")[0])
#                 parsed_command.append(command.split("=")[1].rsplit(";")[1])
#             parsed_commands.append(parsed_command)

def command_parse(input_file):
    commands = []
    for line in input_file:
        stripped_line = "".join(line.split())
        command = stripped_line.split("//")[0]
        if command != "":
            commands.append(command)
    labels_dict = {}
    parsed_commands = []
    current_command_addr = 0
    for command in commands:
        parsed_command = []
        if command.startswith("@"):
            parsed_command.append(command)
            current_command_addr += 1
        elif command.startswith("("):
            labels_dict[command[1:-1]] = current_command_addr
            continue
        elif "=" in command:
            parsed_command.append(command.split("=")[0])
            parsed_command.append("=")
            parsed_command.append(command.split("=")[1])
            current_command_addr += 1
        else:
            parsed_command.append(command.split(";")[0])
            parsed_command.append(";")
            parsed_command.append(command.split(";")[1])
            current_command_addr += 1
        parsed_commands.append(parsed_command)
    print(labels_dict)
    print(parsed_commands)
    return [parsed_commands, labels_dict]  # potenciálně důvod, proč z toho udělat class?
