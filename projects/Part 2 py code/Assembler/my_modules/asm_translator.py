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
        "D+1": "0011111",
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
    var_dict = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }
    addr_of_next_var = 16
    output_lines = []
    for command in parsed_commands:
        if re.match(r"@\d+", command[0]):
            output_lines.append("0" + "{0:015b}".format(int(command[0][1:])) + "\n")
        elif re.match(r"@R\d+", command[0]):
            output_lines.append("0" + "{0:015b}".format(int(command[0][2:])) + "\n")
        elif command[0][0] == "@" and command[0][1:] in labels:
            output_lines.append("0" + "{0:015b}".format(labels[command[0][1:]]) + "\n")
        elif command[0][0] == "@" and command[0][1:] in var_dict:
            output_lines.append("0" + "{0:015b}".format(var_dict[command[0][1:]]) + "\n")
        elif command[0][0] == "@" and command[0][1:] not in var_dict:
            var_dict[command[0][1:]] = addr_of_next_var
            output_lines.append("0" + "{0:015b}".format(addr_of_next_var) + "\n")
            addr_of_next_var += 1
        elif command[1] == "=":
            output_lines.append("111" + comp_dict[command[2]] + dest_dict[command[0]] + "000\n")
        else:
            output_lines.append("111" + comp_dict[command[0]] + "000" + jump_dict[command[2]] + "\n")
    return output_lines
