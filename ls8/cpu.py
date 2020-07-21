"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.running = False

    def ram_read(self, register):
        return self.memory[register]

    def ram_write(self, value, register):
        self.memory[register] = value

    def load(self, file_):
        """Load a program into memory."""

        program = []

        with open(f'ls8/examples/{file_}') as f:
            for line in f:
                line = line.split("#")
                # print(line)
                try:
                    v = int(line[0])
                    # print(v)
                    program.append(v)
                except ValueError:
                    continue

                address = 0

                for instruction in program:
                    self.ram_write(instruction, address)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # op = op.upper()

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "HLT":
            self.running = False
        elif op == "LDI":
            self.reg[reg_a] = reg_b
        elif op == "PRN":
            print(self.ram_read(int(reg_a)))
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def binaryToDecimal(self, binary):
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return decimal

    def run(self):
        """Run the CPU."""
        self.running = True

        ops = {
            1: ["HLT", 0],
            130: ["LDI", 2],
            71: ["PRN", 1]
        }

        address = 0
        while self.running:
            num = self.binaryToDecimal(self.ram_read(address))
            command = ops[num]
            params = [0] * 2
            print(command)
            for i in range(0, command[1]):
                address += 1
                params[i] = self.ram_read(address)

            self.alu(command[0], params[0], params[1])

            address += 1