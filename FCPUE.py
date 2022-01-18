from FAssembler import INSTRUCTION_DICT

def get_str_from_op(opcode: int):
    opcodeList = list(INSTRUCTION_DICT.values())
    strCodeList = list(INSTRUCTION_DICT.keys())
    pos = opcodeList.index(opcode)
    return strCodeList[pos]

class Memory:
    def __init__(self) -> None:
        self.instructions = []
    
class FakeCPU:
    def __init__(self, memory: Memory) -> None:
        self.general_registers = [0] * 8
        self.stack_register = 0
        self.program_register = 0
        self.instructions = memory.instructions
        self.FUNC_CALLBACKS = {
            0x10: self.add,
            0x11: self.sub,
            0x12: self.mul,
            0x13: self.mov,
            0x14: self.jmp,
            0x15: self.blt,
            0x16: self.bgt,
            0x17: self.beq,
        }
        self.regsnap = []
    def execute(self):
        self.program_register = 0
        self.stack_register = 0
        while self.program_register < len(self.instructions):
            ins_func = self.FUNC_CALLBACKS.get(self.instructions[self.program_register])
            ins_func()
    def add(self): # val can be a register
        # self.instructions[self.program_register:self.program_register+4]
        dr1, sr1, sr2 = self.instructions[self.program_register+1:self.program_register+4]
        self.general_registers[dr1-1] = self.general_registers[sr1-1] + self.general_registers[sr2-1]
        self.program_register += 4
    def sub(self):
        dr1, sr1, sr2 = self.instructions[self.program_register+1:self.program_register+4]
        self.general_registers[dr1-1] = self.general_registers[sr1-1] - self.general_registers[sr2-1]
        self.program_register += 4
    def mul(self):
        dr1, sr1, sr2 = self.instructions[self.program_register+1:self.program_register+4]
        self.general_registers[dr1-1] = self.general_registers[sr1-1] * self.general_registers[sr2-1]
        self.program_register += 4
    def mov(self):
        dr1 = self.instructions[self.program_register+1]
        self.general_registers[dr1-1] = int.from_bytes(self.instructions[self.program_register+2:self.program_register+5], 'little')
        self.program_register += 6
    def jmp(self):
        self.instructions[self.program_register:self.program_register+5]
    def blt(self):
        pass
    def bgt(self):
        pass
    def beq(self):
        pass
    # Take snapshot of CPU
    def snapshot(self):
        self.regsnap.append(self.registers)

with open('./bin/arithmetic.bin', 'rb') as bin:
    cursor = 0
    mem = Memory()
    mem.instructions = bin.read()
    cpu = FakeCPU(mem)
    cpu.execute()
    print(mem.instructions)
    for i, reg in enumerate(cpu.general_registers):
        print(f"r{i}: {reg}")



# Fake CPU Emulator is a an emulator for a fake cpu.
# fake cpu specs:
# 8 GPRs -> 0x01 to 0x08
# 1 SPR -> 0x09, 1 PCR 0x0a
# at least 8 bit instruction size
# first 8 bits: instruction
# ADD[32-bit wide]-> add dr, sr1, sr2           ------- Opcode: 0x10
# SUB[32-bit wide]-> sub dr, sr1, sr2           ------- Opcode: 0x11
# MUL[32-bit wide]-> mul dr, sr1, sr2           ------- Opcode: 0x12
# LOD[48-bit wide]-> LOD dr, imm[32-bit wide]   ------- Opcode: 0x13
# JMP[40-bit wide]-> JMP imm[32-bit wide]       ------- Opcode: 0x14
# BLT[48-bit wide]-> BLT, sr1, sr2, offset      ------- Opcode: 0x15
# BGT[48-bit wide]-> BGT, sr1, sr2, offset      ------- Opcode: 0x16
# BEQ[48-bit wide]-> BEQ, sr1, sr2, offset      ------- Opcode: 0x17
# Registers - 32bits
# rid 0 - 7 = general purpose register
# rid 8 = stack pointer register
# rid 9 = program counter register