from typing import List

from .containers import DNA, Node


def is_mutant(sequence: List[str]):
    dna = DNA(dna=sequence)

    h_len = len(dna.dna[0])
    v_len = len(dna.dna)

    for line in dna.dna:
        node = Node(h=line, v_len=v_len, h_len=h_len)

        if node.is_mutant():
            return True
    return False
