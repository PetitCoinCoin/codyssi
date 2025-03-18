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


def parse_input(raw: str) -> None:
    loc_a, loc_b = raw.split(" <-> ")
    data[loc_a] = data.get(loc_a, set()) | {loc_b}
    data[loc_b] = data.get(loc_b, set()) | {loc_a}


def find_shortest() -> dict:
    seen = {}
    queue = []
    heappush(queue, (0, "STT"))
    while queue:
        duration, step = heappop(queue)
        if step in seen:
            continue
        seen[step] = duration
        for next_step in data[step]:
            heappush(queue, (duration + 1, next_step))
    return seen


if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        [parse_input(x) for x in file.read().strip().split("\n")]
    if args.part == 1:
        print(len(data.keys()))
    elif args.part == 2:
        print(sum(x <= 3 for x in find_shortest().values()))
    else:
        print(sum(find_shortest().values()))
    print(time() - t)
