import sys

Registers = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100",
    "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "s1": "01001",
    "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110",
    "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011",
    "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101",
    "t5": "11110", "t6": "11111"
}


updated_register = {i: '0'*32 for i in Registers.keys()}
updated_register['sp'] = '0'*23 + '100000000'

Registers = {val:key for key,val in Registers.items()}


data_memory = {hex(0x0001_0000 + i*4): '00000000000000000000000000000000' for i in range(32)}


R_type = {
    'add': ['0000000', '000', '0110011'], 'sub': ['0100000', '000', '0110011'],
    'sll': ['0000000', '001', '0110011'], 'slt': ['0000000', '010', '0110011'],
    'sltu': ['0000000', '011', '0110011'], 'xor': ['0000000', '100', '0110011'],
    'srl': ['0000000', '101', '0110011'], 'or': ['0000000', '110', '0110011'],
    'and': ['0000000', '111', '0110011']
}
R_type_reversed = {tuple(value): key for key, value in R_type.items()}

# I-Type Instructions
I_type = {
    'lw': ['010', '0000011'], 'addi': ['000', '0010011'],
    'sltiu': ['011', '0010011'], 'jalr': ['000', '1100111']
}

# B-Type Instructions
B_type = {
    'beq': ['000', '1100011'], 'bne': ['001', '1100011'],
    'blt': ['100', '1100011'], 'bge': ['101', '1100011'],
    'bltu': ['110', '1100011'], 'bgeu': ['111', '1100011']
}

BONUS_Type = {
    'rst': ['0000000', '000', '0110111'],
    'halt': ['0000000', '000', '0111001'],
    'rvrs': ['0000001', '000', '0110111'],
    'mul': ['0000001', '000', '0111001']
}

def reset_registers():
    updated_register = {register: '0'*32 for register in Registers.keys()}
    updated_register['zero'] = '0'*32  
    return updated_register
def bonus(line, updated_register, pc):
    opcode = line[25:32]
    command = line[0:7]
    
    if command == '0000000':  
        if opcode == '0110111':  # rst instruction
            updated_register = reset_registers()
        elif opcode == '0111001':  # halt instruction
            pc = '1'*32  
            return updated_register, pc 
    elif command == '0000001': 
        if opcode == '0110111': 
            rd, rs = Registers[line[20:25]], Registers[line[12:17]]
            updated_register[rd] = updated_register[rs][::-1]
        elif opcode == '0111001':  # mul instruction
            rd, rs1, rs2 = Registers[line[20:25]], Registers[line[12:17]], Registers[line[7:12]]
            updated_register[rd] = bin(int(updated_register[rs1], 2) * int(updated_register[rs2], 2))[2:].zfill(32)

    return updated_register, pc


def twos_complement(number, bit_length):
    if number >= 0:
        binary = bin(number)[2:].zfill(bit_length)
        return binary
    binary = bin(abs(number))[2:]  
    binary = binary.zfill(bit_length)
    inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary)
    inverted_binary = bin(int(inverted_binary, 2) + 1)[2:] 
    return inverted_binary.zfill(bit_length)


def calculate_twos_complement(binary):

    inverted = ''.join('1' if bit == '0' else '0' for bit in binary)
    
    carry = 1
    result = ''
    for bit in inverted[::-1]:
        if bit == '0' and carry == 1:
            result = '1' + result
            carry = 0
        elif bit == '1' and carry == 1:
            result = '0' + result
            carry = 1
        else:
            result = bit + result
    
    return result

def convert_binary_to_int(binary_str):
    if binary_str[0] == '1':
        two_complement = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        two_complement = bin(int(two_complement, 2) + 1)[2:]
        return -int(two_complement, 2)
    else:
        return int(binary_str, 2)

def midam_r(line, updated_register):
    funct7 = line[0:7]
    funct3 = line[17:20]
    opcode = '0110011'
    op = R_type_reversed[(funct7, funct3, opcode)]
    rs2 = updated_register[Registers[line[7:12]]]
    rs1 = updated_register[Registers[line[12:17]]]
    
    
    print(op,rs2,rs1)
    rd = Registers[line[20:25]]
    
    ops = {
        'add':lambda b,c:twos_complement(b+c,32),
        'slt': lambda b,c: '0'*31+'1' if b>c else '0'*32,
        'xor': lambda b, c: twos_complement(b^c,32),
        'or': lambda b,c: twos_complement(b | c,32),
        'and': lambda b,c: twos_complement(b&c,32),
        'sub': lambda b,c: twos_complement(c-b,32)
    }
    operations = {
        'add': lambda b, c: bin(int(b, 2) + int(c, 2))[2:].zfill(32),
        'slt': lambda b, c: '0'*31+'1' if int(b, 2) < int(c, 2) else '0'*32,
        'sltu': lambda b, c: '0'*31+'1' if int(b, 2) < int(c, 2) else '0'*32,
        'xor': lambda b, c: bin(int(b, 2) ^ int(c, 2))[2:].zfill(32),
        'or': lambda b, c: bin(int(b, 2) | int(c, 2))[2:].zfill(32),
        'and': lambda b, c: bin(int(b, 2) & int(c, 2))[2:].zfill(32),
        'sub': lambda b, c: twos_complement(int(c, 2) - int(b, 2),32),
        'sll': lambda b, c: bin((int(c, 2) << int(b[27:32], 2)))[2:].zfill(32),
        'srl': lambda b, c: bin((int(c, 2) >> int(b[27:32], 2)) & 0xFFFFFFFF)[2:].zfill(32)
    }
    signed_rs2 = convert_binary_to_int(rs2)
    signed_rs1 = convert_binary_to_int(rs1)
    if op in ops:
        updated_register[rd] = ops[op](signed_rs2, signed_rs1)
    elif funct3 == '001':
        updated_register[rd] = twos_complement(convert_binary_to_int(rs1)<<int(rs2[27:32],2),32)
    elif funct3 == '101':
        updated_register[rd] = twos_complement(convert_binary_to_int(rs1)>>int(rs2[27:32],2),32)
    elif funct3 == '011':
        updated_register[rd] = '0'*31 + '1' if int(rs2,2) < int(rs1,2) else '0'*32
    
    return updated_register



def midam_u(line, updated_register, pc):
    rd = Registers[line[20:25]]
    imm = (line[:20])
    if imm[0] == '1':
        imm = calculate_twos_complement(imm)
        imm = -int(imm,2)
        
    else:
        imm = int(imm,2)  
    opcode = line[25:32]

    if opcode == '0110111':  # lui instruction
        updated_register[rd] = bin(imm << 12)[2:].zfill(32)
        print(f"U-type instruction: lui {rd}, {imm}")
    elif opcode == '0010111':  # auipc instruction
        updated_register[rd] = bin(int(pc, 2) + (imm << 12))[2:].zfill(32)
        print(f"U-type instruction: auipc {rd}, {imm}")

    return updated_register

def savar_i(line, updated_register, pc):
    rs1 = updated_register[Registers[line[12:17]]]
    rd = Registers[line[20:25]]
    imm = line[0:12]
    x = int(line[0:12])
    
    if imm[0] == '1':
        imm = calculate_twos_complement(imm)
        imm = -int(imm,2)
        
    else:
        imm = int(imm,2)    
    opcode = line[25:32]

    if opcode == '0000011':  # lw instruction
        # mem_address = bin(int(rs1, 2) + imm)[2:].zfill(32)
        mem_address = bin(convert_binary_to_int(rs1) + imm)[2:].zfill(32)
        updated_register[rd] = data_memory[hex(int(mem_address, 2))]
        print(f"I-type instruction: lw {rd}, {imm}({Registers[line[12:17]]})")
        return updated_register, pc
    
    elif opcode == '1100111':  # jalr instruction
        updated_register[rd] = twos_complement(int(pc, 2) + 4, 32)
        
        # new_pc = bin(int(rs1, 2) + imm)[2:].zfill(32)
        # new_pc = twos_complement(int(rs1,2)+imm,32)
        new_pc = twos_complement(convert_binary_to_int(rs1) + imm,32)
        new_pc = new_pc[:-1] + '0'

        print(f"I-type instruction: jalr {rd}, {Registers[line[12:17]]}, {imm}")
        return updated_register, new_pc
    
    elif line[17:20] == '000':  # addi instruction
        
        # updated_register[rd] = twos_complement(int(rs1,2)+imm,32)
        updated_register[rd] = twos_complement(convert_binary_to_int(rs1) + imm,32)
        
        print(f"I-type instruction: addi {rd}, {Registers[line[12:17]]}, {imm}")

        return updated_register, pc
    else:  # sltiu instruction

        updated_register[rd] = '0'*31+'1' if int(rs1, 2) < x else '0'*32
        print(f"I-type instruction: sltiu {rd}, {Registers[line[12:17]]}, {imm}")
        return updated_register, pc

def savar_j(line, updated_register, pc):
    imm = line[0] + line[12:20] + line[11] + line[1:11] + '0'
   
    if imm[0] == '1':
        imm = calculate_twos_complement(imm)
        imm = -int(imm,2)
    else:
        imm = int(imm,2)   
    
    
    rd = Registers[line[20:25]]
    updated_register[rd] = twos_complement(int(pc, 2) + 4, 32)
    pc = twos_complement(int(pc,2)+imm,32)
    print(f"J-type instruction: jal {rd}, {imm}")
    return updated_register, pc

def savar_s(line, updated_register):
    imm = (line[0:7] + line[20:25])
    if imm[0] == '1':
        imm = calculate_twos_complement(imm)
        imm = -int(imm,2)
    else:
        imm = int(imm,2)  
    rs2 = Registers[line[7:12]]
    rs1 = updated_register[Registers[line[12:17]]]
    # mem_address = bin(int(rs1, 2) + imm)[2:].zfill(32)
    mem_address = twos_complement(int(rs1,2)+imm,32)
    data_memory[hex(int(mem_address, 2))] = updated_register[rs2]
    print(f"S-type instruction: sw {Registers[line[7:12]]}, {imm}({Registers[line[12:17]]})")
    return updated_register


def savar_b(line, updated_register, pc):
    imm = line[0] + line[24] + line[1:7] + line[20:24] + '0'
    
    if imm[0] == '1':
        imm = calculate_twos_complement(imm)
        imm = -int(imm,2)
        
    else:
        imm = int(imm, 2)
    
    
    rs1 = updated_register[Registers[line[12:17]]]
    rs2  = updated_register[Registers[line[7:12]]]
    
    funct3 = line[17:20]
    print('B-type instruction:',funct3)
    branch_ops = {
        '000': lambda a, b: a == b,  # beq
        '001': lambda a, b: a != b,  # bne
        '100': lambda a, b: convert_binary_to_int(a)>=convert_binary_to_int(b),  # blt
        '101': lambda a, b: int(a, 2) >= int(b, 2),  # bge
        '110': lambda a, b: convert_binary_to_int(a)<convert_binary_to_int(b),  # bltu
        '111': lambda a, b: int(a, 2) < int(b, 2)  # bgeu
    }
    
    if branch_ops[funct3](rs2, rs1):
        # new_pc = bin(int(pc, 2) + imm)[2:].zfill(32)
        
        new_pc = twos_complement(int(pc,2) + imm,32)
        print(int(new_pc,2))
    else:
        new_pc = bin(int(pc, 2) + 4)[2:].zfill(32)
   
    return new_pc



file_path = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
output_path = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'

with open(file_path, 'r') as f, open(output_path, 'w') as w:
    instructions = f.readlines()
    pc = '0'*29 + '000'

    while instructions[int(pc, 2) // 4]!='00000000000000000000000001100011':
        instruction = instructions[int(pc, 2) // 4]
        
        if instruction == '00000000000000000000000001100011\n':  
            break
        
        elif instruction[25:32] == '0110011':
            updated_register = midam_r(instruction, updated_register)
            pc = bin(int(pc, 2) + 4)[2:].zfill(32)
        elif instruction[25:32] in ['0110111', '0010111']:
            updated_register = midam_u(instruction, updated_register, pc)
            pc = bin(int(pc, 2) + 4)[2:].zfill(32)
        elif instruction[25:32] in ['0000011', '0010011', '1100111']:
            updated_register, pc = savar_i(instruction, updated_register, pc)
            if instruction[25:32] != '1100111':
               pc = bin(int(pc, 2) + 4)[2:].zfill(32)
        elif instruction[25:32] == '1101111':
            updated_register, pc = savar_j(instruction, updated_register, pc)
            # pc = bin(int(pc, 2) + 4)[2:].zfill(32)
        elif instruction[25:32] == '0100011':
            updated_register = savar_s(instruction, updated_register)
            pc = bin(int(pc, 2) + 4)[2:].zfill(32)
        elif instruction[25:32] == '1100011':
            pc = savar_b(instruction, updated_register, pc)
        elif instruction[25:32] == '0110111' and instruction[0:7] == '0000000':
            break
        elif instruction[25:32] in ['0110111', '0111001', '0110111', '0111001']:
            updated_register, pc = bonus(instruction, updated_register, pc)
            pc = bin(int(pc, 2) + 4)[2:].zfill(32)
            

        updated_register['zero'] = '0'*32
        w.write('0b' + pc + ' ')
        for i in updated_register:
            w.write('0b' + updated_register[i] + ' ')
        w.write('\n')

    w.write('0b' + pc + ' ')
    for i in updated_register:
        w.write('0b' + updated_register[i] + ' ')
    w.write('\n')
    for address, value in data_memory.items():
        w.write('0x'+format(int(address, 16), '08x') + ':0b' + value + '\n')
