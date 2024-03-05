Midam  = ["xor", "and", "or", "sll", "srl", "and", "sub", "stlu", "stl"]

with open('input.txt', 'r') as file:
    line_no = 0
    # Read each line from the file
    for line in file:
        line_no = line_no +1
        # Remove commas from the line and store it in the "command" list
        command = list(line.strip().replace(',', ''))
        if(command[0] in Midam):
            print(midam_r)
            continue


#The above part, stores a single line of the input text file in a list, nammed command, every following program will run from the inputs in command.


Registers = {'rs' + str(i): format(i, '04b') for i in range(16)}    #Binary code for every register rs0-rs15, where rs0 = 0000 and rs15 = 1111  


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



#Midam Wala Part Starts:
def midam_r(command, line_no):
    #Error handling Start
    if(command[0]!= "xor" or command[0]!= "sll" or command[0]!= "srl" or command[0]!= "or" or command[0]!= "and" or command[0]!= "add" or command[0]!= "sub" or command[0]!= "slt" or command[0]!= "stlu"):
        return (f"Wrong Function Call: Function Called - Midam_R at line {line_no}")
    
    if(len(command)!=4 or ((len(command[1])!=3) or (len(command[2])!=3) or (len(command[3])!=3))):
        return (f"Invalid input at line {line_no}")
    #Error Handling End. Now Assembly -> Binary starts

    if(command[0]==add):
        return(f"{R_type["add"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["add"][1]} {Registers[str(command[1])]} {R_type["add"][-1]} ")

    if(command[0]==slt):
        return(f"{R_type["slt"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["slt"][1]} {Registers[str(command[1])]} {R_type["slt"][-1]} ")
    
    if(command[0]==sltu):
        return(f"{R_type["sltu"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["sltu"][1]} {Registers[str(command[1])]} {R_type["sltu"][-1]} ")

    if(command[0]==xor):
        return(f"{R_type["xor"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["xor"][1]} {Registers[str(command[1])]} {R_type["xor"][-1]} ")

    if(command[0]==sll):
        return(f"{R_type["sll"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["sll"][1]} {Registers[str(command[1])]} {R_type["sll"][-1]} ")

    if(command[0]==srl):
        return(f"{R_type["srl"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["srl"][1]} {Registers[str(command[1])]} {R_type["srl"][-1]} ")

    if(command[0]==or):
        return(f"{R_type["or"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["or"][1]} {Registers[str(command[1])]} {R_type["or"][-1]} ")

    if(command[0]==and):
        return(f"{R_type["and"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["and"][1]} {Registers[str(command[1])]} {R_type["and"][-1]} ")

    if(command[0] = "sub"):
        if(len(command[2]) == 3):
            return(f"{R_type["sub"][0]} {Registers[str(command[-1])]} {Registers[str(command[-2])]} {R_type["sub"][1]} {Registers[str(command[1])]} {R_type["sub"][-1]} ")
        a = int(str(command[2][1::]))
        return(f"{R_type["sub"][0]} {Registers[str(command[-1])]} {format(a, '04b')} {R_type["sub"][1]} {Registers[str(command[1])]} {R_type["sub"][-1]} ")