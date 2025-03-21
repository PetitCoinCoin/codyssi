from __future__ import annotations
import argparse

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

@dataclass
class Pos:
    x: int
    y: int

    def __gt__(self, p: Pos) -> bool:
        if self.x == p.x:
            return self.y > p.y
        return self.x > p.x

    def __str__(self):
        return f"{self.x}, {self.y}"

def parse_input(raw) -> Pos:
    return Pos(*[int(x) for x in raw[1:-1].split(", ")])

def manhattan(p1: Pos, p2: Pos) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().strip().split("\n")]
    distances = [manhattan(Pos(0, 0), position) for position in data]
    if args.part == 1:
        print(max(distances) - min(distances))
    elif args.part == 2:
        # No tie, only one closest
        closest = [pos for pos in data if manhattan(Pos(0, 0), pos) == min(distances)][0]
        print(min(manhattan(closest, position) for position in data if position != closest))
    else:
        path = 0
        seen = {}
        step = Pos(0, 0)
        while len(seen) != len(data):
            distances = [manhattan(step, position) for position in data if str(position) not in seen]
            closests = [position for position in data if manhattan(step, position) == min(distances)]
            closests.sort()
            closest = closests[0]
            path += min(distances)
            seen[str(closest)] = True
            step = closest
        print(path)
    print(time() - t)
