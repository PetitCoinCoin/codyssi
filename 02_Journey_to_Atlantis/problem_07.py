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
        freq, swaps, test = file.read().strip().split("\n\n")
    freq = [int(x) for x in freq.split("\n")]
    swaps = [tuple([int(x) for x in sub.split("-")]) for sub in swaps.split("\n")]
    test = int(test)
    if args.part == 1:
        for a, b in swaps:
            freq[a - 1], freq[b - 1] = freq[b - 1], freq[a - 1]
    elif args.part == 2:
        for i in range(len(swaps)):
            a, b = swaps[i]
            c, _ = swaps[(i + 1) % len(swaps)]
            freq[b - 1], freq[c - 1], freq[a - 1] = freq[a - 1], freq[b - 1], freq[c - 1]
    else:
        for a, b in swaps:
            a -= 1
            b -= 1
            if a > b:
                a, b = b, a
            block_len = min(b - a, len(freq) - b)
            freq = freq[:a] + freq[b : b + block_len] + freq[a + block_len: b] + freq[a : a + block_len] + freq[b + block_len:]
    print(freq[test - 1])
    print(time() - t)
