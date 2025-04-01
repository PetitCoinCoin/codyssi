from __future__ import annotations

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
class Node:
    id: int
    code: str
    right: Node | None = None
    left: Node | None = None
    parent: Node | None = None

@dataclass
class Tree:
    root: Node
    layers: int = 1

    def insert(self, node: Node) -> str:
        return self.__insert_at(self.root, node, 1)
    
    def __insert_at(self, current: Node, node: Node, layer: int, trace: str = "") -> str:
        self.layers = max(self.layers, layer + 1)
        if node.id >= current.id:
            if not current.right:
                current.right = node
                node.parent = current
                return trace + "-" + current.code
            return self.__insert_at(current.right, node, layer + 1, trace + "-" + current.code)
        if not current.left:
            current.left = node
            node.parrent = current
            return trace + "-" + current.code
        return self.__insert_at(current.left, node, layer + 1, trace + "-" + current.code)

    def find_max_layer(self) -> int:
        max_sum = 0
        layer = [self.root]
        while layer:
            layer_sum = 0
            new_layer = []
            for node in layer:
                layer_sum += node.id
                if node.right:
                    new_layer.append(node.right)
                if node.left:
                    new_layer.append(node.left)
            layer = new_layer
            max_sum = max(max_sum, layer_sum)
        return max_sum

def parse_node(raw: str) -> Node:
    code, id = raw.split(" | ")
    return Node(id=int(id), code=code)

def build_tree() -> Tree:
    root = data.pop(0)
    tree = Tree(root)
    for node in data:
        tree.insert(node)
    return tree

def find_lca(ancestors_a: str, ancestors_b: str) -> str:
    ancestors_a = ancestors_a.split("-")
    ancestors_b = ancestors_b.split("-")
    commons = [n for n in ancestors_a if n in ancestors_b]
    return commons[-1]

if __name__ == "__main__":
    args = _parse_args()
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data_input, requested_input = file.read().strip().split("\n\n")
    data = [parse_node(line) for line in data_input.split("\n")]
    requested = [parse_node(line) for line in requested_input.split("\n")]
    tree = build_tree()
    if args.part == 1:
        print(tree.layers * tree.find_max_layer())
    elif args.part == 2:
        print(tree.insert(Node(id=500000, code="pwet"))[1:])
    else:
        ancestors = [tree.insert(node)[1:] for node in requested]
        print(find_lca(*ancestors))
    print(time() - t)
