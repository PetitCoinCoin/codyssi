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

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    symbols = [int(f"{symbol}1") for symbol in data.pop()]
    data = [int(x) for x in data]
    if args.part == 1:
        pass
    elif args.part == 2:
        symbols = symbols[::-1]
    else:
        data = [10 * data[i] + data[i+1] for i in range(0, len(data) - 1, 2)]
        symbols = symbols[:(len(symbols) - len(data) - 1):-1]
    offset = data.pop(0)
    print(offset + sum((x * m) for (x, m) in zip(data, symbols)))
    print(time() - t)
