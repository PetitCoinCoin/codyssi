import argparse
import math

from dataclasses import dataclass
from pathlib import Path
from time import time

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--part", "-p",
        type=int,
        choices={1, 2, 3},
        help="Set puzzle part"
    )
    args = parser.parse_args()
    if not args.part:
        parser.error("Which part are you solving?")
    return args

MOD = 100

@dataclass
class Instruction:
    value: int
    row: int
    col: int

class Dice:
    size: int
    faces: dict
    absorption: dict
    values: dict
    with_loop: bool
    
    def __init__(self, size: int = 80, *, with_loop: bool = False) -> None:
        self.size = size
        self.values = {
            k: {
                (r, c): 0  # value from 0 to 99 instead of 1 to 100
                for r in range(self.size)
                for c in range(self.size)
            }
            for k in range(1, 7)
        }
        self.faces = {
            (0, 1): 1,
            (1, 0): 5,
            (1, 1): 2,
            (1, 2): 6,
            (2, 1): 3,
            (3, 1): 4,
        }
        self.absorption = {k: 0 for k in range(1, 7)}
        self.with_loop = with_loop
    
    @property
    def current(self) -> int:
        return self.faces[(0, 1)]

    def apply(self, instruction: Instruction) -> None:
        if instruction.row > -1:
            func = self._add_to_full_row if self.with_loop else self._add_to_row
            func(instruction.row, instruction.value)
        elif instruction.col > -1:
            func = self._add_to_full_col if self.with_loop else self._add_to_col
            func(instruction.col, instruction.value)
        else:
            self._add_to_face(instruction.value)

    def _add_to_row(self, row: int, value: int, face: int | None = None) -> None:
        if face is None:
            face = self.current
        for c in range(self.size):
            self.values[face][(row, c)] = (self.values[face][(row, c)] + value) % MOD
        self.absorption[face] += value * self.size
    
    def _add_to_col(self, col: int, value: int, face: int | None = None) -> None:
        if face is None:
            face = self.current
        for r in range(self.size):
            self.values[face][(r, col)] = (self.values[face][(r, col)] + value) % MOD
        self.absorption[face] += value * self.size

    def _add_to_face(self, value: int) -> None:
        for r in range(self.size):
            for c in range(self.size):
                self.values[self.current][(r, c)] = (self.values[self.current][(r, c)] + value) % MOD
        self.absorption[self.current] += value * self.size * self.size

    def _add_to_full_row(self, row: int, value: int) -> None:
        self._add_to_row(row, value)
        self._add_to_row(self.size - 1 - row, value, self.faces[(2, 1)])
        self._add_to_col(row, value, self.faces[(1, 0)])
        self._add_to_col(self.size - 1 - row, value, self.faces[(1, 2)])

    def _add_to_full_col(self, col: int, value: int) -> None:
        for r in range(4):
            self._add_to_col(col, value, self.faces[(r, 1)])

    def rotate_left(self, face: int) -> None:
        new_val = {
            (self.size - c - 1, r): self.values[face][r, c]
            for r in range(self.size)
            for c in range(self.size)
        }
        self.values[face] = new_val

    def rotate_right(self, face: int) -> None:
        new_val = {
            (c, self.size - r - 1): self.values[face][r, c]
            for r in range(self.size)
            for c in range(self.size)
        }
        self.values[face] = new_val

    def twist(self, direction: str) -> None:
        match direction:
            case "D":
                self.faces[(0, 1)], self.faces[(1, 1)], self.faces[(2, 1)], self.faces[(3, 1)] = self.faces[(1, 1)], self.faces[(2, 1)], self.faces[(3, 1)], self.faces[(0, 1)]
                self.rotate_left(self.faces[(1, 0)])
                self.rotate_right(self.faces[(1, 2)])
            case "U":
                self.faces[(0, 1)], self.faces[(1, 1)], self.faces[(2, 1)], self.faces[(3, 1)] = self.faces[(3, 1)], self.faces[(0, 1)], self.faces[(1, 1)], self.faces[(2, 1)]
                self.rotate_right(self.faces[(1, 0)])
                self.rotate_left(self.faces[(1, 2)])
            case "L":
                self.faces[(1, 0)], self.faces[(0, 1)], self.faces[(1, 2)], self.faces[(2, 1)] = self.faces[(2, 1)], self.faces[(1, 0)], self.faces[(0, 1)], self.faces[(1, 2)],
                self.rotate_left(self.faces[(3, 1)])
                self.rotate_right(self.faces[(1, 2)])
                self.rotate_right(self.faces[(1, 1)])
                self.rotate_right(self.faces[(2, 1)])
                self.rotate_right(self.faces[(1, 0)])
                self.rotate_right(self.faces[(0, 1)])
            case "R":
                self.faces[(1, 0)], self.faces[(0, 1)], self.faces[(1, 2)], self.faces[(2, 1)] = self.faces[(0, 1)], self.faces[(1, 2)], self.faces[(2, 1)], self.faces[(1, 0)]
                self.rotate_right(self.faces[(3, 1)])
                self.rotate_left(self.faces[(1, 1)])
                self.rotate_left(self.faces[(1, 2)])
                self.rotate_left(self.faces[(1, 0)])
                self.rotate_left(self.faces[(2, 1)])
                self.rotate_left(self.faces[(0, 1)])
            case _:
                print("WTF", direction)

    def execute(self) -> None:
        for i in range(len(instructions) - 1):
            self.apply(instructions[i])
            self.twist(twists[i])
        self.apply(instructions[-1])
    
    def _find_dominant_strip(self, face: int) -> int:
        columns = [sum(self.values[face][i, c] for i in range(self.size)) for c in range(self.size)]
        rows = [sum(self.values[face][r, i] for i in range(self.size)) for r in range(self.size)]
        return max(max(columns), max(rows)) + self.size

    def dominant(self) -> int:
        return math.prod(self._find_dominant_strip(face) for face in range(1, 7))

def parse_instruction(raw: str) -> Instruction:
    items = raw.split()
    match items[0]:
        case "FACE":
            row = -1
            col = -1
        case "ROW":
            row = int(items[1]) - 1
            col = -1
        case "COL":
            row = -1
            col = int(items[1]) - 1
        case _:
            print("WTF", items[0])
    return Instruction(int(items[-1]), row, col)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        instr_input, twists_input = file.read().strip().split("\n\n")
    twists = [x for x in twists_input]
    instructions = [parse_instruction(line) for line in instr_input.split("\n")]
    dice = Dice(with_loop=args.part == 3)
    dice.execute()
    if args.part == 1:
        print(math.prod(sorted(dice.absorption.values())[-2:]))
    elif args.part == 2:
        print(dice.dominant())
    else:
        print(dice.dominant())
    print(time() - t)
