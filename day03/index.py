from typing import List, Tuple, Optional
from enum import Enum
import numpy as np

file = open("day03/input.txt", mode="r")
input = file.readlines()
file.close()
wires = [wire.split(",") for wire in input]


class Direction(Enum):
    Right = "R"
    Up = "U"
    Left = "L"
    Down = "D"


Wire = List[str]
Point = Tuple[int, int]


def get_wire_points(wire: Wire) -> List[Point]:
    points = []
    index = (0, 0)
    for instruction in wire:
        direction, length = instruction[0], int(instruction[1:])
        for i in range(length):
            if direction == Direction.Right.value:
                index = (index[0] + 1, index[1])
            if direction == Direction.Left.value:
                index = (index[0] - 1, index[1])
            if direction == Direction.Up.value:
                index = (index[0], index[1] + 1)
            if direction == Direction.Down.value:
                index = (index[0], index[1] - 1)
            points.append(index)
    return points


def get_wire_intersections(wires: List[Wire]) -> List[Point]:
    wire_sets = []
    for wire in wires:
        points = get_wire_points(wire)
        wire_sets.append(set(points))
    intersections = wire_sets[0].intersection(*wire_sets[1:])
    return intersections


def part1(wires: List[Wire]) -> int:
    intersections = get_wire_intersections(wires)
    manhattan_distnaces = [abs(i[0]) + abs(i[1]) for i in intersections]
    return min(manhattan_distnaces)


def part2(wires: List[Wire]) -> int:
    steps = []
    intersections = get_wire_intersections(wires)
    wire_points = [get_wire_points(wire) for wire in wires]
    for intersection in intersections:
        intersection_steps = 0
        for points in wire_points:
            num_steps = points.index(intersection) + 1
            intersection_steps += num_steps
        steps.append(intersection_steps)

    return min(steps)


print(f"Part 1: {part1(wires)}")
print(f"Part 2: {part2(wires)}")
