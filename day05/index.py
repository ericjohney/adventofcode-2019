from typing import List, Tuple, Optional
import numpy as np
from enum import Enum

file = open("day05/input.txt", mode="r")
input = file.read().strip()
file.close()
opcodes: List[int] = [int(o) for o in input.split(",")]


class Opcode(Enum):
    Add = 1
    Multiply = 2
    Input = 3
    Output = 4
    End = 99


class ParameterMode(Enum):
    Position = 0
    Immediate = 1


OPCODE_PARAMETERS = {
    Opcode.Add.value: 3,
    Opcode.Multiply.value: 3,
    Opcode.Input.value: 1,
    Opcode.Output.value: 1,
    Opcode.End.value: 0,
}

Opcodes = List[int]


class Computer:
    pointer = 0

    def __init__(self, opcodes: Opcodes):
        self.opcodes = list(opcodes)

    def do_add(self, parameters: List[int]) -> int:
        *values, save_location = parameters
        self.opcodes[save_location] = sum(values)

    def do_multiply(self, parameters: List[int]) -> int:
        *values, save_location = parameters
        self.opcodes[save_location] = values[0] * values[1]

    def get_parameter_value(self, parameter_modes: List[int], parameters: List[int]) -> int:
        values = 
        for i, param in enumerate(parameters):
            if parameter_modes[i] == ParameterMode.Position.value:
                parameters[i] = self.opcodes[param]
            if parameter_modes[i] == ParameterMode.Immediate.value:
                pass

    def read_next_opcode(self) -> List[int]:
        raw_opcode = self.opcodes[self.pointer]
        opcode = raw_opcode % 100
        raw_parameter_modes = str(raw_opcode)[::-1][2:]
        num_params = OPCODE_PARAMETERS[opcode]
        parameter_modes: List[int] = np.zeros(num_params, dtype=int)
        for i in range(len(raw_parameter_modes)):
            parameter_modes[i] = int(raw_parameter_modes[i])

        parameters = self.opcodes[self.pointer + 1 : self.pointer + 1 + num_params]
        for i, param in enumerate(parameters):
            if parameter_modes[i] == ParameterMode.Position.value:
                parameters[i] = self.opcodes[param]
            if parameter_modes[i] == ParameterMode.Immediate.value:
                pass

        self.pointer += num_params

        return [opcode, *parameters]

    def compute(self) -> Opcodes:
        while self.pointer < len(self.opcodes):
            opcode, *parameters = self.read_next_opcode()
            if opcode == Opcode.End.value:
                break

            if opcode == Opcode.Add.value:
                self.do_add(parameters)
            elif opcode == Opcode.Multiply.value:
                self.do_multiply(parameters)

        return opcodes


def part1(input: Opcodes) -> int:
    computer = Computer(opcodes)
    return computer.compute()


def part2(input: Opcodes) -> Optional[Tuple[int, int]]:
    pass


print(f"Part 1: {part1(opcodes)}")
# print(f"Part 2: {part2(opcodes)}")
