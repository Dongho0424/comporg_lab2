# There might be some bugs. If NOP show up, it is probably due to bug.
# Copy and paste machine code below. Lab2 fibo machine code is hard coded.
bin = """00000000000000000000000000000000
00001000010000000000000001101111
11111110000000010000000100010011
00000000000100010010111000100011
00000000100000010010110000100011
00000000100100010010101000100011
00000010000000010000010000010011
11111110101001000010011000100011
11111110110001000010011110000011
00000000000001111001011001100011
00000000000000000000011110010011
00000100010000000000000001101111
11111110110001000010011100000011
00000000000100000000011110010011
00000000111101110001011001100011
00000000000100000000011110010011
00000011000000000000000001101111
11111110110001000010011110000011
11111111111101111000011110010011
00000000000001111000010100010011
11111011100111111111000011101111
00000000000001010000010010010011
11111110110001000010011110000011
11111111111001111000011110010011
00000000000001111000010100010011
11111010010111111111000011101111
00000000000001010000011110010011
00000000111101001000011110110011
00000000000001111000010100010011
00000001110000010010000010000011
00000001100000010010010000000011
00000001010000010010010010000011
00000010000000010000000100010011
00000000000000001000000001100111
11111110000000010000000100010011
00000000000100010010111000100011
00000000100000010010110000100011
00000010000000010000010000010011
00000000001100000000011110010011
11111110111101000010011000100011
11111110110001000010010100000011
11110110010111111111000011101111
11111110101001000010010000100011
00000001110000010010000010000011
00000001100000010010010000000011
00000010000000010000000100010011
00000000000000000000000001101111"""

bin_stripped = bin.replace('_','')
binLine = bin_stripped.splitlines()

def decompile(line):
    opcode = line[25:32]
    funct3 = line[17:20]
    funct7 = line[0:7]
    assembly = []

    if opcode == "0110011":     # R-type
        rd = 'x'+str(int(line[20:25],2))
        rs1 = 'x'+str(int(line[12:17],2))
        rs2 = 'x'+str(int(line[7:12],2))

        if funct3 == "000":
            if funct7 == "0000000":
               inst = "ADD"
            elif funct7 == "0100000":
                inst = "SUB"
            else:
                inst= "NOP"
        elif funct3 == "100":
            inst = "XOR"
        elif funct3 == "110":
            inst = "OR"
        elif funct3 == "111":
            inst = "AND"
        elif funct3 == "101":
            if funct7 == "0000000":
                inst = "SRL"
            elif funct7 == "0100000":
                inst = "SRA"
            else:
                inst = "NOP"
        elif funct3 == "010":
            inst = "SLT"
        elif funct3 == "011":
            inst = "SLTU"
        else:
            inst = "NOP"
        assembly = [inst, rd, rs1, rs2]

    elif opcode == "0010011":   # I-type
        rd = 'x'+str(int(line[20:25],2))
        rs1 = 'x'+str(int(line[12:17],2))
        imm = str(int(line[0:12],2) if int(line[0:12],2) < 2048 else int(line[0:12],2)-4096)

        if funct3 == "000":
            inst = "ADDI"
        elif funct3 == "100":
            inst = "XORI"
        elif funct3 == "110":
            inst = "ORI"
        elif funct3 == "111":
            inst = "ANDI"
        elif funct3 == "001":
            inst = "SLLI"
        elif funct3 == "101":
            if funct7 == "0000000":
                inst = "SRLI"
            elif funct7 == "0100000":
                inst = "SRAI"
            else:
                inst = "NOP"
        elif funct3 == "010":
            inst = "SLTI"
        elif funct3 == "011":
            inst = "SLTIU"
        else:
            inst = "NOP"
        assembly = [inst, rd, rs1, imm]
    
    elif opcode == "0000011":   # Load
        rd = 'x'+str(int(line[20:25],2))
        rs1 = 'x'+str(int(line[12:17],2))
        imm = str(int(line[0:12],2) if int(line[0:12],2) < 2048 else int(line[0:12],2)-4096)

        if funct3 == "000":
            inst = "LB"
        elif funct3 == "001":
            inst = "LH"
        elif funct3 == "010":
            inst = "LW"
        elif funct3 == "100":
            inst = "LBU"
        elif funct3 == "101":
            inst = "LHU"
        else:
            inst = "NOP"
        assembly = [inst, rd, imm+'('+rs1+')']
    
    elif opcode == "0100011":   # Store
        rs1 = 'x'+str(int(line[12:17],2))
        rs2 = 'x'+str(int(line[7:12],2))
        imm = str(int(line[0:7]+line[20:25],2) if int(line[0:7]+line[20:25],2) < 2048 else int(line[0:7]+line[20:25],2)-4096)
        
        if funct3 == "000":
            inst = "SB"
        elif funct3 == "001":
            inst = "SH"
        elif funct3 == "010":
            inst = "SW"
        else:
            inst = "NOP"
        assembly = [inst, rs2, imm+'('+rs1+')']
    
    elif opcode == "1100011":   # Branch
        rs1 = 'x'+str(int(line[12:17],2))
        rs2 = 'x'+str(int(line[7:12],2))
        imm = str(int(line[0]+line[24]+line[1:7]+line[20:24]+'0',2) if int(line[0]+line[24]+line[1:7]+line[20:24]+'0',2) < 4096 else int(line[0]+line[24]+line[1:7]+line[20:24]+'0',2)-8192)

        if funct3 == "000":
            inst = "BEQ"
        elif funct3 == "001":
            inst = "BNE"
        elif funct3 == "100":
            inst = "BLT"
        elif funct3 == "101":
            inst = "BGE"
        elif funct3 == "110":
            inst = "BLTU"
        elif funct3 == "111":
            inst = "BGEU"
        else:
            inst = "NOP"
        assembly = [inst, rs1, rs2, imm]
    
    elif opcode == "1101111":   # Jump and Link
        inst = "JAL"
        rd = 'x'+str(int(line[20:25],2))
        imm = str(int(line[0]+line[12:20]+line[11]+line[1:11]+'0',2) if int(line[0]+line[12:20]+line[11]+line[1:11]+'0',2) < 1048576 else int(line[0]+line[12:20]+line[11]+line[1:11]+'0',2)-2097152)
        assembly = [inst, rd, imm]
    elif opcode == "1100111":   # Jump and Link Reg
        rd = 'x'+str(int(line[20:25],2))
        rs1 = 'x'+str(int(line[12:17],2))
        imm = str(int(line[0:12],2) if int(line[0:12],2) < 2048 else int(line[0:12],2)-4096)
        
        if funct3 == "000":
            inst = "JALR"
        else:
            inst = "NOP"
        assembly = [inst, rd, rs1, imm]
    else:
        assembly = ["NOP"]

    return assembly

i=0
for line in binLine:
    print(str(i), end='\t')
    for element in decompile(line):
        print(element, end='\t')
    print()
    i += 4