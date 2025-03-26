import argparse

from heapq import heappop, heappush
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

GRID = 50

def parse_input(raw: str) -> None:
    for r, row in enumerate(raw.split("\n")):
        for c, char in enumerate(row.split(" ")):
            data[(r, c)] = int(char)

def shortest_path(stop: tuple) -> int:
    seen = {}
    queue = []
    heappush(queue, (data[(0, 0)], 0, 0))
    while queue:
        dist, r, c = heappop(queue)
        if (r, c) == stop:
            return dist
        if seen.get((r, c)):
            continue
        seen[(r, c)] = True
        for dr, dc in [(0, 1), (1, 0)]:
            if data.get((r + dr, c + dc)):
                heappush(queue, (dist + data[(r + dr, c + dc)], r + dr, c + dc))
    return 0

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        parse_input(file.read().strip())
    if args.part == 1:
        columns = [sum(data[i, c] for i in range(GRID)) for c in range(GRID)]
        rows = [sum(data[r, i] for i in range(GRID)) for r in range(GRID)]
        print(min(min(columns), min(rows)))
    elif args.part == 2:
        print(shortest_path((14, 14)))
    else:
        print(shortest_path((GRID - 1, GRID - 1)))
    print(time() - t)
