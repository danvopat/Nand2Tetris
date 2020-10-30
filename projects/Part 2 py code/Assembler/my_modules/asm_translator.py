def asm_translator(parsed_commands, labels):
    import re
    comp_dict = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "M": "1110000",
        "!M": "1110001",
        "-A": "0110011",
        "-M": "1110011",
        "D+1": "00111111",
        "A+1": "0110111",
        "M+1": "1110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "M-1": "1110010",
        "D+A": "0000010",
        "D+M": "1000010",
        "D-A": "0010011",
        "D-M": "1010011",
        "A-D": "0000111",
        "M-D": "1000111",
        "D&A": "0000000",
        "D&M": "1000000",
        "D|A": "0010101",
        "D|M": "1010101",
    }
    dest_dict = {
        "": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }
    jump_dict = {
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }
    output_lines = []
    for command in parsed_commands:
        if re.match(r"@\d+", command[0]):
            output_lines.append("0" + "{0:015b}".format(int(command[0][1:])) + "\n")
        elif re.match(r"@R\d+", command[0]):
            output_lines.append("0" + "{0:015b}".format(int(command[0][2:])) + "\n")
        elif command[0][0] == "@" and command[0][1:] in labels:
            output_lines.append("0" + "{0:015b}".format(labels[command[0][1:]]) + "\n")
        elif command[1] == "=":
            output_lines.append("111" + comp_dict[command[2]] + dest_dict[command[0]] + "000\n")
        else:
            output_lines.append("111" + comp_dict[command[0]] + "000" + jump_dict[command[2]] + "\n")
    return output_lines
