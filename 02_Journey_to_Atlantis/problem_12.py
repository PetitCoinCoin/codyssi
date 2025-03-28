import argparse
import re

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

GRID = 30
MOD = 1073741823 + 1

@dataclass
class Instruction:
    is_shift: bool
    action: callable
    value: int
    row: int
    col: int

def parse_grid(raw: str) -> None:
    for r, row in enumerate(raw.split("\n")):
        for c, char in enumerate(row.split(" ")):
            grid[(r, c)] = int(char)

def parse_instruction(raw: str) -> Instruction:
    if raw.startswith("SHIFT"):
        is_shift = True
        pattern = r"[\D]+(\d+)[\D]+(\d+)"
        item, value = re.findall(pattern, raw)[0]
        if raw.startswith("SHIFT ROW"):
            col = 0
            row = item
            action=shift_row
        else:
            row = 0
            col = item
            action=shift_col
    else:
        is_shift = False
        if raw.startswith("ADD"):
            action = lambda x, y: x + y
        elif raw.startswith("SUB"):
            action = lambda x, y: x - y
        elif raw.startswith("MULTIPLY"):
            action = lambda x, y: x * y
        else:
            print("WTF")
        if "ALL" in raw:
            row = 0
            col = 0
            value = raw.split(" ")[1]
        else:
            pattern = r"[\D]+(\d+)[\D]+(\d+)"
            value, item = re.findall(pattern, raw)[0]
            if "ROW" in raw:
                row = item
                col = 0
            else:
                col = item
                row = 0
    return Instruction(
        is_shift=is_shift,
        action=action,
        value=int(value),
        row=int(row) - 1,
        col=int(col) - 1,
    )

def shift_row(row: int, offset: int) -> None:
    r = [grid[(row, c)] for c in range(GRID)]
    r = r[-offset:] + r[:-offset]
    for c, val in enumerate(r):
        grid[(row, c)] = val

def shift_col(col: int, offset: int) -> None:
    c = [grid[(r, col)] for r in range(GRID)]
    c = c[-offset:] + c[:-offset]
    for r, val in enumerate(c):
        grid[(r, col)] = val

def execute(inst: Instruction) -> None:
    if inst.is_shift:
        inst.action(inst.row if inst.row > -1 else inst.col, inst.value)
    else:
        if inst.row == -1 and inst.col == -1:
            for k, v in grid.items():
                grid[k] = inst.action(v, inst.value) % MOD
        elif inst.row == -1:
            for r in range(GRID):
                grid[(r, inst.col)] = inst.action(grid[(r, inst.col)], inst.value) % MOD
        else:
            for c in range(GRID):
                grid[(inst.row, c)] = inst.action(grid[(inst.row, c)], inst.value) % MOD


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    grid = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        g_input, i_input, f_input = file.read().strip().split("\n\n")
    parse_grid(g_input)
    instructions = [parse_instruction(line) for line in i_input.split("\n")]
    flows = f_input.split("\n")
    if args.part == 1:
        for instruction in instructions:
            execute(instruction)
    elif args.part == 2:
        for flow in flows:
            if flow == "TAKE":
                instruction = instructions.pop(0)
            elif flow == "CYCLE":
                instructions.append(instruction)
            else:
                execute(instruction)
    else:
        while instructions:
            for flow in flows:
                if not instructions:
                    break
                if flow == "TAKE":
                    instruction = instructions.pop(0)
                elif flow == "CYCLE":
                    instructions.append(instruction)
                else:
                    execute(instruction)
    columns = [sum(grid[i, c] for i in range(GRID)) for c in range(GRID)]
    rows = [sum(grid[r, i] for i in range(GRID)) for r in range(GRID)]
    print(max(max(columns), max(rows)))
    print(time() - t)
