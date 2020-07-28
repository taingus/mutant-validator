from typing import (
    List,
    Union,
)

from .containers import (
    DNA,
    Node,
)


def is_mutant(sequence: Union[List[str], DNA]):
    if isinstance(sequence, list):
        sequence = DNA(dna=sequence)

    v_len = len(sequence.dna)
    h_len = len(sequence.dna[0])

    for pos, line in enumerate(sequence.dna):
        f_line = "".join(
            [
                sequence.dna[x][pos + x]
                for x in range(0, v_len - pos)
                if pos + x <= h_len <= v_len
            ]
        )
        node = Node(h=line, f=f_line)

        if node.is_mutant():
            return True

    for col in range(0, len(sequence.dna[0])):
        v_line = "".join([sequence.dna[x][col] for x in range(0, v_len)])
        f_line = "".join(
            [
                sequence.dna[col + x][x]
                for x in range(0, h_len - col)
                if col + x <= h_len <= v_len
            ]
        )
        node = Node(v=v_line, f=f_line)

        if node.is_mutant():
            return True

    return False
