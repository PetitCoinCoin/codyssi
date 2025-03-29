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
    steps, length = raw.split(" | ")
    start, end = steps.split(" -> ")
    if start not in data:
        data[start] = {}
    data[start][end] = int(length)

def shortest_from_start(*, with_length: bool = False) -> dict:
    seen = {}
    queue = []
    heappush(queue, (0, "STT"))
    while queue:
        dist, step = heappop(queue)
        if step in seen:
            continue
        seen[step] = dist
        for next_step in data.get(step, {}).keys():
            additional_distance = data[step][next_step] if with_length else 1
            heappush(queue, (additional_distance + dist, next_step))
    return seen

def find_max_cycle() -> int:
    cycles = {}
    for start in set(data.keys()):
        queue = []
        heappush(queue, (0, start, start))
        while queue:
            dist, step, path = heappop(queue)
            for next_step in data.get(step, {}).keys():
                if next_step == start:
                    cycles[start] = max(cycles.get(start, 0), dist + data[step][next_step])
                elif next_step in path:
                    continue
                else:
                    heappush(queue, (dist + data[step][next_step], next_step, path + "-" + next_step))
    return max(cycles.values())

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    data = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        for line in file.read().strip().split("\n"):
            parse_input(line)
    if args.part == 1:
        result = 1
        for distance in sorted(shortest_from_start().values(), reverse=True)[:3]:
            result *= distance
        print(result)
    elif args.part == 2:
        result = 1
        for distance in sorted(shortest_from_start(with_length=True).values(), reverse=True)[:3]:
            result *= distance
        print(result)
    else:
        print(find_max_cycle())
    print(time() - t)
