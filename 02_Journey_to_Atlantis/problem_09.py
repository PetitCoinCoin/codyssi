import argparse
import re

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
class Transaction:
    x_from: str
    x_to: str
    amount: int

def parse_initial_balances(raw: str) -> dict:
    return {
        item.split(" HAS ")[0]: int(item.split(" HAS ")[1])
        for item in raw.split("\n")
    }

def parse_transactions(raw: str) -> list:
    pattern = r"FROM ([\w\-]+) TO ([\w\-]+) AMT (\d+)"
    return [
        Transaction(
            x_from=found[0],
            x_to=found[1],
            amount=int(found[2]),
        )
        for item in raw.split("\n")
        for found in re.findall(pattern, item)
    ]

def receive_money(receiver: str, amount: int) -> None:
    balances[receiver] += amount
    while debts[receiver] and balances[receiver]:
        if debts[receiver][0][0] > balances[receiver]:
            paid = balances[receiver]
            debts[receiver][0][0] -= paid
            balances[receiver] = 0
            receive_money(debts[receiver][0][1], paid)
        else:
            debt, recep = debts[receiver].pop(0)
            balances[receiver] -= debt
            receive_money(recep, debt)

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n\n")
    balances = parse_initial_balances(data[0])
    transactions = parse_transactions(data[1])
    if args.part == 1:
        for transaction in transactions:
            balances[transaction.x_from] -= transaction.amount
            balances[transaction.x_to] += transaction.amount
    elif args.part == 2:
        for transaction in transactions:
            effective_amount = min(balances[transaction.x_from], transaction.amount)
            balances[transaction.x_from] -= effective_amount
            balances[transaction.x_to] += effective_amount
    else:
        debts = {k: [] for k in balances.keys()}
        for transaction in transactions:
            effective_amount = min(balances[transaction.x_from], transaction.amount)
            debt = transaction.amount - effective_amount
            balances[transaction.x_from] -= effective_amount
            if debt:
                debts[transaction.x_from].append([debt, transaction.x_to])
            receive_money(transaction.x_to, effective_amount)
    amounts = sorted(balances.values(), reverse=True)
    print(sum(amounts[:3]))
    print(time() - t)
