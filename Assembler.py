#The above part, stores a single line of the input text file in a list, nammed command, every following program will run from the inputs in command.
# Registers = {'rs' + str(i): format(i, '05b') for i in range(16)}    #Binary code for every register rs0-rs15, where rs0 = 0000 and rs15 = 1111  
import sys
Registers = {
  "zero": "00000",
  "ra": "00001",
  "sp": "00010",
  "gp": "00011",
  "tp": "00100",
  "t0": "00101",
  "t1": "00110",
  "t2": "00111",
  "s0": "01000",
  "fp": "01000",
  "s1": "01001",
  "a0": "01010",
  "a1": "01011",
  "a2": "01100",
  "a3": "01101",
  "a4": "01110",
  "a5": "01111",
  "a6": "10000",
  "a7": "10001",
  "s2": "10010",
  "s3": "10011",
  "s4": "10100",
  "s5": "10101",
  "s6": "10110",
  "s7": "10111",
  "s8": "11000",
  "s9": "11001",
  "s10": "11010",
  "s11": "11011",
  "t3": "11100",
  "t4": "11101",
  "t5": "11110",
  "t6": "11111"
}


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
    'lw':['010','0000011'],
    'addi':['000','0010011'],
    'sltiu':['011','0010011'],
    'jalr':['000','1100111']
}

B_Type = {
    'beq':['000','1100011'],
    'bne':['001','1100011'],
    'blt':['100','1100011'],
    'bge':['101','1100011'],
    'bltu':['110','1100011'],
    'bgeu':['111','1100011']
}


def twos_complement(number, bit_length):
    if number >= 0:
        # If number is positive, convert it directly to binary and zero-pad to the desired length
        binary = bin(number)[2:].zfill(bit_length)
        return binary
    binary = bin(abs(number))[2:]  
    binary = binary.zfill(bit_length)
    inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary)
    inverted_binary = bin(int(inverted_binary, 2) + 1)[2:] 
    return inverted_binary.zfill(bit_length)




def binary(binary):
    if binary[0] == '0':
        return int(binary, 2)
    else:
        inverted_binary = ''.join('1' if bit == '0' else '0' for bit in binary)
        decimal = -int(inverted_binary, 2) - 1
        return decimal

def midam_r(command, line_no):
    try:
        funct7,funct3,opcode = R_type[command[0]]
        
        rd, rs1, rs2 = Registers[command[1]], Registers[command[2]], Registers[command[3]]
        
        return f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}"
    except:
        return "Incorrect syntax"

def savar_i(command, line_no):
    try:
        funct3,opcode = I_Type[command[0]]
        rd = Registers[command[1]]
    
        
        
        # convert imm to binary

        if(command[0] == 'lw'):
            x=command[-1].split('(')
            rs1 = Registers[command[-1].split('(')[1][:-1]]
            x = twos_complement(int(x[0]),12)
        
        if(command[0] == 'addi' or command[0] == 'sltiu'):
            x = twos_complement(int(command[-1]),12)
            rs1 = Registers[command[2]]

        if(command[0] == 'jalr'):
            x = twos_complement(int(command[-1]),12)
            rs1 = '0110'
        

        if(int(command[-1].split('(')[0]) != binary(x)):
            return f"Overflow error"
        return f"{x}{rs1}{funct3}{rd}{opcode}"
    except:
        return "Incorrect syntax"
    
def savar_s(command,line_no):
    try:
        x=command[-1].split('(')
        
        rs1 = Registers[command[-1].split('(')[1][:-1]]
        rs2 = Registers[command[1]]
        
        y = twos_complement(int(x[0]),12)
        x=y[::-1]
        if(binary(y) != int(command[-1].split('(')[0])):
            return "Overflow error"
        return f"{x[5:][::-1]}{rs2}{rs1}010{x[:5][::-1]}0100011"
    except:
        return "Incorrect syntax"
       
def savar_b(command):
    try:
        funct3,opcode = B_Type[command[0]]
        rs1,rs2 = Registers[command[1]], Registers[command[2]]
        
        y = twos_complement(int(command[-1]),32)
        x=y[::-1]

        if(int(command[-1])!=binary(y)):
            return f"Overflow error"

        return f"{x[12]}{x[5:11][::-1]}{rs2}{rs1}{funct3}{x[1:5][::-1]}{x[11]}{opcode}"
    except:
        return "Error" + command[0]


def savar_u(command):
    try:
        y = twos_complement(int(command[-1]),32)
        rd = Registers[command[1]]
        x=y[::-1]
        if(int(command[-1])!=binary(y)):
            return "Overflow error"
        if(command[0] == 'lui'):
            return f"{x[12:][::-1]}{rd}0110111"
        if(command[0] == 'auipc'):
            return f"{x[12:][::-1]}{rd}0010111"
    except:
        return "Incorrect Syntax"

def savar_j(command):
    try:
        rd = Registers[command[1]]
        y = twos_complement(int(command[-1]),21)
        x = y[::-1]
        if(int(command[-1])!=binary(y)):
            return "Overflow error" 
        return f"{x[20]}{x[1:11][::-1]}{x[11]}{x[12:20][::-1]}{rd}1101111"
    except:
        return "Incorrect syntax"
    
def midam_label_2(command, line_no, intial_label_no, intial_label):
    imm_dec  = line_no - intial_label_no


    funct3,opcode = B_Type[command[0]]
    rs1,rs2 = Registers[command[1]], Registers[command[2]]
        
    y = twos_complement(imm_dec,32)
    x=y[::-1]


    return f"{x[12]}{x[5:11][::-1]}{rs2}{rs1}{funct3}{x[1:5][::-1]}{x[11]}{opcode}"

file_path = sys.argv[1]
output_path = sys.argv[2]

with open(file_path, 'r') as file:
    line_no = 0
    x = file.readlines()
    file.seek(0)
    present = False
    label = {"d;asfh": "dalsjk"}
    for line in file:
        line_no = line_no +1
        parts = line.split()
        if(parts[0][-1] == ":"):
            label = {parts[0][:-1:] : line_no}


with open(file_path, 'r') as file, open(output_path,'w') as output:
    line_no = 0
    x = file.readlines()
    file.seek(0)
    present = False
    intial_label = "zxcjHkgafsd"
    intial_label_no = 10000000000
    for line in file:
        line_no = line_no +1
        
        parts = line.split()

        if(parts[0][-1]==":"):
            command = [parts[1]] + parts[2].replace(',', ' ').split(' ') 
            intial_label_no = line_no
            intial_label = parts[0][:-1]
        else:    
            command = [parts[0]] + parts[1].replace(',', ' ').split(' ') 


        if(command[-1] == intial_label): 
            output.write(midam_label_2(command, line_no, intial_label_no, intial_label) + '\n')
            continue
        
        elif(command[-1] in label):
            a = [command[0], command[1], command[2], str(line_no - label[command[-1]])]
            funct3,opcode = B_Type[command[0]]
            rs1,rs2 = Registers[command[1]], Registers[command[2]]
        
            y = twos_complement(int(line_no - label[command[-1]]),32)
            x=y[::-1]


            output.write( f"{x[12]}{x[5:11][::-1]}{rs2}{rs1}{funct3}{x[1:5][::-1]}{x[11]}{opcode} \n")
            continue

                
        if(command == ['beq','zero','zero','0']):
            present = True
            output.write(savar_b(command) + '\n')
            break
        if(command[0] in R_type):
            output.write(midam_r(command,line_no) + '\n')
        elif(command[0] in I_Type):
            output.write(savar_i(command,line_no) + '\n')
        elif(command[0] == 'sw'):
            output.write(savar_s(command,line_no) + '\n')
        elif(command[0] == 'lui' or command[0] == 'auipc'):
            output.write(savar_u(command) + '\n')
        elif(command[0] in B_Type):
            output.write(savar_b(command) + '\n')

        elif(command[0] == 'jal'):
            output.write(savar_j(command) + '\n')
        else:
            output.write("Invalid input at line " + str(line) + '\n')
        if(line_no == len(x)):
            if(command != ['beq','zero','zero','0']):
                output.write("Virtual halt not present as last command" + '\n')
                present=True
                break
    if(present == False):
        output.write("Virtual halt not present")
        
