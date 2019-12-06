from typing import List, Tuple, Optional
import re

start = 284_639
end = 748_759


def part1() -> int:
    valid_count = 0
    for i in range(start, end + 1):
        str_num = [int(j) for j in str(i)]
        is_valid = False
        for j, _ in enumerate(range(len(str_num) - 1), 1):
            if str_num[j] == str_num[j - 1]:
                is_valid = True
            if str_num[j] < str_num[j - 1]:
                is_valid = False
                break
        if is_valid:
            valid_count += 1
    return valid_count


def part2() -> int:
    def is_valid(num: int) -> bool:
        str_num = [int(j) for j in str(num)]
        sorted_num = sorted(str_num)

        if str_num != sorted_num:
            return False

        num_stack: List[int] = []
        for j in str_num:
            if len(num_stack) > 0 and j != num_stack[-1]:
                if len(num_stack) == 2:
                    return True
                else:
                    num_stack.clear()

            num_stack.append(j)

        if len(num_stack) == 2:
            return True

        return False

    valid_count = 0
    for i in range(start, end + 1):
        if is_valid(i):
            valid_count += 1

    return valid_count


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
