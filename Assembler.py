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

#Midam Wala Part Starts:
# def midam_r(command, line_no):
#     #Error handling Start
#     if(command[0]!= "xor" or command[0]!= "sll" or command[0]!= "srl" or command[0]!= "or" or command[0]!= "and" or command[0]!= "add" or command[0]!= "sub" or command[0]!= "slt" or command[0]!= "stlu"):
#         return (f"Wrong Function Call: Function Called - Midam_R at line {line_no}")
    
#     if(len(command)!=4 or ((len(command[1])!=3) or (len(command[2])!=3) or (len(command[3])!=3))):
#         return (f"Invalid input at line {line_no}")
#     #Error Handling End. Now Assembly -> Binary starts

#     if(command[0]=='add'):
#         return(f"{R_type["add"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["add"][1]} {Registers[str(command[1])]} {R_type["add"][-1]} ")

#     if(command[0]=='slt'):
#         return(f"{R_type["slt"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["slt"][1]} {Registers[str(command[1])]} {R_type["slt"][-1]} ")
    
#     if(command[0]=='sltu'):
#         return(f"{R_type["sltu"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["sltu"][1]} {Registers[str(command[1])]} {R_type["sltu"][-1]} ")

#     if(command[0]=='xor'):
#         return(f"{R_type["xor"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["xor"][1]} {Registers[str(command[1])]} {R_type["xor"][-1]} ")

#     if(command[0]=='sll'):
#         return(f"{R_type["sll"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["sll"][1]} {Registers[str(command[1])]} {R_type["sll"][-1]} ")

#     if(command[0]=='srl'):
#         return(f"{R_type["srl"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["srl"][1]} {Registers[str(command[1])]} {R_type["srl"][-1]} ")

#     if(command[0]=='or'):
#         return(f"{R_type["or"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["or"][1]} {Registers[str(command[1])]} {R_type["or"][-1]} ")

#     if(command[0]=='and'):
#         return(f"{R_type["and"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["and"][1]} {Registers[str(command[1])]} {R_type["and"][-1]} ")

#     if(command[0] == "sub"):
#         if(len(command[2]) == 3):
#             return(f"{R_type["sub"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["sub"][1]} {Registers[str(command[1])]} {R_type["sub"][-1]} ")
#         a = int(str(command[2][1::]))
#         return(f"{R_type["sub"][0]} {Registers[str(command[-1])]} {format(a, '04b')} {R_type["sub"][1]} {Registers[str(command[1])]} {R_type["sub"][-1]} ")

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




# def binary(num):
#     fin = 0
#     for i in range(len(str(num))-1,0,-1):
    
#         fin+=int(num[i])*(2**i)
#     return fin
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
        return  f"Incorrect syntax at {line_no}"

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
            return f"Overflow error at {line_no}"
        return f"{x}{rs1}{funct3}{rd}{opcode}"
    except:
        return f"Incorrect syntax at {line_no}"
    
def savar_s(command,line_no):
    try:
        x=command[-1].split('(')
        
        rs1 = Registers[command[-1].split('(')[1][:-1]]
        rs2 = Registers[command[1]]
        
        y = twos_complement(int(x[0]),12)
        x=y[::-1]
        if(binary(y) != int(command[-1].split('(')[0])):
            return f"Overflow error at {line_no}"
        return f"{x[5:][::-1]}{rs2}{rs1}010{x[:5][::-1]}0100011"
    except:
        return f"Incorrect syntax {line_no}"
       
def savar_b(command,line_no):
    try:
        funct3,opcode = B_Type[command[0]]
        rs1,rs2 = Registers[command[1]], Registers[command[2]]
        
        
        
        y = twos_complement(int(command[-1]),32)
        x=y[::-1]

        if(int(command[-1])!=binary(y)):
            return f"Overflow error at {line_no}"

        return f"{x[12]}{x[5:11][::-1]}{rs2}{rs1}{funct3}{x[1:5][::-1]}{x[11]}{opcode}"
    except:
        return f"Incorrect syntax at {line_no}"

def savar_u(command,line_no):
    try:
        y = twos_complement(int(command[-1]),32)
        rd = Registers[command[1]]
        x=y[::-1]
        if(int(command[-1])!=binary(y)):
            return f"Overflow error at {line_no}"
        if(command[0] == 'lui'):
            return f"{x[12:][::-1]}{rd}0110111"
        if(command[0] == 'auipc'):
            return f"{x[12:][::-1]}{rd}0010111"
    except:
        return f"Incorrect Syntax at {line_no}"

def savar_j(command,line_no):
    try:
        rd = Registers[command[1]]
        y = twos_complement(int(command[-1]),21)
        x = y[::-1]
        if(int(command[-1])!=binary(y)):
            return f"Overflow error at {line_no}" 
        return f"{x[20]}{x[1:11][::-1]}{x[11]}{x[12:20][::-1]}{rd}1101111"
    except:
        return f"Incorrect syntax at {line_no}"




file_path = sys.argv[1]
output_path = sys.argv[2]



with open(file_path, 'r') as file, open(output_path,'w') as output:
    line_no = 0
    x = file.readlines()
    file.seek(0)
    present = False
    for line in file:
        if(line == ''):
            continue
        line_no = line_no+1
        
        parts = line.split()
        command = [parts[0]] + parts[1].replace(',', ' ').split(' ') 
        
            
        if(command == ['beq','zero','zero','0']):
            present = True
            output.write(savar_b(command,line_no) + '\n')
            break
        if(command[0] in R_type):
            output.write(midam_r(command,line_no) + '\n')
        elif(command[0] in I_Type):
            output.write(savar_i(command,line_no) + '\n')
        elif(command[0] == 'sw'):
            output.write(savar_s(command,line_no) + '\n')
        elif(command[0] == 'lui' or command[0] == 'auipc'):
            output.write(savar_u(command,line_no) + '\n')
        elif(command[0] in B_Type):
            output.write(savar_b(command, line_no) + '\n')
        elif(command[0] == 'jal'):
            output.write(savar_j(command, line_no) + '\n')
        else:
            output.write("Invalid input at line " + str(line) + '\n')
        if(line_no == len(x)):
            if(command != ['beq','zero','zero','0']):
                output.write("Virtual halt not present as last command" + '\n')
                present=True
                break
    if(present == False):
        output.write("Virtual halt not present")
        
