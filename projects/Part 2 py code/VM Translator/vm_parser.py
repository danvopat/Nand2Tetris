def command_parse(input_file):
    commands = []
    for line in input_file:
        command = line.strip().split("//")[0]
        if command != "":
            commands.append(command)

    parsed_commands = []
    for command in commands:
        parsed_command = command.split(" ")
        parsed_commands.append(parsed_command)

    return parsed_commands
