from __future__ import annotations

import argparse
import math
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

@dataclass
class Item:
    id: int
    name: str
    quality: int
    cost: int
    material: int

    def __gt__(self, other: Item) -> bool:
        if self.quality == other.quality:
            return self.cost > other.cost
        return self.quality > other.quality

def parse_input(raw: str) -> Item:
    pattern = r"(\d+) (\w+) \| Quality : (\d+), Cost : (\d+), Unique Materials : (\d+)"
    id, name, quality, cost, material = re.findall(pattern, raw)[0]
    return Item(
        id=int(id),
        name=name,
        quality=int(quality),
        cost=int(cost),
        material=int(material),
    )

def optimize_cost(max_cost: int) -> int:
    dp = [[(0, 0)] * (max_cost + 1) for _ in range(len(data) + 1)]
    for item in data:
        for cost in range(max_cost + 1):
            if item.cost <= cost:
                previous = dp[item.id - 1][cost - item.cost]
                dp[item.id][cost] = min(
                    dp[item.id - 1][cost],
                    (previous[0] - item.quality, previous[1] + item.material),
                )
            else:
                dp[item.id][cost] = dp[item.id - 1][cost]
        crafted = []
    for i in range(len(data), 0, -1):
        if dp[i][max_cost] != dp[i - 1][max_cost]:
            crafted.append(data[i - 1])
            max_cost -= data[i - 1].cost
    return sum(item.quality for item in crafted) * sum(item.material for item in crafted)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(line) for line in file.read().strip().split("\n")]
    if args.part == 1:
        data.sort()
        print(sum(item.material for item in data[-5:]))
    elif args.part == 2:
        print(optimize_cost(30))
    else:
        print(optimize_cost(300))
    print(time() - t)
