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

def count_alpha(raw: str) -> int:
    return sum(x.isalpha() for x in raw)

def reduce_str(raw: str, *, updated: bool = False) -> int:
    reduced = True
    while reduced:
        reduced = False
        new_raw = ""
        i = 0
        while i < len(raw):
            if raw[i].isdigit():
                if i < len(raw) - 1 and (
                    raw[i + 1].isalpha() if updated
                    else not raw[i + 1].isdigit()
                ):
                    i += 1
                elif i > 0 and new_raw and (
                    new_raw[-1].isalpha() if updated
                    else not new_raw[-1].isdigit()
                ):
                    new_raw = new_raw[:-1]
                else:
                    new_raw += raw[i]
            else:
                new_raw += raw[i]
            i += 1
        reduced = len(new_raw) < len(raw)
        raw = new_raw
    return len(raw)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    if args.part == 1:
        print(sum(count_alpha(x) for x in data))
    elif args.part == 2:
        print(sum(reduce_str(x) for x in data))
    else:
        print(sum(reduce_str(x, updated=True) for x in data))
    print(time() - t)
