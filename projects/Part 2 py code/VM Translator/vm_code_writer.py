pointers= {
    "sp": 0,
    "local": 1,
    "argument": 2,
    "this": 3,
    "that": 4
}
base_addresses = {
    "constant": 0,
    "temp": 5,
    "stack": 256
}

output_asm_commands = []
#add,sub, neg, eq, gt, lt, and, or, not
def vm_translate(parsed_commands, input_file_name):
    sp = base_addresses["stack"]
    for i, command in enumerate(parsed_commands):
        asm_commands = [f"//{' '.join(command)}"]
        command_type = command[0]
        memory_segment = command[1] if len(command) == 3 else None
        segment_index = int(command[2]) if len(command) == 3 else None

        if memory_segment == "constant":
            if command_type == "push":
                asm_commands.extend([f"@{segment_index}", "D=A", f"@{sp}", "M=D", "@0", "M=M+1"])
                sp += 1

        if memory_segment in pointers:
            if command_type == "push":
                asm_commands.extend([f"@{segment_index}", "D=A", f"@{pointers[memory_segment]}", "A=M+D", "D=M", f"@{sp}", "M=D", "@0", "M=M+1"])
                sp += 1
            if command_type == "pop":
                asm_commands.extend([f"@{segment_index}", "D=A", f"@{pointers[memory_segment]}","M=M+D", f"@{sp-1}", "D=M", f"@{pointers[memory_segment]}", "A=M", "M=D", f"@{segment_index}", "D=A",f"@{pointers[memory_segment]}", "M=M-D", "@0", "M=M-1"])
                sp -= 1

        if memory_segment == "temp":
            if command_type == "push":
                asm_commands.extend([f"@{segment_index+5}", "D=M", f"@{sp}", "M=D", "@0", "M=M+1"])
                sp += 1
            if command_type == "pop":
                asm_commands.extend([f"@{sp-1}", "D=M", f"@{5+segment_index}", "M=D", "@0", "M=M-1"])
                sp -= 1

        if memory_segment == "pointer":
            pointer_addr = pointers["this"] if segment_index == 0 else pointers["that"]
            if command_type == "push":
                asm_commands.extend([f"@{pointer_addr}", "D=M", f"@{sp}", "M=D", "@0", "M=M+1"])
                sp += 1
            if command_type == "pop":
                asm_commands.extend([f"@{sp-1}", "D=M", f"@{pointer_addr}", "M=D", "@0", "M=M-1"])
                sp -= 1

        if memory_segment == "static":
            if command_type == "push":
                asm_commands.extend([f"@{input_file_name}.{segment_index}", "D=M", f"@{sp}", "M=D", "@0", "M=M+1"])
                sp += 1
            if command_type == "pop":
                asm_commands.extend([f"@{sp-1}", "D=M", f"@{input_file_name}.{segment_index}", "M=D", "@0", "M=M-1"])
                sp -= 1


        if command_type == "add":
            asm_commands.extend([f"@{sp-1}", "D=M", f"@{sp-2}", "D=D+M", f"@{sp-2}", "M=D", "@0", "M=M-1"])
            sp -= 1
        if command_type == "sub":
            asm_commands.extend([f"@{sp-1}", "D=M", f"@{sp-2}", "D=M-D", f"@{sp-2}", "M=D", "@0", "M=M-1"])
            sp -= 1
        if command_type == "neg":
            asm_commands.extend([f"@{sp-1}", "M=-M"])
        if command_type == "eq":
            asm_commands.extend([f"@{sp-1}", "D=M",f"@{sp-2}", "D=D-M", f"@EQ{i}", "D; JEQ",  f"@{sp-2}", "M=0", f"@END{i}","0;JMP", f"(EQ{i})", f"@{sp-2}", "M=-1", f"(END{i})", "@0", "M=M-1"])
            sp -= 1
        if command_type == "gt":
            asm_commands.extend([f"@{sp-1}", "D=M", f"@{sp-2}", "D=M-D", f"@GT{i}", "D; JGT", f"@{sp-2}", "M=0", f"@END{i}","0;JMP", f"(GT{i})", f"@{sp-2}", "M=-1", f"(END{i})", "@0", "M=M-1"])
            sp -= 1
        if command_type == "lt":
            asm_commands.extend([f"@{sp-1}", "D=M", f"@{sp-2}", "D=D-M", f"@GT{i}", "D; JGT", f"@{sp-2}", "M=0", f"@END{i}","0;JMP", f"(GT{i})", f"@{sp-2}", "M=-1", f"(END{i})", "@0", "M=M-1"])
            sp -= 1
        if command_type == "and":
            asm_commands.extend([f"@{sp-1}", "D=M", f"@{sp-2}", "D=D&M", f"@{sp-2}", "M=D", "@0", "M=M-1"])
            sp -= 1
        if command_type == "or":
            asm_commands.extend([f"@{sp-1}", "D=M", f"@{sp-2}", "D=D|M", f"@{sp-2}", "M=D", "@0", "M=M-1"])
            sp -= 1
        if command_type == "not":
            asm_commands.extend([f"@{sp-1}", "M=!M"])

        output_asm_commands.extend(asm_commands)
    return output_asm_commands

