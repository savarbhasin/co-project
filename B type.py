# Define B-type command mappings
B_type = {
    "beq": {"opcode": "1100011", "funct3": "000"},
    "bne": {"opcode": "1100011", "funct3": "001"},
    "bge": {"opcode": "1100011", "funct3": "101"},
    "blt":{"opcode":"1100011","funct3":"100"},
    "bltu":{"opcode":"1100011","funct3":"110"},
    "bgeu":{"opcode":"1100011","funct3":"111"}

}

# Assemble B-type instructions
def assemble_b_type_instruction(command, line_no):
    t = command

    if t[0] in B_type and len(t) == 4:
        opcode = B_type[t[0]]["opcode"]
        
        funct3 = B_type[t[0]]["funct3"]

        rs1 = Registers.get(t[2], None)
        rs2 = Registers.get(t[1], None)

        if rs1 is None or rs2 is None:
            return "Syntax error: Invalid register name at line {line_no}"

        imm_value = 0
        if t[3].isdigit():
            imm_value = int(t[3], 16)
        else:
            print("Invalid label Immidiate value at line {line_no}")

        imm_binary = format(imm_value & 0xfff, '012b')

        return imm_binary[11] + imm_binary[1:5] + rs2 + rs1 + funct3 + imm_binary[5:] + opcode
    else:
        return "Syntax error: Invalid B-type command or incorrect format"
# Call the function directly
with open("output.txt", "w") as output_file:
    output_file.write(output)