import argparse

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

def parse_input(raw: str) -> list:
    return [range(int(a.split("-")[0]), int(a.split("-")[1]) + 1) for a in raw.split(" ")]

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [parse_input(raw) for raw in file.read().strip().split("\n")]
    if args.part == 1:
        print(len([
            box
            for item in data
            for pile in item
            for box in pile
        ]))
    elif args.part == 2:
        piles = [set(item[0]) | set(item[1]) for item in data]
        print(sum(len(pile) for pile in piles))
    else:
        piles = [set(item[0]) | set(item[1]) for item in data]
        max_boxes = 0
        for i in range(len(piles) - 1):
            max_boxes = max(len(piles[i] | piles[i + 1]), max_boxes)
        print(max_boxes)
    print(time() - t)
