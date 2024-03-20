import sys
Registers = {
  "zero": "00000",
  "ra":   "00001",
  "sp":   "00010",
  "gp":   "00011",
  "tp":   "00100",
  "t0":   "00101",
  "t1":   "00110",
  "t2":   "00111",
  "s0":   "01000",
  "fp":   "01000",
  "s1":   "01001",
  "a0":   "01010",
  "a1":   "01011",
  "a2":   "01100",
  "a3":   "01101",
  "a4":   "01110",
  "a5":   "01111",
  "a6":   "10000",
  "a7":   "10001",
  "s2":   "10010",
  "s3":   "10011",
  "s4":   "10100",
  "s5":   "10101",
  "s6":   "10110",
  "s7":   "10111",
  "s8":   "11000",
  "s9":   "11001",
  "s10":  "11010",
  "s11":  "11011",
  "t3":   "11100",
  "t4":   "11101",
  "t5":   "11110",
  "t6":   "11111",
}

updated_register = {i: 0 for i in Registers.keys()}


#R-Type Instructions Below. Format = instruction -> Func7 -> Func3 -> Opcode
R_type = {
    'add':  ['0000000', '000', '0110011'],
    'sub':  ['0100000', '000', '0110011'],
    'sll':  ['0000000', '001', '0110011'],
    'slt':  ['0000000', '010', '0110011'],
    'sltu': ['0000000', '011', '0110011'],
    'xor':  ['0000000', '100', '0110011'],
    'srl':  ['0000000', '101', '0110011'],
    'or':   ['0000000', '110', '0110011'],
    'and':  ['0000000', '111', '0110011']
}

I_Type = {
    'lw':   ['010','0000011'],
    'addi': ['000','0010011'],
    'sltiu':['011','0010011'],
    'jalr': ['000','1100111']
}

B_Type = {
    'beq': ['000','1100011'],
    'bne': ['001','1100011'],
    'blt': ['100','1100011'],
    'bge': ['101','1100011'],
    'bltu':['110','1100011'],
    'bgeu':['111','1100011']
}


def get_keys_from_multi_valued_key(dictionary, multi_valued_key):
    keys = []
    for key, values in dictionary.items():
        if multi_valued_key in values:
            keys.append(key)
    return keys

def twos_complement(number, bit_length):
    if number >= 0:
        binary = bin(number)[2:].zfill(bit_length)
        return binary
    binary = bin(abs(number))[2:]  
    binary = binary.zfill(bit_length)
    inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary)
    inverted_binary = bin(int(inverted_binary, 2) + 1)[2:] 
    return inverted_binary.zfill(bit_length)


def midam_r(line, updated_register):
    R_type_keys = get_keys_from_multi_valued_key(R_type, line[27:])
    if R_type_keys:
        a = get_keys_from_multi_valued_key(Registers, line[21:26])
        rs2 = get_keys_from_multi_valued_key(Registers, line[6:12])
        rs1 = get_keys_from_multi_valued_key(Registers, line[12:18])
        b = twos_complement(updated_register[rs1], 32)
        c = twos_complement(updated_register[rs1], 32)
        operations = {
            'add': lambda b, c: int(b) + int(c),
            'slt': lambda b, c: 1 if int(b) < int(c) else 0,
            'sltu': lambda b, c: 1 if int(b, 2) < int(c, 2) else 0,
            'xor': lambda b, c: int(b) ^ int(c),
            'or': lambda b, c: int(b, 2) | int(c, 2),
            'and': lambda b, c: int(b, 2) & int(c, 2),
            'sub': lambda b, c: twos_complement(int(b)) - twos_complement(int(c)),
            'sll': lambda b, c: 0 if int(c[1:], 2) >= 32 else int(b[int(c[1:]):] + '0' * int(c[1:], 2)) #My version
            # 'sll': lambda b, c: int(b) << int(c[1:]) if int(c[1:]) < 32 else 0 #ChatGPtVersion
        }
        if a in operations:
            updated_register[a] = operations[a](b, c)
        else:
            updated_register[a] = 0 if int(c[1:], 2) >= 32 else int('0' * int(c[1:], 2) + str(b[int(c[1:]):]))
    return updated_register

def midam_u(line, updated_register, pc):
    rd = get_keys_from_multi_valued_key(Registers, line[20:25])
    imm = int(line[:20:], 2)    
    if imm>32:
        updated_register[rd] = 0
    else:
        updated_register[rd] = int((line[:20:] + '0'*12)[:32:], 2)
    if line[27::] == "0010111":
        #Assuming pc is given in binary
        updated_register[rd] = updated_register[rd] + int(pc, 2)
    return updated_register  

def nihal_b(line, updated_register, pc, label_addresses):
    opcode = line[25:32]
    rs1 = get_keys_from_multi_valued_key(Registers, line[12:17])
    rs2 = get_keys_from_multi_valued_key(Registers, line[7:12])
    imm = twos_complement(int(line[:7] + line[20:25] + line[7:12] + line[25:], 2), 32)
    b_type_instructions = {
        'beq': lambda a, b: updated_register[a] == updated_register[b],
        'bne': lambda a, b: updated_register[a] != updated_register[b],
        'blt': lambda a, b: updated_register[a] < updated_register[b],
        'bge': lambda a, b: updated_register[a] >= updated_register[b],
        'bltu': lambda a, b: int(updated_register[a], 2) < int(updated_register[b], 2),
        'bgeu': lambda a, b: int(updated_register[a], 2) >= int(updated_register[b], 2)
    }

    if opcode in b_type_instructions:
        if b_type_instructions[opcode](rs1, rs2):
            # Calculate the target address using the label's address
            target_address = label_addresses[line[32:]] if line[32:] in label_addresses else 0
            updated_pc = pc + imm - target_address
            return updated_pc, True
    return pc, 


def simulate_nihal_b(instructions):
    label_addresses = {}
    pc = 0
    while pc < len(instructions):
        line = instructions[pc]
        if ':' in line:
            # Label found, record its address
            label = line.split(':')[0]
            label_addresses[label] = pc
            line = line.split(':')[1].strip()
        # Check for B-Type instructions
        if line[25:32] in B_Type:
            pc, branch_taken = nihal_b(line, updated_register, pc, label_addresses)
            if branch_taken:
                continue
        pc += 1 
        
