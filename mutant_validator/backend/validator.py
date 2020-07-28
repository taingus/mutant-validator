from typing import List

from .containers import DNA, Node


def is_mutant(sequence: List[str]):
    dna = DNA(dna=sequence)

    for line in dna.dna:
        node = Node(h=line)

        if node.is_mutant():
            return True
    return False
