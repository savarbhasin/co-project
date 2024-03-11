
    # J-TYPE INSTRUCTIONS 

    # Define J-type instruction opcode
J_type_opcode = "1101111"

    # Assemble J-type instructions
def assemble_j_type_instruction(command, line_no):
        t = command

        if len(t) == 3 and t[0] == 'jal':
            rd = Registers.get(t[1], None)

            if rd is None:
                return f"Syntax error: Invalid register name at line {line_no}"

            imm_value = 0
            if t[2].startswith('-'):  # Negative immediate value
                imm_value = (1 << 20) - int(t[2][1:])
            else:
                imm_value = int(t[2])

            imm_binary = format(imm_value & 0xfffff, '020b')

            return imm_binary[0] + imm_binary[10:20] + imm_binary[9] + imm_binary[1:9] + rd + J_type_opcode
        else:
             return f"Syntax error: Invalid J-type instruction or incorrect format at line {line_no}"
