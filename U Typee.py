register = {'x0': '00000', 'x1': '00001', 'x2': '00010', 'x3': '00011', 'x4': '00100','x5': '00101', 'x6': '00110', 'x7': '00111', 'x8': '01000', 'x9': '01001', 
'x10': '01010', 'x11': '01011', 'x12': '01100', 'x13': '01101', 'x14': '01110','x15': '01111', 'x16': '10000', 'x17': '10001', 'x18': '10010', 'x19': '10011', 
'x20': '10100', 'x21': '10101', 'x22': '10110', 'x23': '10111', 'x24': '11000','x25': '11001', 'x26': '11010', 'x27': '11011', 'x28': '11100', 'x29': '11101', 
'x30': '11110', 'x31': '11111', 'zero': '00000', 'ra': '00001', 'sp': '00010', 'gp': '00011', 'tp': '00100','t0': '00101', 't1': '00110', 't2': '00111', 's0': '01000', 's1': '01001',
'a0': '01010', 'a1': '01011', 'a2': '01100', 'a3': '01101', 'a4': '01110','a5': '01111', 'a6': '10000', 'a7': '10001', 's2': '10010', 's3': '10011',
's4': '10100', 's5': '10101', 's6': '10110', 's7': '10111', 's8': '11000','s9': '11001', 's10': '11010', 's11': '11011', 't3': '11100', 't4': '11101', 't5': '11110', 't6': '11111'}

opcode = {"auipc":"0010111","lui":"0110111"}

def imm_bin(imm_value, num_bits):
    binary_str = f"{imm_value:0{num_bits}b}"
    return binary_str

instruction_str = "auipc s2,30"
instruction_list = instruction_str.split()

if ',' in instruction_list[-1]:
    register, immediate = instruction_list[-1].split(',')
    instruction_list[-1] = register
    instruction_list.append(immediate)

print("Instruction List:", instruction_list)
print(f'{imm_bin(int(instruction_list[2]),20)}{register[instruction_list[1]]}{opcode[instruction_list[0]]}')