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
        data = [int(x) for x in file.read().strip().split("\n")]
    if args.part == 1:
        print(sum(data))
    elif args.part == 2:
        data.sort()
        print(sum(data[:-20]))
    else:
        print(sum(x if not i % 2 else -x for i, x in enumerate(data)))
    print(time() - t)
