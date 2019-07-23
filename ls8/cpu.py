"""CPU functionality."""

import sys

ldi = 0b10000010
prn = 0b01000111
hlt = 0b00000001
call = 0b01010000
add = 0b10100000
ret = 0b00010001
mul = 0b10100010

class Commands:
    def __init__(self, cpu):
        self.list = {ldi: self.ldi, prn:self.prn, hlt:self.hlt, mul:self.mul}
        self.list[ldi] = self.ldi
        self.cpu = cpu

    def ldi(self):
        op_a = self.cpu.ram_read(self.cpu.pc + 1)
        op_b = self.cpu.ram_read(self.cpu.pc + 2)
        self.cpu.register[op_a] = op_b
        return 2

    def prn(self):
        op_a = self.cpu.ram_read(self.cpu.pc + 1)
        print(self.cpu.register[op_a])
        return 1

    def mul(self):
        op_a = self.cpu.ram_read(self.cpu.pc + 1)
        op_b = self.cpu.ram_read(self.cpu.pc + 2)
        print(self.cpu.register[op_a] * self.cpu.register[op_b])
        return 2

    def hlt(self):
        return len(self.cpu.ram)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [None] * 256
        self.pc = 0
        self.commands = Commands(self)

    def load(self):
        """Load a program into memory."""
        # For now, we've just hardcoded a program:
        with open(f"{sys.argv[1]}") as f:
            i = 0
            for line in f:
                if(i < len(self.ram)):
                    command = line.replace(" ", "")[:8]
                    if(self.isValidCommand(command)):
                        self.ram[i] = int(command, 2)
                    i += 1
                else:
                    print("STACK OVERFLOW") 
                
    def ram_read(self, address):
        return self.ram[address] if address < len(self.ram) else None

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        ir = self.ram_read(0)
        while True:
            if(ir == None):
                return

            if(ir in self.commands.list):
                inc = self.commands.list[ir]()
            else:
                print(f"ERROR: Invalid command {ir}")
            
            self.pc += 1 + inc
            ir = self.ram_read(self.pc)
    
    def isValidCommand(self, command):
        for char in command:
            if(char != "0" and char !="1"):
                return False
        return True
