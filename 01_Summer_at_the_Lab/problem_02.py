import argparse
import statistics
import re

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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [x == "TRUE" for x in file.read().strip().split("\n")]
    if args.part == 1:
        print(sum(i + 1 for i, x in enumerate(data) if x))
    elif args.part == 2:
        print(sum(
            data[i] and data[i + 1] if not i % 4 else data[i] or data[i + 1]
            for i in range(0, len(data), 2)
        ))
    else:
        result = 0
        while len(data) > 1:
            result += sum(data)
            data = [
                data[i] and data[i + 1] if not i % 4 else data[i] or data[i + 1]
                for i in range(0, len(data), 2)
            ]
        print(result + data[0])
    print(time() - t)
