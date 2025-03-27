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

def to_base_10(rec: Record) -> int:
    BASE_CHAR = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    return sum(BASE_CHAR.index(char) * (rec.base ** exp) for exp, char in enumerate(rec.value[::-1]))

def convert_to_68(val: int) -> str:
    BASE_CHAR = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^"
    BASE = 68
    n = 0
    result = ""
    while val // (BASE ** n) > 0:
        n += 1
    while n > 0:
        n -= 1
        result += BASE_CHAR[int(val // (BASE ** n))]
        val %= BASE ** n
    return result

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [Record(x.split(" ")[0], int(x.split(" ")[-1])) for x in file.read().strip().split("\n")]
    if args.part == 1:
        print(max(to_base_10(x) for x in data))
    elif args.part == 2:
        print(convert_to_68(sum(to_base_10(x) for x in data)))
    else:
        sum_records = sum(to_base_10(x) for x in data)
        base = 68
        while sum_records // (base ** 4) > 0:
            base += 1
        print(base)
    print(time() - t)
