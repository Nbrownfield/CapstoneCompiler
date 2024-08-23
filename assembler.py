import sys
import re
from cocotb.types import LogicArray, Range

branches = {}
labels = {}

#goes through .s file to check for branch labels
def checklabels(file):
    linenum = 0
    with open(file) as f:
        for line in f:
            line = line.replace('\n', '').replace('\r', '').replace('\t', '')
            nug = re.split(r'[, ]',line)
            
            #ignore comments
            if line[0]=='@':
                continue
            
            #store address of branch instructions
            if (nug[0].lower() == "b") or (nug[0].lower() == "bl") or (nug[0].lower() == "beq") or (nug[0].lower() == "bge"):
                branches[nug[1]] = linenum
            
            #store address of instructions with branch label
            if line[0]=='.':
                labels[line[1:]] = linenum
            
            #increment memory address for each instruction 
            else:
                linenum = linenum + 1

#checks first word of command for conditions (ADD vs ADDEQ, SUB vs SUBS, etc)
def checkCond(word):

    #branch command
    if word[0].lower() == 'b':

        #all branch commands s=0
        sField = 0

        #if only 1 letter (b), then unconditional branch
        if len(word) == 1:
            cond = LogicArray("1110")
        
        #if 3 letters (beq), check condition
        elif len(word) == 3:
            if word[1:3].lower() == "eq": #equal
                cond = LogicArray("0000")
            elif word[1:3].lower() == "ne": #not equal
                cond = LogicArray("0001")
            elif word[1:3].lower() == "cs": #carry set
                cond = LogicArray("0010")
            elif word[1:3].lower() == "hs": #unsigned higher or same (carry set)
                cond = LogicArray("0010")
            elif word[1:3].lower() == "cc": #carry clear
                cond = LogicArray("0011")
            elif word[1:3].lower() == "lo": #unsigned lower (carry clear)
                cond = LogicArray("0011")
            elif word[1:3].lower() == "mi": #minus / negative
                cond = LogicArray("0100")
            elif word[1:3].lower() == "pl": #plus / positive or zero
                cond = LogicArray("0101")
            elif word[1:3].lower() == "vs": #overflow
                cond = LogicArray("0110")
            elif word[1:3].lower() == "vc": #no overflow
                cond = LogicArray("0111")
            elif word[1:3].lower() == "hi": #unsigned higher
                cond = LogicArray("1000")
            elif word[1:3].lower() == "ls": #unsigned lower or same
                cond = LogicArray("1001")
            elif word[1:3].lower() == "ge": #signed greater than or equal
                cond = LogicArray("1010")
            elif word[1:3].lower() == "lt": #signed less than
                cond = LogicArray("1011")
            elif word[1:3].lower() == "gt": #signed greater than
                cond = LogicArray("1100")
            elif word[1:3].lower() == "le": #signed less than or equial
                cond = LogicArray("1101")
            elif word[1:3].lower() == "al": #always / unconditional
                cond = LogicArray("1110")
    
    #regular 3 letter commands (add, mov, etc)
    else:
        #i.e. sub
        if len(word) == 3:
            sField = 0
            cond = LogicArray("1110")
        #i.e. subs
        elif len(word) == 4 and word[3] == 's':
            sField = 1
            cond = LogicArray("1110")
        #i.e subeq
        elif len(word) == 5:
            sField = 0
            if word[3:5].lower() == "eq": #equal
                cond = LogicArray("0000")
            elif word[3:5].lower() == "ne": #not equal
                cond = LogicArray("0001")
            elif word[3:5].lower() == "cs": #carry set
                cond = LogicArray("0010")
            elif word[3:5].lower() == "hs": #unsigned higher or same (carry set)
                cond = LogicArray("0010")
            elif word[3:5].lower() == "cc": #carry clear
                cond = LogicArray("0011")
            elif word[3:5].lower() == "lo": #unsigned lower (carry clear)
                cond = LogicArray("0011")
            elif word[3:5].lower() == "mi": #minus / negative
                cond = LogicArray("0100")
            elif word[3:5].lower() == "pl": #plus / positive or zero
                cond = LogicArray("0101")
            elif word[3:5].lower() == "vs": #overflow
                cond = LogicArray("0110")
            elif word[3:5].lower() == "vc": #no overflow
                cond = LogicArray("0111")
            elif word[3:5].lower() == "hi": #unsigned higher
                cond = LogicArray("1000")
            elif word[3:5].lower() == "ls": #unsigned lower or same
                cond = LogicArray("1001")
            elif word[3:5].lower() == "ge": #signed greater than or equal
                cond = LogicArray("1010")
            elif word[3:5].lower() == "lt": #signed less than
                cond = LogicArray("1011")
            elif word[3:5].lower() == "gt": #signed greater than
                cond = LogicArray("1100")
            elif word[3:5].lower() == "le": #signed less than or equial
                cond = LogicArray("1101")
            elif word[3:5].lower() == "al": #always / unconditional
                cond = LogicArray("1110")

    return (cond, sField)

def dataProcCommand(cmd, op, nug):
    cond, sField = checkCond(nug[0])
    rd = LogicArray(int(nug[1].lower()[1:]), Range(3, "downto", 0))
    rn = LogicArray(int(nug[2].lower()[1:]), Range(3, "downto", 0))
            
    src2 = nug[3]
    if src2[0].lower() == 'r':
        #src2 register
        imm = 0
        rm = LogicArray(int(src2[1:], 0), Range(11, "downto", 0))
        bfinal = LogicArray(0, Range(31, "downto", 0))
        bfinal[31:28] = cond
        bfinal[27:26] = op
        bfinal[25] = imm
        bfinal[24:21] = cmd
        bfinal[20] = sField
        bfinal[19:16] = rn
        bfinal[15:12] = rd
        bfinal[11:0] = rm
        print(bfinal)
    else:
        #src2 immediate
        imm = 1
        v = LogicArray(int(src2[1:], 0), Range(11, "downto", 0))
        bfinal = LogicArray(0, Range(31, "downto", 0))
        bfinal[31:28] = cond
        bfinal[27:26] = op
        bfinal[25] = imm
        bfinal[24:21] = cmd
        bfinal[20] = sField
        bfinal[19:16] = rn
        bfinal[15:12] = rd
        bfinal[11:0] = v
        print(bfinal)


checklabels(sys.argv[1])

with open(sys.argv[1]) as f:
    #for loop, repeats for every line in .s file
    for line in f:
    
        #ignore comments
        if line[0]=='@':
            continue
            
        #ignore branch labels
        if line[0]=='.':
            continue
            
        #take in line of assembly and convert it into an array, each element being one of the words
        line = line.replace('\n', '').replace('\r', '').replace('\t', '')
        nug = re.split(r'[, ]',line)
        
        #remove empty strings from array
        while '' in nug:
            nug.remove('')
            
        #ignore array if empty
        if not nug:
            continue   
        
        print(nug)
        
        #translating mov command
        if nug[0].lower() == "mov":
            
            if nug[1].lower() == "pc":
                #for mov pc, lr
                rd = LogicArray(15, Range(3, "downto", 0))
            else:
                #rd is first register, register that will store value
                rd = LogicArray(int(nug[1].lower()[1:]), Range(3, "downto", 0))
            
            #src2 is value stored in rd
            src2 = nug[2]
            if src2[0].lower() == 'r':
                #src2 register
                rm = LogicArray(int(src2[1:], 0), Range(11, "downto", 0))
                b0 = LogicArray("1110000110100000")
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:16] = b0
                bfinal[15:12] = rd
                bfinal[11:0] = rm
                print(bfinal)
            	
            elif src2 == 'lr':
                #src2 register (mov pc, lr)
                rm = LogicArray(14, Range(11, "downto", 0))
                b0 = LogicArray("1110000110100000")
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:16] = b0
                bfinal[15:12] = rd
                bfinal[11:0] = rm
                print(bfinal)
            	
            else:
            	#src2 immediate
                v = LogicArray(int(src2[1:], 0), Range(11, "downto", 0))
                b0 = LogicArray("1110001110100000")
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:16] = b0
                bfinal[15:12] = rd
                bfinal[11:0] = v
                print(bfinal)

### DATA PROCESSING COMMANDS ###

        #and command
        elif nug[0].lower() == "and":
            cmd = LogicArray("0000")
            op = LogicArray("00")
            dataProcCommand(cmd, op, nug)

        #xor command
        elif nug[0].lower() == "eor":
            cmd = LogicArray("0001")
            op = LogicArray("00")
            dataProcCommand(cmd, op, nug)

        #sub command	
        elif nug[0].lower() == "sub":
            cmd = LogicArray("0010")
            op = LogicArray("00")
            dataProcCommand(cmd, op, nug)

        #translating add command	
        elif "add" in nug[0].lower():
            cmd = LogicArray("0100")
            op = LogicArray("00")
            dataProcCommand(cmd, op, nug)
        
        #and command
        elif nug[0].lower() == "and":
            cond, sField = checkCond(nug[0])
            cmd = LogicArray("0000")
            op = LogicArray("00")
            dataProcCommand(cmd, op, nug)
        
        #orr command 	
        elif nug[0].lower() == "orr":
            cond, sField = checkCond(nug[0])
            cmd = LogicArray("1100")
            op = LogicArray("00")
            dataProcCommand(cmd, op, nug)
        
### fyi add checkcond function to these commands thanks ###
        #str command, for now assuming in form str rd, [rn, #imm] (offset)
        elif nug[0].lower() == "str":
            rd = LogicArray(int(nug[1].lower()[1:]), Range(3, "downto", 0))
            rn = LogicArray(int(nug[2].replace('[', '')[1:]), Range(3, "downto", 0))
            
            src2 = nug[3].replace(']', '')
            if src2[0].lower() == 'r':
                #src2 register
                rm = LogicArray(int(src2[1:], 0), Range(3, "downto", 0))
                b0 = LogicArray("111001111000")
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:20] = b0
                bfinal[19:16] = rn
                bfinal[15:12] = rd
                bfinal[11:4] = "00000001"
                bfinal[3:0] = rm
                print(bfinal)
            else:
                #scr2 immediate
                imm12 = LogicArray(int(src2[1:], 0), Range(11, "downto", 0))
                b0 = LogicArray("111001011000")
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:20] = b0
                bfinal[19:16] = rn
                bfinal[15:12] = rd
                bfinal[11:0] = imm12
                print(bfinal)
                
        #ldr command, for now assuming in form ldr rd, [rn, #imm] (offset)
        elif nug[0].lower() == "ldr":
            rd = LogicArray(int(nug[1].lower()[1:]), Range(3, "downto", 0))
            rn = LogicArray(int(nug[2].replace('[', '')[1:]), Range(3, "downto", 0))
            
            src2 = nug[3].replace(']', '')
            if src2[0].lower() == 'r':
                #src2 register
                rm = LogicArray(int(src2[1:], 0), Range(3, "downto", 0))
                b0 = LogicArray("111001111001")
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:20] = b0
                bfinal[19:16] = rn
                bfinal[15:12] = rd
                bfinal[11:4] = "00000001"
                bfinal[3:0] = rm
                print(bfinal)
            else:
                #scr2 immediate
                imm12 = LogicArray(int(src2[1:], 0), Range(11, "downto", 0))
                b0 = LogicArray("111001011001")
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:20] = b0
                bfinal[19:16] = rn
                bfinal[15:12] = rd
                bfinal[11:0] = imm12
                print(bfinal)
        
        #branch command  	
        elif nug[0].lower() == "b":
            #checks if word is in labels array made by first run thru of file
            if nug[1] in labels:
                addr = labels[nug[1]]
                v = addr - (branches[nug[1]] + 2)
                imm24 = LogicArray(v, Range(23, "downto", 0))
                b0 = "11101010"
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:24] = b0
                bfinal[23:0] = imm24
                print(bfinal)
        elif nug[0].lower() == "beq":
            #checks if word is in labels array made by first run thru of file
            if nug[1] in labels:
                addr = labels[nug[1]]
                v = addr - (branches[nug[1]] + 2)
                imm24 = LogicArray(v, Range(23, "downto", 0))
                b0 = "00001010"
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:24] = b0
                bfinal[23:0] = imm24
                print(bfinal)
        elif nug[0].lower() == "bge":
            #checks if word is in labels array made by first run thru of file
            if nug[1] in labels:
                addr = labels[nug[1]]
                v = addr - (branches[nug[1]] + 2)
                imm24 = LogicArray(v, Range(23, "downto", 0))
                b0 = "10101010"
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:24] = b0
                bfinal[23:0] = imm24
                print(bfinal)
                
	#branch link
        elif nug[0].lower() == "bl":
            #checks if word is in labels array made by first run thru of file
            if nug[1] in labels:
                addr = labels[nug[1]]
                v = addr - (branches[nug[1]] + 2)
                imm24 = LogicArray(v, Range(23, "downto", 0))
                b0 = "11101011"
                bfinal = LogicArray(0, Range(31, "downto", 0))
                bfinal[31:24] = b0
                bfinal[23:0] = imm24
                print(bfinal)
