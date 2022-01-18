from enum import Enum
from struct import pack
from array import array
output = bytearray()

# ADD[32-bit wide]-> add dr, sr1, sr2           ------- Opcode: 0x10   -- A-Type instructions
# SUB[32-bit wide]-> sub dr, sr1, sr2           ------- Opcode: 0x11   -- A-Type instructions
# MUL[32-bit wide]-> mul dr, sr1, sr2           ------- Opcode: 0x12   -- A-Type instructions
# MOV[48-bit wide]-> mov dr, imm[32-bit wide]   ------- Opcode: 0x13   -- M-Type instructions
# JMP[40-bit wide]-> jmp imm[32-bit wide]       ------- Opcode: 0x14   -- J-Type instructions
# BLT[56-bit wide]-> blt, sr1, sr2, offset      ------- Opcode: 0x15   -- B-Type instructions
# BGT[56-bit wide]-> bgt, sr1, sr2, offset      ------- Opcode: 0x16   -- B-Type instructions
# BEQ[56-bit wide]-> beq, sr1, sr2, offset      ------- Opcode: 0x17   -- B-Type instructions

INSTRUCTION_DICT = {
    'add' : 0x10,
    'sub' : 0x11,
    'mul' : 0x12,
    'mov' : 0x13,
    'jmp' : 0x14,
    'blt' : 0x15,
    'bgt' : 0x16,
    'beq' : 0x17,
}
# 8 GPRs -> 0x01 to 0x08
# 1 SPR -> 0x09, 1 PCR 0x0a
REGISTER_DICT = {
    'r0' : 0x01,
    'r1' : 0x02,
    'r2' : 0x03,
    'r3' : 0x04,
    'r4' : 0x05,
    'r5' : 0x06,
    'r6' : 0x07,
    'r7' : 0x08,
    'spr': 0x09,
    'pcr': 0x0a
}

A_TYPE = ['add', 'sub', 'mul']
B_TYPE = ['blt', 'bgt', 'beq']
J_TYPE = ['jmp']
M_TYPE = ['mov']


def get_instruction_type(instruction: str):
    if instruction in A_TYPE:
        return 'a'
    elif instruction in B_TYPE:
        return 'b'
    elif instruction in J_TYPE:
        return 'j'
    elif instruction in M_TYPE:
        return 'm'
    else:
        err = f'Instruction of unknown type {instruction}'
        raise ValueError(err)

if __name__ == '__main__':
    with open('./src/arithmetic.pasm', 'r') as f:
        content = f.readlines()
    for ins in content:
        ins = ins.strip()
        # Support for comments:
        if (loc := ins.find(';')) != -1:
            ins = ins[:loc]
        ins = ins.replace(',', ' ').split()
        insType = ins[0]
        output.append(INSTRUCTION_DICT.get(insType))
        # binary output depends on instruction type
        if get_instruction_type(insType) == 'a':
            output.append(REGISTER_DICT.get(ins[1]))
            output.append(REGISTER_DICT.get(ins[2]))
            output.append(REGISTER_DICT.get(ins[3]))
        elif get_instruction_type(insType) == 'b':
            output.append(REGISTER_DICT.get(ins[1]))
            output.append(REGISTER_DICT.get(ins[2]))
            output.append(int(ins[3], 16))
        elif get_instruction_type(insType) == 'j':
            output.append(int(ins[1], 16))
        elif get_instruction_type(insType) == 'm':
            output.append(REGISTER_DICT.get(ins[1]))
            packed = pack('<i', int(ins[2], 16))
            output += packed
    with open('./bin/arithmetic.bin', 'wb') as out:
        out.write(output)