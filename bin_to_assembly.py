# There might be some bugs. If NOP show up, it is probably due to bug.
# Copy and paste machine code below. Lab2 fibo machine code is hard coded.
bin = """
0000000_00000_00000_000_00000_0000000
0000000_00010_00001_000_10000_0110011
0100000_01000_00100_000_10001_0110011
0000000_00101_00011_100_10010_0110011
0000000_00101_00011_110_10011_0110011
0000000_00011_00101_111_10100_0110011
0100000_00110_00001_000_10101_0110011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_0010011
0000000_00000_00000_000_00000_1101111
"""

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