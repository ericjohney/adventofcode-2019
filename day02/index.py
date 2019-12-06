from typing import List, Tuple, Optional
from enum import Enum

file = open("day02/input.txt", mode="r")
input = file.read().strip()
file.close()
opcodes: List[int] = [int(o) for o in input.split(",")]


class Opcode(Enum):
    Add = 1
    Multipy = 2
    End = 99


def compute(
    input: List[int], noun: Optional[int] = None, verb: Optional[int] = None
) -> List[int]:
    opcodes = list(input)
    if noun:
        opcodes[1] = noun
    if verb:
        opcodes[2] = verb

    index = 0
    while index < len(opcodes):
        opcode = opcodes[index]
        if opcode == Opcode.End.value:
            break

        *value_locations, save_location = opcodes[index + 1 : index + 4]
        values = [opcodes[i] for i in value_locations]
        if opcode == Opcode.Add.value:
            opcodes[save_location] = sum(values)
            index += 4
        elif opcode == Opcode.Multipy.value:
            opcodes[save_location] = values[0] * values[1]
            index += 4

    return opcodes


def part1(input: List[int]) -> int:
    return compute(input)[0]


def part2(input: List[int]) -> Optional[Tuple[int, int]]:
    for noun in range(0, 99):
        for verb in range(0, 99):
            opcodes = compute(input, noun=noun, verb=verb)
            if opcodes[0] == 19_690_720:
                return (noun, verb)

    return None


print(f"Part 1: {part1(opcodes)}")
print(f"Part 2: {part2(opcodes)}")
