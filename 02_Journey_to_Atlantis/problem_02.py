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

def parse_input(raw: str) -> tuple:
    functions, values = raw.split("\n\n")
    func_values = [int(x) for x in re.findall(r"(\d+)", functions)]
    return (
        lambda x: ((x ** func_values[2]) * func_values[1]) + func_values[0],
        [int(x) for x in values.split("\n")],
    )


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        convert, data = parse_input(file.read().strip())
    if args.part == 1:
        print(convert(statistics.median(data)))
    elif args.part == 2:
        print(convert(sum(x for x in data if not x % 2)))
    else:
        max_price = 15000000000000
        # convert function is increasing so it's safe to take max room
        print(max(room for room in data if convert(room) <= max_price))
    print(time() - t)
