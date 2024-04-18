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
  "t6": "11111",
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
BONUS_Type = {
    'rst': ['0000000', '000', '0110111'],
    'halt': ['0000000', '000', '0111001'],
    'rvrs': ['0000001', '000', '0110111'],
    'mul': ['0000001', '000', '0111001']
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
        return f"Incorrect syntax at line number: {line_no}"

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
            rs1 = Registers[command[2]]
        

        if(int(command[-1].split('(')[0]) != binary(x)):
            return f"Overflow error"
        return f"{x}{rs1}{funct3}{rd}{opcode}"
    except:
        return f"Incorrect syntax at line number: {line_no}"
    
def savar_s(command,line_no):
    try:
        x=command[-1].split('(')
        
        rs1 = Registers[command[-1].split('(')[1][:-1]]
        rs2 = Registers[command[1]]
        
        y = twos_complement(int(x[0]),12)
        x=y[::-1]
        if(binary(y) != int(command[-1].split('(')[0])):
            return f"Overflow error at line number: {line_no}"
        return f"{x[5:][::-1]}{rs2}{rs1}010{x[:5][::-1]}0100011"
    except:
        return f"Incorrect syntax at line number: {line_no}"
       
def savar_b(command, line_no):
    try:
        funct3,opcode = B_Type[command[0]]
        rs1,rs2 = Registers[command[1]], Registers[command[2]]
        
        y = twos_complement(int(command[-1]),32)
        x=y[::-1]

        if(int(command[-1])!=binary(y)):
            return f"Overflow error at line number: {line_no}"

        return f"{x[12]}{x[5:11][::-1]}{rs2}{rs1}{funct3}{x[1:5][::-1]}{x[11]}{opcode}"
    except:
        return f"Syntax Error at Line number: {line_no}"


def savar_u(command, line_no):
    try:
        y = twos_complement(int(command[-1]),32)
        rd = Registers[command[1]]
        x=y[::-1]
        if(int(command[-1])!=binary(y)):
            return f"Overflow error at Line Number: {line_no}"
        if(command[0] == 'lui'):
            return f"{x[12:][::-1]}{rd}0110111"
        if(command[0] == 'auipc'):
            return f"{x[12:][::-1]}{rd}0010111"
    except:
        return f"Incorrect Syntax at Line Number: {line_no}"

def savar_j(command, line_no):
    try:
        rd = Registers[command[1]]
        y = twos_complement(int(command[-1]),21)
        x = y[::-1]

        if(int(command[-1])!=binary(y)):
            return f"Overflow error at Line number: {line_no}" 
        return f"{x[20]}{x[1:11][::-1]}{x[11]}{x[12:20][::-1]}{rd}1101111"
    
    except:
        return f"Incorrect syntax at Line number: {line_no}"
    
def midam_label_2(command, line_no, intial_label_no, intial_label):
    imm_dec  = line_no - intial_label_no


    funct3,opcode = B_Type[command[0]]
    rs1,rs2 = Registers[command[1]], Registers[command[2]]
        
    y = twos_complement(imm_dec,32)
    x=y[::-1]


    return f"{x[12]}{x[5:11][::-1]}{rs2}{rs1}{funct3}{x[1:5][::-1]}{x[11]}{opcode}"



def bonus(command, line_no):
    try:
        funct3, funct7, opcode = BONUS_Type[command[0]]
        if command[0] == 'rst':
            return f"{funct7}00000{opcode}"
        elif command[0] == 'halt':
            return f"{'0'*7}{'0'*5}{'0'*3}{'0'*5}{opcode}"
        elif command[0] == 'rvrs':
            rd, rs = Registers[command[1]], Registers[command[2]]
            return f"{funct7}{rs}000{funct3}{rd}{opcode}"
        elif command[0] == 'mul':
            rd, rs1, rs2 = Registers[command[1]], Registers[command[2]], Registers[command[3]]
            return f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}"
        else:
            return f"incorrect syntax at line {line_no}"
    except KeyError:
        return f"incorrect syntax at line {line_no}"

file_path = sys.argv[1]
output_path = sys.argv[2]


with open(file_path, 'r') as file:
    line_no = 0
    x = file.readlines()
    file.seek(0)
    present = False
    label = {}
    for line in file:
        
        parts = line.split()
        if(parts[0][-1] == ":"):
            label[parts[0][:-1:]] =  line_no
        line_no = line_no +1



with open(file_path, 'r') as file, open(output_path,'w') as output:
    line_no = 0
    x = file.readlines()
    file.seek(0)
    present = False
    for line in file:
        line_no = line_no +1
        
        parts = line.split()

        if(parts[0][-1]==":"):
            command = [parts[1]] + parts[2].replace(',', ' ').split(' ') 
            

        else:    
            command = [parts[0]] + parts[1].replace(',', ' ').split(' ') 
        if(command[-1] in label):
            
            if(command[0] in B_Type):
                # print(command)
                # funct3,opcode = B_Type[command[0]]
                # rs1,rs2 = Registers[command[1]], Registers[command[2]]
            
                # y = twos_complement(int(line_no - label[command[-1]]),32)
                # x=y[::-1]


                # output.write( f"{x[12]}{x[5:11][::-1]}{rs2}{rs1}{funct3}{x[1:5][::-1]}{x[11]}{opcode}\n")
                command[-1] = str((label[command[-1]] - line_no+1)*4)
                output.write(savar_b(command, line_no)+"\n")

            else:
                command[-1] =str((label[command[-1]] - line_no+1)*4)

                output.write(savar_j(command, line_no) + '\n')
                
            continue   
        if(command == ['beq','zero','zero','0']):
            present = True
            output.write(savar_b(command, line_no) + '\n')
            break
        if(command[0] in R_type):
            output.write(midam_r(command,line_no) + '\n')
        elif(command[0] in I_Type):
            output.write(savar_i(command,line_no) + '\n')
        elif(command[0] == 'sw'):
            output.write(savar_s(command,line_no) + '\n')
        elif(command[0] == 'lui' or command[0] == 'auipc'):
            output.write(savar_u(command, line_no) + '\n')
        elif(command[0] in B_Type):
            output.write(savar_b(command, line_no) + '\n')

        elif(command[0] == 'jal'):
            output.write(savar_j(command, line_no) + '\n')
        elif(command[0] in ['mul','rvrs','halt','rst']):
            output.write(bonus(command,line_no) + '\n')
        else:
            output.write("Invalid input at line " + str(line) + '\n')
        if(line_no == len(x)):
            if(command != ['beq','zero','zero','0']):
                output.write("Virtual halt not present as last command" + '\n')
                present=True
                break
    if(present == False):
        output.write("Virtual halt not present")
