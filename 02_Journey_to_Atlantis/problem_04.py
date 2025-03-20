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
    return ord(letter) - 64

def compress(raw: str) -> str:
    idx = int(len(raw) // 10)
    return raw[:idx] + str(len(raw) - 2 * idx) + raw[-idx:]

def lossless_compress(raw: list) -> str:
    compressed = ""
    char = raw.pop(0)
    freq = 1
    while raw:
        next_char = raw.pop(0)
        if char == next_char:
            freq += 1
        else:
            compressed += str(freq) + char
            char = next_char
            freq = 1
    return compressed + str(freq) + char

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")
    if args.part == 1:
        pass
    elif args.part == 2:
        data = [compress(item) for item in data]
    else:
        data = [lossless_compress([c for c in item]) for item in data]
    print(sum(
        int(char) if char.isdigit() else char_position(char)
        for item in data
        for char in item
    ))
    print(time() - t)
