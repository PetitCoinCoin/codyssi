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
class Record:
    value: str
    base: int

def convert_to_65(val: int) -> str:
    BASE_CHAR = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#"
    n = 0
    result = ""
    while val // (65 ** n) > 0:
        n += 1
    while n > 0:
        n -= 1
        result += BASE_CHAR[int(val // (65 ** n))]
        val %= 65 ** n
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [Record(x.split(" ")[0], int(x.split(" ")[-1])) for x in file.read().strip().split("\n")]
    if args.part == 1:
        print(sum(x.base for x in data))
    elif args.part == 2:
        print(sum(int(x.value, x.base) for x in data))
    else:
        print(convert_to_65(sum(int(x.value, x.base) for x in data)))
    print(time() - t)
