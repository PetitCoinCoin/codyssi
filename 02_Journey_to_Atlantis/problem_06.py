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

def char_position(letter: str) -> int:
    if letter.islower():
        return ord(letter) - 96
    return ord(letter) - 64 + 26

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip()
    uncorrupted = [x for x in data if x.lower() != x.upper()]
    if args.part == 1:
        print(len(uncorrupted))
    elif args.part == 2:
        print(sum(char_position(x) for x in uncorrupted))
    else:
        result = []
        for i in range(len(data)):
            if data[i].lower() != data[i].upper():
                result.append(char_position(data[i]))
            else:
                delta = result[-1] * 2 - 5
                while delta < 1:
                    delta += 52
                while delta > 52:
                    delta -= 52
                result.append(delta)
        print(sum(result))
    print(time() - t)
