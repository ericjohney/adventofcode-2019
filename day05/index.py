from typing import List, Tuple, Optional
import numpy as np
from enum import Enum

file = open("day05/input.txt", mode="r")
input = file.read().strip()
file.close()
opcodes: List[int] = [int(o) for o in input.split(",")]

Opcodes = List[int]

class Opcode(Enum):
    Add = 1
    Multiply = 2
    Input = 3
    Output = 4
    JumpIfTrue = 5
    JumpIfFalse = 6
    LessThan = 7
    Equals = 8
    End = 99

class Parameter:
    raw_value: int
    mode: int
    def __init__(self, raw_value: int, mode: int):
        self.raw_value = raw_value
        self.mode = mode

    def get_value(self, opcodes: Opcodes) -> int:
        if self.mode == ParameterMode.Position.value:
            return opcodes[self.raw_value]
        if self.mode == ParameterMode.Immediate.value:
            return self.raw_value

class ParameterMode(Enum):
    Position = 0
    Immediate = 1


OPCODE_PARAMETERS = {
    Opcode.Add.value: 3,
    Opcode.Multiply.value: 3,
    Opcode.Input.value: 1,
    Opcode.Output.value: 1,
    Opcode.JumpIfTrue.value: 2,
    Opcode.JumpIfFalse.value: 2,
    Opcode.LessThan.value: 3,
    Opcode.Equals.value: 3,
    Opcode.End.value: 0,
}



class Computer:
    pointer = 0

    def __init__(self, opcodes: Opcodes):
        self.opcodes = list(opcodes)

    def do_add(self, parameters: List[Parameter]) -> int:
        *values, save_location = parameters
        values = [v.get_value(self.opcodes) for v in values]
        self.opcodes[save_location.raw_value] = sum(values)

    def do_multiply(self, parameters: List[Parameter]) -> int:
        *values, save_location = parameters
        values = [v.get_value(self.opcodes) for v in values]
        self.opcodes[save_location.raw_value] = values[0] * values[1]

    def do_input(self, parameters: List[Parameter], value: int) -> int:
        save_location = parameters[0]
        self.opcodes[save_location.raw_value] = value

    def do_output(self, parameters: List[Parameter]) -> int:
        value = parameters[0].get_value(self.opcodes)
        print(f"output: {value}")

    def do_jump_if_true(self, parameters: List[Parameter]) -> int:
        values = [v.get_value(self.opcodes) for v in parameters]
        if values[0] != 0:
            self.pointer = values[1]

    def do_jump_if_false(self, parameters: List[Parameter]) -> int:
        values = [v.get_value(self.opcodes) for v in parameters]
        if values[0] == 0:
            self.pointer = values[1]

    def do_less_than(self, parameters: List[Parameter]) -> int:
        *values, save_location = parameters
        values = [v.get_value(self.opcodes) for v in values]
        if values[0] < values[1]:
            self.opcodes[save_location.raw_value] = 1
        else:
            self.opcodes[save_location.raw_value] = 0

    def do_equals(self, parameters: List[Parameter]) -> int:
        *values, save_location = parameters
        values = [v.get_value(self.opcodes) for v in values]
        if values[0] == values[1]:
            self.opcodes[save_location.raw_value] = 1
        else:
            self.opcodes[save_location.raw_value] = 0

    def read_next_opcode(self) -> Tuple[int, List[Parameter]]:
        raw_opcode = self.opcodes[self.pointer]
        opcode = int(str(raw_opcode)[-2:])
        num_params = OPCODE_PARAMETERS[opcode]
        raw_parameter_modes = str(raw_opcode)[::-1][2:].ljust(num_params, '0')

        parameter_modes: List[int] = np.zeros(num_params, dtype=int)
        for i in range(len(raw_parameter_modes)):
            parameter_modes[i] = int(raw_parameter_modes[i])

        parameters = self.opcodes[self.pointer + 1 : self.pointer + 1 + num_params]

        for i, param in enumerate(parameters):
            parameters[i] = Parameter(param, parameter_modes[i])

        self.pointer += 1 + num_params

        return (opcode, *parameters)

    def compute(self, input_value) -> Opcodes:
        while self.pointer < len(self.opcodes):
            opcode, *parameters = self.read_next_opcode()
            if opcode == Opcode.End.value:
                break

            if opcode == Opcode.Add.value:
                self.do_add(parameters)
            elif opcode == Opcode.Multiply.value:
                self.do_multiply(parameters)
            elif opcode == Opcode.Input.value:
                self.do_input(parameters, input_value)
            elif opcode == Opcode.Output.value:
                self.do_output(parameters)
            elif opcode == Opcode.JumpIfTrue.value:
                self.do_jump_if_true(parameters)
            elif opcode == Opcode.JumpIfFalse.value:
                self.do_jump_if_false(parameters)
            elif opcode == Opcode.LessThan.value:
                self.do_less_than(parameters)
            elif opcode == Opcode.Equals.value:
                self.do_equals(parameters)

        return self.opcodes


def part1(input: Opcodes) -> int:
    computer = Computer(opcodes)
    return computer.compute(1)[0]


def part2(input: Opcodes) -> int:
    computer = Computer(opcodes)
    return computer.compute(5)[0]


print(f"Part 1: {part1(opcodes)}")
print(f"Part 2: {part2(opcodes)}")
