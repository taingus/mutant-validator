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

    if h_len > 3:
        for pos, line in enumerate(sequence.dna):
            f_line = ""
            b_line = ""
            if v_len >= 4 and h_len >= 4:
                f_line = "".join(
                    [
                        sequence.dna[pos + x][x]
                        for x in range(0, v_len - pos)
                        if pos + x <= h_len <= v_len
                    ]
                )
                b_line = "".join(
                    [
                        sequence.dna[pos + x][v_len - 1 - x]
                        for x in range(0, v_len - pos)
                        if h_len - x >= 0 and v_len - x >= 0
                    ]
                )
            node = Node(h=line, f=f_line, b=b_line)

            if node.is_mutant():
                return True

    if v_len > 3:
        for col in range(0, len(sequence.dna[0])):
            f_line = ""
            b_line = ""
            if v_len >= 4 and h_len >= 4:
                f_line = "".join(
                    [
                        sequence.dna[x][col + x]
                        for x in range(0, h_len - col)
                        if col + x <= h_len <= v_len
                    ]
                )
                b_line = "".join(
                    [
                        sequence.dna[x][col - x]
                        for x in range(0, h_len - col)
                        if h_len - x >= 0 and v_len - x >= 0 and col - x >= 0
                    ]
                )

            v_line = "".join([sequence.dna[x][col] for x in range(0, v_len)])
            node = Node(v=v_line, f=f_line, b=b_line)

            if node.is_mutant():
                return True

    return False
